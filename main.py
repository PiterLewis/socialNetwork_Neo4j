from neo4j import GraphDatabase
from conexion import obtener_conexion
import datos_semilla


def inicio():
    datos_semilla.menu_interactivo()

if __name__ == "__main__":
    inicio()