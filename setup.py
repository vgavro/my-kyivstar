from setuptools import setup

setup(
    name="my-kyivstar",
    version="0.0.3",
    description="Check balance using cli from account.kyivstar.ua",
    author="Victor Gavro",
    author_email="vgavro@gmail.com",
    url="https://github.com/vgavro/my-kyivstar",
    license="MIT License",
    classifiers=[
        # https://pypi.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
    ],
    py_modules=["my_kyivstar"],
    install_requires=[
        'requests',
        'requests-toolbelt',
        'lxml',
        'cssselect',
        'pyyaml',
    ],
    entry_points={
        'console_scripts': [
            'my-kyivstar=my_kyivstar:main',
        ],
    },
)
