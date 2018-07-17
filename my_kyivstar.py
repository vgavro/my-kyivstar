#!/usr/bin/env python
import re
import json
import os.path

from requests_toolbelt.sessions import BaseUrlSession
from lxml import html
import yaml
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter


def pprint(data):
    rv = json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False)
    print(highlight(rv, JsonLexer(), TerminalFormatter()))


class KyivstarSession(BaseUrlSession):
    base_url = 'https://account.kyivstar.ua/'

    def __init__(self, phone, password, **kwargs):
        self.phone, self.password = phone, password
        super().__init__(**kwargs)

    def login(self):
        # This is based on https://github.com/dukegh/kyivstar/blob/master/Kyivstar.php
        # Many thanks to him for this!
        resp = self.get('cas/login')
        doc = html.fromstring(resp.text)
        lt = doc.cssselect('input[name=lt]')[0].value
        execution = doc.cssselect('input[name=execution]')[0].value
        jsessionid = self.cookies['JSESSIONID']

        resp = self.get(f'cas/auth/auth.nocache.js;jsessionid={jsessionid}')
        bc = re.search('bc=\'([\w\d]+)\'', resp.text).group(1)

        resp = self.get(f'cas/auth/{bc}.cache.js')
        auth_hash = re.search('\'authSupport\.rpc\',\'([\w\d]+)\'', resp.text).group(1)

        payload = (
            f'7|0|9|https://account.kyivstar.ua/cas/auth/|{auth_hash}|'
            f'ua.kyivstar.cas.shared.rpc.AuthSupportRPCService|authenticate|'
            f'java.lang.String/2004016611|Z|{self.phone}|{self.password}|'
            f'https://account.kyivstar.ua/cas/login#password:|1|2|3|4|5|5|5|5|6|5|7|8|0|0|9|'
        )
        resp = self.post('cas/auth/authSupport.rpc', data=payload,
                         headers={'Content-Type': 'text/x-gwt-rpc; charset=utf-8'})
        if resp.text.startswith('//EX'):
            raise RuntimeError(resp.text[4:])
        assert resp.text.startswith('//OK')
        token = re.search('AuthResult/\d+","([\w\d-]+)"', resp.text).group(1)

        resp = self.post(f'cas/login;jsessionid={jsessionid}', data={
            'execution': execution, 'lt': lt, '_eventId': 'submit', 'password': self.password,
            'username': self.phone, 'rememberMe': True, 'token': token,
            'authenticationType': 'MSISDN_PASSWORD',
        })

    def _parse_page_data(self, resp):
        return json.loads(re.search('var pageData = ({.*});\n\n', resp.text).group(1))

    def get_account_info(self):
        resp = self.get('https://new.kyivstar.ua/ecare/')
        data = self._parse_page_data(resp)
        return data['slots']['RightContent'][0]['data']


def main():
    for config_path in ('.my-kyivstar.yaml', os.path.expanduser('~/.my-kyivstar.yaml')):
        if os.path.exists(config_path):
            session = KyivstarSession(**yaml.load(open(config_path)))
            break
    else:
        raise RuntimeError('Expected config in .my-kyivstar.yaml or ~/.my-kyivstar.yaml')

    session.login()
    data = session.get_account_info()
    pprint(data)


if __name__ == '__main__':
    main()
