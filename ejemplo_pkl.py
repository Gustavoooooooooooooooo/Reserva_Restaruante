import mysql.connector

# Conectar a la base de datos
conexion = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="gustavo",
    database="restaurante_reserva"
)

cursor = conexion.cursor()

def agregar_mesa(id_mesa, reservador, cantidad_personas, fecha_reserva):
    # Verificar si la mesa está libre
    consulta_verificacion = "SELECT estado FROM mesas WHERE id = %s"
    cursor.execute(consulta_verificacion, (id_mesa,))
    resultado = cursor.fetchone()
    
    if resultado and resultado[0] == 'libre':
        # Cambiar el estado de la mesa a ocupado y actualizar los datos del reservador
        consulta_actualizar = """
        UPDATE mesas
        SET estado = %s, reservador = %s, cantidad_personas = %s, fecha_reserva = %s
        WHERE id = %s
        """
        cursor.execute(consulta_actualizar, ('ocupado', reservador, cantidad_personas, fecha_reserva, id_mesa))
        
        # Guardar los cambios
        conexion.commit()
        print(f"Mesa {id_mesa} ocupada por {reservador}.")
    else:
        print(f"La mesa {id_mesa} ya está ocupada o no existe.")

