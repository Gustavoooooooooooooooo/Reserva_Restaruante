import wx  # Interfaz gráfica
import pickle  # Serialización de datos
import subprocess  # Ejecutar scripts externos

# Clase que maneja el registro de usuarios
class Registro(wx.Frame):
    def __init__(self, *args, **kw):
        super(Registro, self).__init__(*args, **kw)

        # Establecer icono, título y tamaño de la ventana
        icono = wx.Icon("../Reserva_Restaruante/imagenes de mesas/icono.png", wx.BITMAP_TYPE_PNG)
        self.SetIcon(icono)
        self.SetTitle("Registro")
        self.SetSize((300, 350))

        # Crear panel y layout para organizar elementos visuales
        pantalla_registro = wx.Panel(self)
        visor_centralizador = wx.BoxSizer(wx.VERTICAL)

        # Campos de texto y botones para el registro
        self.etiqueta_usuario = wx.StaticText(pantalla_registro, label="Ingrese el nombre de Usuario")
        visor_centralizador.Add(self.etiqueta_usuario, 0, wx.ALL | wx.CENTER, 5)
        self.usuario = wx.TextCtrl(pantalla_registro)
        visor_centralizador.Add(self.usuario, 0, wx.ALL | wx.CENTER, 5)

        self.etiqueta_contrasena = wx.StaticText(pantalla_registro, label="Ingrese la contraseña")
        visor_centralizador.Add(self.etiqueta_contrasena, 0, wx.ALL | wx.CENTER, 5)
        self.contraseña = wx.TextCtrl(pantalla_registro)
        visor_centralizador.Add(self.contraseña, 0, wx.ALL | wx.CENTER, 5)

        self.etiqueta_rol = wx.StaticText(pantalla_registro, label="Seleccione su rol")
        visor_centralizador.Add(self.etiqueta_rol, 0, wx.ALL | wx.CENTER, 5)
        opciones = ["Usuario", "Administrador"]
        self.rol = wx.ListBox(pantalla_registro, choices=opciones, style=wx.LB_SINGLE)
        visor_centralizador.Add(self.rol, 0, wx.ALL | wx.CENTER, 5)

        self.registro = wx.Button(pantalla_registro, label="Registrarse")
        self.registro.Bind(wx.EVT_BUTTON, self.registro_cuenta)
        visor_centralizador.Add(self.registro, 0, wx.ALL | wx.CENTER, 5)

        # Establecer el layout
        visor_centralizador.Fit(pantalla_registro)
        pantalla_registro.SetSizer(visor_centralizador)

    # Guardar los datos del nuevo usuario
    def registro_cuenta(self, event):
        usuario_registro = self.usuario.GetValue()
        contraseña_registro = self.contraseña.GetValue()
        rol_registro = self.rol.GetStringSelection()

        with open("Base de datos.pkl", "rb+") as datos:
            registracion = pickle.load(datos)
            # Guardar en la categoría correspondiente
            if rol_registro == "Usuario":
                registracion["Usuario"].append({usuario_registro: contraseña_registro})
            elif rol_registro == "Administrador":
                registracion["Administrador"].append({usuario_registro: contraseña_registro})

            datos.seek(0)  # Volver al inicio del archivo para sobreescribir
            pickle.dump(registracion, datos)
            wx.MessageBox("Se ha registrado correctamente", "Registro", wx.OK | wx.ICON_INFORMATION)
            self.Close()

# Clase para manejar el inicio de sesión
class Login(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title="Login")

        # Crear panel y layout
        pantalla_principal = wx.Panel(self)
        icono = wx.Icon("../Reserva_Restaruante/imagenes de mesas/icono.png", wx.BITMAP_TYPE_PNG)
        self.SetIcon(icono)
        visor_centralizador = wx.BoxSizer(wx.VERTICAL)

        # Campos de texto para usuario y contraseña
        self.etiqueta_usuario = wx.StaticText(pantalla_principal, label="Coloque su nombre de usuario")
        visor_centralizador.Add(self.etiqueta_usuario, 0, wx.ALL | wx.CENTER, 5)
        self.usuario = wx.TextCtrl(pantalla_principal)
        visor_centralizador.Add(self.usuario, 0, wx.ALL | wx.EXPAND, 5)

        self.etiqueta_contraseña = wx.StaticText(pantalla_principal, label="Coloque su contraseña")
        visor_centralizador.Add(self.etiqueta_contraseña, 0, wx.ALL | wx.CENTER, 5)
        self.contraseña = wx.TextCtrl(pantalla_principal)
        visor_centralizador.Add(self.contraseña, 0, wx.ALL | wx.EXPAND, 5)

        # Botones para iniciar sesión y registrarse
        self.validacion = wx.Button(pantalla_principal, label="Ingresar")
        self.validacion.Bind(wx.EVT_BUTTON, self.validacion_cuenta)
        visor_centralizador.Add(self.validacion, 0, wx.ALL | wx.CENTER, 5)

        self.registro = wx.Button(pantalla_principal, label="Registrarse")
        self.registro.Bind(wx.EVT_BUTTON, self.registro_cuenta)
        visor_centralizador.Add(self.registro, 0, wx.ALL | wx.CENTER, 5)

        pantalla_principal.SetSizer(visor_centralizador)

    # Validar las credenciales de usuario
    def validacion_cuenta(self, event):
        usuario_validacion = self.usuario.GetValue()
        contraseña_validacion = self.contraseña.GetValue()

        with open("Base de datos.pkl", "rb") as datos:
            archivo_base_datos = pickle.load(datos)
            verificacion_administrador = None

            # Verificar si el usuario es "Usuario" o "Administrador"
            for diccionario in archivo_base_datos["Usuario"]:
                if usuario_validacion in diccionario and diccionario[usuario_validacion] == contraseña_validacion:
                    verificacion_administrador = False
            for diccionario in archivo_base_datos["Administrador"]:
                if usuario_validacion in diccionario and diccionario[usuario_validacion] == contraseña_validacion:
                    verificacion_administrador = True

        # Ejecutar el script correspondiente
        if verificacion_administrador:
            subprocess.run(["python", "../Reserva_Restaruante/Administradores/Administradores.py"])
        else:
            subprocess.run(["python", "../Reserva_Restaruante/Usuarios/Usuarios.py"])

        self.Close()

    # Mostrar la ventana de registro
    def registro_cuenta(self, event):
        pantalla_registro = Registro(None)
        pantalla_registro.Show()

# Iniciar la aplicación
app = wx.App(False)
frame = Login()
frame.Show()
app.MainLoop()

