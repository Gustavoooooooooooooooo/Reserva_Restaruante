import wx  # Librería para interfaz gráfica
import mysql.connector  # Conexión a base de datos MySQL
import sys
import os

# Importar función personalizada para la reserva de mesa
sys.path.append(os.path.abspath('../Reserva_Restaruante/MesasBD'))
from MesaBD import reservar_mesa

# Clase principal que maneja la interfaz de usuario para la reserva de mesas
class Usuario(wx.Frame):
    def __init__(self):
        # Cargar imágenes de las mesas (ocupada/libre) y el ícono del programa
        self.imagen_mesa_ocupada = wx.Image("../Reserva_Restaruante/imagenes de mesas/mesa ocupada.png", wx.BITMAP_TYPE_PNG)
        self.imagen_mesa_libre = wx.Image("../Reserva_Restaruante/imagenes de mesas/mesa libre.png", wx.BITMAP_TYPE_PNG)
        self.icono = wx.Icon("../Reserva_Restaruante/imagenes de mesas/icono.png", wx.BITMAP_TYPE_PNG)
        
        # Inicialización de la ventana principal
        super().__init__(parent=None, title="Usuario")
        self.pantalla_principal = wx.Panel(self)
        self.SetIcon(self.icono)
        
        # Cargar las mesas desde la base de datos
        self.cargar_mesas()

    def cargar_mesas(self):
        """Método para cargar y actualizar el estado de las mesas desde la base de datos"""
        if hasattr(self, 'visor'):
            self.visor.Clear(True)  # Limpiar el visor si ya fue inicializado

        # Grid para organizar los botones de las mesas
        self.visor = wx.GridSizer(0, 4, 10, 10)

        # Conexión a la base de datos MySQL
        conexion = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="gustavo",
            database="restaurante_reserva"
        )
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM mesa")  # Obtener datos de todas las mesas
        mesas = cursor.fetchall()

        # Escalar imágenes de mesas para ajustarlas a los botones
        new_width, new_height = 70, 70
        imagen_mesa_libre_escalada = self.imagen_mesa_libre.Scale(new_width, new_height).ConvertToBitmap()
        imagen_mesa_ocupada_escalada = self.imagen_mesa_ocupada.Scale(new_width, new_height).ConvertToBitmap()

        # Crear un botón por cada mesa, asignando función según su estado (ocupada/libre)
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

            self.visor.Add(boton_mesa, 0, wx.EXPAND)  # Añadir botón al grid

        # Actualizar el layout con los botones de las mesas
        self.visor.Fit(self.pantalla_principal)
        self.pantalla_principal.SetSizer(self.visor)
        self.Layout()

    def mostrar_info_mesa(self, nombre):
        """Mostrar un mensaje con el nombre de la persona que reservó la mesa"""
        wx.MessageBox(f"Mesa ocupada por {nombre}", "Información de la Mesa", wx.OK | wx.ICON_INFORMATION)

    def pantalla_mesa_libre(self, id):
        """Abrir una nueva ventana para reservar una mesa libre"""
        parent = self
        mesa_libre = Mesa_libre(id, parent, None)
        mesa_libre.Show()

    def actualizar_mesas(self):
        """Actualizar el estado de las mesas después de una reserva"""
        self.cargar_mesas()

# Clase para manejar la reserva de una mesa libre
class Mesa_libre(wx.Frame):
    def __init__(self, id, parent, *args, **kw):
        super(Mesa_libre, self).__init__(*args, **kw)
        self.id_mesa = id  # Identificador de la mesa
        self.parent = parent

        # Crear la ventana para introducir los datos de la reserva
        pantalla_mesa = wx.Panel(self)
        icono = wx.Icon("../Reserva_Restaruante/imagenes de mesas/icono.png", wx.BITMAP_TYPE_PNG)
        self.SetIcon(icono)
        visor = wx.BoxSizer(wx.VERTICAL)
        self.SetSize(350, 400)

        # Etiquetas y campos de entrada para los datos de la reserva
        self.nombre_etiqueta = wx.StaticText(pantalla_mesa, label="Nombre del reservador")
        visor.Add(self.nombre_etiqueta, 0, wx.ALL | wx.CENTER, 5)
        self.nombre = wx.TextCtrl(pantalla_mesa)
        visor.Add(self.nombre, 0, wx.ALL | wx.CENTER, 5)

        self.cantidad_personas_etiqueta = wx.StaticText(pantalla_mesa, label="Cantidad de personas")
        visor.Add(self.cantidad_personas_etiqueta, 0, wx.ALL | wx.CENTER, 5)
        self.cantidad_personas = wx.TextCtrl(pantalla_mesa)
        visor.Add(self.cantidad_personas, 0, wx.ALL | wx.CENTER, 5)

        self.fecha_etiqueta = wx.StaticText(pantalla_mesa, label="Fecha de la reserva (AÑO-MES-DIA)")
        visor.Add(self.fecha_etiqueta, 0, wx.ALL | wx.CENTER, 5)
        self.fecha = wx.TextCtrl(pantalla_mesa)
        visor.Add(self.fecha, 0, wx.ALL | wx.CENTER, 5)

        self.planta_etiqueta = wx.StaticText(pantalla_mesa, label="Planta del edificio")
        visor.Add(self.planta_etiqueta, 0, wx.ALL | wx.CENTER, 5)

        # Opciones para seleccionar la planta
        opciones = ["Planta Alta", "Planta Media", "Planta Baja"]
        self.planta = wx.ListBox(pantalla_mesa, choices=opciones, style=wx.LB_SINGLE)
        visor.Add(self.planta, 0, wx.ALL | wx.CENTER, 5)

        # Botón para confirmar la reserva
        self.reserva = wx.Button(pantalla_mesa, label="Reservar")
        self.reserva.Bind(wx.EVT_BUTTON, self.reserva_mesa)
        visor.Add(self.reserva, 0, wx.ALL | wx.CENTER, 5)

        # Ajustar layout
        visor.Fit(pantalla_mesa)
        pantalla_mesa.SetSizer(visor)

    def reserva_mesa(self, event):
        """Guardar la reserva de mesa en la base de datos"""
        nombre = self.nombre.GetValue()
        cantidad_personas = self.cantidad_personas.GetValue()
        fecha = self.fecha.GetValue()
        planta = self.planta.GetStringSelection()

        # Validar que todos los campos estén completos
        if not nombre or not cantidad_personas or not fecha or not planta:
            wx.MessageBox("Por favor, complete todos los campos", "Error", wx.OK | wx.ICON_ERROR)
        else:
            # Reservar la mesa usando la función importada
            reservar_mesa(self.id_mesa, nombre, cantidad_personas, fecha, planta)
            wx.MessageBox("Mesa reservada exitosamente", "Reserva", wx.OK | wx.ICON_INFORMATION)
            
            self.Close()
            self.parent.actualizar_mesas()  # Actualizar las mesas en la ventana principal

# Iniciar la aplicación gráfica
app = wx.App(False)
frame = Usuario()
frame.Show()
app.MainLoop()
