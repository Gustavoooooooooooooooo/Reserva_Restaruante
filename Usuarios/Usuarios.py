import wx
import pickle
import sys

class Login(wx.Frame):
    def __init__(self):

        super().__init__(parent=None, title="Usuario")
        pantalla_principal = wx.Panel(self)
        icono = wx.Icon("../Reserva_Restaruante/imagenes de mesas/icono.png", wx.BITMAP_TYPE_PNG)
        self.SetIcon(icono)
        visor = wx.BoxSizer(wx.VERTICAL)


        pantalla_principal.SetSizer(visor)


app = wx.App(False)
frame = Login()
frame.Show()
app.MainLoop()
