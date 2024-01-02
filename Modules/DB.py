import pymongo
import settings


class DB:
    class _DB:
        def __init__(self):
            self.client = pymongo.MongoClient(settings.MONGODB_URL)

    _instance = None

    def __init__(self):
        if not DB._instance:
            DB._instance = DB._DB()
        else:
            print('Already connected to MongoDB')

    def __getattr__(self, name):
        return getattr(self._instance, name)
