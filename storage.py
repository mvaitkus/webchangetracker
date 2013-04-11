"""
Created on Apr 11, 2013

@author: mvaitkus
"""
import datetime
import sqlite3

class Storage(object):
    """
    Stores a collection of key/value pairs to sqlitedb
    
    Has current version and transaction log
    """
    
    def __init__(self, database):
        self.database = database
        self.setup_DB()
        
    def setup_DB(self):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS changelog(site TEXT,object TEXT,event TEXT, price NUMERIC, time DATETIME);')
        cursor.execute('CREATE TABLE IF NOT EXISTS objects(site TEXT, object TEXT, price NUMERIC, added DATETIME, removed DATETIME);')
        conn.commit()
        conn.close()
        
    def get_items(self, site):
        conn = sqlite3.connect(self.database)
        validItems = {}
        for row in conn.cursor().execute('SELECT object, price from objects where removed is null and site = ?', (site,)).fetchall():
            validItems[row[0]] = row[1]
        conn.close()
        return validItems
    
    def insert_items(self, site, itemMap):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        currentTime = datetime.datetime.now()
        for k, v in itemMap.items():
            cursor.execute('INSERT INTO changelog (site, object, event, price, time) values (?,?,?,?,?)', (site, k, 'added', v, currentTime))
            cursor.execute('INSERT INTO objects(site,object,price,added) values (?,?,?,?)', (site, k, v, currentTime))
        conn.commit()
        conn.close()
        
    def remove_items(self, site, itemMap):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        currentTime = datetime.datetime.now()
        for k, v in itemMap.items():
            cursor.execute('INSERT INTO changelog (site, object, event, price, time) values (?,?,?,?,?)', (site, k, 'removed', v, currentTime))
            cursor.execute('UPDATE objects set removed = ? where object = ? and site = ?', (currentTime, k, site))
        conn.commit()
        conn.close()
        
    def change_items(self, site, itemMap):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        currentTime = datetime.datetime.now()
        for k, v in itemMap.items():
            cursor.execute('INSERT INTO changelog (site, object, event, price, time) values (?,?,?,?,?)', (site, k, 'changed', v, currentTime))
            cursor.execute('UPDATE objects set price = ? where object = ? and site = ?', (v, k, site))
        conn.commit()
        conn.close()