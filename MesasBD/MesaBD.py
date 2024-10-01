import mysql.connector

# Conectar a la base de datos
conexion = mysql.connector.connect(
    host="127.0.0.1",          # Dirección del host donde está la base de datos
    user="root",               # Nombre de usuario de la base de datos
    password="gustavo",        # Contraseña del usuario
    database="restaurante_reserva"  # Nombre de la base de datos a la que se conecta
)

cursor = conexion.cursor()  # Crear un cursor para ejecutar las consultas

def crear_mesa():
    """
    Crear una nueva mesa en la base de datos con estado 'libre'.
    """
    creacion_mesa = """
    INSERT INTO mesa (estado, reservador, cantidad_personas, fecha_reserva, ubicacion_mesa) 
    VALUES (%s, %s, %s, %s, %s);
    """
    cursor.execute(creacion_mesa, ("libre", None, None, None, None))  # Insertar una mesa libre
    conexion.commit()  # Guardar los cambios

def eliminar_mesa(id_mesa):
    """
    Función para eliminar una mesa de la base de datos.
    (Funcionalidad no implementada, actualmente retorna 'a')
    """
    return "a"

def vaciar_mesa(id_mesa):
    """
    Vaciar una mesa, cambiando su estado a 'libre' si está ocupada.
    
    :param id_mesa: Identificador de la mesa a vaciar.
    """
    # Verificar si la mesa está libre
    consulta_verificacion = "SELECT estado FROM mesa WHERE id_mesa = %s"
    cursor.execute(consulta_verificacion, (id_mesa,))
    resultado = cursor.fetchone()
    
    if resultado and resultado[0] == 'libre':
        # Cambiar el estado de la mesa a libre y actualizar los datos del reservador
        consulta_actualizar = """
        UPDATE mesa
        SET estado = %s, reservador = %s, cantidad_personas = %s, fecha_reserva = %s, ubicacion_mesa = %s
        WHERE id_mesa = %s
        """
        cursor.execute(consulta_actualizar, ('libre', None, None, None, None, id_mesa,))
        
        # Guardar los cambios
        conexion.commit()  # Confirmar los cambios realizados en la base de datos
        print(f"Mesa {id_mesa} vaciada exitosamente.")  # Mensaje de éxito
    else:
        print(f"La mesa {id_mesa} no está ocupada o no existe.")  # Mensaje de error

def reservar_mesa(id_mesa, reservador, cantidad_personas, fecha_reserva, ubicacion_mesa):
    """
    Reservar una mesa, cambiando su estado a 'ocupado'.
    
    :param id_mesa: Identificador de la mesa a reservar.
    :param reservador: Nombre del reservador.
    :param cantidad_personas: Número de personas para la reserva.
    :param fecha_reserva: Fecha de la reserva.
    :param ubicacion_mesa: Ubicación de la mesa.
    """
    # Verificar si la mesa está libre
    consulta_verificacion = "SELECT estado FROM mesa WHERE id_mesa = %s"
    cursor.execute(consulta_verificacion, (id_mesa,))
    resultado = cursor.fetchone()
    
    if resultado and resultado[0] == 'libre':
        # Cambiar el estado de la mesa a ocupado y actualizar los datos del reservador
        consulta_actualizar = """
        UPDATE mesa
        SET estado = %s, reservador = %s, cantidad_personas = %s, fecha_reserva = %s, ubicacion_mesa = %s
        WHERE id_mesa = %s
        """
        cursor.execute(consulta_actualizar, ('ocupado', reservador, cantidad_personas, fecha_reserva, ubicacion_mesa, id_mesa,))
        
        # Guardar los cambios
        conexion.commit()  # Confirmar los cambios realizados en la base de datos
        print(f"Mesa {id_mesa} ocupada por {reservador}.")  # Mensaje de éxito
    else:
        print(f"La mesa {id_mesa} ya está ocupada o no existe.")  # Mensaje de error



