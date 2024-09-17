import wx
import pickle
import os

class Login(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title="Administradores")
        pantalla_principal = wx.Panel(self)
        icono = wx.Icon("../Reserva_Restaruante/imagenes de mesas/icono.png", wx.BITMAP_TYPE_PNG)
        self.SetIcon(icono)
        
        visor = wx.BoxSizer(wx.VERTICAL)
        
        self.boton_quitar_mesa = wx.Button(pantalla_principal, label="Quitar Mesa")
        visor.Add(self.boton_quitar_mesa, 0, wx.ALL | wx.CENTER, 10)

        self.boton_quitar_mesa.Bind(wx.EVT_BUTTON, self.quitar_mesa)

        pantalla_principal.SetSizer(visor)

    def quitar_mesa(self, event):

            
            wx.MessageBox(f"Se ha quitado la mesa: {mesa_eliminada}", "Mesa Eliminada", wx.OK | wx.ICON_INFORMATION)
            wx.MessageBox("No hay mesas para quitar.", "Advertencia", wx.OK | wx.ICON_WARNING)

app = wx.App(False)
frame = Login()
frame.Show()
app.MainLoop()
