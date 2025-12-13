from managers.user_manager import UserManager
from managers.message_manager import MessageManager
from managers.post_manager import PostManager
from connection import get_connection

def clear_db():
    conn = get_connection().get_driver()
    with conn.session() as session:
        session.run("MATCH (n) DETACH DELETE n")
    print("Database cleared.")

def seed():
    clear_db()
    
    um = UserManager()
    mm = MessageManager()
    pm = PostManager()

    print("\n--- Seeding Users ---")
    # Users
    u1 = um.create_user("Alice", "Person")
    u2 = um.create_user("Bob", "Person")
    u3 = um.create_user("Charlie", "Person")
    u4 = um.create_user("David", "Person")
    u5 = um.create_user("Eve", "Person")
    
    # Companies & Education
    c1 = um.create_user("TechCorp", "Company")
    e1 = um.create_user("University of Data", "EducationCenter")

    print("\n--- Seeding Relationships ---")
    # Relationships
    um.create_connection("Alice", "Bob", "FRIEND")
    um.create_connection("Bob", "Charlie", "FRIEND")
    um.create_connection("Alice", "David", "FAMILY") # David is family of Alice
    um.create_connection("David", "Eve", "FAMILY")   # Eve is family of David (so Eve is family of family of Alice)
    
    um.create_connection("Alice", "TechCorp", "WORK")
    um.create_connection("Bob", "TechCorp", "WORK")
    um.create_connection("Charlie", "University of Data", "ACADEMIC")

    print("\n--- Seeding Messages ---")
    # Messages
    # Alice <-> Bob conversation
    mm.send_message("Alice", "Bob", "Hi Bob!", "conv1", 1)
    mm.send_message("Bob", "Alice", "Hey Alice, how are you?", "conv1", 2)
    mm.send_message("Alice", "Bob", "I'm good, working on Neo4j.", "conv1", 3) # Interaction > 2 messages
    
    # Bob <-> Charlie conversation
    mm.send_message("Bob", "Charlie", "Yo Charlie", "conv2", 1)
    mm.send_message("Charlie", "Bob", "Sup Bob", "conv2", 2)
    mm.send_message("Bob", "Charlie", "Not much", "conv2", 3)
    
    # Alice <-> David (less interaction)
    mm.send_message("Alice", "David", "Hi uncle connection", "conv3", 1)

    print("\n--- Seeding Posts ---")
    # Posts
    # Alice posts and mentions Bob (who she works with at TechCorp - both have WORK relation to TechCorp, but direct WORK relation?)
    # Requirement: "Obtener todos los usuarios mencionados por un usuario determinado los cuales tengan una relación laboral con el usuario que los mencionó."
    # Typically implementation: User->WORK->Company<-WORK<-User.
    # But let's assume direct WORK relation for simplicity or indirect via Company?
    # The query in PostManager checks `(author)-[:WORK]-(mentioned)`. This implies DIRECT work relationship.
    # Let's add a direct work relationship for the test case to work as traditionally expected in this schema, 
    # OR we need to update the query to check shared company. 
    # Let's stick to the prompt's implied direct relationship for now, OR better:
    # "Users mentioned... who have a work relationship with the user". 
    # Let's add a direct WORK link between Alice and Bob to test this specific query requirement.
    um.create_connection("Alice", "Bob", "WORK") 
    
    pm.create_post("Alice", "Project Update", "We are making progress", mentions=["Bob", "Charlie"])
    # Bob is mentioned and has WORK relation. Charlie is mentioned but NO WORK relation.

    print("Seeding complete.")

if __name__ == "__main__":
    seed()
