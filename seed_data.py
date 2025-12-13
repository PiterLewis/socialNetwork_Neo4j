from user_manager import UserManager
from message_manager import MessageManager
from post_manager import PostManager
from connection import get_connection

def clear_db():
    conn = get_connection()
    conn.connect_to_neo()
    conn.clean_all()
    conn.close()
    print("Database cleared.")

def seed():
    clear_db()
    
    um = UserManager()
    mm = MessageManager()
    pm = PostManager()

    print("\n--- Sembrando Usuarios ---")
    u1 = um.create_user("Ana", "Person")
    u2 = um.create_user("Beto", "Person")
    u3 = um.create_user("Carlos", "Person")
    u4 = um.create_user("David", "Person")
    u5 = um.create_user("Eva", "Person")
    c1 = um.create_user("TecnoSoluciones", "Company")
    e1 = um.create_user("Universidad de Datos", "EducationCenter")
    print("\n--- Sembrando Relaciones ---")
    um.create_connection("Ana", "Beto", "FRIEND")
    um.create_connection("Beto", "Carlos", "FRIEND")
    um.create_connection("Ana", "David", "FAMILY") 
    um.create_connection("David", "Eva", "FAMILY")   
    um.create_connection("Ana", "TecnoSoluciones", "WORK")
    um.create_connection("Beto", "TecnoSoluciones", "WORK")
    um.create_connection("Carlos", "Universidad de Datos", "ACADEMIC")
    print("\n--- Sembrando Mensajes ---")
    mm.send_message("Ana", "Beto", "¡Hola Beto!", "conv1", 1)
    mm.send_message("Beto", "Ana", "Hola Ana, ¿cómo estás?", "conv1", 2)
    mm.send_message("Ana", "Beto", "Bien, trabajando en Neo4j.", "conv1", 3) 
    mm.send_message("Beto", "Carlos", "Qué pasa Carlos", "conv2", 1)
    mm.send_message("Carlos", "Beto", "Todo bien Beto", "conv2", 2)
    mm.send_message("Beto", "Carlos", "Aquí andamos", "conv2", 3)
    mm.send_message("Ana", "David", "Hola tío David", "conv3", 1)
    print("\n--- Sembrando Publicaciones ---")
    um.create_connection("Ana", "Beto", "WORK") 
    pm.create_post("Ana", "Actualización del Proyecto", "Estamos progresando mucho", mentions=["Beto", "Carlos"])
    print("Sembrado completo.")

if __name__ == "__main__":
    seed()
