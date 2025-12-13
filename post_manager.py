from connection import get_connection
from datetime import datetime

class PostManager:
    def __init__(self):
        self.driver = get_connection().get_driver()

    def create_post(self, author_name, title, body, mentions=None):
        timestamp = datetime.now().isoformat()
        if mentions is None:
            mentions = []
        
        query = (
            "MATCH (u:Person {name: $author}) "
            "CREATE (p:Post {title: $title, body: $body, date: $timestamp}) "
            "CREATE (u)-[:PUBLISHED]->(p) "
            "WITH p "
            "UNWIND $mentions AS connection_name "
            "MATCH (m:Person {name: connection_name}) "
            "CREATE (p)-[:MENTIONS]->(m) "
            "RETURN p"
        )

        
        if not mentions:
            query = (
                "MATCH (u:Person {name: $author}) "
                "CREATE (p:Post {title: $title, body: $body, date: $timestamp}) "
                "CREATE (u)-[:PUBLISHED]->(p) "
                "RETURN p"
            )

        self.driver.execute_query(query, author=author_name, title=title, body=body, timestamp=timestamp, mentions=mentions, database="neo4j")
        print(f"Post created by {author_name}")

    def get_mentioned_work_colleagues(self, author_name):
        query = (
            "MATCH (author:Person {name: $name})-[:PUBLISHED]->(p:Post)-[:MENTIONS]->(mentioned:Person) "
            "WHERE (author)-[:WORK]-(mentioned) "
            "RETURN DISTINCT mentioned.name AS name"
        )
        result, summary, keys = self.driver.execute_query(query, name=author_name, database="neo4j")
        return [record["name"] for record in result]
