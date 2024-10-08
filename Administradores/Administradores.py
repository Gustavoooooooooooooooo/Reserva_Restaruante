import wx, subprocess, os, sys, mysql.connector

# Importa funciones para manejar las mesas desde el módulo MesaBD
sys.path.append(os.path.abspath('../Reserva_Restaruante/MesasBD'))
from MesaBD import crear_mesa, eliminar_mesa, vaciar_mesa

# Clase principal de la interfaz para el Administrador del sistema
class Administrador(wx.Frame):
    def __init__(self):
        # Se cargan imágenes para representar los estados de las mesas
        self.imagen_mesa_ocupada = wx.Image("../Reserva_Restaruante/imagenes/mesa ocupada.png", wx.BITMAP_TYPE_PNG)
        self.imagen_mesa_libre = wx.Image("../Reserva_Restaruante/imagenes/mesa libre.png", wx.BITMAP_TYPE_PNG)
        self.imagen_informacion = wx.Image("../Reserva_Restaruante/imagenes/informacion.png", wx.BITMAP_TYPE_PNG)
        self.icono = wx.Icon("../Reserva_Restaruante/imagenes/icono.png", wx.BITMAP_TYPE_PNG)
        
        super().__init__(parent=None, title="Administrador")  # Inicializa el marco wxPython
        
        # Se define el panel principal
        self.pantalla_principal = wx.Panel(self)
        self.SetIcon(self.icono)  # Establece el ícono de la ventana

        # Carga las mesas desde la base de datos
        self.cargar_mesas()

    def cargar_mesas(self):

        #Método que carga y actualiza las mesas desde la base de datos.
        if hasattr(self, 'visor_principal'):
            self.visor_principal.Clear(True)  # Limpia el visor si ya existe

        self.visor_mesa = wx.GridSizer(0, 4, 10, 10) # Organiza los botones de las mesas en un grid de 4 columnas
        self.visor_principal = wx.BoxSizer(wx.VERTICAL) # Visor principal donde convergeran los otros visores
        self.visor_botones = wx.BoxSizer(wx.HORIZONTAL) # Visor donde se ubicaran los botones

        # Conexión a la base de datos MySQL
        self.conexion = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="gustavo",
            database="restaurante_reserva"
        )
        self.cursor = self.conexion.cursor()
        self.cursor.execute("SELECT * FROM mesa")  # Consulta todas las mesas
        self.mesas = self.cursor.fetchall()  # Obtiene las mesas

        # Escala las imágenes para ajustarlas al tamaño de los botones
        self.ancho, self.alto = 70, 70
        self.imagen_informacion_escalada = self.imagen_informacion.Scale(self.ancho-40, self.alto-40).ConvertToBitmap()
        self.imagen_mesa_libre_escalada = self.imagen_mesa_libre.Scale(self.ancho, self.alto).ConvertToBitmap()
        self.imagen_mesa_ocupada_escalada = self.imagen_mesa_ocupada.Scale(self.ancho, self.alto).ConvertToBitmap()

        # Ciclo que recorre cada mesa y crea un botón según su estado (libre u ocupada)
        for mesa in self.mesas:
            self.id_mesa, self.estado, self.reservador, self.cantidad_personas, self.fecha_reserva, self.ubicacion_mesa = mesa

            # Si la mesa está libre, crea un botón con la imagen de mesa libre
            if self.estado == 'libre':
                boton_mesa = wx.Button(self.pantalla_principal, size=(self.ancho, self.alto), style=wx.BORDER_NONE)
                boton_mesa.SetBitmap(self.imagen_mesa_libre_escalada)
                boton_mesa.Bind(wx.EVT_BUTTON, lambda event, id=self.id_mesa: self.operaciones_mesa_libre(id))
            else:
                # Si está ocupada, crea un botón con la imagen de mesa ocupada
                boton_mesa = wx.Button(self.pantalla_principal, size=(self.ancho, self.alto), style=wx.BORDER_NONE)
                boton_mesa.SetBitmap(self.imagen_mesa_ocupada_escalada)
                boton_mesa.Bind(wx.EVT_BUTTON, lambda event,reservador=self.reservador,cantidad_personas=self.cantidad_personas,fecha_reserva=self.fecha_reserva,ubicacion_mesa=self.ubicacion_mesa, id=self.id_mesa: self.pantalla_mesa_ocupada(id,reservador,cantidad_personas,fecha_reserva,ubicacion_mesa))

            self.visor_mesa.Add(boton_mesa, 0, wx.EXPAND)  # Añade el botón al visor de la interfaz

        # Botón para mostrar instrucciones
        self.instrucciones = wx.Button(self.pantalla_principal, size =(self.ancho-40,self.alto-40), style=wx.BORDER_NONE)
        self.instrucciones.SetBitmap(self.imagen_informacion_escalada)
        self.instrucciones.Bind(wx.EVT_BUTTON, self.mostrar_instrucciones)
        self.visor_botones.Add(self.instrucciones, 0, wx.ALIGN_BOTTOM | wx.ALIGN_LEFT, 10)

        # Botón para retroceder al login
        self.retroceder = wx.Button(self.pantalla_principal,label = "Volver")
        self.retroceder.Bind(wx.EVT_BUTTON, self.volver_login)
        self.visor_botones.Add(self.retroceder, 0, wx.ALIGN_BOTTOM | wx.ALIGN_LEFT, 10)

        # Botón para crear una nueva mesa
        self.mesa_creador = wx.Button(self.pantalla_principal, label = "Crear Mesa")
        self.mesa_creador.Bind(wx.EVT_BUTTON, self.Creacion_mesa)
        self.visor_botones.Add(self.mesa_creador, 0, wx.ALIGN_BOTTOM | wx.ALIGN_LEFT, 10)


        #self.sizer_principal.Add(self.visor_mesa, 1, wx.EXPAND | wx.ALL, 10)  # Sizer de mesas ocupa la mayor parte del espacio
        
        self.visor_principal.Add(self.visor_mesa, 1, wx.EXPAND | wx.ALL, 10)  # Sizer de mesas ocupa la mayor parte del espacio
        self.visor_principal.Add(self.visor_botones, 0, wx.ALIGN_RIGHT | wx.ALL, 10)

        self.visor_principal.Fit(self.pantalla_principal)
        self.pantalla_principal.SetSizer(self.visor_principal)  # Establece el layout en el panel
        self.Layout()

    def mostrar_instrucciones(self, event):
    # Muestra las instrucciones para el uso de la interfaz con las mesas libres y ocupadas.
        mensaje = "Las mesas azules son las mesas libres y las mesas naranjas son las mesas ocupadas."
        dialogo = wx.MessageDialog(self, mensaje, "Información sobre Mesas", wx.OK | wx.ICON_INFORMATION)
        dialogo.ShowModal()
        dialogo.Destroy()

    def volver_login(self, event):
        #Cierra la ventana actual y regresa a la pantalla de login.
        self.Close()
        subprocess.Popen(["python", "../Reserva_Restaruante/Login.py"])

    def Creacion_mesa(self, event):
        #Llama a la función externa para crear una nueva mesa y actualiza la lista.
        crear_mesa()
        self.actualizar_mesas()

    def operaciones_mesa_libre(self, id):
        #Realiza operaciones sobre una mesa libre, como eliminarla.
        operacion = wx.MessageDialog(None, "¿Desea eliminar la mesa?", "Mesa Libre", wx.YES_NO | wx.ICON_QUESTION)
        respuesta = operacion.ShowModal()

        if respuesta == wx.ID_YES:
            eliminar_mesa(id)
        self.actualizar_mesas()

    def pantalla_mesa_ocupada(self, id, reservador, cantidad_personas, fecha_reserva, ubicacion_mesa):
        #Abre una nueva ventana con información sobre la mesa ocupada.
        parent = self
        mesa_libre = Mesa_Ocupada(id, parent, reservador, cantidad_personas, fecha_reserva, ubicacion_mesa, None)
        mesa_libre.Show()

    def actualizar_mesas(self):
        #Método para recargar y actualizar las mesas en la interfaz.
        self.cargar_mesas()  # Recarga las mesas desde la base de datos


