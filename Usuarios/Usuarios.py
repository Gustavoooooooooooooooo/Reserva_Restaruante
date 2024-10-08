import wx, subprocess, sys, os, mysql.connector
import datetime as dt

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
        if hasattr(self, 'visor_principal'):
            self.visor_principal.Clear(True)

        
        self.visor_mesa = wx.GridSizer(0, 4, 10, 10) # Organiza los botones de las mesas en un grid de 4 columnas
        self.visor_principal = wx.BoxSizer(wx.VERTICAL) # Visor principal donde convergeran los otros visores
        self.visor_botones = wx.BoxSizer(wx.HORIZONTAL) # Visor donde se ubicaran los botones

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
            self.visor_mesa.Add(self.boton_mesa, 0, wx.EXPAND)

        # Botón para regresar al login
        self.retroceder = wx.Button(self.pantalla_principal, label="Volver")
        self.retroceder.Bind(wx.EVT_BUTTON, self.volver_login)
        self.visor_botones.Add(self.retroceder, 0, wx.ALIGN_BOTTOM | wx.ALIGN_LEFT, 5)

        # Botón para mostrar instrucciones
        self.instrucciones = wx.Button(self.pantalla_principal, size=(self.ancho-40, self.alto-40), style=wx.BORDER_NONE)
        self.instrucciones.SetBitmap(self.imagen_informacion_escalada)
        self.instrucciones.Bind(wx.EVT_BUTTON, self.mostrar_instrucciones)
        self.visor_botones.Add(self.instrucciones, 0, wx.ALIGN_BOTTOM | wx.ALIGN_LEFT, 5)

        self.visor_principal.Add(self.visor_mesa, 1, wx.EXPAND | wx.ALL, 10)  # Sizer de mesas ocupa la mayor parte del espacio
        self.visor_principal.Add(self.visor_botones, 0, wx.ALIGN_RIGHT | wx.ALL, 10)

        # Establece el layout en el panel
        self.visor_principal.Fit(self.pantalla_principal)
        self.pantalla_principal.SetSizer(self.visor_principal)
        self.Layout()

    def volver_login(self, event):
        #Cierra la ventana actual y regresa al login.
        self.Close()
        subprocess.Popen(["python", "../Reserva_Restaruante/Login.py"])

    def mostrar_info_mesa(self, nombre):
        #Muestra un mensaje con la información del reservador de la mesa ocupada.
        wx.MessageBox(f"Mesa ocupada por {nombre}", "Información de la Mesa", wx.OK | wx.ICON_INFORMATION)

    def mostrar_instrucciones(self, event):
    # Muestra las instrucciones para el uso de la interfaz con las mesas libres y ocupadas.
        mensaje = "Las mesas azules son las mesas libres y las mesas naranjas son las mesas ocupadas."
        dialogo = wx.MessageDialog(self, mensaje, "Información sobre Mesas", wx.OK | wx.ICON_INFORMATION)
        dialogo.ShowModal()
        dialogo.Destroy()

    def pantalla_mesa_libre(self, id):
        #Abre la ventana para reservar una mesa libre.
        mesa_libre = Mesa_libre(id, self, None)
        mesa_libre.Show()

    def actualizar_mesas(self):
        #Recarga las mesas desde la base de datos y actualiza la interfaz.
        self.cargar_mesas()


