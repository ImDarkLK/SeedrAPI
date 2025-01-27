import requests
from json import loads
from .errors import (
    LoginRequired,
    InvalidLogin,
    InvalidToken,
    TokenExpired
)

class SeedrAPI:
    def __init__(self, email=None, password=None, token=None):
        if email and password:
            data = {'grant_type':'password', 'client_id':'seedr_chrome', 'type':'login', 'username': email, 'password': password}
            req = requests.post('https://www.seedr.cc/oauth_test/token.php', data=data)
            if 'access_token' in req.text:
                self.token = req.json()['access_token']
            else:
                raise InvalidLogin('Invalid username and password combination.')
        elif token:
            req = requests.get(f'https://www.seedr.cc/api/folder?access_token={token}')
            if 'space_max' in req.text:
                self.token = token
            else:
                raise InvalidToken('The access token provided is invalid.')
        else:
            raise LoginRequired('Account login required.')

    def get_drive(self):
        token = self.token
        url = f'https://www.seedr.cc/api/folder?access_token={token}'
        req = requests.get(url)
        if 'invalid_token' in req.text:
            raise TokenExpired('Access token expired. Need to make new API Instance.')
        else:
            return loads(req.text)

    def get_folder(self, id):
        token = self.token
        url = f'https://www.seedr.cc/api/folder/{id}?access_token={token}'
        req = requests.get(url)
        if 'access_denied' in req.text:
            raise Exception('Folder id invalid.')
        elif 'invalid_token' in req.text:
            raise TokenExpired('Access token expired. Need to make new API Instance.')
        else:
            return loads(req.text)

    def get_file(self, id):
        token = self.token
        data = {'access_token':token, 'func':'fetch_file', 'folder_file_id':id}
        req = requests.post('https://www.seedr.cc/oauth_test/resource.php', data=data)
        if 'access_denied' in req.text:
            raise Exception('File id invalid.')
        elif 'invalid_token' in req.text:
            raise TokenExpired('Access token expired. Need to make new API Instance.')
        else:
            return loads(req.text)

    def add_torrent(self, magnet):
        token = self.token
        data = {'access_token':token, 'func':'add_torrent', 'torrent_magnet':magnet}
        req = requests.post('https://www.seedr.cc/oauth_test/resource.php', data=data)
        if 'invalid_token' in req.text:
            raise TokenExpired('Access token expired. Need to make new API Instance.')
        else:
            return loads(req.text)

    def delete_folder(self, id):
        token = self.token
        data = {'access_token':token, 'func':'delete', 'delete_arr':[{'type':'folder', 'id': id}]}
        req = requests.post('https://www.seedr.cc/oauth_test/resource.php', data=data)
        if 'invalid_token' in req.text:
            raise TokenExpired('Access token expired. Need to make new API Instance.')
        else:
            return loads(req.text)

    def delete_file(self, id):
        token = self.token
        data = {'access_token':token, 'func':'delete', 'delete_arr':[{'type':'file', 'id': id}]}
        req = requests.post('https://www.seedr.cc/oauth_test/resource.php', data=data)
        if 'invalid_token' in req.text:
            raise TokenExpired('Access token expired. Need to make new API Instance.')
        else:
            return loads(req.text)

    def rename(self, id, name):
        token = self.token
        data = {'access_token':token, 'func':'rename', 'rename_to':name, 'file_id':id}
        req = requests.post('https://www.seedr.cc/oauth_test/resource.php', data=data)
        if 'invalid_token' in req.text:
            raise TokenExpired('Access token expired. Need to make new API Instance.')
        else:
            return loads(req.text)
