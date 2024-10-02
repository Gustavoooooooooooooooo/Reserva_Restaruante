import mysql.connector

# Conectar a la base de datos
conexion = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="gustavo",
    database="restaurante_reserva"
)

cursor = conexion.cursor()

def crear_mesa():
    creacion_mesa = """
    INSERT INTO mesa (estado,reservador,cantidad_personas,fecha_reserva,ubicacion_mesa) VALUES (%s,%s,%s,%s,%s);
    """
    cursor.execute(creacion_mesa, ("libre",None,None,None,None))
    conexion.commit()

def eliminar_mesa(id_mesa):
    eliminacion_mesa = "DELETE FROM mesa WHERE id_mesa = %s;"
    cursor.execute(eliminacion_mesa,(id_mesa,))
    conexion.commit()

def vaciar_mesa(id_mesa):
    # Verificar si la mesa está libre
    consulta_verificacion = "SELECT estado FROM mesa WHERE id_mesa = %s"
    cursor.execute(consulta_verificacion, (id_mesa,))
    resultado = cursor.fetchone()
    
    if resultado and resultado[0] != 'libre':
        # Cambiar el estado de la mesa a ocupado y actualizar los datos del reservador
        consulta_actualizar = """
        UPDATE mesa
        SET estado = %s, reservador = %s, cantidad_personas = %s, fecha_reserva = %s, ubicacion_mesa = %s
        WHERE id_mesa = %s
        """
        cursor.execute(consulta_actualizar, ('libre', None, None, None,None, id_mesa,))
        
        # Guardar los cambios
        conexion.commit()
        print(f"Mesa {id_mesa} vaciada exitosamente.")
    else:
        print(f"La mesa {id_mesa} no está ocupada o no existe.")


def reservar_mesa(id_mesa, reservador, cantidad_personas, fecha_reserva, ubicacion_mesa):
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
        cursor.execute(consulta_actualizar, ('ocupado', reservador, cantidad_personas, fecha_reserva,ubicacion_mesa, id_mesa,))
        
        # Guardar los cambios
        conexion.commit()
        print(f"Mesa {id_mesa} ocupada por {reservador}.")
    else:
        print(f"La mesa {id_mesa} ya está ocupada o no existe.")



