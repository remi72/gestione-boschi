# -*- coding: utf-8 -*-
__author__ = 'remigioscolari'

import wx


class NotEmptyValidator(wx.PyValidator):
    def Clone(self):
        return NotEmptyValidator()

    def TransferToWindow(self):
        return True

    def TransferFromWindow(self):
        return True

    def Validate(self, ctl):
        win = self.GetWindow()
        val = win.GetValue().strip()
        if val == '':
            wx.MessageBox('campo obbligatorio')
            win.SetBackgroundColour('yellow')
            win.Refresh()
            win.SetFocus()
            return False
        else:
            win.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
            win.Refresh()
            return True


class NumberValidator(wx.PyValidator):
    def Clone(self):
        return NumberValidator()

    def TransferToWindow(self):
        return True

    def TransferFromWindow(self):
        return True

    def Validate(self, ctl):
        win = self.GetWindow()
        val = win.GetValue().strip()
        val = 0 if val == '' else val
        try:
            float(val)
            win.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
            win.Refresh()
            return True
        except ValueError:
            wx.MessageBox('Richiesto valore numerico')
            win.SetBackgroundColour('yellow')
            win.Refresh()
            win.SetFocus()
            return False


class NumberNotEmptyValidator(wx.PyValidator):
    def Clone(self):
        return NumberNotEmptyValidator()

    def TransferToWindow(self):
        return True

    def TransferFromWindow(self):
        return True

    def Validate(self, ctl):
        win = self.GetWindow()
        val = win.GetValue().strip()
        try:
            float(val)
            win.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
            win.Refresh()
            return True
        except ValueError:
            wx.MessageBox('Richiesto valore numerico')
            win.SetBackgroundColour('yellow')
            win.Refresh()
            win.SetFocus()
            return False
