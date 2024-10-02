import wx, subprocess, os, sys, mysql.connector

sys.path.append(os.path.abspath('../Reserva_Restaruante/MesasBD'))
from MesaBD import crear_mesa, eliminar_mesa, vaciar_mesa

class Administrador(wx.Frame):
    def __init__(self):
        self.imagen_mesa_ocupada = wx.Image("../Reserva_Restaruante/imagenes/mesa ocupada.png", wx.BITMAP_TYPE_PNG)
        self.imagen_mesa_libre = wx.Image("../Reserva_Restaruante/imagenes/mesa libre.png", wx.BITMAP_TYPE_PNG)
        self.imagen_informacion = wx.Image("../Reserva_Restaruante/imagenes/informacion.png", wx.BITMAP_TYPE_PNG)
        self.icono = wx.Icon("../Reserva_Restaruante/imagenes/icono.png", wx.BITMAP_TYPE_PNG)
        super().__init__(parent=None, title="Administrador")

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
                boton_mesa = wx.Button(self.pantalla_principal, size=(self.ancho, self.alto), style=wx.BORDER_NONE)
                boton_mesa.SetBitmap(self.imagen_mesa_libre_escalada)
                boton_mesa.Bind(wx.EVT_BUTTON, lambda event, id=self.id_mesa: self.operaciones_mesa_libre(id))
            else:
                boton_mesa = wx.Button(self.pantalla_principal, size=(self.ancho, self.alto), style=wx.BORDER_NONE)
                boton_mesa.SetBitmap(self.imagen_mesa_ocupada_escalada)
                boton_mesa.Bind(wx.EVT_BUTTON, lambda event,reservador=self.reservador,cantidad_personas=self.cantidad_personas,fecha_reserva=self.fecha_reserva,ubicacion_mesa=self.ubicacion_mesa, id=self.id_mesa: self.pantalla_mesa_ocupada(id,reservador,cantidad_personas,fecha_reserva,ubicacion_mesa))

            self.visor.Add(boton_mesa, 0, wx.EXPAND)

        self.instrucciones = wx.Button(self.pantalla_principal, size =(self.ancho-40,self.alto-40), style=wx.BORDER_NONE)
        self.instrucciones.SetBitmap(self.imagen_informacion_escalada)
        self.instrucciones.Bind(wx.EVT_BUTTON,self.mostrar_instrucciones)
        if self.instrucciones.GetContainingSizer():
            self.instrucciones.GetContainingSizer().Remove(self.instrucciones)
        self.visor.Add(self.instrucciones, 0, wx.ALIGN_BOTTOM | wx.ALIGN_LEFT, 5)

        self.retroceder = wx.Button(self.pantalla_principal,label = "Volver")
        self.retroceder.Bind(wx.EVT_BUTTON, self.volver_login)
        if self.retroceder.GetContainingSizer():
            self.retroceder.GetContainingSizer().Remove(self.retroceder)
        self.visor.Add(self.retroceder, 0, wx.ALIGN_BOTTOM | wx.ALIGN_LEFT, 5)


        self.mesa_creador = wx.Button(self.pantalla_principal, label = "Crear Mesa")
        self.mesa_creador.Bind(wx.EVT_BUTTON, self.Creacion_mesa)
        if self.mesa_creador.GetContainingSizer():
            self.mesa_creador.GetContainingSizer().Remove(self.mesa_creador)
        self.visor.Add(self.mesa_creador, 0, wx.ALIGN_BOTTOM | wx.ALIGN_LEFT, 5)

        self.visor.Fit(self.pantalla_principal)
        self.pantalla_principal.SetSizer(self.visor)
        self.Layout()

    def mostrar_instrucciones(self,event):
        print("a")

    def volver_login(self,event):
        self.Close()
        subprocess.Popen(["python","../Reserva_Restaruante/Login.py"])

    def Creacion_mesa(self,event):
        crear_mesa()
        self.actualizar_mesas()


    def operaciones_mesa_libre(self,id):
        operacion = wx.MessageDialog(None,"¿Desea eliminar la mesa?","Mesa Libre", wx.YES_NO | wx.ICON_QUESTION)
        respuesta = operacion.ShowModal()

        if respuesta == wx.ID_YES:
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
        icono = wx.Icon("../Reserva_Restaruante/imagenes/icono.png", wx.BITMAP_TYPE_PNG)
        self.SetIcon(icono)
        visor = wx.BoxSizer(wx.VERTICAL)
        self.SetSize(350,400)

        

        self.informacion_etiqueta = wx.StaticText(pantalla_mesa, label = f"Reservador: {self.reservador}\nCantidad de Personas: {self.cantidad_personas}\nFecha de la Reserva: {self.fecha_reserva}\nUbicacion de la Mesa: {self.ubicacion_mesa}")
        visor.Add(self.informacion_etiqueta, 0, wx.ALL, 5)

        self.alineadora = wx.BoxSizer(wx.HORIZONTAL)

        self.eliminar_mesa = wx.Button(pantalla_mesa,label = "Eliminar Mesa")
        self.eliminar_mesa.Bind(wx.EVT_BUTTON, self.eliminacion_de_mesa)
        self.alineadora.Add(self.eliminar_mesa, 0, wx.ALL, 5)

        self.vaciar_mesa = wx.Button(pantalla_mesa,label = "Vaciar Mesa")
        self.vaciar_mesa.Bind(wx.EVT_BUTTON, self.desocupacion)
        self.alineadora.Add(self.vaciar_mesa, 0,wx.ALL, 5)

        self.cancelar = wx.Button(pantalla_mesa, label= "Retroceder")
        self.cancelar.Bind(wx.EVT_BUTTON, self.retroceder)
        self.alineadora.Add(self.cancelar, 0,wx.ALL, 5)

        visor.Fit(pantalla_mesa)
        visor.Add(self.alineadora, 0,wx.DOWN)
        pantalla_mesa.SetSizer(visor)

    def eliminacion_de_mesa(self,event):
        eliminar_mesa(self.id_mesa)
        self.parent.actualizar_mesas()
        wx.MessageBox("Mesa eliminada exitosamente", "Eliminacion", wx.OK | wx.ICON_INFORMATION)
        self.Close()

    def desocupacion(self,event):
        vaciar_mesa(self.id_mesa)
        self.parent.actualizar_mesas()
        wx.MessageBox("Mesa vaciada exitosamente", "Desocupacion", wx.OK | wx.ICON_INFORMATION)
        self.Close()

    def retroceder(self,event):
        self.Close()

app = wx.App(False)
frame = Administrador()
frame.Show()
app.MainLoop()
