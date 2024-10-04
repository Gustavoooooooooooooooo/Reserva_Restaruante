import wx, pickle, subprocess

# Clase para la ventana de registro de nuevos usuarios
class Registro(wx.Frame):
    def __init__(self, *args, **kw):
        super(Registro, self).__init__(*args, **kw)

        # Establecer el icono de la ventana
        icono = wx.Icon("../Reserva_Restaruante/imagenes/icono.png", wx.BITMAP_TYPE_PNG)
        self.SetIcon(icono)

        # Crear panel principal de la ventana de registro
        self.pantalla_registro = wx.Panel(self)
        self.SetTitle("Registro")  # Título de la ventana
        self.SetSize((300, 350))  # Tamaño de la ventana

        # Crear un sizer vertical para organizar los elementos
        self.visor_centralizador = wx.BoxSizer(wx.VERTICAL)

        # Etiqueta para el campo de usuario
        self.etiqueta_usuario = wx.StaticText(self.pantalla_registro, label="Ingrese el nombre de Usuario que va a utilizar")
        self.visor_centralizador.Add(self.etiqueta_usuario, 0, wx.ALL | wx.CENTER, 5)

        # Campo de texto para ingresar el usuario
        self.usuario = wx.TextCtrl(self.pantalla_registro)
        self.visor_centralizador.Add(self.usuario, 0, wx.ALL | wx.CENTER, 5)

        # Etiqueta para el campo de contraseña
        self.etiqueta_contrasena = wx.StaticText(self.pantalla_registro, label="Ingrese la contraseña que va a utilizar")
        self.visor_centralizador.Add(self.etiqueta_contrasena, 0, wx.ALL | wx.CENTER, 5)

        # Campo de texto para ingresar la contraseña
        self.contraseña = wx.TextCtrl(self.pantalla_registro)
        self.visor_centralizador.Add(self.contraseña, 0, wx.ALL | wx.CENTER, 5)

        # Etiqueta para seleccionar el rol del usuario (Usuario o Administrador)
        self.etiqueta_rol = wx.StaticText(self.pantalla_registro, label="Ingrese el rol que va a cumplir")
        self.visor_centralizador.Add(self.etiqueta_rol, 0, wx.ALL | wx.CENTER, 5)

        # Lista desplegable con las opciones de roles
        opciones = ["Usuario", "Administrador"]
        self.rol = wx.ListBox(self.pantalla_registro, choices=opciones, style=wx.LB_SINGLE)
        self.visor_centralizador.Add(self.rol, 0, wx.ALL | wx.CENTER, 5)

        # Botón para finalizar el registro
        self.registro = wx.Button(self.pantalla_registro, label="Registrarse")
        self.registro.Bind(wx.EVT_BUTTON, self.registro_cuenta)  # Llamar método para registrar cuenta
        self.visor_centralizador.Add(self.registro, 0, wx.ALL | wx.CENTER, 5)

        # Configurar el layout del panel
        self.visor_centralizador.Fit(self.pantalla_registro)
        self.pantalla_registro.SetSizer(self.visor_centralizador)

    # Método para registrar una nueva cuenta
    def registro_cuenta(self, event):
        self.usuario_registro = self.usuario.GetValue()
        self.contraseña_registro = self.contraseña.GetValue()
        self.rol_registro = self.rol.GetStringSelection()

        # Verificar si todos los campos están llenos
        try:
            if not self.usuario_registro or not self.contraseña_registro or not self.rol_registro:
                wx.MessageBox("Por favor, complete todos los campos", "Error", wx.OK | wx.ICON_ERROR)
            else:
                self.validar_nombre()
                # Abrir el archivo de la base de datos para agregar el nuevo usuario
                with open("Base de datos.pkl", "rb+") as datos:
                    registracion = pickle.load(datos)
                    usuario_existente = False

                    # Comprobar si el nombre de usuario ya existe
                    for usuario in registracion[self.rol_registro]:
                        if self.usuario_registro in usuario:
                            usuario_existente = True
                            break

                    # Si el usuario ya existe, mostrar un mensaje de error
                    if usuario_existente:
                        wx.MessageBox("El nombre de usuario ya existe. Por favor, elija otro.", "Error", wx.OK | wx.ICON_ERROR)
                    else:
                        # Agregar el usuario nuevo a la base de datos
                        if self.rol_registro == "Usuario":
                            registracion["Usuario"].append({self.usuario_registro: self.contraseña_registro})
                        elif self.rol_registro == "Administrador":
                            registracion["Administrador"].append({self.usuario_registro: self.contraseña_registro})

                        # Guardar los cambios en la base de datos
                        datos.seek(0)
                        pickle.dump(registracion, datos)

                        # Mostrar mensaje de éxito
                        wx.MessageBox("Se ha registrado correctamente", "Registro", wx.OK | wx.ICON_INFORMATION)
                        self.Close()  # Cerrar la ventana de registro
        except ValueError:
            wx.MessageBox("Ha ocurrido un error, vuelva a intentar registrarse", "Error", wx.OK | wx.ICON_ERROR)

    def validar_nombre(self):

        self.nombre_verificacion = self.usuario_registro.strip()

        if not self.nombre_verificacion:
            wx.MessageBox("El nombre no puede estar vacio", "Error", wx.OK | wx.ICON_ERROR)
            raise ValueError


