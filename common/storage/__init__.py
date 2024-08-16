from mimetypes import guess_type
from secrets import token_hex
from common.constants import FILE_KEY


class StorageService(object):

    def __init__(self, kind):
        self.kind = kind

    def generate_unique_name(self, filename):
        extension = filename.rsplit('.', 1)[-1]
        return f'{self.kind}-{token_hex(4)}.{extension}'

    @staticmethod
    def get_content_type(filename):
        return guess_type(filename)[0]

    def get_key(self, filename):
        return FILE_KEY[self.kind].format(name=self.generate_unique_name(filename))

    def upload(self, key, data, content_type=None):
        pass

    def download(self, key):
        pass

    def get_url(self, key):
        pass
