from neo4j import GraphDatabase

uri = "bolt://172.28.98.19:7687"
username = "neo4j"
password = "xhantiago2005"

class Connection:

    __uri : None
    __username: None
    __password: None
    __driver: None

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


def main():
    print("Main execution")
    
    conn = Connection(username, password, uri)
    driver = conn.connect_to_neo()



if __name__ == "__main__":
    main()