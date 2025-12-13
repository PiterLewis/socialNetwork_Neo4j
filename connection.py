from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

load_dotenv()

class Conexion:

    def __init__(self):
        self.__usuario = os.getenv("NEO4J_USERNAME")
        self.__contrasena = os.getenv("NEO4J_PASSWORD")
        self.__uri = os.getenv("NEO4J_CONN_URI")
        self.__driver = None 

    def conectar_neo(self):
        if self.__driver:
            print("Ya conectado a Neo4j.")
            return self.__driver
        try:
            instancia_driver = GraphDatabase.driver(self.__uri, auth=(self.__usuario, self.__contrasena))
            self.__driver = instancia_driver
        except Exception as e:
            print(f"No se pudo conectar: {e}. Chequea la conexión o instancia el objeto de conexion primero")
            self.__driver = None
        return self.__driver

    def obtener_driver(self):
        return self.conectar_neo()

    def cerrar(self):
        if self.__driver:
            self.__driver.close()
            print("Conexión del driver cerrada.")
            self.__driver = None

    def limpiar_todo(self):
        if not self.__driver:
            print("No hay driver de Neo4j conectado para limpiar la base de datos.")
            return

        try:
            resultado, resumen, llaves = self.__driver.execute_query(
                "MATCH (n) DETACH DELETE n",
                database="neo4j"
            )
            print(f"¡Base de datos limpia! Nodos borrados: {resumen.counters.nodes_deleted}, relaciones borradas: {resumen.counters.relationships_deleted}.")
        
        except Exception as e:
            print(f"Error al limpiar la base de datos: {e}")


def obtener_conexion():
    return Conexion()