class Mesa_libre(wx.Frame):
    def __init__(self, id, parent, *args, **kw):
        #Inicializa la interfaz para reservar una mesa libre.
        super(Mesa_libre, self).__init__(title = "Reserva",*args, **kw)
        self.id_mesa = id
        self.parent = parent

        # Crea el panel de la ventana para la reserva
        self.pantalla_mesa = wx.Panel(self)
        icono = wx.Icon("../Reserva_Restaruante/imagenes/icono.png", wx.BITMAP_TYPE_PNG)
        self.SetIcon(icono)
        self.visor = wx.BoxSizer(wx.VERTICAL)
        self.SetSize(350, 400)

        # Etiquetas y campos para la información de la reserva
        self.nombre_etiqueta = wx.StaticText(self.pantalla_mesa, label="Coloque el nombre de la persona que reserva la mesa")
        self.visor.Add(self.nombre_etiqueta, 0, wx.ALL | wx.CENTER, 5)

        self.nombre = wx.TextCtrl(self.pantalla_mesa)
        self.visor.Add(self.nombre, 0, wx.ALL | wx.CENTER, 5)

        self.cantidad_personas_etiqueta = wx.StaticText(self.pantalla_mesa, label="Coloque la cantidad de personas que serán en la mesa")
        self.visor.Add(self.cantidad_personas_etiqueta, 0, wx.ALL | wx.CENTER, 5)

        self.cantidad_personas = wx.TextCtrl(self.pantalla_mesa)
        self.visor.Add(self.cantidad_personas, 0, wx.ALL | wx.CENTER, 5)

        self.fecha_etiqueta = wx.StaticText(self.pantalla_mesa, label="Coloque la fecha de la reserva en AÑO-MES-DIA")
        self.visor.Add(self.fecha_etiqueta, 0, wx.ALL | wx.CENTER, 5)

        self.fecha = wx.TextCtrl(self.pantalla_mesa)
        self.visor.Add(self.fecha, 0, wx.ALL | wx.CENTER, 5)

        # Selector de planta del edificio
        self.planta_etiqueta = wx.StaticText(self.pantalla_mesa, label="Ingrese en qué planta del edificio reservará")
        self.visor.Add(self.planta_etiqueta, 0, wx.ALL | wx.CENTER, 5)

        opciones = ["Planta Alta", "Planta Media", "Planta Baja"]
        self.planta = wx.ListBox(self.pantalla_mesa, choices=opciones, style=wx.LB_SINGLE)
        self.visor.Add(self.planta, 0, wx.ALL | wx.CENTER, 5)

        # Botón para confirmar la reserva
        self.reserva = wx.Button(self.pantalla_mesa, label="Registrarse")
        self.reserva.Bind(wx.EVT_BUTTON, self.reserva_mesa)
        self.visor.Add(self.reserva, 0, wx.ALL | wx.CENTER, 5)

        # Establece el layout del panel
        self.visor.Fit(self.pantalla_mesa)
        self.pantalla_mesa.SetSizer(self.visor)

    def reserva_mesa(self, event):

        #Valida los datos ingresados y registra la reserva en la base de datos.

        try:
            self.nombre = self.nombre.GetValue()
            self.cantidad_personas = self.cantidad_personas.GetValue()
            self.fecha = self.fecha.GetValue()
            self.planta = self.planta.GetStringSelection()
        except ValueError:
            self.validar_nombre()
        try:


            # Validación de los campos
            if not self.nombre or not self.cantidad_personas or not self.fecha or not self.planta:
                wx.MessageBox("Por favor, complete todos los campos", "Error", wx.OK | wx.ICON_ERROR)
            else:

                self.validar_fecha()
                self.validar_nombre()

                if int(self.cantidad_personas) > 7:
                    wx.MessageBox("El maximo de personas es de 7 por mesa", "Error", wx.OK | wx.ICON_ERROR)
                    raise ValueError
                elif int(self.cantidad_personas) < 1:
                    wx.MessageBox("El minimo de personas es de 1 persona", "Error", wx.OK | wx.ICON_ERROR)
                    raise ValueError
                    
                # Llama a la función que registra la reserva en la base de datos
                reservar_mesa(self.id_mesa, self.nombre, self.cantidad_personas, self.fecha, self.planta)
                wx.MessageBox("Mesa reservada exitosamente", "Reserva", wx.OK | wx.ICON_INFORMATION)

                # Cierra la ventana de reserva y actualiza la lista de mesas
                self.Close()
                self.parent.actualizar_mesas()

        except ValueError:
                wx.MessageBox("Algo a sucedido, verifique que ha completado correctamente todos los campos", "Error", wx.OK | wx.ICON_ERROR)
                self.Close()

    def validar_fecha(self):
            try:
                # Convertir la cadena introducida en un objeto datetime
                self.fecha_reserva = dt.datetime.strptime(self.fecha, "%Y-%m-%d").date()
                
                # Obtener la fecha actual
                self.fecha_actual = dt.date.today()
                
                # Definir el límite de 2 años desde la fecha actual
                self.limite_dos_anios = self.fecha_actual + dt.timedelta(days=2*365)  # Aproximado, puedes ajustar para años bisiestos
                
                # Verificar si la fecha es anterior a la actual
                if self.fecha_reserva < self.fecha_actual:
                    wx.MessageBox("La mesa no puede ser reservada en una fecha que ya paso", "Error", wx.OK | wx.ICON_ERROR)
                    raise ValueError
                
                # Verificar si la fecha excede los 2 años de límite
                if self.fecha_reserva > self.limite_dos_anios:
                    wx.MessageBox("Nuestro limite de reserva es de 2 años", "Error", wx.OK | wx.ICON_ERROR)
                    raise ValueError               
            
            except Exception  as e:
                wx.MessageBox("Verifique que la fecha este bien introducida", "Error", wx.OK | wx.ICON_ERROR)
                raise ValueError
            
    def validar_nombre(self):

        self.nombre_verificacion = self.nombre.strip()

        if not self.nombre_verificacion:
            wx.MessageBox("El nombre no puede estar vacio", "Error", wx.OK | wx.ICON_ERROR)
            raise ValueError
# Configura y ejecuta la aplicación wxPython
app = wx.App(False)
frame = Usuario()
frame.Show()
app.MainLoop()
