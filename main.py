from neo4j import GraphDatabase
from connection import obtener_conexion
import seed_data


def inicio():
    seed_data.menu_interactivo()

if __name__ == "__main__":
    inicio()