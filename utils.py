from tinydb import TinyDB, Query
import datetime

class Bans:
    def __init__(self):
        self.__db = TinyDB('3pseatBans.json')
        self.__user = Query()
    def getTable(self, server):
        return self.__db.table(server)
    def check(self, server, name):
        db = self.getTable(server)
        if not db.search(self.__user.name.matches(name)):
            db.insert({'name': name, 'count': 0})
        result = db.search(self.__user.name == name)
        user = result.pop(0)
        return user['count']
    def up(self, server, name):
        db = self.getTable(server)
        # Add 1 to user count
        val = self.check(server, name) + 1
        db.update({'count': val}, self.__user.name == name)
        # Add 1 to server count
        val = self.check(server, 'server') + 1
        db.update({'count': val}, self.__user.name == name)
        return val
    def clear(self, server, name):
        db = self.getTable(server)
        self.check(server, name)
        db.update({'count': 0}, self.__user.name == name)
    def getDB(self, server):
        return self.getTable(server)

def getTime():
    now = datetime.datetime.now()
    return '[' + now.strftime('%Y-%m-%d %H:%M:%S') + '] '