from user_manager import GestorUsuarios
from message_manager import GestorMensajes
from post_manager import GestorPublicaciones
from connection import obtener_conexion

<<<<<<< HEAD
def limpiar_bd():
    conn = obtener_conexion()
    conn.conectar_neo()
    conn.limpiar_todo()
    conn.cerrar()
    print("Base de datos limpiada.")
=======
def clear_db():
    conn = get_connection()
    conn.connect_to_neo()
    conn.clean_all()
    conn.close()
    print("Base de datos limpia")
>>>>>>> f593055cbdea242f61a0036f77db050e50ba724b

def semilla():
    limpiar_bd()
    
    gu = GestorUsuarios()
    gm = GestorMensajes()
    gp = GestorPublicaciones()

    print("\n--- Generando Ejemplos de Usuarios ---")
    u1 = gu.crear_usuario("Ana", "Persona")
    u2 = gu.crear_usuario("Beto", "Persona")
    u3 = gu.crear_usuario("Carlos", "Persona")
    u4 = gu.crear_usuario("David", "Persona")
    u5 = gu.crear_usuario("Eva", "Persona")
    c1 = gu.crear_usuario("TecnoSoluciones", "Empresa")
    e1 = gu.crear_usuario("Universidad de Datos", "CentroEducativo")
    print("\n--- Generando Ejemplos de Relaciones ---")
    gu.crear_relacion("Ana", "Beto", "AMIGO")
    gu.crear_relacion("Beto", "Carlos", "AMIGO")
    gu.crear_relacion("Ana", "David", "FAMILIA") 
    gu.crear_relacion("David", "Eva", "FAMILIA")   
    gu.crear_relacion("Ana", "TecnoSoluciones", "TRABAJO")
    gu.crear_relacion("Beto", "TecnoSoluciones", "TRABAJO")
    gu.crear_relacion("Carlos", "Universidad de Datos", "ACADEMICO")
    print("\n--- Generando Ejemplos de Mensajes ---")
    gm.enviar_mensaje("Ana", "Beto", "¡Hola Beto!", "conv1", 1)
    gm.enviar_mensaje("Beto", "Ana", "Hola Ana, ¿cómo estás?", "conv1", 2)
    gm.enviar_mensaje("Ana", "Beto", "Bien, trabajando en Neo4j.", "conv1", 3) 
    gm.enviar_mensaje("Beto", "Carlos", "Qué pasa Carlos", "conv2", 1)
    gm.enviar_mensaje("Carlos", "Beto", "Todo bien Beto", "conv2", 2)
    gm.enviar_mensaje("Beto", "Carlos", "Aquí andamos", "conv2", 3)
    gm.enviar_mensaje("Ana", "David", "Hola tío David", "conv3", 1)
    print("\n--- Generando Ejemplos de Publicaciones ---")
    gu.crear_relacion("Ana", "Beto", "TRABAJO") 
    gp.crear_publicacion("Ana", "Actualización del Proyecto", "Estamos progresando mucho", menciones=["Beto", "Carlos"])
    print("\n--- Ejemplos completados ---")


def menu_interactivo():
    gu = GestorUsuarios()
    gp = GestorPublicaciones()
    
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
        
        opcion = input("Seleccione una opción: ")
        
        match opcion:
            case "1":
                semilla()
            case "2":
                nombre = input("Nombre del usuario: ")
                print("Tipos disponibles: Persona, Empresa, CentroEducativo")
                tipo_usuario = input("Tipo de usuario (Enter para 'Persona'): ")
                if not tipo_usuario:
                    tipo_usuario = "Persona"
                try:
                    gu.crear_usuario(nombre, tipo_usuario)
                    print(f"Usuario {nombre} ({tipo_usuario}) creado exitosamente.")
                except Exception as e:
                    print(f"Error al crear usuario: {e}")
            case "3":
                nombre1 = input("Nombre del primer usuario: ")
                nombre2 = input("Nombre del segundo usuario: ")
                print("Tipos disponibles: AMIGO, FAMILIA, ACADEMICO, TRABAJO")
                tipo_rel = input("Tipo de relación: ")
                try:
                    gu.crear_relacion(nombre1, nombre2, tipo_rel)
                    print(f"Relación {tipo_rel} creada entre {nombre1} y {nombre2}.")
                except Exception as e:
                    print(f"Error al crear relación: {e}")
            case "4":
                autor = input("Nombre del autor: ")
                titulo = input("Título del post: ")
                cuerpo = input("Contenido del post: ")
                menciones_input = input("Menciones (nombres separados por coma, Enter para ninguna): ")
                menciones = [m.strip() for m in menciones_input.split(",")] if menciones_input else []
                try:
                    gp.crear_publicacion(autor, titulo, cuerpo, menciones)
                    print(f"Post creado por {autor} exitosamente.")
                except Exception as e:
                    print(f"Error al crear post: {e}")
            case "5":
                confirmar = input("¿Seguro que quiere borrar TODA la base de datos? (s/n): ")
                if confirmar.lower() == 's':
                    limpiar_bd()
            case "6":
                print("Cerrando...")
                break
            case _:
                print("Opción no válida, intente de nuevo.")

if __name__ == "__main__":
    menu_interactivo()
