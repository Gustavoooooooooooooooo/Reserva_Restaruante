import wx
import mysql.connector

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

        if not nombre or not cantidad_personas or not fecha:
            wx.MessageBox("Por favor, complete todos los campos", "Error", wx.OK | wx.ICON_ERROR)
            return
        
        nombre = self.nombre.GetValue()
        cantidad_personas = self.cantidad_personas.GetValue()
        fecha = self.fecha.GetValue()


class Usuario(wx.Frame):
    def __init__(self):

        self.imagen_mesa_ocupada = wx.Bitmap("../Reserva_Restaruante/imagenes de mesas/mesa ocupada.png", wx.BITMAP_TYPE_PNG)
        self.imagen_mesa_libre = wx.Bitmap("../Reserva_Restaruante/imagenes de mesas/mesa libre.png", wx.BITMAP_TYPE_PNG)
        self.icono = wx.Icon("../Reserva_Restaruante/imagenes de mesas/icono.png", wx.BITMAP_TYPE_PNG)
        super().__init__(parent=None, title="Usuario")   

        self.pantalla_principal = wx.Panel(self)
        self.SetIcon(self.icono)
        self.visor = wx.BoxSizer(wx.VERTICAL)

        conexion = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="gustavo",
            database="restaurante_reserva"
        )
        cursor = conexion.cursor()
        cursor.execute("SELECT id, estado FROM mesas")
        mesas = cursor.fetchall()

        # Crear botones dinámicos para cada mesa
        for mesa in mesas:
            id_mesa, estado = mesa

            # Determinar imagen según estado
            if estado == 'libre':
                imagen_mesa = self.imagen_mesa_libre
            else:
                imagen_mesa = self.imagen_mesa_ocupada

            # Crear botón para la mesa
            boton_mesa = wx.Button(self.pantalla_principal, label=f"Mesa {id_mesa}", size=imagen_mesa.GetSize(), style=wx.BORDER_NONE)
            boton_mesa.SetBitmap(imagen_mesa)
            boton_mesa.Bind(wx.EVT_BUTTON, lambda event, id=id_mesa: self.mostrar_info_mesa(id))
            self.visor.Add(boton_mesa, 0, wx.ALL | wx.CENTER, 5)

        self.pantalla_principal.SetSizer(self.visor)
        self.Layout()

        self.pantalla_principal.SetSizer(self.visor)

    def mostrar_info_mesa(self, id_mesa):
        wx.MessageBox(f"Mostrando información de la mesa {id_mesa}", "Información de la Mesa", wx.OK | wx.ICON_INFORMATION)

    def pantalla_mesa_libre(self,event):
        mesa_libre = Mesa_libre(None)
        mesa_libre.Show()


app = wx.App(False)
frame = Usuario()
frame.Show()
app.MainLoop()

