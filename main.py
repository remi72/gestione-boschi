# -*- coding: utf-8 -*-
__author__ = 'remigioscolari'

import wx.grid
import funzioni
from classi import *
from validatore import *
from stampa import stampa
from math import pi
import os
import shutil

boschi = []
proprietari = []
tronchi = []
totalemc = 0
corteccia = False
totalenettomc = 0
totaleeuromc = 0
legna_da_ardere = []
totaleq = 0
totale_euro_ardere = 0
spese = []
totale_spese = 0
lista_ore = []
totale_ore = 0
totale_euro_ore = 0


class PannelloPrincipale(wx.Panel):
    def __init__(self, *a, **k):
        self.locale = wx.Locale(wx.LANGUAGE_ITALIAN)
        wx.Panel.__init__(self, *a, **k)
        self.cerca1 = wx.SearchCtrl(self, -1, size=wx.Size(200, -1), style=wx.TE_PROCESS_ENTER)
        self.cerca1.ShowSearchButton(True)
        self.cerca1.ShowCancelButton(True)
        self.button_nuovo_bosco = wx.Button(self, wx.ID_ANY, u"Nuovo Bosco")
        self.lista_boschi_listbox = wx.ListBox(self, size=wx.Size(200, 490), choices=crea_lista_boschi())

        self.schede = wx.Notebook(self)
        self.pannello_bosco = PannelloBosco(self.schede)
        self.pannello_bosco.SetBackgroundColour(wx.Colour(221,221,221))
        self.pannello_tronchi = PannelloTronchi(self.schede)
        self.pannello_tronchi.SetBackgroundColour(wx.Colour(221,221,221))
        self.pannello_ardere = PannelloArdere(self.schede)
        self.pannello_ardere.SetBackgroundColour(wx.Colour(221,221,221))
        self.pannello_spese = PannelloSpese(self.schede)
        self.pannello_spese.SetBackgroundColour(wx.Colour(221,221,221))
        self.pannello_ore = PannelloOre(self.schede)
        self.pannello_ore.SetBackgroundColour(wx.Colour(221,221,221))
        self.pannello_totali = PannelloTotali(self.schede)
        self.pannello_totali.SetBackgroundColour(wx.Colour(221,221,221))

        bSizer4 = wx.BoxSizer(wx.HORIZONTAL)
        bSizer5 = wx.BoxSizer(wx.VERTICAL)
        bSizer4.Add(bSizer5, 0, wx.ALL, 5)
        bSizer5.Add(self.cerca1, 0, wx.ALL, 5)
        bSizer5.Add(self.button_nuovo_bosco, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)
        bSizer5.Add(self.lista_boschi_listbox, 0, wx.ALL, 5)

        self.schede.AddPage(self.pannello_bosco, u"Dati Bosco", False)
        self.schede.AddPage(self.pannello_tronchi, u"Tronchi", False)
        self.schede.AddPage(self.pannello_ardere, u"Legna da Ardere", False)
        self.schede.AddPage(self.pannello_spese, u"Spese", False)
        self.schede.AddPage(self.pannello_ore, u"Ore Lavoro", False)
        self.schede.AddPage(self.pannello_totali, u"Totali", False)

        # Connect Events
        self.schede.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.pannello_totali.fai_totali)
        self.lista_boschi_listbox.Bind(wx.EVT_LISTBOX, self.selezioneBosco)
        self.button_nuovo_bosco.Bind(wx.EVT_BUTTON, self.nuovo_bosco)
        self.cerca1.Bind(wx.EVT_TEXT_ENTER, self.cerca)
        self.cerca1.Bind(wx.EVT_SEARCHCTRL_SEARCH_BTN, self.cerca)

        bSizer4.Add(self.schede, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(bSizer4)

        self.Layout()
        self.Centre(wx.BOTH)

    def selezioneBosco(self, event):
        n = self.lista_boschi_listbox.GetSelections()
        bosco = boschi[n[0]]
        proprietario_bosco = 0
        for proprietario in proprietari:
            if bosco.idproprietario == proprietario.idproprietario:
                proprietario_bosco = proprietario
                break
        self.pannello_bosco.dati_bosco(bosco, proprietario_bosco)
        self.pannello_tronchi.crea_griglia_tronchi()
        self.pannello_ardere.crea_griglia_ardere()
        self.pannello_spese.crea_griglia_spesa()
        self.pannello_ore.crea_griglia_ore()
        self.pannello_totali.fai_totali()

    def nuovo_bosco(self, event):
        dlg = DlgInserisciBosco(self)
        retcode = dlg.ShowModal()
        if retcode == wx.ID_OK:
            proprietario, bosco = dlg.leggi_dati()
            proprietario.inserisciProprietario()
            db = Db("SELECT * FROM proprietario ORDER BY idproprietario DESC LIMIT 1")
            idproprietario = (db.eseguiQuery())[0][0]

            bosco.idproprietario = idproprietario
            bosco.inserisciBosco()

            frame.pannello_principale.lista_boschi_listbox.SetItems(crea_lista_boschi())
            self.pannello_bosco.azzera()
            dlg.Destroy()

    def cerca(self, event):
        stringa = self.cerca1.GetValue()
        frame.pannello_principale.lista_boschi_listbox.SetItems(crea_lista_boschi(stringa))


class PannelloBosco(wx.Panel):
    def __init__(self, *a, **k):
        wx.Panel.__init__(self, *a, **k)
        self.nome = wx.TextCtrl(self, style=wx.TE_READONLY)
        self.cognome = wx.TextCtrl(self, style=wx.TE_READONLY)
        self.citta = wx.TextCtrl(self, style=wx.TE_READONLY)
        self.indirizzo = wx.TextCtrl(self, style=wx.TE_READONLY)
        self.numero = wx.TextCtrl(self, style=wx.TE_READONLY)
        self.provincia = wx.TextCtrl(self, style=wx.TE_READONLY)
        self.telefono = wx.TextCtrl(self, style=wx.TE_READONLY)
        self.luogo = wx.TextCtrl(self, style=wx.TE_READONLY)
        self.mappale = wx.TextCtrl(self, style=wx.TE_READONLY)
        self.denuncia = wx.TextCtrl(self, style=wx.TE_READONLY)
        self.data = wx.TextCtrl(self, style=wx.TE_READONLY)
        self.prezzomc = wx.TextCtrl(self, style=wx.TE_READONLY)
        self.prezzoq = wx.TextCtrl(self, style=wx.TE_READONLY)
        self.forfait = wx.TextCtrl(self, style=wx.TE_READONLY)
        self.button_modifica_bosco = wx.Button(self, wx.ID_ANY, u"Modifica")
        self.button_elimina_bosco = wx.Button(self, wx.ID_ANY, u"Elimina")
        labels = ('Nome:', 'Cognome:', u"Città:", 'Indirizzo:', 'Numero:', 'Provincia:', 'Telefono:',
                  'Luogo:', 'Mappale:', 'Denuncia Taglio:', 'Data Denuncia:', u'Prezzo metro cubo €:',
                  u'Prezzo al quintale €:', u'Forfait €:')

        bSizer1 = wx.BoxSizer(wx.VERTICAL)
        gbsizer = wx.GridBagSizer(16, 5)
        gbsizer.Add(wx.StaticText(self, -1, 'PROPRIETARIO'), pos=(0, 0), span=(1, 2), flag=wx.ALIGN_CENTER_HORIZONTAL)
        gbsizer.Add(wx.StaticText(self, -1, 'BOSCO'), pos=(0, 3), span=(1, 2), flag=wx.ALIGN_CENTER_HORIZONTAL)
        gbsizer.Add(self.nome, pos=(1, 1))
        gbsizer.Add(self.cognome, pos=(2, 1))
        gbsizer.Add(self.citta, pos=(3, 1))
        gbsizer.Add(self.indirizzo, pos=(4, 1))
        gbsizer.Add(self.numero, pos=(5, 1))
        gbsizer.Add(self.provincia, pos=(6, 1))
        gbsizer.Add(self.telefono, pos=(7, 1))
        gbsizer.Add(self.luogo, pos=(1, 4))
        gbsizer.Add(self.mappale, pos=(2, 4))
        gbsizer.Add(self.denuncia, pos=(3, 4))
        gbsizer.Add(self.data, pos=(4, 4))
        gbsizer.Add(self.prezzomc, pos=(5, 4))
        gbsizer.Add(self.prezzoq, pos=(6, 4))
        gbsizer.Add(self.forfait, pos=(7, 4))
        for i, label in enumerate(labels):
            if i < 7:
                gbsizer.Add(wx.StaticText(self, -1, label), pos=(i + 1, 0), flag=wx.ALIGN_RIGHT)
            else:
                gbsizer.Add(wx.StaticText(self, -1, label), pos=(i - 6, 3), flag=wx.ALIGN_RIGHT)
        bSizer1.Add(gbsizer, 0, wx.ALL, 50)
        bSizer1.AddSpacer((0, 0), 1, wx.EXPAND, 5)
        bSizer2 = wx.BoxSizer(wx.HORIZONTAL)
        bSizer1.Add(bSizer2, 0, wx.EXPAND, 5)
        bSizer2.AddSpacer((0, 0), 1, wx.EXPAND, 5)
        bSizer2.Add(self.button_modifica_bosco, 0, wx.ALL, 5)
        bSizer2.Add(self.button_elimina_bosco, 0, wx.ALL, 5)

        bSizer1.Fit(self)
        self.SetSizer(bSizer1)

        # Connect Events
        self.button_modifica_bosco.Bind(wx.EVT_BUTTON, self.modifica_bosco)
        self.button_elimina_bosco.Bind(wx.EVT_BUTTON, self.elimina_bosco)

    def dati_bosco(self, bosco, proprietario):
        self.nome.SetValue(proprietario.nome)
        self.cognome.SetValue(proprietario.cognome)
        self.citta.SetValue(proprietario.citta)
        self.indirizzo.SetValue(proprietario.indirizzo)
        self.numero.SetValue(proprietario.numero)
        self.provincia.SetValue(proprietario.provincia)
        self.telefono.SetValue(proprietario.tel)
        self.luogo.SetValue(bosco.luogo)
        self.mappale.SetValue(bosco.mappale)
        self.denuncia.SetValue(bosco.denuncia_taglio)
        self.data.SetValue(bosco.data_denuncia.strftime('%d-%m-%Y'))
        self.prezzomc.SetValue('{:.2f}'.format(bosco.prezzomc) if bosco.prezzomc != 0 else '')
        self.prezzoq.SetValue('{:.2f}'.format(bosco.prezzoq) if bosco.prezzoq != 0 else '')
        self.forfait.SetValue('{:.2f}'.format(bosco.forfait) if bosco.forfait != 0 else '')

    def azzera(self):
        self.nome.SetValue('')
        self.cognome.SetValue('')
        self.citta.SetValue('')
        self.indirizzo.SetValue('')
        self.numero.SetValue('')
        self.provincia.SetValue('')
        self.telefono.SetValue('')
        self.luogo.SetValue('')
        self.mappale.SetValue('')
        self.denuncia.SetValue('')
        self.data.SetValue('')
        self.prezzomc.SetValue('')
        self.prezzoq.SetValue('')
        self.forfait.SetValue('')

    def modifica_bosco(self, event):
        n = frame.pannello_principale.lista_boschi_listbox.GetSelections()
        p = 0
        try:
            bosco = boschi[n[0]]
            for proprietario in proprietari:
                if bosco.idproprietario == proprietario.idproprietario:
                    p = proprietario
                    break
        except IndexError:
            wx.MessageBox('seleziona un bosco')
            return

        dlg = DlgInserisciBosco(self, bosco, p)
        retcode = dlg.ShowModal()
        if retcode == wx.ID_OK:
            proprietario, bosco = dlg.leggi_dati()
            proprietario.modificaProprietario()
            bosco.modificaBosco()
            frame.pannello_principale.lista_boschi_listbox.SetItems(crea_lista_boschi())
            self.azzera()
            dlg.Destroy()

    def elimina_bosco(self, event):
        n = frame.pannello_principale.lista_boschi_listbox.GetSelections()
        try:
            bosco = boschi[n[0]]
            if dlg_yes_no(self, question='Se elimini il bosco tutti i dati associati al bosco verranno eliminati'):
                bosco.eliminaBosco()
            frame.pannello_principale.lista_boschi_listbox.SetItems(crea_lista_boschi())
            self.azzera()
        except IndexError:
            wx.MessageBox(u"seleziona il bosco")
            return


class PannelloTronchi(wx.Panel):
    def __init__(self, *a, **k):
        wx.Panel.__init__(self, *a, **k)

        self.tabella_tronchi = wx.grid.Grid(self, size=wx.Size(405, 480))
        # Grid
        self.tabella_tronchi.CreateGrid(0, 5)
        self.tabella_tronchi.EnableEditing(False)
        self.tabella_tronchi.EnableGridLines(True)
        self.tabella_tronchi.EnableDragGridSize(False)
        self.tabella_tronchi.SetMargins(0, 0)

        # Columns
        self.tabella_tronchi.EnableDragColMove(False)
        self.tabella_tronchi.EnableDragColSize(True)
        self.tabella_tronchi.SetColLabelSize(20)
        self.tabella_tronchi.SetColLabelValue(0, 'Placchetta')
        self.tabella_tronchi.SetColSize(0, 70)
        self.tabella_tronchi.SetColLabelValue(1, 'Specie')
        self.tabella_tronchi.SetColSize(1, 95)
        self.tabella_tronchi.SetColLabelValue(2, 'Lung. m')
        self.tabella_tronchi.SetColSize(2, 60)
        self.tabella_tronchi.SetColLabelValue(3, 'Diametro cm')
        self.tabella_tronchi.SetColLabelValue(4, 'mc')
        self.tabella_tronchi.SetColSize(4, 60)
        self.tabella_tronchi.SetColLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        # Rows
        self.tabella_tronchi.EnableDragRowSize(True)
        self.tabella_tronchi.SetRowLabelSize(20)
        self.tabella_tronchi.SetRowLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        # Cell Defaults
        self.tabella_tronchi.SetDefaultCellAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        self.corteccia = wx.CheckBox(self)
        self.totalemc = wx.TextCtrl(self, size=wx.Size(80, -1), style=wx.TE_RIGHT | wx.TE_READONLY)
        self.totale_netto = wx.TextCtrl(self, size=wx.Size(80, -1), style=wx.TE_RIGHT | wx.TE_READONLY)
        self.prezzo_vendita = wx.TextCtrl(self, size=wx.Size(80, -1), style=wx.TE_RIGHT)
        self.prezzo_vendita.SetBackgroundColour(wx.Colour(255, 250, 100))
        self.ricavo = wx.TextCtrl(self, size=wx.Size(90, 25), style=wx.TE_RIGHT | wx.TE_READONLY)
        self.ricavo.SetFont(wx.Font(12, 70, 90, 92))
        self.button_stampa = wx.Button(self, wx.ID_ANY, u"Stampa")
        self.button_nuovo_tronco = wx.Button(self, wx.ID_ANY, u"Nuovo")
        self.button_modifica_tronco = wx.Button(self, wx.ID_ANY, u"Modifica")
        self.button_elimina_tronco = wx.Button(self, wx.ID_ANY, u"Elimina")
        self.Layout()

        bSizer = wx.BoxSizer(wx.VERTICAL)
        bSizer2 = wx.BoxSizer(wx.HORIZONTAL)
        gbsizer = wx.GridBagSizer(10, 10)
        bSizer.Add(gbsizer, 0, wx.ALL, 5)
        bSizer.Add(bSizer2, 0, wx.ALL, 5)
        gbsizer.Add(self.tabella_tronchi, (0, 0), (6, 1), flag=wx.ALIGN_CENTER_HORIZONTAL)
        gbsizer.Add(wx.StaticText(self, -1, 'Totale mc:'), pos=(0, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        gbsizer.Add(self.totalemc, pos=(0, 2))
        gbsizer.Add(wx.StaticText(self, -1, 'Corteccia:'), pos=(1, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        gbsizer.Add(self.corteccia, pos=(1, 2))

        gbsizer.Add(wx.StaticText(self, -1, 'Netto mc:'), pos=(2, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        gbsizer.Add(self.totale_netto, pos=(2, 2))
        gbsizer.Add(wx.StaticText(self, -1, u'Vendita €:'), pos=(3, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        gbsizer.Add(self.prezzo_vendita, pos=(3, 2))
        gbsizer.Add(wx.StaticText(self, -1, u'Totale €:'), pos=(4, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        gbsizer.Add(self.ricavo, pos=(4, 2))

        bSizer2.Add(self.button_stampa, 0, wx.ALL, 5)
        bSizer2.AddSpacer((1000, 0), 1, wx.EXPAND, 5)
        bSizer2.Add(self.button_nuovo_tronco, 0, wx.ALL, 5)
        bSizer2.Add(self.button_modifica_tronco, 0, wx.ALL, 5)
        bSizer2.Add(self.button_elimina_tronco, 0, wx.ALL, 5)

        bSizer.Fit(self)
        self.SetSizer(bSizer)

        # Connect Events
        self.button_stampa.Bind(wx.EVT_BUTTON, self.fai_stampa)
        self.button_nuovo_tronco.Bind(wx.EVT_BUTTON, self.nuovo_tronco)
        self.button_modifica_tronco.Bind(wx.EVT_BUTTON, self.modifica_tronco)
        self.button_elimina_tronco.Bind(wx.EVT_BUTTON, self.elimina_tronco)
        self.corteccia.Bind(wx.EVT_CHECKBOX, self.chkbox)
        self.prezzo_vendita.Bind(wx.EVT_TEXT, self.venditacg)

    def crea_griglia_tronchi(self):
        n = frame.pannello_principale.lista_boschi_listbox.GetSelections()
        bosco = boschi[n[0]]
        global corteccia, tronchi, totalemc
        if bosco.corteccia == 1:
            corteccia = True
        else:
            corteccia = False
        self.corteccia.SetValue(corteccia)
        self.prezzo_vendita.SetValue(str(bosco.venditamc) if bosco.venditamc != 0 else '')
        tronchi = funzioni.leggiTronchi(bosco)
        righe = self.tabella_tronchi.GetNumberRows()
        if righe > 0:
            self.tabella_tronchi.DeleteRows(0, righe)
        totalemc = 0
        for i, tronco in enumerate(tronchi):
            self.tabella_tronchi.InsertRows(-1)
            self.tabella_tronchi.SetCellValue(i, 0, str(tronco.placchetta).zfill(5))
            self.tabella_tronchi.SetCellValue(i, 1, tronco.specie)
            self.tabella_tronchi.SetCellValue(i, 2, str(tronco.lunghezza))
            self.tabella_tronchi.SetCellValue(i, 3, str(tronco.diametro))
            self.tabella_tronchi.SetCellValue(i, 4, str(tronco.mc))
            totalemc += tronco.mc
        self.tabella_tronchi.Scroll(-1, 100000)
        self.totalemc.SetValue(str(totalemc))
        self.fai_totale_netto()

    def nuovo_tronco(self, event):
        n = frame.pannello_principale.lista_boschi_listbox.GetSelections()
        try:
            bosco = boschi[n[0]]
        except IndexError:
            wx.MessageBox('seleziona un bosco')
            return
        dlg = DlgInserisciTronco(self, bosco)
        dlg.Show()

    def modifica_tronco(self, event):
        try:
            nb = frame.pannello_principale.lista_boschi_listbox.GetSelections()
            nt = self.tabella_tronchi.GetSelectedRows()
            bosco = boschi[nb[0]]
        except IndexError:
            wx.MessageBox('seleziona un bosco')
            return
        try:
            tronco = tronchi[nt[0]]
            dlg = DlgInserisciTronco(self, bosco, tronco)
            dlg.Show()

        except IndexError:
            wx.MessageBox('seleziona un tronco')
            return

    def elimina_tronco(self, event):
        n = self.tabella_tronchi.GetSelectedRows()
        try:
            tronco = tronchi[n[0]]
            if dlg_yes_no(self):
                tronco.eliminaTronco()
            self.crea_griglia_tronchi()

        except IndexError:
            wx.MessageBox('seleziona un tronco')
            return

    def fai_totale_netto(self):
        global totalenettomc, totaleeuromc, corteccia
        prezzo_vendita = float(self.prezzo_vendita.GetValue()) if self.prezzo_vendita.GetValue() != '' else 0
        if corteccia:
            totalenettomc = round(totalemc - ((totalemc / 100) * 10), 3)
            self.totale_netto.SetValue(str(totalenettomc))
            totaleeuromc = round((totalenettomc * prezzo_vendita), 2)
            self.ricavo.SetValue('{:.2f}'.format(totaleeuromc))
        else:
            totalenettomc = ''
            self.totale_netto.SetValue(totalenettomc)
            totaleeuromc = round((totalemc * prezzo_vendita), 2)
            self.ricavo.SetValue('{:.2f}'.format(totaleeuromc))

    def chkbox(self, event):
        n = frame.pannello_principale.lista_boschi_listbox.GetSelections()
        try:
            bosco = boschi[n[0]]
        except IndexError:
            wx.MessageBox('seleziona un bosco')
            self.corteccia.SetValue(False)
            return
        global corteccia
        corteccia = self.corteccia.GetValue()
        if corteccia:
            bosco.corteccia = 1
        else:
            bosco.corteccia = 0
        bosco.modificaBosco()
        self.fai_totale_netto()

    def venditacg(self, event):
        n = frame.pannello_principale.lista_boschi_listbox.GetSelections()
        try:
            bosco = boschi[n[0]]
        except IndexError:
            wx.MessageBox('seleziona un bosco')
            self.prezzo_vendita.ChangeValue('')
            return
        try:
            prezzo_vendita = float(self.prezzo_vendita.GetValue()) if self.prezzo_vendita.GetValue() != '' else 0
        except ValueError:
            wx.MessageBox('Richiesto valore numerico')
            self.prezzo_vendita.SetValue(self.prezzo_vendita.GetValue()[0:-1])
            self.prezzo_vendita.SetFocus()
            return
        bosco.venditamc = prezzo_vendita
        bosco.modificaBosco()
        self.fai_totale_netto()

    def fai_stampa(self, event):
        n = frame.pannello_principale.lista_boschi_listbox.GetSelections()
        try:
            bosco = boschi[n[0]]
        except IndexError:
            wx.MessageBox('seleziona un bosco')
            return
        if tronchi:
            saveFileDialog = wx.FileDialog(self, message="Salva File",
                                           defaultDir="",
                                           defaultFile="{}".format(bosco.luogo),
                                           wildcard="File PDF (*.pdf)|*.pdf",
                                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
            if saveFileDialog.ShowModal() == wx.ID_OK:
                file = saveFileDialog.GetPath()
                saveFileDialog.Destroy()
                ok = stampa(file, tronchi, totalemc, corteccia, totalenettomc)
                if ok:
                    if os.name == 'posix':
                        os.system('open "{}"'.format(file))
                    else:
                        wx.MessageBox('File creato correttamente !')
        else:
            wx.MessageBox('Niente da stampare !')


class PannelloArdere(wx.Panel):
    def __init__(self, *a, **k):
        wx.Panel.__init__(self, *a, **k)
        self.tabella_ardere = wx.grid.Grid(self, size=wx.Size(545, -1))

        # Grid
        self.tabella_ardere.CreateGrid(0, 5)
        self.tabella_ardere.EnableEditing(False)
        self.tabella_ardere.EnableGridLines(True)
        self.tabella_ardere.EnableDragGridSize(False)
        self.tabella_ardere.SetMargins(0, 0)

        # Columns
        self.tabella_ardere.EnableDragColMove(False)
        self.tabella_ardere.EnableDragColSize(True)
        self.tabella_ardere.SetColLabelSize(20)
        self.tabella_ardere.SetColLabelValue(0, 'Data')
        self.tabella_ardere.SetColSize(0, 95)
        self.tabella_ardere.SetColLabelValue(1, 'Quintali')
        self.tabella_ardere.SetColSize(1, 70)
        self.tabella_ardere.SetColLabelValue(2, u'Prezzo €')
        self.tabella_ardere.SetColSize(2, 70)
        self.tabella_ardere.SetColLabelValue(3, u'Totale €')
        self.tabella_ardere.SetColSize(3, 80)
        self.tabella_ardere.SetColLabelValue(4, 'Note')
        self.tabella_ardere.SetColSize(4, 190)
        self.tabella_ardere.SetColLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        # Rows
        self.tabella_ardere.EnableDragRowSize(True)
        self.tabella_ardere.SetRowLabelSize(20)
        self.tabella_ardere.SetRowLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        # Cell Defaults
        self.tabella_ardere.SetDefaultCellAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        self.totaleq = wx.TextCtrl(self, size=wx.Size(80, 25), style=wx.TE_RIGHT | wx.TE_READONLY)
        self.totale_euro_ardere = wx.TextCtrl(self, size=wx.Size(80, 25), style=wx.TE_RIGHT | wx.TE_READONLY)
        self.totale_euro_ardere.SetFont(wx.Font(12, 70, 90, 92, False, wx.EmptyString))

        self.button_nuovo_ardere = wx.Button(self, wx.ID_ANY, u"Nuovo")
        self.button_modifica_ardere = wx.Button(self, wx.ID_ANY, u"Modifica")
        self.button_elimina_ardere = wx.Button(self, wx.ID_ANY, u"Elimina")

        self.Layout()

        bSizer1 = wx.BoxSizer(wx.VERTICAL)
        bSizer1.Add(self.tabella_ardere, 3, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)
        bSizer2 = wx.BoxSizer(wx.HORIZONTAL)
        bSizer2.Add(wx.StaticText(self, -1, 'Totale q'), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        bSizer2.Add(self.totaleq, 0, wx.ALL, 5)
        bSizer2.Add(wx.StaticText(self, -1, u'Totale €'), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        bSizer2.Add(self.totale_euro_ardere, 0, wx.ALL, 5)
        bSizer2.AddSpacer((0, 0), 1, wx.EXPAND, 5)
        bSizer2.Add(self.button_nuovo_ardere, 0, wx.ALL, 5)
        bSizer2.Add(self.button_modifica_ardere, 0, wx.ALL, 5)
        bSizer2.Add(self.button_elimina_ardere, 0, wx.ALL, 5)
        bSizer1.Add(bSizer2, 0, wx.EXPAND, 5)
        bSizer1.Fit(self)
        self.SetSizer(bSizer1)

        # Connect Events
        self.button_nuovo_ardere.Bind(wx.EVT_BUTTON, self.nuovo_ardere)
        self.button_modifica_ardere.Bind(wx.EVT_BUTTON, self.modifica_ardere)
        self.button_elimina_ardere.Bind(wx.EVT_BUTTON, self.elimina_ardere)

    def crea_griglia_ardere(self):
        n = frame.pannello_principale.lista_boschi_listbox.GetSelections()
        bosco = boschi[n[0]]
        global legna_da_ardere
        legna_da_ardere = funzioni.leggiArdere(bosco)
        righe = self.tabella_ardere.GetNumberRows()
        if righe > 0:
            self.tabella_ardere.DeleteRows(0, righe)
        global totale_euro_ardere
        global totaleq
        totale_euro_ardere = 0
        totaleq = 0
        for i, ardere in enumerate(legna_da_ardere):
            self.tabella_ardere.InsertRows(-1)
            self.tabella_ardere.SetCellValue(i, 0, str(ardere.data.strftime('%d-%m-%Y')))
            self.tabella_ardere.SetCellValue(i, 1, str(ardere.quintali))
            self.tabella_ardere.SetCellValue(i, 2, '{:.2f}'.format(ardere.prezzo))
            self.tabella_ardere.SetCellValue(i, 3, '{:.2f}'.format(ardere.totale))
            self.tabella_ardere.SetCellValue(i, 4, ardere.note)
            totale_euro_ardere += ardere.totale
            totaleq += ardere.quintali
        self.tabella_ardere.Scroll(-1, 100000)
        self.totaleq.SetValue(str(totaleq))
        self.totale_euro_ardere.SetValue('{:.2f}'.format(totale_euro_ardere))

    def nuovo_ardere(self, event):
        n = frame.pannello_principale.lista_boschi_listbox.GetSelections()
        try:
            bosco = boschi[n[0]]
        except IndexError:
            wx.MessageBox('seleziona un bosco')
            return
        dlg = DlgInserisciArdere(self, bosco)
        retcode = dlg.ShowModal()
        if retcode == wx.ID_OK:
            ardere = dlg.leggi_dati()
            ardere.inserisciArdere()
        self.crea_griglia_ardere()

    def modifica_ardere(self, event):
        try:
            nb = frame.pannello_principale.lista_boschi_listbox.GetSelections()
            na = self.tabella_ardere.GetSelectedRows()
            bosco = boschi[nb[0]]
        except IndexError:
            wx.MessageBox('seleziona un bosco')
            return
        try:
            ardere = legna_da_ardere[na[0]]
            dlg = DlgInserisciArdere(self, bosco, ardere)
            retcode = dlg.ShowModal()
            if retcode == wx.ID_OK:
                ardere = dlg.leggi_dati()
                ardere.modificaArdere()
            self.crea_griglia_ardere()
        except IndexError:
            wx.MessageBox('seleziona la legna')
            return

    def elimina_ardere(self, event):
        n = self.tabella_ardere.GetSelectedRows()
        try:
            ardere = legna_da_ardere[n[0]]
            if dlg_yes_no(self):
                ardere.eliminaArdere()
            self.crea_griglia_ardere()
        except IndexError:
            wx.MessageBox(u"seleziona la legna da eliminare")
            return


class PannelloSpese(wx.Panel):
    def __init__(self, *a, **k):
        wx.Panel.__init__(self, *a, **k)
        self.tabella_spese = wx.grid.Grid(self, size=wx.Size(590, -1))

        # Grid
        self.tabella_spese.CreateGrid(0, 6)
        self.tabella_spese.EnableEditing(False)
        self.tabella_spese.EnableGridLines(True)
        self.tabella_spese.EnableDragGridSize(False)
        self.tabella_spese.SetMargins(0, 0)

        # Columns
        self.tabella_spese.EnableDragColMove(False)
        self.tabella_spese.EnableDragColSize(True)
        self.tabella_spese.SetColLabelSize(20)
        self.tabella_spese.SetColLabelValue(0, 'Data')
        self.tabella_spese.SetColSize(0, 95)
        self.tabella_spese.SetColLabelValue(1, 'Tipo Spesa')
        self.tabella_spese.SetColSize(1, 165)
        self.tabella_spese.SetColLabelValue(2, u'Prezzo €')
        self.tabella_spese.SetColSize(2, 60)
        self.tabella_spese.SetColLabelValue(3, u"Unità")
        self.tabella_spese.SetColSize(3, 40)
        self.tabella_spese.SetColLabelValue(4, u'Totale €')
        self.tabella_spese.SetColSize(4, 60)
        self.tabella_spese.SetColLabelValue(5, 'Note')
        self.tabella_spese.SetColSize(5, 130)
        self.tabella_spese.SetColLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        # Rows
        self.tabella_spese.EnableDragRowSize(True)
        self.tabella_spese.SetRowLabelSize(20)
        self.tabella_spese.SetRowLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        # Cell Defaults
        self.tabella_spese.SetDefaultCellAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        self.totale_spese = wx.TextCtrl(self, size=wx.Size(80, 25), style=wx.TE_RIGHT | wx.TE_READONLY)
        self.totale_spese.SetFont(wx.Font(12, 70, 90, 92, False, wx.EmptyString))
        self.button_nuovo_spesa = wx.Button(self, wx.ID_ANY, u"Nuovo")
        self.button_modifica_spesa = wx.Button(self, wx.ID_ANY, u"Modifica")
        self.button_elimina_spesa = wx.Button(self, wx.ID_ANY, u"Elimina")

        self.Layout()

        bSizer1 = wx.BoxSizer(wx.VERTICAL)
        bSizer1.Add(self.tabella_spese, 3, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)
        bSizer2 = wx.BoxSizer(wx.HORIZONTAL)
        bSizer2.Add(wx.StaticText(self, -1, u'Totale spese €'), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        bSizer2.Add(self.totale_spese, 0, wx.ALL, 5)
        bSizer2.AddSpacer((0, 0), 1, wx.EXPAND, 5)
        bSizer2.Add(self.button_nuovo_spesa, 0, wx.ALL, 5)
        bSizer2.Add(self.button_modifica_spesa, 0, wx.ALL, 5)
        bSizer2.Add(self.button_elimina_spesa, 0, wx.ALL, 5)
        bSizer1.Add(bSizer2, 0, wx.EXPAND, 5)
        bSizer1.Fit(self)

        self.SetSizer(bSizer1)

        # Connect Events
        self.button_nuovo_spesa.Bind(wx.EVT_BUTTON, self.nuovo_spesa)
        self.button_modifica_spesa.Bind(wx.EVT_BUTTON, self.modifica_spesa)
        self.button_elimina_spesa.Bind(wx.EVT_BUTTON, self.elimina_spesa)

    def crea_griglia_spesa(self):
        n = frame.pannello_principale.lista_boschi_listbox.GetSelections()
        bosco = boschi[n[0]]
        global spese
        spese = funzioni.leggiSpese(bosco)
        righe = self.tabella_spese.GetNumberRows()
        if righe > 0:
            self.tabella_spese.DeleteRows(0, righe)
        global totale_spese
        totale_spese = 0
        for i, spesa in enumerate(spese):
            self.tabella_spese.InsertRows(-1)
            self.tabella_spese.SetCellValue(i, 0, str(spesa.data.strftime('%d-%m-%Y')))
            self.tabella_spese.SetCellValue(i, 1, spesa.tipo)
            self.tabella_spese.SetCellValue(i, 2, '{:.2f}'.format(spesa.prezzo_uni))
            self.tabella_spese.SetCellValue(i, 3, str(spesa.unita))
            self.tabella_spese.SetCellValue(i, 4, '{:.2f}'.format(spesa.totale))
            self.tabella_spese.SetCellValue(i, 5, spesa.note)
            totale_spese += spesa.totale
        self.tabella_spese.Scroll(-1, 100000)
        self.totale_spese.SetValue('{:.2f}'.format(totale_spese))

    def nuovo_spesa(self, event):
        n = frame.pannello_principale.lista_boschi_listbox.GetSelections()
        try:
            bosco = boschi[n[0]]
        except IndexError:
            wx.MessageBox('seleziona un bosco')
            return
        dlg = DlgInserisciSpesa(self, bosco)
        retcode = dlg.ShowModal()
        if retcode == wx.ID_OK:
            spesa = dlg.leggi_dati()
            spesa.inserisciSpesa()
        self.crea_griglia_spesa()

    def modifica_spesa(self, event):
        try:
            nb = frame.pannello_principale.lista_boschi_listbox.GetSelections()
            ns = self.tabella_spese.GetSelectedRows()
            bosco = boschi[nb[0]]
        except IndexError:
            wx.MessageBox('seleziona un bosco')
            return
        try:
            spesa = spese[ns[0]]
            dlg = DlgInserisciSpesa(self, bosco, spesa)
            retcode = dlg.ShowModal()
            if retcode == wx.ID_OK:
                spesa = dlg.leggi_dati()
                spesa.modificaSpesa()
                self.crea_griglia_spesa()
        except IndexError:
            wx.MessageBox(u"seleziona la spesa")
            return

    def elimina_spesa(self, event):
        n = self.tabella_spese.GetSelectedRows()
        try:
            spesa = spese[n[0]]
            if dlg_yes_no(self):
                spesa.eliminaSpesa()
            self.crea_griglia_spesa()
        except IndexError:
            wx.MessageBox(u"seleziona la spesa da eliminare")
            return


class PannelloOre(wx.Panel):
    def __init__(self, *a, **k):
        wx.Panel.__init__(self, *a, **k)
        self.tabella_ore = wx.grid.Grid(self, size=wx.Size(590, -1))

        # Grid
        self.tabella_ore.CreateGrid(0, 6)
        self.tabella_ore.EnableEditing(False)
        self.tabella_ore.EnableGridLines(True)
        self.tabella_ore.EnableDragGridSize(False)
        self.tabella_ore.SetMargins(0, 0)

        # Columns
        self.tabella_ore.EnableDragColMove(False)
        self.tabella_ore.EnableDragColSize(True)
        self.tabella_ore.SetColLabelSize(20)
        self.tabella_ore.SetColLabelValue(0, 'Data')
        self.tabella_ore.SetColSize(0, 95)
        self.tabella_ore.SetColLabelValue(1, 'Ore')
        self.tabella_ore.SetColSize(1, 50)
        self.tabella_ore.SetColLabelValue(2, u'Prezzo €')
        self.tabella_ore.SetColSize(2, 50)
        self.tabella_ore.SetColLabelValue(3, u"Totale €")
        self.tabella_ore.SetColSize(3, 60)
        self.tabella_ore.SetColLabelValue(4, "Tipo Lavoro")
        self.tabella_ore.SetColSize(4, 150)
        self.tabella_ore.SetColLabelValue(5, 'Note')
        self.tabella_ore.SetColSize(5, 145)

        self.tabella_ore.SetColLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        # Rows
        self.tabella_ore.EnableDragRowSize(True)
        self.tabella_ore.SetRowLabelSize(20)
        self.tabella_ore.SetRowLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        # Cell Defaults
        self.tabella_ore.SetDefaultCellAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        self.totale_ore = wx.TextCtrl(self, size=wx.Size(80, 25), style=wx.TE_RIGHT | wx.TE_READONLY)
        self.totale_euro_ore = wx.TextCtrl(self, size=wx.Size(80, 25), style=wx.TE_RIGHT | wx.TE_READONLY)
        self.totale_euro_ore.SetFont(wx.Font(12, 70, 90, 92, False, wx.EmptyString))
        self.button_nuovo_ore = wx.Button(self, wx.ID_ANY, u"Nuovo")
        self.button_modifica_ore = wx.Button(self, wx.ID_ANY, u"Modifica")
        self.button_elimina_ore = wx.Button(self, wx.ID_ANY, u"Elimina")

        self.Layout()

        bSizer1 = wx.BoxSizer(wx.VERTICAL)
        bSizer1.Add(self.tabella_ore, 3, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)
        bSizer2 = wx.BoxSizer(wx.HORIZONTAL)
        bSizer2.Add(wx.StaticText(self, -1, 'Totale ore:'), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        bSizer2.Add(self.totale_ore, 0, wx.ALL, 5)
        bSizer2.Add(wx.StaticText(self, -1, u'Totale €:'), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        bSizer2.Add(self.totale_euro_ore, 0, wx.ALL, 5)
        bSizer2.AddSpacer((0, 0), 1, wx.EXPAND, 5)
        bSizer2.Add(self.button_nuovo_ore, 0, wx.ALL, 5)
        bSizer2.Add(self.button_modifica_ore, 0, wx.ALL, 5)
        bSizer2.Add(self.button_elimina_ore, 0, wx.ALL, 5)
        bSizer1.Add(bSizer2, 0, wx.EXPAND, 5)
        bSizer1.Fit(self)

        self.SetSizer(bSizer1)

        # Connect Events
        self.button_nuovo_ore.Bind(wx.EVT_BUTTON, self.nuovo_ore)
        self.button_modifica_ore.Bind(wx.EVT_BUTTON, self.modifica_ore)
        self.button_elimina_ore.Bind(wx.EVT_BUTTON, self.elimina_ore)

    def crea_griglia_ore(self):
        n = frame.pannello_principale.lista_boschi_listbox.GetSelections()
        bosco = boschi[n[0]]
        global lista_ore, totale_ore, totale_euro_ore
        lista_ore = funzioni.leggiOre(bosco)
        righe = self.tabella_ore.GetNumberRows()
        if righe > 0:
            self.tabella_ore.DeleteRows(0, righe)
        totale_euro_ore = 0
        totale_ore = 0
        for i, ore in enumerate(lista_ore):
            self.tabella_ore.InsertRows(-1)
            self.tabella_ore.SetCellValue(i, 0, str(ore.data.strftime('%d-%m-%Y')))
            self.tabella_ore.SetCellValue(i, 1, str(ore.numero_ore))
            self.tabella_ore.SetCellValue(i, 2, '{:.2f}'.format(ore.prezzo_uni))
            self.tabella_ore.SetCellValue(i, 3, '{:.2f}'.format(ore.totale))
            self.tabella_ore.SetCellValue(i, 4, ore.tipo_lavoro)
            self.tabella_ore.SetCellValue(i, 5, ore.note)
            totale_ore += ore.numero_ore
            totale_euro_ore += ore.totale
        self.tabella_ore.Scroll(-1, 100000)
        self.totale_ore.SetValue(str(totale_ore))
        self.totale_euro_ore.SetValue('{:.2f}'.format(totale_euro_ore))

    def nuovo_ore(self, event):
        n = frame.pannello_principale.lista_boschi_listbox.GetSelections()
        try:
            bosco = boschi[n[0]]
        except IndexError:
            wx.MessageBox('seleziona un bosco')
            return
        dlg = DlgInserisciOre(self, bosco)
        retcode = dlg.ShowModal()
        if retcode == wx.ID_OK:
            ore = dlg.leggi_dati()
            ore.inserisciOre()
        self.crea_griglia_ore()

    def modifica_ore(self, event):
        try:
            nb = frame.pannello_principale.lista_boschi_listbox.GetSelections()
            no = self.tabella_ore.GetSelectedRows()
            bosco = boschi[nb[0]]
        except IndexError:
            wx.MessageBox('seleziona un bosco')
            return
        try:
            ore = lista_ore[no[0]]
            dlg = DlgInserisciOre(self, bosco, ore)
            retcode = dlg.ShowModal()
            if retcode == wx.ID_OK:
                ore = dlg.leggi_dati()
                ore.modificaOre()
            self.crea_griglia_ore()

        except IndexError:
            wx.MessageBox(u"seleziona le ore")
            return

    def elimina_ore(self, event):
        n = self.tabella_ore.GetSelectedRows()
        try:
            ore = lista_ore[n[0]]
            if dlg_yes_no(self):
                ore.eliminaOre()
            self.crea_griglia_ore()

        except IndexError:
            wx.MessageBox(u"seleziona la spesa da eliminare")
            return


class PannelloTotali(wx.Panel):
    def __init__(self, *a, **k):
        wx.Panel.__init__(self, *a, **k)

        self.totale_metri_cubi = wx.TextCtrl(self, style=wx.TE_RIGHT | wx.TE_READONLY)
        self.corteccia = wx.TextCtrl(self, size=(30, -1), style=wx.TE_RIGHT | wx.TE_READONLY)
        self.totale_nettomq = wx.TextCtrl(self, style=wx.TE_RIGHT | wx.TE_READONLY)
        self.totale_euro_mq = wx.TextCtrl(self, style=wx.TE_RIGHT | wx.TE_READONLY)
        self.totale_euro_mq.SetBackgroundColour(wx.Colour(180, 250, 200))
        self.totale_legna_ardere = wx.TextCtrl(self, style=wx.TE_RIGHT | wx.TE_READONLY)
        self.totale_euro_ardere = wx.TextCtrl(self, style=wx.TE_RIGHT | wx.TE_READONLY)
        self.totale_euro_ardere.SetBackgroundColour(wx.Colour(180, 250, 200))
        self.totale_spese = wx.TextCtrl(self, style=wx.TE_RIGHT | wx.TE_READONLY)
        self.totale_spese.SetBackgroundColour(wx.Colour(250, 150, 200))
        self.totale_ore_lavoro = wx.TextCtrl(self, style=wx.TE_RIGHT | wx.TE_READONLY)
        self.totale_euro_ore = wx.TextCtrl(self, style=wx.TE_RIGHT | wx.TE_READONLY)
        self.totale_euro_ore.SetBackgroundColour(wx.Colour(250, 150, 200))
        self.acquisto_mc = wx.TextCtrl(self, style=wx.TE_RIGHT | wx.TE_READONLY)
        self.totale_euro_acq_mc = wx.TextCtrl(self, style=wx.TE_RIGHT | wx.TE_READONLY)
        self.totale_euro_acq_mc.SetBackgroundColour(wx.Colour(250, 150, 200))
        self.acquisto_q = wx.TextCtrl(self, style=wx.TE_RIGHT | wx.TE_READONLY)
        self.totale_euro_acq_q = wx.TextCtrl(self, style=wx.TE_RIGHT | wx.TE_READONLY)
        self.totale_euro_acq_q.SetBackgroundColour(wx.Colour(250, 150, 200))
        self.euro_forfait = wx.TextCtrl(self, style=wx.TE_RIGHT | wx.TE_READONLY)
        self.euro_forfait.SetBackgroundColour(wx.Colour(250, 150, 200))
        self.euro_netto = wx.TextCtrl(self, size=wx.Size(-1, 25), style=wx.TE_RIGHT | wx.TE_READONLY)
        self.euro_netto.SetFont(wx.Font(12, 70, 90, 92, False, wx.EmptyString))
        self.euro_netto.SetBackgroundColour(wx.Colour(255, 250, 100))

        self.testo_netto = wx.StaticText(self, -1, u"TOTALE NETTO:")
        self.testo_netto.SetFont(wx.Font(12, 70, 90, 92, False, wx.EmptyString))

        bsizer = wx.BoxSizer(wx.VERTICAL)
        gbSizer1 = wx.GridBagSizer(15, 5)

        gbSizer1.Add(wx.StaticText(self, -1, u"TRONCHI:"), pos=(0, 0), flag=wx.ALIGN_CENTER_VERTICAL)
        gbSizer1.Add(wx.StaticText(self, -1, u"Totale metri cubi:"), pos=(1, 0), flag=wx.ALIGN_CENTER_VERTICAL)
        gbSizer1.Add(self.totale_metri_cubi, pos=(1, 1), flag=wx.ALL)
        gbSizer1.AddSpacer((30, 0), pos=(1, 2))
        gbSizer1.Add(wx.StaticText(self, -1, u"corteccia:"), pos=(1, 3),
                     flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        gbSizer1.Add(self.corteccia, pos=(1, 4), flag=wx.ALL)
        gbSizer1.Add(wx.StaticText(self, -1, u"Totale netto metri cubi:"), pos=(2, 0), flag=wx.ALIGN_CENTER_VERTICAL)
        gbSizer1.Add(self.totale_nettomq, pos=(2, 1), flag=wx.ALL)
        gbSizer1.Add(wx.StaticText(self, -1, u"Totale tronchi €:"), pos=(2, 3),
                     flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        gbSizer1.Add(self.totale_euro_mq, pos=(2, 4), flag=wx.ALL)

        gbSizer1.Add(wx.StaticText(self, -1, u"LEGNA DA ARDERE:"), pos=(3, 0), flag=wx.ALIGN_CENTER_VERTICAL)
        gbSizer1.Add(wx.StaticText(self, -1, u"Totale legna da ardere q:"), pos=(4, 0), flag=wx.ALIGN_CENTER_VERTICAL)
        gbSizer1.Add(self.totale_legna_ardere, pos=(4, 1), flag=wx.ALL)
        gbSizer1.Add(wx.StaticText(self, -1, u"Totale legna da ardere €:"), pos=(4, 3),
                     flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        gbSizer1.Add(self.totale_euro_ardere, pos=(4, 4), flag=wx.ALL)

        gbSizer1.Add(wx.StaticText(self, -1, u"ORE LAVORO:"), pos=(5, 0), flag=wx.ALIGN_CENTER_VERTICAL)
        gbSizer1.Add(wx.StaticText(self, -1, u"Totale ore lavoro:"), pos=(6, 0), flag=wx.ALIGN_CENTER_VERTICAL)
        gbSizer1.Add(self.totale_ore_lavoro, pos=(6, 1), flag=wx.ALL)
        gbSizer1.Add(wx.StaticText(self, -1, u"Totale ore lavoro €:"), pos=(6, 3),
                     flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        gbSizer1.Add(self.totale_euro_ore, pos=(6, 4), flag=wx.ALL)

        gbSizer1.Add(wx.StaticText(self, -1, u"SPESE:"), pos=(7, 0), flag=wx.ALIGN_CENTER_VERTICAL)
        gbSizer1.Add(wx.StaticText(self, -1, u"Totale spese €:"), pos=(8, 3),
                     flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        gbSizer1.Add(self.totale_spese, pos=(8, 4), flag=wx.ALL)

        gbSizer1.Add(wx.StaticText(self, -1, u"ACQUISTO BOSCO:"), pos=(9, 0), flag=wx.ALIGN_CENTER_VERTICAL)
        gbSizer1.Add(wx.StaticText(self, -1, u"Acquisto al mc €:"), pos=(10, 0), flag=wx.ALIGN_CENTER_VERTICAL)
        gbSizer1.Add(self.acquisto_mc, pos=(10, 1), flag=wx.ALL)
        gbSizer1.Add(wx.StaticText(self, -1, u"Totale acquisto mc €:"), pos=(10, 3),
                     flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        gbSizer1.Add(self.totale_euro_acq_mc, pos=(10, 4), flag=wx.ALL)
        gbSizer1.Add(wx.StaticText(self, -1, u"Acquisto al q €:"), pos=(11, 0), flag=wx.ALIGN_CENTER_VERTICAL)
        gbSizer1.Add(self.acquisto_q, pos=(11, 1), flag=wx.ALL)
        gbSizer1.Add(wx.StaticText(self, -1, u"Totale acquisto q €:"), pos=(11, 3),
                     flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        gbSizer1.Add(self.totale_euro_acq_q, pos=(11, 4), flag=wx.ALL)
        gbSizer1.Add(wx.StaticText(self, -1, u"Forfait €:"), pos=(12, 3),
                     flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        gbSizer1.Add(self.euro_forfait, pos=(12, 4), flag=wx.ALL)

        gbSizer1.Add(self.testo_netto, pos=(13, 3), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        gbSizer1.Add(self.euro_netto, pos=(13, 4), flag=wx.ALL)
        bsizer.Add(gbSizer1, 1, wx.EXPAND | wx.ALL, 15)

        self.SetSizer(bsizer)
        bsizer.Layout()

    def fai_totali(self, event=0):
        frame.pannello_principale.pannello_tronchi.fai_totale_netto()
        self.totale_metri_cubi.SetValue(str(totalemc))
        self.corteccia.SetValue('Si' if corteccia else 'No')
        self.totale_nettomq.SetValue(str(totalenettomc))
        self.totale_euro_mq.SetValue('{:.2f}'.format(totaleeuromc))
        self.totale_legna_ardere.SetValue(str(totaleq))
        self.totale_euro_ardere.SetValue('{:.2f}'.format(totale_euro_ardere))
        self.totale_spese.SetValue('{:.2f}'.format(totale_spese))
        self.totale_ore_lavoro.SetValue(str(totale_ore))
        self.totale_euro_ore.SetValue('{:.2f}'.format(totale_euro_ore))
        n = frame.pannello_principale.lista_boschi_listbox.GetSelections()
        prezzomc = 0
        prezzoq = 0
        forfait = 0

        try:
            bosco = boschi[n[0]]
            prezzomc = bosco.prezzomc
            prezzoq = bosco.prezzoq
            forfait = bosco.forfait
        except:
            pass

        self.acquisto_mc.SetValue('{:.2f}'.format(prezzomc))
        self.acquisto_q.SetValue('{:.2f}'.format(prezzoq))
        self.euro_forfait.SetValue('{:.2f}'.format(forfait))
        tot_acq_mc = prezzomc * (totalemc if not corteccia else totalenettomc)
        self.totale_euro_acq_mc.SetValue('{:.2f}'.format(tot_acq_mc))
        tot_acq_q = prezzoq * totaleq
        self.totale_euro_acq_q.SetValue('{:.2f}'.format(tot_acq_q))
        totale_netto = (totaleeuromc + totale_euro_ardere) - \
                       (tot_acq_mc + tot_acq_q + forfait + totale_spese + totale_euro_ore)
        self.euro_netto.SetValue('{:.2f}'.format(totale_netto))

        try:
            event.Skip()
        except AttributeError:
            pass


class DlgInserisciBosco(wx.Dialog):
    def __init__(self, parent, bosco=0, proprietario=0):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title='Nuovo Bosco')
        self.bosco = bosco
        self.proprietario = proprietario
        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        self.cognome = wx.TextCtrl(self, validator=NotEmptyValidator())
        self.nome = wx.TextCtrl(self, validator=NotEmptyValidator())
        self.citta = wx.TextCtrl(self)
        self.indirizzo = wx.TextCtrl(self, size=wx.Size(150, -1))
        self.n = wx.TextCtrl(self, size=wx.Size(50, -1))
        self.provincia = wx.TextCtrl(self)
        self.tel = wx.TextCtrl(self)

        self.luogo = wx.TextCtrl(self, validator=NotEmptyValidator())
        self.mappale = wx.TextCtrl(self, validator=NumberNotEmptyValidator())
        self.denuncia_taglio = wx.TextCtrl(self)
        self.data_denuncia = wx.DatePickerCtrl(self, dt=wx.DateTime.Now())
        self.prezzomc = wx.TextCtrl(self, validator=NumberValidator())
        self.prezzoq = wx.TextCtrl(self, validator=NumberValidator())
        self.forfait = wx.TextCtrl(self, validator=NumberValidator())
        self.corteccia = 0
        self.venditamc = 0

        self.line1 = wx.StaticLine(self, style=wx.LI_HORIZONTAL)
        self.line2 = wx.StaticLine(self, style=wx.LI_HORIZONTAL)

        self.button_ok = wx.Button(self, wx.ID_OK, u"Ok")
        self.button_ok.SetDefault()
        self.button_cancel = wx.Button(self, wx.ID_CANCEL, u"Annulla")

        if bosco != 0 and proprietario != 0:
            self.cognome.SetValue(proprietario.cognome)
            self.nome.SetValue(proprietario.nome)
            self.citta.SetValue(proprietario.citta)
            self.indirizzo.SetValue(proprietario.indirizzo)
            self.n.SetValue(proprietario.numero)
            self.provincia.SetValue(proprietario.provincia)
            self.tel.SetValue(proprietario.tel)

            self.luogo.SetValue(bosco.luogo)
            self.mappale.SetValue(bosco.mappale)
            self.denuncia_taglio.SetValue(bosco.denuncia_taglio)
            self.data_denuncia.SetValue(funzioni.wxdatetime_from_db_date(bosco.data_denuncia))
            self.prezzomc.SetValue(str(bosco.prezzomc))
            self.prezzoq.SetValue(str(bosco.prezzoq))
            self.forfait.SetValue(str(bosco.forfait))
            self.corteccia = bosco.corteccia
            self.venditamc = bosco.venditamc

        bSizer1 = wx.BoxSizer(wx.VERTICAL)
        bSizer2 = wx.BoxSizer(wx.HORIZONTAL)
        fgSizer2 = wx.FlexGridSizer(7, 6, 0, 0)

        fgSizer2.Add(wx.StaticText(self, -1, u"Cognome:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 5)
        fgSizer2.Add(self.cognome, 0, wx.ALL, 5)
        fgSizer2.Add(wx.StaticText(self, -1, u"Nome:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 5)
        fgSizer2.Add(self.nome, 0, wx.ALL, 5)
        fgSizer2.Add(wx.StaticText(self, -1, u"Città:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 5)
        fgSizer2.Add(self.citta, 0, wx.ALL, 5)
        fgSizer2.Add(wx.StaticText(self, -1, u"Indirizzo:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 5)
        fgSizer2.Add(self.indirizzo, 0, wx.ALL, 5)
        fgSizer2.Add(wx.StaticText(self, -1, u"n:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 5)
        fgSizer2.Add(self.n, 0, wx.ALL, 5)
        fgSizer2.Add(wx.StaticText(self, -1, u"Provincia:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 5)
        fgSizer2.Add(self.provincia, 0, wx.ALL, 5)
        fgSizer2.Add(wx.StaticText(self, -1, u"Telefono:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 5)
        fgSizer2.Add(self.tel, 0, wx.ALL, 5)
        fgSizer2.AddSpacer((0, 0), 0, wx.EXPAND, 5)
        fgSizer2.AddSpacer((0, 0), 0, wx.EXPAND, 5)
        fgSizer2.AddSpacer((0, 0), 0, wx.EXPAND, 5)
        fgSizer2.AddSpacer((0, 0), 0, wx.EXPAND, 5)
        fgSizer2.Add(wx.StaticText(self, -1, u"Luogo:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 5)
        fgSizer2.Add(self.luogo, 0, wx.ALL, 5)
        fgSizer2.Add(wx.StaticText(self, -1, u"Mappale:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 5)
        fgSizer2.Add(self.mappale, 0, wx.ALL, 5)
        fgSizer2.Add(wx.StaticText(self, -1, u"Denuncia Taglio:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 5)
        fgSizer2.Add(self.denuncia_taglio, 0, wx.ALL, 5)
        fgSizer2.Add(wx.StaticText(self, -1, u"Data Denuncia:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 5)
        fgSizer2.Add(self.data_denuncia, 0, wx.ALL, 5)
        fgSizer2.AddSpacer((0, 0), 0, wx.EXPAND, 5)
        fgSizer2.AddSpacer((0, 0), 0, wx.EXPAND, 5)
        fgSizer2.AddSpacer((0, 0), 0, wx.EXPAND, 5)
        fgSizer2.AddSpacer((0, 0), 0, wx.EXPAND, 5)
        fgSizer2.Add(wx.StaticText(self, -1, u"Prezzo mc €:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 5)
        fgSizer2.Add(self.prezzomc, 0, wx.ALL, 5)
        fgSizer2.Add(wx.StaticText(self, -1, u"Prezzo q €:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 5)
        fgSizer2.Add(self.prezzoq, 0, wx.ALL, 5)
        fgSizer2.Add(wx.StaticText(self, -1, u"Forfait €:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 5)
        fgSizer2.Add(self.forfait, 0, wx.ALL, 5)

        bSizer2.AddSpacer((0, 0), 0, wx.EXPAND, 5)
        bSizer2.Add(self.button_ok, 0, wx.ALL, 5)
        bSizer2.Add(self.button_cancel, 0, wx.ALL, 5)

        bSizer1.Add(fgSizer2, 1, wx.ALL, 5)
        bSizer1.Add(self.line2, 0, wx.EXPAND, 5)
        bSizer1.Add(bSizer2, 0, wx.ALL, 5)
        self.SetSizer(bSizer1)
        self.Layout()
        bSizer1.Fit(self)
        self.Centre(wx.BOTH)

    def leggi_dati(self):
        idproprietario = self.proprietario.idproprietario if self.proprietario != 0 else ''
        cognome = self.cognome.GetValue().capitalize()
        nome = self.nome.GetValue().capitalize()
        citta = self.citta.GetValue().title()
        indirizzo = self.indirizzo.GetValue().title()
        n = self.n.GetValue()
        provincia = self.provincia.GetValue().upper()
        tel = self.tel.GetValue()
        proprietario = Proprietario(idproprietario, cognome, nome, citta, indirizzo, n, provincia, tel)

        idbosco = self.bosco.idbosco if self.bosco != 0 else ''
        luogo = self.luogo.Value
        mappale = self.mappale.Value if self.mappale.Value != '' else 'Null'
        denuncia_taglio = self.denuncia_taglio.Value if self.denuncia_taglio.Value != '' else 'Null'
        data_denuncia = self.data_denuncia.Value.FormatISODate()
        prezzomc = self.prezzomc.Value if self.prezzomc.Value != '' else 0
        prezzoq = self.prezzoq.Value if self.prezzoq.Value != '' else 0
        forfait = self.forfait.Value if self.forfait.Value != '' else 0

        bosco = Bosco(idbosco, idproprietario, luogo, mappale, denuncia_taglio, data_denuncia, prezzomc, prezzoq,
                      forfait, self.corteccia, self.venditamc)

        return proprietario, bosco


class DlgInserisciTronco(wx.Dialog):
    def __init__(self, parent, bosco, tronco=0):
        wx.Dialog.__init__(self, parent)
        self.parent = parent
        self.tronco = tronco
        self.bosco = bosco

        self.specie = wx.TextCtrl(self, validator=NotEmptyValidator())
        self.placchetta = wx.SpinCtrl(self, size=wx.Size(100, 30), min=1, max=99999, initial=1)
        self.placchetta.SetFont(wx.Font(18, 70, 90, 90, False, wx.EmptyString))
        self.lunghezza = wx.TextCtrl(self, size=wx.Size(100, 30), style=wx.TE_CENTRE)
        self.lunghezza.SetFont(wx.Font(18, 70, 90, 90, False, wx.EmptyString))
        self.diametro = wx.TextCtrl(self, size=wx.Size(100, 30), style=wx.TE_CENTRE)
        self.diametro.SetFont(wx.Font(18, 70, 90, 90, False, wx.EmptyString))
        self.button_ok = wx.Button(self, wx.ID_OK)
        self.button_ok.SetDefault()
        self.button_annulla = wx.Button(self, wx.ID_CANCEL, 'Annulla')

        if self.tronco != 0:
            self.specie.SetValue(tronco.specie)
            self.placchetta.SetValue(tronco.placchetta)
            self.lunghezza.SetValue(str(tronco.lunghezza))
            self.diametro.SetValue(str(tronco.diametro))

        gSizer1 = wx.FlexGridSizer(4, 3, 0, 0)
        gSizer1.Add(wx.StaticText(self, -1, u"Specie:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)
        gSizer1.Add(self.specie, 0, wx.ALL, 10)
        gSizer1.AddSpacer((0, 0), 1, wx.EXPAND, 5)
        gSizer1.Add(wx.StaticText(self, -1, u"Placchetta"), 0, wx.ALL, 0)
        gSizer1.Add(wx.StaticText(self, -1, u"Lunghezza m"), 0, wx.ALL, 0)
        gSizer1.Add(wx.StaticText(self, -1, u"Diametro cm"), 0, wx.ALL, 0)
        gSizer1.Add(self.placchetta, 0, wx.ALL, 5)
        gSizer1.Add(self.lunghezza, 0, wx.ALL, 5)
        gSizer1.Add(self.diametro, 0, wx.ALL, 5)
        gSizer1.AddSpacer((0, 0), 1, wx.EXPAND, 5)
        gSizer1.Add(self.button_ok, 0, wx.ALL, 10)
        gSizer1.Add(self.button_annulla, 0, wx.ALL, 10)

        self.SetSizer(gSizer1)
        self.Layout()
        gSizer1.Fit(self)

        self.Centre(wx.BOTH)

        # Connect Events
        self.button_ok.Bind(wx.EVT_BUTTON, self.leggi_dati)
        self.button_annulla.Bind(wx.EVT_BUTTON, self.annulla)

    def leggi_dati(self, event):
        placchetta = self.placchetta.GetValue()
        try:
            lunghezza = float(self.lunghezza.GetValue())
            self.lunghezza.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
            self.lunghezza.Refresh()
        except ValueError:
            wx.MessageBox('Richiesto valore numerico')
            self.lunghezza.SetBackgroundColour('yellow')
            self.lunghezza.Refresh()
            self.lunghezza.SetFocus()
            return
        try:
            diametro = float(self.diametro.GetValue())
            self.diametro.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
            self.diametro.Refresh()
        except ValueError:
            wx.MessageBox('Richiesto valore numerico')
            self.diametro.SetBackgroundColour('yellow')
            self.diametro.Refresh()
            self.diametro.SetFocus()
            return
        idbosco = self.bosco.idbosco
        specie = self.specie.GetValue()
        mc = round(((diametro ** 2 * pi * lunghezza) / 40000), 3)
        if self.tronco != 0:
            t = Tronco(self.tronco.idtronco, idbosco, specie, placchetta, lunghezza, diametro, mc)
            t.modificaTronco()
            self.Destroy()
        else:
            t = Tronco('', idbosco, specie, placchetta, lunghezza, diametro, mc)
            t.inserisciTronco()
        self.placchetta.SetValue(placchetta + 1)
        self.lunghezza.SetValue('')
        self.diametro.SetValue('')
        self.lunghezza.SetFocus()
        self.parent.crea_griglia_tronchi()

    def annulla(self, event):
        self.Destroy()


class DlgInserisciArdere(wx.Dialog):
    def __init__(self, parent, bosco, ardere=0):
        wx.Dialog.__init__(self, parent)
        self.ardere = ardere
        self.bosco = bosco
        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        self.data = wx.DatePickerCtrl(self, dt=wx.DateTime.Now())
        self.quintali = wx.TextCtrl(self, validator=NumberNotEmptyValidator())
        self.prezzo = wx.TextCtrl(self, validator=NumberNotEmptyValidator())
        self.note = wx.TextCtrl(self, size=wx.Size(200, -1))
        self.button_ok = wx.Button(self, wx.ID_OK, u"Ok")
        self.button_ok.SetDefault()
        self.button_annulla = wx.Button(self, wx.ID_CANCEL, u"Annulla")

        gSizer2 = wx.FlexGridSizer(6, 2, 0, 0)
        gSizer2.Add(wx.StaticText(self, -1, u"Data"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)
        gSizer2.Add(self.data, 0, wx.ALL, 10)
        gSizer2.Add(wx.StaticText(self, -1, u"Quintali"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)
        gSizer2.Add(self.quintali, 0, wx.ALL, 5)
        gSizer2.Add(wx.StaticText(self, -1, u"Prezzo €:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)
        gSizer2.Add(self.prezzo, 0, wx.ALL, 5)
        gSizer2.Add(wx.StaticText(self, -1, u"Note:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)
        gSizer2.Add(self.note, 0, wx.ALL, 5)
        gSizer2.Add(self.button_ok, 0, wx.ALL, 10)
        gSizer2.Add(self.button_annulla, 0, wx.ALL, 10)

        if self.ardere != 0:
            self.data.SetValue(funzioni.wxdatetime_from_db_date(ardere.data))
            self.quintali.SetValue(str(ardere.quintali))
            self.prezzo.SetValue(str(ardere.prezzo))
            self.note.SetValue(ardere.note)

        self.SetSizer(gSizer2)
        self.Layout()
        gSizer2.Fit(self)

    def leggi_dati(self):
        data = self.data.Value.FormatISODate()
        quintali = self.quintali.GetValue()
        prezzo = self.prezzo.GetValue()
        note = self.note.GetValue()
        totale = round((float(quintali) * float(prezzo)), 2)
        if self.ardere != 0:
            a = Ardere(self.ardere.idardere, self.bosco.idbosco, data, quintali, prezzo, totale, note)
            return a
        else:
            a = Ardere('', self.bosco.idbosco, data, quintali, prezzo, totale, note)
            return a


class DlgInserisciOre(wx.Dialog):
    def __init__(self, parent, bosco, ore=0):
        wx.Dialog.__init__(self, parent)
        self.ore = ore
        self.bosco = bosco
        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        self.data = wx.DatePickerCtrl(self, dt=wx.DateTime.Now())
        self.ore_lavoro = wx.TextCtrl(self, validator=NumberNotEmptyValidator())
        self.prezzo = wx.TextCtrl(self, validator=NumberNotEmptyValidator())
        self.tipo = wx.TextCtrl(self, size=wx.Size(150, -1))
        self.note = wx.TextCtrl(self, size=wx.Size(150, -1))
        self.button_ok = wx.Button(self, wx.ID_OK, u"Ok")
        self.button_ok.SetDefault()
        self.button_annulla = wx.Button(self, wx.ID_CANCEL, u"Annulla")

        gSizer2 = wx.FlexGridSizer(7, 2, 0, 0)
        gSizer2.Add(wx.StaticText(self, -1, u"Data:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)
        gSizer2.Add(self.data, 0, wx.ALL, 10)
        gSizer2.Add(wx.StaticText(self, -1, u"Numero Ore:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)
        gSizer2.Add(self.ore_lavoro, 0, wx.ALL, 5)
        gSizer2.Add(wx.StaticText(self, -1, u"Prezzo Unitario €:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)
        gSizer2.Add(self.prezzo, 0, wx.ALL, 5)
        gSizer2.Add(wx.StaticText(self, -1, u"Tipo Lavoro:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)
        gSizer2.Add(self.tipo, 0, wx.ALL, 5)
        gSizer2.Add(wx.StaticText(self, -1, u"Note:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)
        gSizer2.Add(self.note, 0, wx.ALL, 5)
        gSizer2.Add(self.button_ok, 0, wx.ALL, 10)
        gSizer2.Add(self.button_annulla, 0, wx.ALL, 10)

        if self.ore != 0:
            self.data.SetValue(funzioni.wxdatetime_from_db_date(ore.data))
            self.ore_lavoro.SetValue(str(ore.numero_ore))
            self.prezzo.SetValue(str(ore.prezzo_uni))
            self.tipo.SetValue(ore.tipo_lavoro)
            self.note.SetValue(ore.note)

        self.SetSizer(gSizer2)
        self.Layout()
        gSizer2.Fit(self)

    def leggi_dati(self):
        data = self.data.Value.FormatISODate()
        ore = self.ore_lavoro.GetValue()
        prezzo = self.prezzo.GetValue()
        tipo = self.tipo.GetValue()
        note = self.note.GetValue()
        totale = round((float(ore) * float(prezzo)), 2)
        if self.ore != 0:
            o = OreLavoro(self.ore.idore, self.bosco.idbosco, data, ore, prezzo, tipo, totale, note)
            return o
        else:
            o = OreLavoro('', self.bosco.idbosco, data, ore, prezzo, tipo, totale, note)
            return o


class DlgInserisciSpesa(wx.Dialog):
    def __init__(self, parent, bosco, spesa=0):
        wx.Dialog.__init__(self, parent)
        self.spesa = spesa
        self.bosco = bosco

        self.data = wx.DatePickerCtrl(self, dt=wx.DateTime.Now())
        self.tipo = wx.TextCtrl(self, size=wx.Size(200, -1))
        self.prezzo = wx.TextCtrl(self, validator=NumberNotEmptyValidator())
        self.unita = wx.TextCtrl(self, validator=NumberValidator())
        self.note = wx.TextCtrl(self, size=wx.Size(200, -1))
        self.button_ok = wx.Button(self, wx.ID_OK, u"Ok")
        self.button_ok.SetDefault()
        self.button_annulla = wx.Button(self, wx.ID_CANCEL, u"Annulla")

        gSizer2 = wx.FlexGridSizer(7, 2, 0, 0)
        gSizer2.Add(wx.StaticText(self, -1, u"Data:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)
        gSizer2.Add(self.data, 0, wx.ALL, 10)
        gSizer2.Add(wx.StaticText(self, -1, u"Tipo Spesa:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)
        gSizer2.Add(self.tipo, 0, wx.ALL, 5)
        gSizer2.Add(wx.StaticText(self, -1, u"Prezzo Unitario €:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)
        gSizer2.Add(self.prezzo, 0, wx.ALL, 5)
        gSizer2.Add(wx.StaticText(self, -1, u"Unità:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)
        gSizer2.Add(self.unita, 0, wx.ALL, 5)
        gSizer2.Add(wx.StaticText(self, -1, u"Note:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)
        gSizer2.Add(self.note, 0, wx.ALL, 5)
        gSizer2.Add(self.button_ok, 0, wx.ALL, 10)
        gSizer2.Add(self.button_annulla, 0, wx.ALL, 10)

        if self.spesa != 0:
            self.data.SetValue(funzioni.wxdatetime_from_db_date(spesa.data))
            self.tipo.SetValue(spesa.tipo)
            self.prezzo.SetValue(str(spesa.prezzo_uni))
            self.unita.SetValue(str(spesa.unita))
            self.note.SetValue(spesa.note)

        self.SetSizer(gSizer2)
        self.Layout()
        gSizer2.Fit(self)

    def leggi_dati(self):
        data = self.data.Value.FormatISODate()
        tipo = self.tipo.GetValue()
        prezzo = self.prezzo.GetValue()
        unita = self.unita.GetValue() if self.unita.GetValue() != '' else 1
        note = self.note.GetValue()
        totale = round((float(prezzo) * float(unita)), 2)
        if self.spesa != 0:
            s = Spesa(self.spesa.idspesa, self.bosco.idbosco, data, tipo, prezzo, unita, totale, note)
            return s
        else:
            s = Spesa('', self.bosco.idbosco, data, tipo, prezzo, unita, totale, note)
            return s


def crea_lista_boschi(stringa=''):
    global boschi, proprietari
    boschi = funzioni.leggiBoschi(stringa)
    proprietari = funzioni.leggiProprietari()
    lista_boschi = [str(Bosco) for Bosco in boschi]
    return lista_boschi


def dlg_yes_no(parent, question='', caption='Sei Sicuro di voler eliminare i dati Selezionati ?'):
    dlg = wx.MessageDialog(parent, question, caption, wx.YES_NO | wx.ICON_QUESTION)
    result = dlg.ShowModal() == wx.ID_YES
    dlg.Destroy()
    return result


class Finestra(wx.Frame):
    def __init__(self, *a, **k):
        wx.Frame.__init__(self, *a, title='Gestione Boschi', size=wx.Size(850, 625),
                          style=wx.DEFAULT_FRAME_STYLE^wx.MAXIMIZE_BOX^wx.RESIZE_BORDER)
        self.SetFont(wx.Font(10, 70, 90, 90))

        menubar = wx.MenuBar()

        mymenu = wx.Menu()
        self.Bind(wx.EVT_MENU, self.on_clic_esporta, mymenu.Append(-1, 'Esporta'))
        self.Bind(wx.EVT_MENU, self.on_clic_importa, mymenu.Append(-1, 'Importa'))
        menubar.Append(mymenu, 'Back-up')

        self.SetMenuBar(menubar)

        self.pannello_principale = PannelloPrincipale(self)

    def on_clic_esporta(self, event):
        file_origine = ''
        if os.name in ("nt", "dos", "ce"):
            file_origine = '%s\\Gestione Boschi\\dati.db' %  os.environ['APPDATA']
        elif os.name == "posix":
            file_origine ='~/Library/Application Support/Gestione Boschi/dati.db'

        dirDialog = wx.DirDialog(self, message="Salva File")
        if dirDialog.ShowModal() == wx.ID_OK:
            path_destinazione = dirDialog.GetPath()
            dirDialog.Destroy()
            shutil.copy(file_origine, path_destinazione)
            wx.MessageBox('Backup Dati eseguito correttamente !')

    def on_clic_importa(self, event):
        file_destinazione = ''
        if os.name in ("nt", "dos", "ce"):
            file_destinazione = '%s\\Gestione Boschi\\dati.db' %  os.environ['APPDATA']
        elif os.name == "posix":
            file_destinazione ='~/Library/Application Support/Gestione Boschi/dati.db'

        openDialog = wx.FileDialog(self, message="Scegli il File",
                                   wildcard="File DB (*.db)|*.db",
                                   style=wx.FD_OPEN)
        if openDialog.ShowModal() == wx.ID_OK:
            file_origine = openDialog.GetPath()
            openDialog.Destroy()
            if dlg_yes_no(self,question='I dati presenti andranno persi', caption='Sei sicuro ?'):
                shutil.copy(file_origine, file_destinazione)
                self.pannello_principale.lista_boschi_listbox.SetItems(crea_lista_boschi())

app = wx.App(False)
frame = Finestra(None)
frame.Show()
app.MainLoop()
