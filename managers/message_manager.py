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
            "   conversation_id: $conv_id, "
            "   sequence_number: $seq_num "
            "}]->(b) "
            "RETURN r"
        )
        with self.driver.session() as session:
            session.run(query, sender=sender_name, receiver=receiver_name, 
                       content=content, timestamp=timestamp, 
                       conv_id=conversation_id, seq_num=seq_num)
            print(f"Message sent from {sender_name} to {receiver_name}")

    def get_messages_after(self, sender_name, receiver_name, date_str):
        query = (
            "MATCH (a:Person {name: $sender})-[r:SENT_MESSAGE]->(b:Person {name: $receiver}) "
            "WHERE r.date > $date "
            "RETURN r.content AS content, r.date AS date"
        )
        with self.driver.session() as session:
            return [record.data() for record in session.run(query, sender=sender_name, receiver=receiver_name, date=date_str)]

    def get_conversation(self, user1, user2):
        # Capture messages in both directions
        query = (
            "MATCH (a:Person)-[r:SENT_MESSAGE]-(b:Person) "
            "WHERE (a.name = $u1 AND b.name = $u2) OR (a.name = $u2 AND b.name = $u1) "
            "RETURN r.conversation_id AS conv_id, r.sequence_number AS seq, "
            "       startNode(r).name AS sender, r.content AS content, r.date AS date "
            "ORDER BY r.date ASC"
        )
        with self.driver.session() as session:
            return [record.data() for record in session.run(query, u1=user1, u2=user2)]
