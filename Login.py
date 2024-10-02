import wx
import pickle
import subprocess

class Registro(wx.Frame):
    def __init__(self, *args, **kw):

        super(Registro, self).__init__(*args, **kw)

        icono = wx.Icon("../Reserva_Restaruante/imagenes de mesas/icono.png", wx.BITMAP_TYPE_PNG)
        self.SetIcon(icono)
        pantalla_registro = wx.Panel(self)
        self.SetTitle("Registro")
        self.SetSize((300, 350))
        visor_centralizador = wx.BoxSizer(wx.VERTICAL)

        self.etiqueta_usuario = wx.StaticText(pantalla_registro, label="Ingrese el nombre de Usuario que va a utilizar")
        visor_centralizador.Add(self.etiqueta_usuario, 0, wx.ALL | wx.CENTER, 5)

        self.usuario = wx.TextCtrl(pantalla_registro)
        visor_centralizador.Add(self.usuario, 0, wx.ALL | wx.CENTER, 5)

        self.etiqueta_contrasena = wx.StaticText(pantalla_registro, label ="Ingrese la contraseña que va a utilizar" )
        visor_centralizador.Add(self.etiqueta_contrasena, 0, wx.ALL | wx.CENTER, 5)

        self.contraseña = wx.TextCtrl(pantalla_registro)
        visor_centralizador.Add(self.contraseña, 0, wx.ALL | wx.CENTER, 5)

        self.etiqueta_rol = wx.StaticText(pantalla_registro, label ="Ingrese el rol que va a cumplir" )
        visor_centralizador.Add(self.etiqueta_rol, 0, wx.ALL | wx.CENTER, 5)

        opciones = ["Usuario","Administrador"]
        self.rol = wx.ListBox(pantalla_registro, choices = opciones, style = wx.LB_SINGLE)
        visor_centralizador.Add(self.rol, 0, wx.ALL | wx.CENTER, 5)

        self.registro = wx.Button(pantalla_registro, label = "Registrarse")
        self.registro.Bind(wx.EVT_BUTTON, self.registro_cuenta)
        visor_centralizador.Add(self.registro, 0, wx.ALL | wx.CENTER, 5)


        visor_centralizador.Fit(pantalla_registro)
        pantalla_registro.SetSizer(visor_centralizador)

    def registro_cuenta(self,event):
        usuario_registro = self.usuario.GetValue()
        contraseña_registro = self.contraseña.GetValue()
        rol_registro = self.rol.GetStringSelection()
        print(rol_registro)

        with open("Base de datos.pkl","rb+") as datos:
            registracion = pickle.load(datos)
            if rol_registro == "Usuario":
                registracion["Usuario"].append({usuario_registro:contraseña_registro})
                print("pase por usuario")
            elif rol_registro == "Administrador":
                registracion["Administrador"].append({usuario_registro:contraseña_registro})
                print("pase por administrador")

            datos.seek(0)
            pickle.dump(registracion,datos)
            wx.MessageBox("Se ha registrado correctamente","Registro", wx.OK | wx.ICON_INFORMATION)
            self.Close()


class Login(wx.Frame):
    def __init__(self):

        super().__init__(parent=None, title="Login")

        pantalla_principal = wx.Panel(self)
        icono = wx.Icon("../Reserva_Restaruante/imagenes de mesas/icono.png", wx.BITMAP_TYPE_PNG)
        self.SetIcon(icono)
        visor_centralizador = wx.BoxSizer(wx.VERTICAL)

        self.etiqueta_usuario = wx.StaticText(pantalla_principal, label="Coloque su nombre de usuario")
        visor_centralizador.Add(self.etiqueta_usuario, 0, wx.ALL | wx.CENTER, 5)

        self.usuario = wx.TextCtrl(pantalla_principal)
        visor_centralizador.Add(self.usuario, 0, wx.ALL | wx.EXPAND, 5)

        self.etiqueta_contraseña = wx.StaticText(pantalla_principal, label="Coloque su contraseña")
        visor_centralizador.Add(self.etiqueta_contraseña, 0, wx.ALL | wx.CENTER, 5)

        self.contraseña = wx.TextCtrl(pantalla_principal)
        visor_centralizador.Add(self.contraseña, 0, wx.ALL | wx.EXPAND, 5)

        self.validacion = wx.Button(pantalla_principal, label="Ingresar")
        self.validacion.Bind(wx.EVT_BUTTON, self.validacion_cuenta)
        visor_centralizador.Add(self.validacion, 0, wx.ALL | wx.CENTER, 5)

        self.registro = wx.Button(pantalla_principal, label ="Registrarse")
        self.registro.Bind(wx.EVT_BUTTON, self.registro_cuenta)
        visor_centralizador.Add(self.registro, 0, wx.ALL | wx.CENTER, 5)

        pantalla_principal.SetSizer(visor_centralizador)

    def validacion_cuenta(self, event):
        self.Close()
        usuario_validacion = self.usuario.GetValue()
        contraseña_validacion = self.contraseña.GetValue()
        datos_cuenta = {}
        datos_cuenta[usuario_validacion] = contraseña_validacion

        with open("Base de datos.pkl","rb") as datos:
            archivo_base_datos = pickle.load(datos)
            verificacion_administrador = None

            for diccionario in archivo_base_datos["Usuario"]:
                if usuario_validacion in diccionario and diccionario[usuario_validacion] == contraseña_validacion:
                    verificacion_administrador = False

            for diccionario in archivo_base_datos["Administrador"]:
                if usuario_validacion in diccionario and diccionario[usuario_validacion] == contraseña_validacion:
                    verificacion_administrador = True

        if verificacion_administrador == True:
            subprocess.run(["python","../Reserva_Restaruante/Administradores/Administradores.py"])
        elif verificacion_administrador == False:
            subprocess.run(["python","../Reserva_Restaruante/Usuarios/Usuarios.py"])


    def registro_cuenta(self, event):
        pantalla_registro = Registro(None)
        pantalla_registro.Show()

app = wx.App(False)
frame = Login()
frame.Show()
app.MainLoop()
