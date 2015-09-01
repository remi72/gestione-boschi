# -*- coding: utf-8 -*-
__author__ = 'remigioscolari'

import wx
from classi import *
from db import *


def leggiBoschi(s=''):
    db = Db('''SELECT * FROM bosco WHERE luogo LIKE '%{0}%' OR mappale = '{0}' OR idproprietario =
    (SELECT idproprietario FROM proprietario WHERE nome LIKE '%{0}%' OR cognome LIKE '%{0}%')
    ORDER BY idbosco DESC'''.format(s))
    rows = db.eseguiQuery()
    boschi = []
    for row in rows:
        b = Bosco(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10])
        boschi.append(b)
    return boschi


def leggiTronchi(bosco):
    db = Db("SELECT * FROM tronco WHERE idbosco = '{}'".format(bosco.idbosco))
    rows = db.eseguiQuery()
    tronchi = []
    for row in rows:
        t = Tronco(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
        tronchi.append(t)
    return tronchi


def leggiProprietari():
    db = Db("SELECT * FROM proprietario")
    rows = db.eseguiQuery()
    proprietari = []
    for row in rows:
        p = Proprietario(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
        proprietari.append(p)
    return proprietari


def leggiArdere(bosco):
    db = Db("SELECT * FROM ardere WHERE idbosco = '{}'".format(bosco.idbosco))
    rows = db.eseguiQuery()
    ardere = []
    for row in rows:
        a = Ardere(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
        ardere.append(a)
    return ardere


def leggiSpese(bosco):
    db = Db("SELECT * FROM spesa WHERE idbosco = '{}'".format(bosco.idbosco))
    rows = db.eseguiQuery()
    spese = []
    for row in rows:
        s = Spesa(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
        spese.append(s)
    return spese


def leggiOre(bosco):
    db = Db("SELECT * FROM ore_lavoro WHERE idbosco = '{}'".format(bosco.idbosco))
    rows = db.eseguiQuery()
    ore = []
    for row in rows:
        o = OreLavoro(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
        ore.append(o)
    return ore


def wxdatetime_from_db_date(date):
    day = date.day
    month = date.month - 1
    year = date.year
    return wx.DateTimeFromDMY(day=day, month=month, year=year)
