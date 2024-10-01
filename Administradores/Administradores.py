import wx
import mysql.connector
import sys
import os
sys.path.append(os.path.abspath('../Reserva_Restaruante/MesasBD'))
from MesaBD import crear_mesa, eliminar_mesa, vaciar_mesa

class Administrador(wx.Frame):
    def __init__(self):
        """Inicializa la ventana principal del administrador con las imágenes de las mesas y el ícono de la aplicación."""
        # Carga imágenes de mesas (ocupada y libre) y un ícono
        self.imagen_mesa_ocupada = wx.Image("../Reserva_Restaruante/imagenes de mesas/mesa ocupada.png", wx.BITMAP_TYPE_PNG)
        self.imagen_mesa_libre = wx.Image("../Reserva_Restaruante/imagenes de mesas/mesa libre.png", wx.BITMAP_TYPE_PNG)
        self.icono = wx.Icon("../Reserva_Restaruante/imagenes de mesas/icono.png", wx.BITMAP_TYPE_PNG)
        super().__init__(parent=None, title="Usuario")  # Inicializa la ventana del frame
        
        # Panel principal donde se colocarán los botones de mesas
        self.pantalla_principal = wx.Panel(self)
        self.SetIcon(self.icono)
        self.cargar_mesas()  # Llama al método para cargar las mesas

    def cargar_mesas(self):
        """Método que carga y actualiza las mesas desde la base de datos"""
        # Si ya existe un visor, lo limpia
        if hasattr(self, 'visor'):
            self.visor.Clear(True)

        # Crea un GridSizer para acomodar las mesas en una cuadrícula
        self.visor = wx.GridSizer(0, 4, 10, 10)

        # Conecta a la base de datos MySQL
        conexion = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="gustavo",
            database="restaurante_reserva"
        )
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM mesa")  # Consulta para obtener todas las mesas
        mesas = cursor.fetchall()  # Guarda el resultado en una lista

        # Escala las imágenes de las mesas a un tamaño fijo
        new_width, new_height = 70, 70
        imagen_mesa_libre_escalada = self.imagen_mesa_libre.Scale(new_width, new_height).ConvertToBitmap()
        imagen_mesa_ocupada_escalada = self.imagen_mesa_ocupada.Scale(new_width, new_height).ConvertToBitmap()

        # Itera sobre las mesas obtenidas de la base de datos
        for mesa in mesas:
            # Desempaqueta la información de cada mesa
            self.id_mesa, self.estado, self.reservador, self.cantidad_personas, self.fecha_reserva, self.ubicacion_mesa = mesa

            # Si la mesa está libre, crea un botón con la imagen correspondiente y enlaza su evento
            if self.estado == 'libre':
                boton_mesa = wx.Button(self.pantalla_principal, size=(new_width, new_height), style=wx.BORDER_NONE)
                boton_mesa.SetBitmap(imagen_mesa_libre_escalada)
                boton_mesa.Bind(wx.EVT_BUTTON, lambda event, id=self.reservador: self.operaciones_mesa_libre(id))
            else:
                # Si la mesa está ocupada, usa la imagen correspondiente y enlaza su evento
                boton_mesa = wx.Button(self.pantalla_principal, size=(new_width, new_height), style=wx.BORDER_NONE)
                boton_mesa.SetBitmap(imagen_mesa_ocupada_escalada)
                boton_mesa.Bind(wx.EVT_BUTTON, lambda event, reservador=self.reservador, cantidad_personas=self.cantidad_personas, fecha_reserva=self.fecha_reserva, ubicacion_mesa=self.ubicacion_mesa, id=self.id_mesa: self.pantalla_mesa_ocupada(id, reservador, cantidad_personas, fecha_reserva, ubicacion_mesa))

            self.visor.Add(boton_mesa, 0, wx.EXPAND)  # Añade el botón al visor

        # Ajusta el layout y establece el visor en el panel principal
        self.visor.Fit(self.pantalla_principal)
        self.pantalla_principal.SetSizer(self.visor)
        self.Layout()

    def operaciones_mesa_libre(self, id):
        """Método que permite eliminar una mesa libre."""
        # Muestra un diálogo de confirmación para eliminar una mesa
        operacion = wx.MessageDialog(None, "¿Desea eliminar la mesa?", "Mesa Libre", wx.YES_NO | wx.ICON_QUESTION)
        respuesta = operacion.ShowModal()

        if respuesta == wx.YES:
            eliminar_mesa(id)  # Llama a la función para eliminar la mesa
        self.actualizar_mesas()  # Actualiza la lista de mesas

    def pantalla_mesa_ocupada(self, id, reservador, cantidad_personas, fecha_reserva, ubicacion_mesa):
        """Método que muestra información de una mesa ocupada."""
        parent = self
        mesa_ocupada = Mesa_Ocupada(id, parent, reservador, cantidad_personas, fecha_reserva, ubicacion_mesa, None)
        mesa_ocupada.Show()  # Abre una nueva ventana con la información de la mesa ocupada

    def actualizar_mesas(self):
        """Actualiza la visualización de las mesas."""
        self.cargar_mesas()  # Vuelve a cargar las mesas desde la base de datos