# Clase para la ventana de login
class Login(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title="Login")

        # Crear el panel principal de la ventana de login
        pantalla_principal = wx.Panel(self)
        icono = wx.Icon("../Reserva_Restaruante/imagenes/icono.png", wx.BITMAP_TYPE_PNG)
        self.SetIcon(icono)
        visor_centralizador = wx.BoxSizer(wx.VERTICAL)

        # Etiqueta para ingresar el nombre de usuario
        self.etiqueta_usuario = wx.StaticText(pantalla_principal, label="Coloque su nombre de usuario")
        visor_centralizador.Add(self.etiqueta_usuario, 0, wx.ALL | wx.CENTER, 5)

        # Campo de texto para ingresar el nombre de usuario
        self.usuario = wx.TextCtrl(pantalla_principal)
        visor_centralizador.Add(self.usuario, 0, wx.ALL | wx.EXPAND, 5)

        # Etiqueta para ingresar la contraseña
        self.etiqueta_contraseña = wx.StaticText(pantalla_principal, label="Coloque su contraseña")
        visor_centralizador.Add(self.etiqueta_contraseña, 0, wx.ALL | wx.CENTER, 5)

        # Campo de texto para ingresar la contraseña
        self.contraseña = wx.TextCtrl(pantalla_principal)
        visor_centralizador.Add(self.contraseña, 0, wx.ALL | wx.EXPAND, 5)

        # Botón para validar el login
        self.validacion = wx.Button(pantalla_principal, label="Ingresar")
        self.validacion.Bind(wx.EVT_BUTTON, self.validacion_cuenta)  # Llamar método para validar login
        visor_centralizador.Add(self.validacion, 0, wx.ALL | wx.CENTER, 5)

        # Botón para abrir la ventana de registro
        self.registro = wx.Button(pantalla_principal, label="Registrarse")
        self.registro.Bind(wx.EVT_BUTTON, self.registro_cuenta)
        visor_centralizador.Add(self.registro, 0, wx.ALL | wx.CENTER, 5)

        # Configurar el layout del panel
        pantalla_principal.SetSizer(visor_centralizador)

    # Método para validar el login de un usuario
    def validacion_cuenta(self, event):
        usuario_validacion = self.usuario.GetValue()
        contraseña_validacion = self.contraseña.GetValue()

        # Verificar si los campos de usuario y contraseña están completos
        if not usuario_validacion or not contraseña_validacion:
            wx.MessageBox("Por favor, complete todos los campos", "Error", wx.OK | wx.ICON_ERROR)
        else:
            datos_cuenta = {usuario_validacion: contraseña_validacion}

            # Abrir el archivo de base de datos y validar credenciales
            with open("Base de datos.pkl", "rb") as datos:
                archivo_base_datos = pickle.load(datos)
                verificacion_administrador = None

                # Comprobar si el usuario es un usuario regular
                for diccionario in archivo_base_datos["Usuario"]:
                    if usuario_validacion in diccionario and diccionario[usuario_validacion] == contraseña_validacion:
                        verificacion_administrador = False

                # Comprobar si el usuario es un administrador
                for diccionario in archivo_base_datos["Administrador"]:
                    if usuario_validacion in diccionario and diccionario[usuario_validacion] == contraseña_validacion:
                        verificacion_administrador = True

                # Mostrar mensaje si el usuario no fue encontrado
                if verificacion_administrador is None:
                    wx.MessageBox("No existe el usuario/administrador ingresado. Ingrese de nuevo.", "Error", wx.OK | wx.ICON_ERROR)

            # Abrir la ventana correspondiente al rol del usuario
            if verificacion_administrador is True:
                self.Close()
                subprocess.Popen(["python", "../Reserva_Restaruante/Administradores/Administradores.py"])
            elif verificacion_administrador is False:
                subprocess.Popen(["python", "../Reserva_Restaruante/Usuarios/Usuarios.py"])
                self.Close()

    # Método para abrir la ventana de registro de usuario
    def registro_cuenta(self, event):
        pantalla_registro = Registro(None)
        pantalla_registro.Show()

# Iniciar la aplicación wxPython
app = wx.App(False)
frame = Login()  # Crear instancia de la ventana de login
frame.Show()  # Mostrar la ventana de login
app.MainLoop()  # Iniciar el loop de la aplicación
