import wx
import mysql.connector
import sys
import os
sys.path.append(os.path.abspath('../Reserva_Restaruante/MesasBD'))
from MesaBD import reservar_mesa

class Usuario(wx.Frame):
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
                boton_mesa.Bind(wx.EVT_BUTTON, lambda event, id=self.id_mesa: self.pantalla_mesa_libre(id))
            else:
                boton_mesa = wx.Button(self.pantalla_principal, size=(new_width, new_height), style=wx.BORDER_NONE)
                boton_mesa.SetBitmap(imagen_mesa_ocupada_escalada)
                boton_mesa.Bind(wx.EVT_BUTTON, lambda event, nombre=self.reservador: self.mostrar_info_mesa(nombre))

            self.visor.Add(boton_mesa, 0, wx.EXPAND)

        self.visor.Fit(self.pantalla_principal)
        self.pantalla_principal.SetSizer(self.visor)
        self.Layout()

    def mostrar_info_mesa(self, nombre):
        wx.MessageBox(f"Mesa ocupada por {nombre}", "Información de la Mesa", wx.OK | wx.ICON_INFORMATION)

    def pantalla_mesa_libre(self, id):
        parent = self
        mesa_libre = Mesa_libre(id,parent,None)
        mesa_libre.Show()

    def actualizar_mesas(self):
        self.cargar_mesas()


class Mesa_libre(wx.Frame):
    def __init__(self,id,parent, *args, **kw,):
        super(Mesa_libre,self).__init__(*args, **kw)
        self.id_mesa = id
        self.parent = parent

        pantalla_mesa = wx.Panel(self)
        icono = wx.Icon("../Reserva_Restaruante/imagenes de mesas/icono.png", wx.BITMAP_TYPE_PNG)
        self.SetIcon(icono)
        visor = wx.BoxSizer(wx.VERTICAL)
        self.SetSize(350,400)

        self.nombre_etiqueta = wx.StaticText(pantalla_mesa, label = "Coloque el nombre de la persona que reserva la mesa")
        visor.Add(self.nombre_etiqueta, 0, wx.ALL | wx.CENTER, 5)

        self.nombre = wx.TextCtrl(pantalla_mesa)
        visor.Add(self.nombre, 0, wx.ALL | wx.CENTER, 5)

        self.cantidad_personas_etiqueta = wx.StaticText(pantalla_mesa, label = "Coloque la cantidad de personas que seran en la mesa")
        visor.Add(self.cantidad_personas_etiqueta, 0, wx.ALL | wx.CENTER, 5)

        self.cantidad_personas = wx.TextCtrl(pantalla_mesa)
        visor.Add(self.cantidad_personas, 0, wx.ALL | wx.CENTER, 5)

        self.fecha_etiqueta = wx.StaticText(pantalla_mesa, label = "Coloque la fecha de la reserva en AÑO-MES-DiA")
        visor.Add(self.fecha_etiqueta, 0, wx.ALL | wx.CENTER, 5)

        self.fecha = wx.TextCtrl(pantalla_mesa)
        visor.Add(self.fecha, 0, wx.ALL | wx.CENTER, 5)

        self.planta_etiqueta = wx.StaticText(pantalla_mesa, label = "Ingrese en qué planta del edificio reservará")
        visor.Add(self.planta_etiqueta, 0, wx.ALL | wx.CENTER, 5)

        opciones = ["Planta Alta", "Planta Media", "Planta Baja"]
        self.planta = wx.ListBox(pantalla_mesa, choices=opciones, style=wx.LB_SINGLE)
        visor.Add(self.planta, 0, wx.ALL | wx.CENTER, 5)

        self.reserva = wx.Button(pantalla_mesa, label="Registrarse")
        self.reserva.Bind(wx.EVT_BUTTON, self.reserva_mesa)
        visor.Add(self.reserva, 0, wx.ALL | wx.CENTER, 5)

        visor.Fit(pantalla_mesa)
        pantalla_mesa.SetSizer(visor)

    def reserva_mesa(self, event):
        nombre = self.nombre.GetValue()
        cantidad_personas = self.cantidad_personas.GetValue()
        fecha = self.fecha.GetValue()
        planta = self.planta.GetStringSelection()

        if not nombre or not cantidad_personas or not fecha or not planta:
            wx.MessageBox("Por favor, complete todos los campos", "Error", wx.OK | wx.ICON_ERROR)
        else:
            reservar_mesa(self.id_mesa, nombre, cantidad_personas, fecha, planta)
            wx.MessageBox("Mesa reservada exitosamente", "Reserva", wx.OK | wx.ICON_EXCLAMATION)
            
            self.Close()
            self.parent.reservar_mesa()


app = wx.App(False)
frame = Usuario()
frame.Show()
app.MainLoop()
