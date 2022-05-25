from random import randint, choice
from typing import Optional, Union, List
from requests import Session
from pprint import pprint
from hashlib import md5
from datetime import datetime
from pytz import utc
from os import listdir

import xmltodict

JWIKI_API = 'https://jwiki.kr/wiki/api.php'

session = Session()


def get_login_token():
    r = session.get(f'{JWIKI_API}?action=query&meta=tokens&type=login&format=json')
    j = r.json()
    return j['query']['tokens']['logintoken']


def get_csrf_token():
    r = session.get(f'{JWIKI_API}?action=query&meta=tokens&type=csrf&format=json')
    j = r.json()
    return j['query']['tokens']['csrftoken']


def login(id_: str, password: str, login_token: Optional[str] = None):
    if login_token is None:
        login_token = get_login_token()

    data = {'lgname': id_, 'lgpassword': password, 'lgtoken': login_token}
    r = session.post(f'{JWIKI_API}?action=login&format=json', data=data)
    return r.json()


def upload(filename: str, file_path: str, csrf_token: Optional[str] = None):
    if csrf_token is None:
        csrf_token = get_csrf_token()

    data = {
        'filename': filename,
        'token': csrf_token,
        'ignorewarnings': True
    }
    file = {'file': (filename, open(file_path, 'rb'), 'multipart/form-data')}
    r = session.post(f'{JWIKI_API}?action=upload&format=json', data, files=file)
    return r.json()


ID = 'Junhg0211@Zastravapera'
PASSWORD = 'tp45tc8ti6qfl8m76jpvk5sul3kansqi'


if __name__ == '__main__':
    print(login(ID, PASSWORD))
    for name in listdir('.'):
        if name.endswith('.png'):
            print(upload(name, name)['upload']['result'])