class Mesa_Ocupada(wx.Frame):
    def __init__(self, id, parent, reservador, cantidad_personas, fecha_reserva, ubicacion_mesa, *args, **kw):
        """Inicializa la ventana con los detalles de una mesa ocupada."""
        super(Mesa_Ocupada, self).__init__(*args, **kw)
        self.id_mesa = id
        self.parent = parent
        self.reservador = reservador
        self.cantidad_personas = cantidad_personas
        self.fecha_reserva = fecha_reserva
        self.ubicacion_mesa = ubicacion_mesa

        # Panel para mostrar información de la mesa
        pantalla_mesa = wx.Panel(self)
        icono = wx.Icon("../Reserva_Restaruante/imagenes de mesas/icono.png", wx.BITMAP_TYPE_PNG)
        self.SetIcon(icono)
        visor = wx.BoxSizer(wx.VERTICAL)
        self.SetSize(350, 400)

        # Muestra información detallada de la mesa ocupada
        self.informacion_etiqueta = wx.StaticText(pantalla_mesa, label=f"Reservador: {self.reservador}\nCantidad de Personas: {self.cantidad_personas}\nFecha de la Reserva: {self.fecha_reserva}\nUbicación de la Mesa: {self.ubicacion_mesa}")
        visor.Add(self.informacion_etiqueta, 0, wx.ALL | wx.CENTER, 5)

        # Botón para eliminar la mesa
        self.eliminar_mesa = wx.Button(pantalla_mesa, label="Eliminar Mesa")
        self.eliminar_mesa.Bind(wx.EVT_BUTTON, self.eliminacion_de_mesa)
        visor.Add(self.eliminar_mesa, 0, wx.ALL | wx.LEFT, 5)

        # Botón para vaciar la mesa
        self.vaciar_mesa = wx.Button(pantalla_mesa, label="Vaciar Mesa")
        self.vaciar_mesa.Bind(wx.EVT_BUTTON, self.desocupacion)
        visor.Add(self.vaciar_mesa, 0, wx.ALL | wx.CENTER, 5)

        # Botón para cancelar y retroceder
        self.cancelar = wx.Button(pantalla_mesa, label="Retroceder")
        self.cancelar.Bind(wx.EVT_BUTTON, self.retroceder)
        visor.Add(self.cancelar, 0, wx.ALL | wx.RIGHT, 5)

        # Ajusta el layout
        visor.Fit(pantalla_mesa)
        pantalla_mesa.SetSizer(visor)

    def eliminacion_de_mesa(self, event):
        """Elimina la mesa ocupada y actualiza la lista de mesas."""
        eliminar_mesa(self.id_mesa)  # Llama a la función para eliminar la mesa
        self.parent.actualizar_mesas()  # Actualiza las mesas en la ventana principal
        wx.MessageBox("Mesa eliminada exitosamente", "Eliminación", wx.OK | wx.ICON_INFORMATION)
        self.Close()

    def desocupacion(self, event):
        """Marca la mesa como libre en la base de datos."""
        vaciar_mesa(self.id_mesa)  # Llama a la función para vaciar la mesa
        self.parent.actualizar_mesas()  # Actualiza la lista de mesas
        wx.MessageBox("Mesa vaciada exitosamente", "Desocupación", wx.OK | wx.ICON_INFORMATION)
        self.Close()

    def retroceder(self, event):
        """Cierra la ventana actual sin realizar cambios."""
        self.Close()  # Cierra la ventana de mesa ocupada

# Configuración básica para iniciar la aplicación
app = wx.App(False)
frame = Administrador()  # Crea una instancia del frame Administrador
frame.Show()  # Muestra la ventana principal
app.MainLoop()  # Inicia el bucle de eventos de la aplicación
