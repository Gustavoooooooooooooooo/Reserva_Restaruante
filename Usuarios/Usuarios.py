import wx, subprocess, sys, os, mysql.connector

sys.path.append(os.path.abspath('../Reserva_Restaruante/MesasBD'))
from MesaBD import reservar_mesa

class Usuario(wx.Frame):
    def __init__(self):
        self.imagen_mesa_ocupada = wx.Image("../Reserva_Restaruante/imagenes/mesa ocupada.png", wx.BITMAP_TYPE_PNG)
        self.imagen_mesa_libre = wx.Image("../Reserva_Restaruante/imagenes/mesa libre.png", wx.BITMAP_TYPE_PNG)
        self.imagen_informacion = wx.Image("../Reserva_Restaruante/imagenes/informacion.png", wx.BITMAP_TYPE_PNG)
        self.icono = wx.Icon("../Reserva_Restaruante/imagenes/icono.png", wx.BITMAP_TYPE_PNG)
        super().__init__(parent=None, title="Usuario")

        self.pantalla_principal = wx.Panel(self)
        self.SetIcon(self.icono)
        self.cargar_mesas()

    def cargar_mesas(self):
        """Método que carga y actualiza las mesas desde la base de datos"""
        if hasattr(self, 'visor'):
            self.visor.Clear(True)

        self.visor = wx.GridSizer(0, 4, 10, 10)

        self.conexion = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="gustavo",
            database="restaurante_reserva"
        )
        self.cursor = self.conexion.cursor()
        self.cursor.execute("SELECT * FROM mesa")
        self.mesas = self.cursor.fetchall()

        self.ancho, self.alto = 70, 70
        self.imagen_informacion_escalada = self.imagen_informacion.Scale(self.ancho-40, self.alto-40).ConvertToBitmap()
        self.imagen_mesa_libre_escalada = self.imagen_mesa_libre.Scale(self.ancho, self.alto).ConvertToBitmap()
        self.imagen_mesa_ocupada_escalada = self.imagen_mesa_ocupada.Scale(self.ancho, self.alto).ConvertToBitmap()

        for mesa in self.mesas:
            self.id_mesa, self.estado, self.reservador, self.cantidad_personas, self.fecha_reserva, self.ubicacion_mesa = mesa

            if self.estado == 'libre':
                self.boton_mesa = wx.Button(self.pantalla_principal, size=(self.ancho, self.alto), style=wx.BORDER_NONE)
                self.boton_mesa.SetBitmap(self.imagen_mesa_libre_escalada)
                self.boton_mesa.Bind(wx.EVT_BUTTON, lambda event, id=self.id_mesa: self.pantalla_mesa_libre(id))
            else:
                self.boton_mesa = wx.Button(self.pantalla_principal, size=(self.ancho, self.alto), style=wx.BORDER_NONE)
                self.boton_mesa.SetBitmap(self.imagen_mesa_ocupada_escalada)
                self.boton_mesa.Bind(wx.EVT_BUTTON, lambda event, nombre=self.reservador: self.mostrar_info_mesa(nombre))

            self.visor.Add(self.boton_mesa, 0, wx.EXPAND)

        self.retroceder = wx.Button(self.pantalla_principal,label = "Volver")
        self.retroceder.Bind(wx.EVT_BUTTON, self.volver_login)
        if self.retroceder.GetContainingSizer():
            self.retroceder.GetContainingSizer().Remove(self.retroceder)
        self.visor.Add(self.retroceder, 0, wx.ALIGN_BOTTOM | wx.ALIGN_LEFT, 5)

        self.instrucciones = wx.Button(self.pantalla_principal, size =(self.ancho-40,self.alto-40), style=wx.BORDER_NONE)
        self.instrucciones.SetBitmap(self.imagen_informacion_escalada)
        self.instrucciones.Bind(wx.EVT_BUTTON,self.mostrar_instrucciones)
        if self.instrucciones.GetContainingSizer():
            self.instrucciones.GetContainingSizer().Remove(self.instrucciones)
        self.visor.Add(self.instrucciones, 0, wx.ALIGN_BOTTOM | wx.ALIGN_LEFT, 5)

        self.visor.Fit(self.pantalla_principal)
        self.pantalla_principal.SetSizer(self.visor)
        self.Layout()

    def volver_login(self,event):
        self.Close()
        subprocess.Popen(["python","../Reserva_Restaruante/Login.py"])

    def mostrar_info_mesa(self, nombre):
        wx.MessageBox(f"Mesa ocupada por {nombre}", "Información de la Mesa", wx.OK | wx.ICON_INFORMATION)

    def mostrar_instrucciones(self,event):
        print("a")

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
        icono = wx.Icon("../Reserva_Restaruante/imagenes/icono.png", wx.BITMAP_TYPE_PNG)
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
            wx.MessageBox("Mesa reservada exitosamente", "Reserva", wx.OK | wx.ICON_INFORMATION)
            
            self.Close()
            self.parent.actualizar_mesas()


app = wx.App(False)
frame = Usuario()
frame.Show()
app.MainLoop()
