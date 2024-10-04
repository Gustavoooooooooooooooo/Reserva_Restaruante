import mysql.connector

# Conectar a la base de datos
conexion = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="gustavo",
    database="restaurante_reserva"
)

# Crear un cursor para ejecutar consultas SQL
cursor = conexion.cursor()

# Función para crear una nueva mesa en la base de datos
def crear_mesa():
    # Consulta SQL para insertar una nueva mesa con estado 'libre'
    creacion_mesa = """
    INSERT INTO mesa (estado, reservador, cantidad_personas, fecha_reserva, ubicacion_mesa) 
    VALUES (%s, %s, %s, %s, %s);
    """
    # Ejecutar la consulta con valores por defecto
    cursor.execute(creacion_mesa, ("libre", None, None, None, None))
    # Confirmar los cambios en la base de datos
    conexion.commit()

# Función para eliminar una mesa por su ID
def eliminar_mesa(id_mesa):
    # Consulta SQL para eliminar una mesa por su ID
    eliminacion_mesa = "DELETE FROM mesa WHERE id_mesa = %s;"
    # Ejecutar la consulta con el ID proporcionado
    cursor.execute(eliminacion_mesa, (id_mesa,))
    # Confirmar los cambios en la base de datos
    conexion.commit()

# Función para vaciar una mesa, es decir, restablecer sus valores a 'libre'
def vaciar_mesa(id_mesa):
    # Consulta para verificar si la mesa está ocupada
    consulta_verificacion = "SELECT estado FROM mesa WHERE id_mesa = %s"
    # Ejecutar la consulta para obtener el estado de la mesa
    cursor.execute(consulta_verificacion, (id_mesa,))
    resultado = cursor.fetchone()
    
    # Si la mesa está ocupada (estado diferente de 'libre')
    if resultado and resultado[0] != 'libre':
        # Actualizar la mesa para establecerla como 'libre' y vaciar sus otros valores
        consulta_actualizar = """
        UPDATE mesa
        SET estado = %s, reservador = %s, cantidad_personas = %s, fecha_reserva = %s, ubicacion_mesa = %s
        WHERE id_mesa = %s
        """
        # Ejecutar la consulta para vaciar la mesa
        cursor.execute(consulta_actualizar, ('libre', None, None, None, None, id_mesa))
        # Confirmar los cambios en la base de datos
        conexion.commit()
        print(f"Mesa {id_mesa} vaciada exitosamente.")
    else:
        print(f"La mesa {id_mesa} no está ocupada o no existe.")

# Función para reservar una mesa
def reservar_mesa(id_mesa, reservador, cantidad_personas, fecha_reserva, ubicacion_mesa):
    # Consulta para verificar si la mesa está libre
    consulta_verificacion = "SELECT estado FROM mesa WHERE id_mesa = %s"
    # Ejecutar la consulta para obtener el estado de la mesa
    cursor.execute(consulta_verificacion, (id_mesa,))
    resultado = cursor.fetchone()
    
    # Si la mesa está libre
    if resultado and resultado[0] == 'libre':
        # Actualizar la mesa para establecerla como 'ocupado' y registrar los detalles de la reserva
        consulta_actualizar = """
        UPDATE mesa
        SET estado = %s, reservador = %s, cantidad_personas = %s, fecha_reserva = %s, ubicacion_mesa = %s
        WHERE id_mesa = %s
        """
        # Ejecutar la consulta para reservar la mesa
        cursor.execute(consulta_actualizar, ('ocupado', reservador, cantidad_personas, fecha_reserva, ubicacion_mesa, id_mesa))
        # Confirmar los cambios en la base de datos
        conexion.commit()

