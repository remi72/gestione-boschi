# -*- coding: utf-8 -*-
__author__ = 'remigioscolari'

from db import Db

db = Db()


class Tronco:
    def __init__(self, idtronco, idbosco, specie, placchetta, lunghezza, diametro, mc):
        self.idtronco = idtronco
        self.idbosco = idbosco
        self.specie = specie
        self.placchetta = placchetta
        self.lunghezza = lunghezza
        self.diametro = diametro
        self.mc = mc

    def inserisciTronco(self):
        db.query = u'''INSERT INTO tronco (idbosco, specie, placchetta, lunghezza, diametro, mc)
                 VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')
                 '''.format(self.idbosco, self.specie, self.placchetta, self.lunghezza, self.diametro,
                            self.mc)
        db.eseguiAggiornamento()

    def eliminaTronco(self):
        db.query = "DELETE FROM tronco WHERE idtronco = '{0}'".format(self.idtronco)
        db.eseguiAggiornamento()

    def modificaTronco(self):
        db.query = u'''UPDATE tronco  SET idbosco = '{0}', specie = '{1}', placchetta = '{2}',
                 lunghezza = '{3}', diametro = '{4}', mc = '{5}' WHERE idtronco = '{6}'
                 '''.format(self.idbosco, self.specie, self.placchetta, self.lunghezza,
                            self.diametro, self.mc, self.idtronco)
        db.eseguiAggiornamento()


class Ardere:
    def __init__(self, idardere, idbosco, data, quintali, prezzo, totale, note):
        self.idardere = idardere
        self.idbosco = idbosco
        self.data = data
        self.quintali = quintali
        self.prezzo = prezzo
        self.totale = totale
        self.note = note

    def inserisciArdere(self):
        db.query = u"INSERT INTO ardere ( idbosco, data, quintali, prezzo, totale, note) \
                    VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')".format \
            (self.idbosco, self.data, self.quintali, self.prezzo, self.totale, self.note)
        db.eseguiAggiornamento()

    def eliminaArdere(self):
        db.query = "DELETE FROM ardere WHERE idardere = '{0}'".format(self.idardere)
        db.eseguiAggiornamento()

    def modificaArdere(self):
        db.query = u'''UPDATE ardere SET idbosco = '{0}', data = '{1}',
                      quintali = '{2}', prezzo = '{3}', totale = '{4}', note = '{5}' WHERE idardere = '{6}'
                   '''.format \
            (self.idbosco, self.data, self.quintali, self.prezzo, self.totale, self.note, self.idardere)
        db.eseguiAggiornamento()


class Spesa:
    def __init__(self, idspesa, idbosco, data, tipo, prezzo_uni, unita, totale, note):
        self.idspesa = idspesa
        self.idbosco = idbosco
        self.data = data
        self.tipo = tipo
        self.prezzo_uni = prezzo_uni
        self.unita = unita
        self.totale = totale
        self.note = note

    def inserisciSpesa(self):
        db.query = u"INSERT INTO spesa (idbosco, data, tipo, prezzo_uni, unita, totale, note) \
                    VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}')".format \
            (self.idbosco, self.data, self.tipo, self.prezzo_uni, self.unita, self.totale, self.note)
        db.eseguiAggiornamento()

    def eliminaSpesa(self):
        db.query = "DELETE FROM spesa WHERE idspesa = '{0}'".format(self.idspesa)
        db.eseguiAggiornamento()

    def modificaSpesa(self):
        db.query = u"UPDATE spesa SET idbosco = '{0}', data = '{1}', tipo = '{2}', \
                    prezzo_uni = '{3}', unita = '{4}', totale = '{5}', note = '{6}' WHERE idspesa = '{7}'".format \
            (self.idbosco, self.data, self.tipo, self.prezzo_uni, self.unita, self.totale, self.note, self.idspesa)
        db.eseguiAggiornamento()


class Proprietario:
    def __init__(self, idproprietario, cognome, nome, citta, indirizzo, numero, provincia, tel):
        self.idproprietario = idproprietario
        self.cognome = cognome
        self.nome = nome
        self.citta = citta
        self.indirizzo = indirizzo
        self.numero = numero
        self.provincia = provincia
        self.tel = tel

    def inserisciProprietario(self):
        db.query = u'''INSERT INTO proprietario (cognome, nome, citta, indirizzo, numero, provincia, tel)
                      VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}' ,'{6}')'''.format \
            (self.cognome, self.nome, self.citta, self.indirizzo, self.numero, self.provincia, self.tel)
        db.eseguiAggiornamento()

    def eliminaProprietario(self):
        db.query = "DELETE FROM proprietario WHERE idproprietario = '{0}'".format(self.idproprietario)
        db.eseguiAggiornamento()

    def modificaProprietario(self):
        db.query = u'''UPDATE proprietario  SET cognome = '{0}', nome = '{1}', citta = '{2}', indirizzo = '{3}',
                      numero = '{4}', provincia = '{5}' ,tel = '{6}' WHERE idproprietario = '{7}'
                   '''.format(self.cognome, self.nome, self.citta, self.indirizzo, self.numero, self.provincia,
                              self.tel, self.idproprietario)
        db.eseguiAggiornamento()


