from neo4j import GraphDatabase
from connection import Connection

uri = "bolt://172.28.98.19:7687"
username = "neo4j"
password = "xhantiago2005"


def main():
    print("Main execution")
    
    conn = Connection(username, password, uri)
    driver = conn.connect_to_neo()



if __name__ == "__main__":
    main()