from common.storage import StorageService


class LocalStorageService(StorageService):

    def __init__(self, kind):
        super().__init__(kind)

    def upload(self, key, data):
        pass

    def get_url(self, key):
        pass
