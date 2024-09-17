import mysql.connector

base_datos_sql = mysql.connector.connection(host = "Reserva_RestauranteDB", user="root", password = "gustavo", database = "restaurante_reserva")
cursor = base_datos_sql.cursor()