# my-kyivstar cli interface

Grabs balance and useful statistics from https://account.kyivstar.ua
Парсит баланс и полезную статистику из https://account.kyivstar.ua

Login logic completely based on php implementation: https://github.com/dukegh/kyivstar
Many thanks to him for this!

## Install

Python 3.6+ required.

```
git clone https://github.com/vgavro/my-kyivstar
sudo pip install ./my-kyivstar
```

Create config in `~/.my-kyivstar.yaml`
```
phone: +380...
password: your-password
```

Then run `my-kyivstar` to get balance.

Response example:
```
{
  "accountData": {
    "balance": "30,42",
    "gsmNextPaymentValue": {
      "label": "Следующий платеж (29.07.2018)",
      "value": "95,00"
    }
  },
  "bonusBalance": {
    "availableAmountSum": "0,00",
    "bonusBalances": [
      {
        "balanceAmount": [
          {
            "unit": "SMS",
            "value": "150"
          }
        ],
        "bonusExpirationDate": "29.07.2018",
        "name": "SMS по Украине:"
      },
      {
        "balanceAmount": [
          {
            "unit": "МБ",
            "value": "4 300"
          }
        ],
        "bonusExpirationDate": "29.07.2018",
        "name": "Интернет:"
      },
      {
        "balanceAmount": [
          {
            "unit": "грн",
            "value": "0,00"
          }
        ],
        "bonusExpirationDate": "21.02.2026",
        "name": "Остаток бонусных средств  «Экстра Деньги»"
      },
      {
        "balanceAmount": [
          {
            "unit": "ч.",
            "value": "02"
          },
          {
            "unit": "мин.",
            "value": "22"
          }
        ],
        "bonusExpirationDate": "29.07.2018",
        "name": "Минуты на другие мобильные:"
      }
    ]
  },
  "currencyName": "грн",
  "currentSubscription": {
    "bonusBalance": "0,00"
  },
  "isTransferAvailable": "",
  "isTransferEnabled": "",
  "paymentHistoryPageUrl": "/ecare/usageStatus",
  "rechargePageUrl": "/ecare/recharge",
  "subscriptionType": "PREPAID"
}
```

## Authors

* [dukegh](https://github.com/dukegh) - PHP implementation.
* [me](https://github.com/vgavro) - Just a handsome guy, you know.

## License

This project is licensed under the MIT License.
