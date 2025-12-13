from user_manager import UserManager
from message_manager import MessageManager
from post_manager import PostManager
from connection import get_connection

def clear_db():
    conn = get_connection()
    conn.connect_to_neo()
    conn.clean_all()
    conn.close()
    print("Base de datos limpia")

def seed():
    clear_db()
    
    um = UserManager()
    mm = MessageManager()
    pm = PostManager()

    print("\n--- Generando Ejemplos de Usuarios ---")
    u1 = um.create_user("Ana", "Person")
    u2 = um.create_user("Beto", "Person")
    u3 = um.create_user("Carlos", "Person")
    u4 = um.create_user("David", "Person")
    u5 = um.create_user("Eva", "Person")
    c1 = um.create_user("TecnoSoluciones", "Company")
    e1 = um.create_user("Universidad de Datos", "EducationCenter")
    print("\n--- Generando Ejemplos de Relaciones ---")
    um.create_connection("Ana", "Beto", "FRIEND")
    um.create_connection("Beto", "Carlos", "FRIEND")
    um.create_connection("Ana", "David", "FAMILY") 
    um.create_connection("David", "Eva", "FAMILY")   
    um.create_connection("Ana", "TecnoSoluciones", "WORK")
    um.create_connection("Beto", "TecnoSoluciones", "WORK")
    um.create_connection("Carlos", "Universidad de Datos", "ACADEMIC")
    print("\n--- Generando Ejemplos de Mensajes ---")
    mm.send_message("Ana", "Beto", "¡Hola Beto!", "conv1", 1)
    mm.send_message("Beto", "Ana", "Hola Ana, ¿cómo estás?", "conv1", 2)
    mm.send_message("Ana", "Beto", "Bien, trabajando en Neo4j.", "conv1", 3) 
    mm.send_message("Beto", "Carlos", "Qué pasa Carlos", "conv2", 1)
    mm.send_message("Carlos", "Beto", "Todo bien Beto", "conv2", 2)
    mm.send_message("Beto", "Carlos", "Aquí andamos", "conv2", 3)
    mm.send_message("Ana", "David", "Hola tío David", "conv3", 1)
    print("\n--- Generando Ejemplos de Publicaciones ---")
    um.create_connection("Ana", "Beto", "WORK") 
    pm.create_post("Ana", "Actualización del Proyecto", "Estamos progresando mucho", mentions=["Beto", "Carlos"])
    print("\n--- Ejemplos completados ---")


def interactive_menu():
    um = UserManager()
    pm = PostManager()
    
    while True:
        print("\n==============================================")
        print("       CONSOLA INTERACTIVA DE NEO4J")
        print("==============================================")
        print("1. Generar Ejemplos")
        print("2. Crear Usuario")
        print("3. Crear Relación")
        print("4. Crear Publicación (Post)")
        print("5. Limpiar Base de Datos")
        print("6. Salir")
        print("==============================================")
        
        option = input("Seleccione una opción: ")
        
        match option:
            case "1":
                seed()
            case "2":
                name = input("Nombre del usuario: ")
                print("Tipos disponibles: Person, Company, EducationCenter")
                user_type = input("Tipo de usuario (Enter para 'Person'): ")
                if not user_type:
                    user_type = "Person"
                try:
                    um.create_user(name, user_type)
                    print(f"Usuario {name} ({user_type}) creado exitosamente.")
                except Exception as e:
                    print(f"Error al crear usuario: {e}")
            case "3":
                name1 = input("Nombre del primer usuario: ")
                name2 = input("Nombre del segundo usuario: ")
                print("Tipos disponibles: FRIEND, FAMILY, ACADEMIC, WORK")
                rel_type = input("Tipo de relación: ")
                try:
                    um.create_connection(name1, name2, rel_type)
                    print(f"Relación {rel_type} creada entre {name1} y {name2}.")
                except Exception as e:
                    print(f"Error al crear relación: {e}")
            case "4":
                author = input("Nombre del autor: ")
                title = input("Título del post: ")
                body = input("Contenido del post: ")
                mentions_input = input("Menciones (nombres separados por coma, Enter para ninguna): ")
                mentions = [m.strip() for m in mentions_input.split(",")] if mentions_input else []
                try:
                    pm.create_post(author, title, body, mentions)
                    print(f"Post creado por {author} exitosamente.")
                except Exception as e:
                    print(f"Error al crear post: {e}")
            case "5":
                confirm = input("¿Seguro que quiere borrar TODA la base de datos? (s/n): ")
                if confirm.lower() == 's':
                    clear_db()
            case "6":
                print("Cerrando...")
                break
            case _:
                print("Opción no válida, intente de nuevo.")

if __name__ == "__main__":
    interactive_menu()
