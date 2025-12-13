from connection import get_connection

class RecommendationManager:
    def __init__(self):
        self.driver = get_connection().get_driver()

    def recommend_by_hops(self, start_user, max_hops=3):

        query = (
            "MATCH (u1:Person {name: $name})-[r1]-(u2:Person) "
            f"MATCH (u2)-[r2*1..{max_hops}]-(u3:Person) "
            "WHERE u1 <> u3 AND NOT (u1)--(u3) "
            "RETURN u2.name AS intermediate, u3.name AS recommendation, length(r2) AS hops "
            "ORDER BY hops ASC"
            "RETURN u2.name AS intermediate, u3.name AS recommendation, length(r2) AS hops "
            "ORDER BY hops ASC"
        )
        result, summary, keys = self.driver.execute_query(query, name=start_user, database="neo4j")
        return [record.data() for record in result]

    def recommend_by_interaction(self, start_user, min_messages=2):    
        query = (
            "MATCH (u1:Person {name: $name})-[r1:SENT_MESSAGE]-(u2:Person) "
            "WITH u1, u2, count(r1) as msg_count_1_2 "
            "WHERE msg_count_1_2 > $min_msg "
            
            "MATCH (u2)-[r2:SENT_MESSAGE]-(u3:Person) "
            "WHERE u1 <> u3 AND NOT (u1)--(u3) "
            "WITH u1, u2, u3, msg_count_1_2, count(r2) as msg_count_2_3 "
            "WHERE msg_count_2_3 > $min_msg "
            
            "RETURN u3.name AS recommendation, u2.name AS via, "
            "msg_count_1_2, msg_count_2_3 "
            "ORDER BY msg_count_1_2 DESC, msg_count_2_3 DESC"
        )
        result, summary, keys = self.driver.execute_query(query, name=start_user, min_msg=min_messages, database="neo4j")
        return [record.data() for record in result]
