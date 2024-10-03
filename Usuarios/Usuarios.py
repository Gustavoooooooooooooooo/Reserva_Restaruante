import wx, subprocess, sys, os, mysql.connector

# Añade la ruta del módulo MesaBD para importar funciones relacionadas con la reserva de mesas
sys.path.append(os.path.abspath('../Reserva_Restaruante/MesasBD'))
from MesaBD import reservar_mesa

class Usuario(wx.Frame):
    def __init__(self):
        """Inicializa la interfaz para el usuario, cargando las imágenes y los elementos visuales."""
        self.imagen_mesa_ocupada = wx.Image("../Reserva_Restaruante/imagenes/mesa ocupada.png", wx.BITMAP_TYPE_PNG)
        self.imagen_mesa_libre = wx.Image("../Reserva_Restaruante/imagenes/mesa libre.png", wx.BITMAP_TYPE_PNG)
        self.imagen_informacion = wx.Image("../Reserva_Restaruante/imagenes/informacion.png", wx.BITMAP_TYPE_PNG)
        self.icono = wx.Icon("../Reserva_Restaruante/imagenes/icono.png", wx.BITMAP_TYPE_PNG)
        super().__init__(parent=None, title="Usuario")

        # Crea el panel principal y establece el ícono de la ventana
        self.pantalla_principal = wx.Panel(self)
        self.SetIcon(self.icono)

        # Carga y visualiza las mesas desde la base de datos
        self.cargar_mesas()

    def cargar_mesas(self):
        """Carga y actualiza las mesas desde la base de datos, mostrando su estado (libre u ocupada)."""
        if hasattr(self, 'visor'):
            self.visor.Clear(True)

        # Organiza los botones de las mesas en un grid de 4 columnas
        self.visor = wx.GridSizer(0, 4, 10, 10)

        # Conexión a la base de datos para obtener el estado de las mesas
        self.conexion = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="gustavo",
            database="restaurante_reserva"
        )
        self.cursor = self.conexion.cursor()
        self.cursor.execute("SELECT * FROM mesa")
        self.mesas = self.cursor.fetchall()

        # Escala las imágenes para ajustarse al tamaño de los botones
        self.ancho, self.alto = 70, 70
        self.imagen_informacion_escalada = self.imagen_informacion.Scale(self.ancho-40, self.alto-40).ConvertToBitmap()
        self.imagen_mesa_libre_escalada = self.imagen_mesa_libre.Scale(self.ancho, self.alto).ConvertToBitmap()
        self.imagen_mesa_ocupada_escalada = self.imagen_mesa_ocupada.Scale(self.ancho, self.alto).ConvertToBitmap()

        # Crea un botón para cada mesa dependiendo de su estado
        for mesa in self.mesas:
            self.id_mesa, self.estado, self.reservador, self.cantidad_personas, self.fecha_reserva, self.ubicacion_mesa = mesa

            # Botón para mesa libre
            if self.estado == 'libre':
                self.boton_mesa = wx.Button(self.pantalla_principal, size=(self.ancho, self.alto), style=wx.BORDER_NONE)
                self.boton_mesa.SetBitmap(self.imagen_mesa_libre_escalada)
                self.boton_mesa.Bind(wx.EVT_BUTTON, lambda event, id=self.id_mesa: self.pantalla_mesa_libre(id))
            else:
                # Botón para mesa ocupada
                self.boton_mesa = wx.Button(self.pantalla_principal, size=(self.ancho, self.alto), style=wx.BORDER_NONE)
                self.boton_mesa.SetBitmap(self.imagen_mesa_ocupada_escalada)
                self.boton_mesa.Bind(wx.EVT_BUTTON, lambda event, nombre=self.reservador: self.mostrar_info_mesa(nombre))

            # Añade el botón al visor de la interfaz
            self.visor.Add(self.boton_mesa, 0, wx.EXPAND)

        # Botón para regresar al login
        self.retroceder = wx.Button(self.pantalla_principal, label="Volver")
        self.retroceder.Bind(wx.EVT_BUTTON, self.volver_login)
        self.visor.Add(self.retroceder, 0, wx.ALIGN_BOTTOM | wx.ALIGN_LEFT, 5)

        # Botón para mostrar instrucciones
        self.instrucciones = wx.Button(self.pantalla_principal, size=(self.ancho-40, self.alto-40), style=wx.BORDER_NONE)
        self.instrucciones.SetBitmap(self.imagen_informacion_escalada)
        self.instrucciones.Bind(wx.EVT_BUTTON, self.mostrar_instrucciones)
        self.visor.Add(self.instrucciones, 0, wx.ALIGN_BOTTOM | wx.ALIGN_LEFT, 5)

        # Establece el layout en el panel
        self.visor.Fit(self.pantalla_principal)
        self.pantalla_principal.SetSizer(self.visor)
        self.Layout()

    def volver_login(self, event):
        """Cierra la ventana actual y regresa al login."""
        self.Close()
        subprocess.Popen(["python", "../Reserva_Restaruante/Login.py"])

    def mostrar_info_mesa(self, nombre):
        """Muestra un mensaje con la información del reservador de la mesa ocupada."""
        wx.MessageBox(f"Mesa ocupada por {nombre}", "Información de la Mesa", wx.OK | wx.ICON_INFORMATION)

    def mostrar_instrucciones(self, event):
        """Muestra las instrucciones para el uso de la interfaz (placeholder)."""
        print("Instrucciones para reservar una mesa.")

    def pantalla_mesa_libre(self, id):
        """Abre la ventana para reservar una mesa libre."""
        mesa_libre = Mesa_libre(id, self, None)
        mesa_libre.Show()

    def actualizar_mesas(self):
        """Recarga las mesas desde la base de datos y actualiza la interfaz."""
        self.cargar_mesas()