# Clase para manejar las mesas ocupadas
class Mesa_Ocupada(wx.Frame):
    def __init__(self, id, parent, reservador, cantidad_personas, fecha_reserva, ubicacion_mesa, *args, **kw):
        #Inicializa la ventana con la información de la mesa ocupada.
        super(Mesa_Ocupada, self).__init__(*args, **kw)
        self.id_mesa = id
        self.parent = parent
        self.reservador = reservador
        self.cantidad_personas = cantidad_personas
        self.fecha_reserva = fecha_reserva
        self.ubicacion_mesa = ubicacion_mesa

        pantalla_mesa = wx.Panel(self)
        icono = wx.Icon("../Reserva_Restaruante/imagenes/icono.png", wx.BITMAP_TYPE_PNG)
        self.SetIcon(icono)
        visor = wx.BoxSizer(wx.VERTICAL)
        self.SetSize(350, 400)

        # Muestra la información de la mesa ocupada
        self.informacion_etiqueta = wx.StaticText(pantalla_mesa, label=f"Reservador: {self.reservador}\nCantidad de Personas: {self.cantidad_personas}\nFecha de la Reserva: {self.fecha_reserva}\nUbicación de la Mesa: {self.ubicacion_mesa}")
        visor.Add(self.informacion_etiqueta, 0, wx.ALL, 5)

        # Botones para eliminar, vaciar o retroceder desde la vista de mesa ocupada
        self.alineadora = wx.BoxSizer(wx.HORIZONTAL)

        self.eliminar_mesa = wx.Button(pantalla_mesa, label="Eliminar Mesa")
        self.eliminar_mesa.Bind(wx.EVT_BUTTON, self.eliminacion_de_mesa)
        self.alineadora.Add(self.eliminar_mesa, 0, wx.ALL, 5)

        self.vaciar_mesa = wx.Button(pantalla_mesa, label="Vaciar Mesa")
        self.vaciar_mesa.Bind(wx.EVT_BUTTON, self.desocupacion)
        self.alineadora.Add(self.vaciar_mesa, 0, wx.ALL, 5)

        self.cancelar = wx.Button(pantalla_mesa, label="Retroceder")
        self.cancelar.Bind(wx.EVT_BUTTON, self.retroceder)
        self.alineadora.Add(self.cancelar, 0, wx.ALL, 5)

        visor.Fit(pantalla_mesa)
        visor.Add(self.alineadora, 0, wx.DOWN)
        pantalla_mesa.SetSizer(visor)

    def eliminacion_de_mesa(self, event):
        #Elimina la mesa ocupada y actualiza la lista en la pantalla principal.
        eliminar_mesa(self.id_mesa)
        self.parent.actualizar_mesas()
        wx.MessageBox("Mesa eliminada exitosamente", "Eliminación", wx.OK | wx.ICON_INFORMATION)
        self.Close()

    def desocupacion(self, event):
        #Vacía la mesa ocupada y actualiza la lista en la pantalla principal.
        vaciar_mesa(self.id_mesa)
        self.parent.actualizar_mesas()
        wx.MessageBox("Mesa vaciada exitosamente", "Desocupación", wx.OK | wx.ICON_INFORMATION)
        self.Close()

    def retroceder(self, event):
        #Cierra la ventana de mesa ocupada y regresa a la pantalla anterior.
        self.Close()


# Configuración de la aplicación wxPython
app = wx.App(False)
frame = Administrador()
frame.Show()
app.MainLoop()