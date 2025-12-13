from neo4j import GraphDatabase

class Connection:

    def __init__(self, username_param, password_param, uri_param):
        self.__username = username_param
        self.__password = password_param
        self.__uri = uri_param
        self.__driver = None 

    def connect_to_neo(self):
        if self.__driver:
            print("Ya conectado a Neo4j.")
            return self.__driver
        try:
            driver_instance = GraphDatabase.driver(self.__uri, auth=(self.__username, self.__password))
            self.__driver = driver_instance
            print("Driver conectado exitosamente:", self.__driver)
        except Exception as e:
            print(f"No se pudo conectar: {e}. Chequea la conexión o instancia el objeto de conexion primero")
            self.__driver = None
        return self.__driver

    def close(self):
        if self.__driver:
            self.__driver.close()
            print("Conexión del driver cerrada.")
            self.__driver = None

    def clean_all(self):
        if not self.__driver:
            print("No hay driver de Neo4j conectado para limpiar la base de datos.")
            return

        try:
            result, summary, keys = self.__driver.execute_query(
                "MATCH (n) DETACH DELETE n",
                database="neo4j"
            )
            print(f"¡Base de datos limpia! Nodos borrados: {summary.counters.nodes_deleted}, relaciones borradas: {summary.counters.relationships_deleted}.")
        
        except Exception as e:
            print(f"Error al limpiar la base de datos: {e}")