class Mesa_libre(wx.Frame):
    def __init__(self, id, parent, *args, **kw):
        """Inicializa la interfaz para reservar una mesa libre."""
        super(Mesa_libre, self).__init__(*args, **kw)
        self.id_mesa = id
        self.parent = parent

        # Crea el panel de la ventana para la reserva
        pantalla_mesa = wx.Panel(self)
        icono = wx.Icon("../Reserva_Restaruante/imagenes/icono.png", wx.BITMAP_TYPE_PNG)
        self.SetIcon(icono)
        visor = wx.BoxSizer(wx.VERTICAL)
        self.SetSize(350, 400)

        # Etiquetas y campos para la información de la reserva
        self.nombre_etiqueta = wx.StaticText(pantalla_mesa, label="Coloque el nombre de la persona que reserva la mesa")
        visor.Add(self.nombre_etiqueta, 0, wx.ALL | wx.CENTER, 5)

        self.nombre = wx.TextCtrl(pantalla_mesa)
        visor.Add(self.nombre, 0, wx.ALL | wx.CENTER, 5)

        self.cantidad_personas_etiqueta = wx.StaticText(pantalla_mesa, label="Coloque la cantidad de personas que serán en la mesa")
        visor.Add(self.cantidad_personas_etiqueta, 0, wx.ALL | wx.CENTER, 5)

        self.cantidad_personas = wx.TextCtrl(pantalla_mesa)
        visor.Add(self.cantidad_personas, 0, wx.ALL | wx.CENTER, 5)

        self.fecha_etiqueta = wx.StaticText(pantalla_mesa, label="Coloque la fecha de la reserva en AÑO-MES-DIA")
        visor.Add(self.fecha_etiqueta, 0, wx.ALL | wx.CENTER, 5)

        self.fecha = wx.TextCtrl(pantalla_mesa)
        visor.Add(self.fecha, 0, wx.ALL | wx.CENTER, 5)

        # Selector de planta del edificio
        self.planta_etiqueta = wx.StaticText(pantalla_mesa, label="Ingrese en qué planta del edificio reservará")
        visor.Add(self.planta_etiqueta, 0, wx.ALL | wx.CENTER, 5)

        opciones = ["Planta Alta", "Planta Media", "Planta Baja"]
        self.planta = wx.ListBox(pantalla_mesa, choices=opciones, style=wx.LB_SINGLE)
        visor.Add(self.planta, 0, wx.ALL | wx.CENTER, 5)

        # Botón para confirmar la reserva
        self.reserva = wx.Button(pantalla_mesa, label="Registrarse")
        self.reserva.Bind(wx.EVT_BUTTON, self.reserva_mesa)
        visor.Add(self.reserva, 0, wx.ALL | wx.CENTER, 5)

        # Establece el layout del panel
        visor.Fit(pantalla_mesa)
        pantalla_mesa.SetSizer(visor)

    def reserva_mesa(self, event):
        """Valida los datos ingresados y registra la reserva en la base de datos."""
        nombre = self.nombre.GetValue()
        cantidad_personas = self.cantidad_personas.GetValue()
        fecha = self.fecha.GetValue()
        planta = self.planta.GetStringSelection()

        # Validación de los campos
        if not nombre or not cantidad_personas or not fecha or not planta:
            wx.MessageBox("Por favor, complete todos los campos", "Error", wx.OK | wx.ICON_ERROR)
        else:
            # Llama a la función que registra la reserva en la base de datos
            reservar_mesa(self.id_mesa, nombre, cantidad_personas, fecha, planta)
            wx.MessageBox("Mesa reservada exitosamente", "Reserva", wx.OK | wx.ICON_INFORMATION)

            # Cierra la ventana de reserva y actualiza la lista de mesas
            self.Close()
            self.parent.actualizar_mesas()


# Configura y ejecuta la aplicación wxPython
app = wx.App(False)
frame = Usuario()
frame.Show()
app.MainLoop()
