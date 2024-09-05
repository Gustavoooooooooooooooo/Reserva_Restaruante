import pickle
Usuarios = [{"cliente123":"cliente123"}]
Administrador = [{"administrador123":"administrador123"}]

b ={"Usuario": Usuarios, "Administrador": Administrador}

nombre = 'gustavo'
contrasena = 'gustavo'
nombre2 = 'galo'
contrasena2 = 'galo'



with open("Base de datos.pkl","wb") as datos:
    pickle.dump(b,datos)

with open("Base de datos.pkl","rb") as datos:
    r = pickle.load(datos)
    print(r)

