import wx
import pickle
import sys

class Login(wx.Frame):
    def __init__(self):

        super().__init__(parent=None, title="Login")
        pantalla_principal = wx.Panel(self)
        icono = wx.Icon("../Reserva_Restaruante/imagenes de mesas/icono.png", wx.BITMAP_TYPE_PNG)
        self.SetIcon(icono)
        visor = wx.BoxSizer(wx.VERTICAL)

        self.etiqueta_usuario = wx.StaticText(pantalla_principal, label="Coloque su nombre de usuario")
        visor.Add(self.etiqueta_usuario, 0, wx.ALL | wx.CENTER, 5)
        self.usuario = wx.TextCtrl(pantalla_principal)
        visor.Add(self.usuario, 0, wx.ALL | wx.EXPAND, 5)
        self.etiqueta_contraseña = wx.StaticText(pantalla_principal, label="Coloque su contraseña")
        visor.Add(self.etiqueta_contraseña, 0, wx.ALL | wx.CENTER, 5)
        self.contraseña = wx.TextCtrl(pantalla_principal)
        visor.Add(self.contraseña, 0, wx.ALL | wx.EXPAND, 5)
        validacion = wx.Button(pantalla_principal, label="Ingresar")
        validacion.Bind(wx.EVT_BUTTON, self.validacion_cuenta)
        visor.Add(validacion, 0, wx.ALL | wx.CENTER, 5)

        pantalla_principal.SetSizer(visor)

    def validacion_cuenta(self, event):

        usuario_validacion = self.usuario.GetValue()
        contraseña_validacion = self.contraseña.GetValue()
        datos_cuenta = {}
        datos_cuenta[usuario_validacion] = contraseña_validacion

        with open("Base de datos.pkl","rb") as base_datos:
            archivo_base_datos = pickle.load(base_datos)

            for i,j in archivo_base_datos.items():
                diccionario = {}
                diccionario[i]=j
                if diccionario == datos_cuenta:
                    if diccionario == {"cliente123":"cliente123"}:
                        administrador = False
                    elif diccionario == {"administrador123":"administrador123"}:
                        administrador = True
                                                                                        # Administrador Usuario:administrador123, Contraseña:administrador123
                                                                                        # Cliente Usuario:cliente123, Contraseña:cliente123
        if administrador == True:
            with open("../Reserva_Restaruante/Administradores/Administradores.py") as administradores:
                exec(administradores.read())
        elif administrador == False:
            with open("../Reserva_Restaruante/Usuarios/Usuarios.py") as usuario:
                exec(usuario.read())

app = wx.App(False)
frame = Login()
frame.Show()
app.MainLoop()
