from neo4j import GraphDatabase
from connection import Connection, get_connection 
import seed_data

def console():
    print("==============================================")
    print("Bienvenido a la consola de Neo4j")
    print("==============================================")
    print("1. Ejecutar nuestra muestra de datos")
    print("2. Salir")
    print("==============================================")
    option = input("Seleccione una opción: ")
    if option == "1":
        seed_data.seed()
    elif option == "2":
        print("Hasta luego")
    else:
        print("Opción no válida")


def main():
    console()

if __name__ == "__main__":
    main()