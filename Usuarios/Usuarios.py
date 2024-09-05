import wx
import pickle
import sys



class Usuario(wx.Frame):
    def __init__(self):

        super().__init__(parent=None, title="Usuario")
        pantalla_principal = wx.Panel(self)
        icono = wx.Icon("../Reserva_Restaruante/imagenes de mesas/icono.png", wx.BITMAP_TYPE_PNG)
        self.SetIcon(icono)
        visor = wx.BoxSizer(wx.VERTICAL)

        self.mesa_ocupada = wx.Bitmap("../Reserva_Restaruante/imagenes de mesas/mesa ocupada.png", wx.BITMAP_TYPE_PNG)
        self.mesa_libre = wx.Bitmap("../Reserva_Restaruante/imagenes de mesas/mesa libre.png", wx.BITMAP_TYPE_PNG)

        self.mesa_ej = wx.Button(pantalla_principal, id=wx.ID_ANY, pos=(1, 1), size=self.mesa_ocupada.GetSize(), style=wx.BORDER_NONE)
        self.mesa_ej.SetBitmap(self.mesa_ocupada)

        pantalla_principal.SetSizer(visor)


app = wx.App(False)
frame = Usuario()
frame.Show()
app.MainLoop()
