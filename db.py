# -*- coding: utf-8 -*-
__author__ = 'remigioscolari'

import sqlite3
import os.path


class Db:
    dir_path = ''
    if os.name in ("nt", "dos", "ce"):
        dir_path = '%s\\Gestione Boschi\\' %  os.environ['APPDATA']
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
    elif os.name == "posix":
        dir_path ='~/Library/Application Support/Gestione Boschi/'
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    database = '%sdati.db' % dir_path

    if not os.path.exists(database):
        conn = sqlite3.connect(database)
        f = open('schemaDati.sql')
        schema = f.read()
        conn.executescript(schema)
        conn.close()

    def __init__(self, query=''):
        self.query = query

    def eseguiQuery(self):
        conn = sqlite3.connect(Db.database, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        cursor = conn.execute(self.query)
        dati = [row for row in cursor]
        conn.close()
        return dati

    def eseguiAggiornamento(self):
        conn = sqlite3.connect(Db.database, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        conn.execute(self.query)
        conn.commit()
        conn.close()
