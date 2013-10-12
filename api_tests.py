from flask import Flask, g
import unittest
import json
from simplekv.fs import FilesystemStore
from flaskext.kvsession import KVSessionExtension

from api import app, db
from common.database import Database

class APITest(unittest.TestCase):

    def setUp(self):
        global db
        store = FilesystemStore('session')
        KVSessionExtension(store, app)
        
        # Load the debug config
        app.config.from_pyfile('../config.defaults.py')
        app.config.from_pyfile('../config_debug.py')
        app.secret_key = app.config['SECRET_KEY']
        db = Database(app.config)

        self._setup_database()
        app.testing = True
        self.app = app.test_client(use_cookies=True)

        self.csrf = ''

    """Setup the database
        by clearing it and loading the schema"""
    def _setup_database(self):
        con = db.get_connection()
        cur = con.cursor()

        cur.execute(open('schema.sql', 'r').read())
        con.commit()
        
        db.put_away_connection(con)

    def test_1_api_base(self):
        rv = self.app.get('/api/')
        data = json.loads(rv.data)
        assert data['status']['code'] is 0
        assert data['csrf_token']
        self.csrf = data['csrf_token']

if __name__ == '__main__':
    unittest.main()