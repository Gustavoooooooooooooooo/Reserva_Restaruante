import wx
import pickle
import sys
import os
sys.path.append("./MesasBD")
from MesaBD import Mesa

class Mesa_libre(wx.Frame):
    def __init__(self, *args, **kw):
        super(Mesa_libre,self).__init__(*args, **kw)

        pantalla_mesa = wx.Panel(self)
        icono = wx.Icon("../Reserva_Restaruante/imagenes de mesas/icono.png", wx.BITMAP_TYPE_PNG)
        self.SetIcon(icono)
        visor = wx.BoxSizer(wx.VERTICAL)

        self.nombre_etiqueta = wx.StaticText(pantalla_mesa, label = "Coloque el nombre de la persona que reserva la mesa")
        visor.Add(self.nombre_etiqueta, 0, wx.ALL | wx.CENTER, 5)

        self.nombre = wx.TextCtrl(pantalla_mesa)
        visor.Add(self.nombre, 0, wx.ALL | wx.CENTER, 5)

        self.cantidad_personas_etiqueta = wx.StaticText(pantalla_mesa, label = "Coloque la cantidad de personas que seran en la mesa")
        visor.Add(self.cantidad_personas_etiqueta, 0, wx.ALL | wx.CENTER, 5)

        self.cantidad_personas = wx.TextCtrl(pantalla_mesa)
        visor.Add(self.cantidad_personas, 0, wx.ALL | wx.CENTER, 5)

        self.fecha_etiqueta = wx.StaticText(pantalla_mesa, label = "Coloque la fecha de la reserva" )
        visor.Add(self.fecha_etiqueta, 0, wx.ALL | wx.CENTER, 5)

        self.fecha = wx.TextCtrl(pantalla_mesa)
        visor.Add(self.fecha, 0, wx.ALL | wx.CENTER, 5)
        
        self.reserva = wx.Button(pantalla_mesa, label = "Registrarse")
        self.reserva.Bind(wx.EVT_BUTTON,self.reserva_mesa)
        visor.Add(self.reserva, 0, wx.ALL | wx.CENTER, 5)

        pantalla_mesa.SetSizer(visor)

    def reserva_mesa(self,event):
        base_datos = Mesa()

        if not nombre or not cantidad_personas or not fecha:
            wx.MessageBox("Por favor, complete todos los campos", "Error", wx.OK | wx.ICON_ERROR)
            return
        
        nombre = self.nombre.GetValue()
        cantidad_personas = self.cantidad_personas.GetValue()
        fecha = self.fecha.GetValue()
        base_datos.agregar_mesa(nombre,cantidad_personas,fecha)


class Usuario(wx.Frame):
    def __init__(self):

        self.imagen_mesa_ocupada = wx.Bitmap("../Reserva_Restaruante/imagenes de mesas/mesa ocupada.png", wx.BITMAP_TYPE_PNG)
        self.imagen_mesa_libre = wx.Bitmap("../Reserva_Restaruante/imagenes de mesas/mesa libre.png", wx.BITMAP_TYPE_PNG)
        self.icono = wx.Icon("../Reserva_Restaruante/imagenes de mesas/icono.png", wx.BITMAP_TYPE_PNG)
        super().__init__(parent=None, title="Usuario")   

        self.pantalla_principal = wx.Panel(self)
        self.SetIcon(self.icono)
        self.visor = wx.BoxSizer(wx.VERTICAL)
        self.mostrar_mesas_ocupadas()

        self.pantalla_principal.SetSizer(self.visor)

    def pantalla_mesa_libre(self,event):
        mesa_libre = Mesa_libre(None)
        mesa_libre.Show()

#f"ID Mesa: {mesa['ID de la mesa']}, Reservador: {mesa['Reservador']}, Personas: {mesa['Cantidad de Personas']}, Fecha: {mesa['Fecha de la reserva']}"

    def mostrar_mesas_ocupadas(self):
        with open("../Reserva_Restaruante/MesasBD/Mesas.pkl", "rb") as archivo:
                base_datos = pickle.load(archivo)
                for mesa in base_datos:
                            
                            self.mesa_informacion = "a"
                            self.mesa_ocupada = wx.Button(self.pantalla_principal, id=wx.ID_ANY, size=self.imagen_mesa_ocupada.GetSize(), style=wx.BORDER_NONE)
                            self.mesa_ocupada.SetBitmap(self.imagen_mesa_ocupada)
                            self.mesa_ocupada.Bind(wx.EVT_BUTTON,mostrar_mensaje)
                            self.visor.Add(self.mesa_ocupada, 0, wx.ALL | wx.CENTER, 5)

                            def mostrar_mensaje(self,event):
                                 return wx.MessageBox(self.mesa_informacion,"Reserva", wx.OK | wx.ICON_INFORMATION)



app = wx.App(False)
frame = Usuario()
frame.Show()
app.MainLoop()
