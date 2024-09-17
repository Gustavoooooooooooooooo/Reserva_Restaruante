import pickle
import os
import mysql.connector
class Mesa():

    Contador_id = "Contador_id.pkl"

    def __init__(self):
        self.__Id_Mesa = self.get_nuevoid()
        self.__base_datos = open("../Reserva_Restaruante/MesasBD/Mesas.pkl", "rb+")

    def get_nuevoid(self):

        if os.path.exists("Contador_id.pkl"):
            with open("Contador_id.pkl", "wb") as iD:
                pickle.dump(0, iD)

        with open("Contador_id.pkl", "rb") as iD:
            ultimo_id = pickle.load(iD)

        nuevo_id = ultimo_id + 1

        with open("Contador_id.pkl", "wb") as iD:
            pickle.dump(nuevo_id, iD)

        return nuevo_id
    
    def agregar_mesa(self,reservador,cantidad_personas,fecha_reserva):
        reserva_mesa = {"ID de la mesa":self.__Id_Mesa,"Reservador": reservador,"Cantidad de Personas":cantidad_personas,"Fecha de la reserva": fecha_reserva}
        pickle.dump(reserva_mesa,self.__base_datos)
