from connection import get_connection
from datetime import datetime

class MessageManager:
    def __init__(self):
        self.driver = get_connection().get_driver()

    def send_message(self, sender_name, receiver_name, content, conversation_id, seq_num):
        timestamp = datetime.now().isoformat()
        query = (
            "MATCH (a:Person {name: $sender}), (b:Person {name: $receiver}) "
            "CREATE (a)-[r:SENT_MESSAGE { "
            "   content: $content, "
            "   date: $timestamp, "
            "   sequence_number: $seq_num "
            "}]->(b) "
            "RETURN r"
        )
        self.driver.execute_query(query, sender=sender_name, receiver=receiver_name, 
                       content=content, timestamp=timestamp, 
                       conv_id=conversation_id, seq_num=seq_num, database="neo4j")
        print(f"Message sent from {sender_name} to {receiver_name}")

    def get_messages_after(self, sender_name, receiver_name, date_str):
        query = (
            "MATCH (a:Person {name: $sender})-[r:SENT_MESSAGE]->(b:Person {name: $receiver}) "
            "WHERE r.date > $date "
            "RETURN r.content AS content, r.date AS date"
        )
        result, summary, keys = self.driver.execute_query(query, sender=sender_name, receiver=receiver_name, date=date_str, database="neo4j")
        return [record.data() for record in result]

    def get_conversation(self, user1, user2):
        query = (
            "MATCH (a:Person)-[r:SENT_MESSAGE]-(b:Person) "
            "WHERE (a.name = $u1 AND b.name = $u2) OR (a.name = $u2 AND b.name = $u1) "
            "RETURN r.conversation_id AS conv_id, r.sequence_number AS seq, "
            "       startNode(r).name AS sender, r.content AS content, r.date AS date "
            "ORDER BY r.date ASC"
        )
        result, summary, keys = self.driver.execute_query(query, u1=user1, u2=user2, database="neo4j")
        return [record.data() for record in result]
