from neo4j import GraphDatabase
from connection import Connection

uri = "bolt://172.28.98.19:7687"
username = "neo4j"
password = "xhantiago2005"


def main():
    print("Main execution")
    
    conn = Connection(username, password, uri)
    driver = conn.connect_to_neo()
    conn.clean_all()
    driver.execute_query("CREATE (p:Person {name : $name, edad: $edad})-[:amigo]->(s:Person {name: $second_name, edad: $second_age}) RETURN p,s", name="Fernando", edad=20, second_name="Santiago", second_age=20, database="neo4j")
    driver.execute_query("""
    CREATE (u:Universidad {name: $name, loc: $loc})
    """, name="U-TAD", loc="Calle Playa de Liencres, 2", database="neo4j")
    driver.execute_query("""
                    MATCH (p:Person) WHERE p.edad = $edad_target
                    MATCH (u:Universidad {name: $university_name})
                    MERGE (p)-[:ESTUDIA_EN]->(u)
                    RETURN p.name AS Persona, u.name AS Universidad
                """, edad_target=20, university_name="U-TAD", database="neo4j")

if __name__ == "__main__":
    main()