class Bosco:
    def __init__(self, idbosco, idproprietario, luogo, mappale, denuncia_taglio, data_denuncia,
                 prezzomc, prezzoq, forfait, corteccia, venditamc):
        self.idbosco = idbosco
        self.idproprietario = idproprietario
        self.luogo = luogo
        self.mappale = mappale
        self.denuncia_taglio = denuncia_taglio
        self.data_denuncia = data_denuncia
        self.prezzomc = prezzomc
        self.prezzoq = prezzoq
        self.forfait = forfait
        self.corteccia = corteccia
        self.venditamc = venditamc

    def inserisciBosco(self):
        db.query = u'''INSERT INTO bosco (idproprietario, luogo, mappale, denuncia_taglio, data_denuncia,
                      prezzomc, prezzoq, forfait, corteccia, venditamc)
                      VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}')
                      '''.format(self.idproprietario, self.luogo, self.mappale, self.denuncia_taglio,
                                 self.data_denuncia, self.prezzomc, self.prezzoq, self.forfait,
                                 self.corteccia, self.venditamc)
        db.eseguiAggiornamento()

    def eliminaBosco(self):
        db.query = "DELETE FROM tronco WHERE idbosco = '{0}'".format(self.idbosco)
        db.eseguiAggiornamento()
        db.query = "DELETE FROM ardere WHERE idbosco = '{0}'".format(self.idbosco)
        db.eseguiAggiornamento()
        db.query = "DELETE FROM spesa WHERE idbosco = '{0}'".format(self.idbosco)
        db.eseguiAggiornamento()
        db.query = "DELETE FROM ore_lavoro WHERE idbosco = '{0}'".format(self.idbosco)
        db.eseguiAggiornamento()
        db.query = "DELETE FROM proprietario WHERE idproprietario = '{0}'".format(self.idproprietario)
        db.eseguiAggiornamento()
        db.query = "DELETE FROM bosco WHERE idbosco = '{0}'".format(self.idbosco)
        db.eseguiAggiornamento()

    def modificaBosco(self):
        db.query = u'''UPDATE bosco  SET idproprietario = '{0}',
                      luogo = '{1}', mappale = '{2}', denuncia_taglio = '{3}',
                      data_denuncia = '{4}', prezzomc = '{5}', prezzoq = '{6}',
                      forfait = '{7}', corteccia = '{8}', venditamc = '{9}' WHERE idbosco = '{10}'
                      '''.format(self.idproprietario, self.luogo, self.mappale, self.denuncia_taglio,
                                 self.data_denuncia, self.prezzomc, self.prezzoq, self.forfait,
                                 self.corteccia, self.venditamc, self.idbosco)
        db.eseguiAggiornamento()


class OreLavoro:
    def __init__(self, idore, idbosco, data, numero_ore, prezzo_uni, tipo_lavoro, totale, note):
        self.idore = idore
        self.idbosco = idbosco
        self.data = data
        self.numero_ore = numero_ore
        self.prezzo_uni = prezzo_uni
        self.tipo_lavoro = tipo_lavoro
        self.totale = totale
        self.note = note

    def inserisciOre(self):
        db.query = u"INSERT INTO ore_lavoro (idbosco, data, numero_ore, prezzo_uni, tipo_lavoro, totale, note) \
                    VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}')".format \
            (self.idbosco, self.data, self.numero_ore, self.prezzo_uni, self.tipo_lavoro, self.totale, self.note)
        db.eseguiAggiornamento()

    def eliminaOre(self):
        db.query = "DELETE FROM ore_lavoro WHERE idore = '{0}'".format(self.idore)
        db.eseguiAggiornamento()

    def modificaOre(self):
        db.query = u"UPDATE ore_lavoro  SET idbosco = '{0}', data = '{1}', numero_ore = '{2}', prezzo_uni = '{3}', \
                    tipo_lavoro = '{4}', totale = '{5}', note = '{6}' WHERE idore = '{7}'".format \
            (self.idbosco, self.data, self.numero_ore, self.prezzo_uni, self.tipo_lavoro, self.totale, self.note,
             self.idore)
        db.eseguiAggiornamento()
