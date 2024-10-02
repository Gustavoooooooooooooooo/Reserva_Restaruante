import wx
import mysql.connector
import sys
import os
sys.path.append(os.path.abspath('../Reserva_Restaruante/MesasBD'))
from MesaBD import crear_mesa, eliminar_mesa, vaciar_mesa

class Administrador(wx.Frame):
    def __init__(self):
        self.imagen_mesa_ocupada = wx.Image("../Reserva_Restaruante/imagenes de mesas/mesa ocupada.png", wx.BITMAP_TYPE_PNG)
        self.imagen_mesa_libre = wx.Image("../Reserva_Restaruante/imagenes de mesas/mesa libre.png", wx.BITMAP_TYPE_PNG)
        self.icono = wx.Icon("../Reserva_Restaruante/imagenes de mesas/icono.png", wx.BITMAP_TYPE_PNG)
        super().__init__(parent=None, title="Usuario")

        self.pantalla_principal = wx.Panel(self)
        self.SetIcon(self.icono)
        self.cargar_mesas()

    def cargar_mesas(self):
        """Método que carga y actualiza las mesas desde la base de datos"""
        if hasattr(self, 'visor'):
            self.visor.Clear(True)

        self.visor = wx.GridSizer(0, 4, 10, 10)

        conexion = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="gustavo",
            database="restaurante_reserva"
        )
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM mesa")
        mesas = cursor.fetchall()

        new_width, new_height = 70, 70
        imagen_mesa_libre_escalada = self.imagen_mesa_libre.Scale(new_width, new_height).ConvertToBitmap()
        imagen_mesa_ocupada_escalada = self.imagen_mesa_ocupada.Scale(new_width, new_height).ConvertToBitmap()

        for mesa in mesas:
            self.id_mesa, self.estado, self.reservador, self.cantidad_personas, self.fecha_reserva, self.ubicacion_mesa = mesa

            if self.estado == 'libre':
                boton_mesa = wx.Button(self.pantalla_principal, size=(new_width, new_height), style=wx.BORDER_NONE)
                boton_mesa.SetBitmap(imagen_mesa_libre_escalada)
                boton_mesa.Bind(wx.EVT_BUTTON, lambda event, id=self.reservador: self.operaciones_mesa_libre(id))
            else:
                boton_mesa = wx.Button(self.pantalla_principal, size=(new_width, new_height), style=wx.BORDER_NONE)
                boton_mesa.SetBitmap(imagen_mesa_ocupada_escalada)
                boton_mesa.Bind(wx.EVT_BUTTON, lambda event,reservador=self.reservador,cantidad_personas=self.cantidad_personas,fecha_reserva=self.fecha_reserva,ubicacion_mesa=self.ubicacion_mesa, id=self.id_mesa: self.pantalla_mesa_ocupada(id,reservador,cantidad_personas,fecha_reserva,ubicacion_mesa))

            self.visor.Add(boton_mesa, 0, wx.EXPAND)

        self.visor.Fit(self.pantalla_principal)
        self.pantalla_principal.SetSizer(self.visor)
        self.Layout()

    def operaciones_mesa_libre(self,id):
        operacion = wx.MessageDialog(None,"¿Desea eliminar la mesa?","Mesa Libre", wx.YES_NO | wx.ICON_QUESTION)
        respuesta = operacion.ShowModal()

        if respuesta == wx.YES:
            eliminar_mesa(id)
        self.actualizar_mesas()

    def pantalla_mesa_ocupada(self, id,reservador,cantidad_personas,fecha_reserva,ubicacion_mesa):
        parent = self
        mesa_libre = Mesa_Ocupada(id,parent,reservador,cantidad_personas,fecha_reserva,ubicacion_mesa,None)
        mesa_libre.Show()

    def actualizar_mesas(self):
        self.cargar_mesas()



class Mesa_Ocupada(wx.Frame):
    def __init__(self,id,parent,reservador,cantidad_personas,fecha_reserva,ubicacion_mesa, *args, **kw,):
        super(Mesa_Ocupada,self).__init__(*args, **kw)
        self.id_mesa = id
        self.parent = parent
        self.reservador = reservador
        self.cantidad_personas = cantidad_personas
        self.fecha_reserva = fecha_reserva
        self.ubicacion_mesa = ubicacion_mesa

        pantalla_mesa = wx.Panel(self)
        icono = wx.Icon("../Reserva_Restaruante/imagenes de mesas/icono.png", wx.BITMAP_TYPE_PNG)
        self.SetIcon(icono)
        visor = wx.BoxSizer(wx.VERTICAL)
        self.SetSize(350,400)


        self.informacion_etiqueta = wx.StaticText(pantalla_mesa, label = f"Reservador: {self.reservador}\nCantidad de Personas: {self.cantidad_personas}\nFecha de la Reserva: {self.fecha_reserva}\nUbicacion de la Mesa: {self.ubicacion_mesa}")
        visor.Add(self.informacion_etiqueta, 0, wx.ALL | wx.CENTER, 5)

        self.eliminar_mesa = wx.Button(pantalla_mesa,label = "Eliminar Mesa")
        self.eliminar_mesa.Bind(wx.EVT_BUTTON, self.eliminacion_de_mesa)
        visor.Add(self.eliminar_mesa, 0, wx.ALL | wx.LEFT, 5)

        self.vaciar_mesa = wx.Button(pantalla_mesa,label = "Vaciar Mesa")
        self.vaciar_mesa.Bind(wx.EVT_BUTTON, self.desocupacion)
        visor.Add(self.vaciar_mesa, 0,wx.ALL | wx.CENTER, 5)

        self.cancelar = wx.Button(pantalla_mesa, label= "Retroceder")
        self.cancelar.Bind(wx.EVT_BUTTON, self.retroceder)
        visor.Add(self.cancelar, 0,wx.ALL | wx.RIGHT, 5)

        visor.Fit(pantalla_mesa)
        pantalla_mesa.SetSizer(visor)

    def eliminacion_de_mesa(self,event):
        eliminar_mesa(self.id_mesa)
        self.parent.actualizar_mesas()
        wx.MessageBox("Mesa eliminada exitosamente", "Eliminacion", wx.OK | wx.ICON_INFORMATION)
        self.desocupacion()

    def desocupacion(self,event):
        vaciar_mesa(self.id_mesa)
        self.parent.actualizar_mesas()
        wx.MessageBox("Mesa vaciada exitosamente", "Desocupacion", wx.OK | wx.ICON_INFORMATION)
        self.desocupacion()

    def retroceder(self,event):
        self.Close()

app = wx.App(False)
frame = Administrador()
frame.Show()
app.MainLoop()
