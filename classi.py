# -*- coding: utf-8 -*-
__author__ = 'remigioscolari'

import os
from sqlobject import *


class Bosco(SQLObject):
    luogo = UnicodeCol()
    mappale = IntCol()
    denuncia_taglio = UnicodeCol()
    data_denuncia = DateCol()
    prezzomc = FloatCol()
    prezzoq = FloatCol()
    forfait = FloatCol()
    corteccia = IntCol()
    venditamc = FloatCol()
    proprietari = MultipleJoin('Proprietario')
    tronchi = MultipleJoin('Tronco')
    arderes = MultipleJoin('Ardere')
    spese = MultipleJoin('Spesa')
    ore = MultipleJoin('OreLavoro')


class Proprietario(SQLObject):
    bosco = ForeignKey('Bosco', cascade=True)
    cognome = UnicodeCol()
    nome = UnicodeCol()
    citta = UnicodeCol()
    indirizzo = UnicodeCol()
    numero = UnicodeCol()
    provincia = UnicodeCol()
    tel = UnicodeCol()


class Tronco(SQLObject):
    bosco = ForeignKey('Bosco', cascade=True)
    ForeignKey = True
    specie = UnicodeCol()
    placchetta = IntCol()
    lunghezza = FloatCol()
    diametro = FloatCol()
    mc = FloatCol()


class Ardere(SQLObject):
    bosco = ForeignKey('Bosco', cascade=True)
    data = DateCol()
    quintali = FloatCol()
    prezzo = FloatCol()
    totale = FloatCol()
    note = UnicodeCol()


class Spesa(SQLObject):
    bosco = ForeignKey('Bosco', cascade=True)
    data = DateCol()
    tipo = UnicodeCol()
    prezzo_uni = FloatCol()
    unita = FloatCol()
    totale = FloatCol()
    note = UnicodeCol()


class OreLavoro(SQLObject):
    bosco = ForeignKey('Bosco', cascade=True)
    data = DateCol()
    numero_ore = FloatCol()
    prezzo_uni = FloatCol()
    tipo_lavoro = UnicodeCol()
    totale = FloatCol()
    note = UnicodeCol()


def crea_database():
    database = '%sdati.db' % dir_path
    connection_string = 'sqlite:' + database
    connection = connectionForURI(connection_string)
    sqlhub.processConnection = connection
    Bosco.createTable()
    Proprietario.createTable()
    Tronco.createTable()
    Ardere.createTable()
    Spesa.createTable()
    OreLavoro.createTable()


dir_path = ''
if os.name in ("nt", "dos", "ce"):
    dir_path = '%s\\Gestione Boschi\\' % os.environ['APPDATA']
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        crea_database()

elif os.name == "posix":
    dir_path = '~/Library/Application Support/Gestione Boschi/'
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        crea_database()


database = '%sdati.db' % dir_path
connection_string = 'sqlite:' + database
connection = connectionForURI(connection_string)
sqlhub.processConnection = connection

