from connection import get_connection

class UserManager:
    def __init__(self):
        self.driver = get_connection().get_driver()

    def create_user(self, name, user_type="Person"):
        """
        user_type can be 'Person', 'Company', or 'EducationCenter'
        """
        query = (
            f"MERGE (u:{user_type} {{name: $name}}) "
            "RETURN u"
        )
        with self.driver.session() as session:
            result = session.run(query, name=name)
            return result.single()[0]

    def create_connection(self, name1, name2, relationship_type):
        """
        relationship_type: 'FRIEND', 'FAMILY', 'ACADEMIC', 'WORK'
        """
        valid_types = ['FRIEND', 'FAMILY', 'ACADEMIC', 'WORK']
        if relationship_type not in valid_types:
            raise ValueError(f"Invalid relationship type. Must be one of {valid_types}")

        query = (
            "MATCH (a {name: $name1}), (b {name: $name2}) "
            f"MERGE (a)-[r:{relationship_type}]->(b) "
            "RETURN r"
        )
        with self.driver.session() as session:
            result = session.run(query, name1=name1, name2=name2)
            return result.single()

    def get_friends_and_family(self, name):
        query = (
            "MATCH (u:Person {name: $name})-[r:FRIEND|FAMILY]-(relative) "
            "RETURN relative.name AS name, type(r) AS relationship"
        )
        with self.driver.session() as session:
            return [record.data() for record in session.run(query, name=name)]

    def get_family_of_family(self, name):
        query = (
            "MATCH (u:Person {name: $name})-[:FAMILY]-(f)-[:FAMILY]-(fof) "
            "WHERE fof <> u "
            "RETURN DISTINCT fof.name AS name"
        )
        with self.driver.session() as session:
            return [record["name"] for record in session.run(query, name=name)]
