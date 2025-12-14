from user_manager import GestorUsuarios
from message_manager import GestorMensajes
from post_manager import GestorPublicaciones
from recommendation_manager import GestorRecomendaciones
from connection import obtener_conexion

def limpiar_bd():
    conn = obtener_conexion()
    conn.conectar_neo()
    conn.limpiar_todo()
    conn.cerrar()
    print("Base de datos limpiada.")

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
    u6 = gu.crear_usuario("Felipe", "Persona")
    u7 = gu.crear_usuario("Gina", "Persona")
    u8 = gu.crear_usuario("Hector", "Persona")
    u9 = gu.crear_usuario("Ian", "Persona")
    u10 = gu.crear_usuario("Julia", "Persona")
    
    c1 = gu.crear_usuario("TecnoSoluciones", "Empresa")
    c2 = gu.crear_usuario("DataCorp", "Empresa")
    e1 = gu.crear_usuario("Universidad de Datos", "CentroEducativo")
    e2 = gu.crear_usuario("Instituto de Arte", "CentroEducativo")

    print("\n--- Generando Ejemplos de Relaciones ---")
    
    gu.crear_relacion("Ana", "Beto", "AMISTAD")
    gu.crear_relacion("Beto", "Carlos", "AMISTAD")
    gu.crear_relacion("Carlos", "Felipe", "AMISTAD")
    gu.crear_relacion("Felipe", "Gina", "AMISTAD")
    gu.crear_relacion("Gina", "Hector", "AMISTAD")
    
    gu.crear_relacion("Ana", "David", "FAMILIA") 
    gu.crear_relacion("David", "Eva", "FAMILIA")
    gu.crear_relacion("Eva", "Hector", "FAMILIA")

    gu.crear_relacion("Ana", "TecnoSoluciones", "LABORAL")
    gu.crear_relacion("Beto", "TecnoSoluciones", "LABORAL")
    gu.crear_relacion("Gina", "DataCorp", "LABORAL")
    gu.crear_relacion("Ian", "DataCorp", "LABORAL")

    gu.crear_relacion("Carlos", "Universidad de Datos", "ACADÉMICO")
    gu.crear_relacion("Julia", "Instituto de Arte", "ACADÉMICO")
    gu.crear_relacion("Ian", "Universidad de Datos", "ACADÉMICO")

    print("\n--- Generando Ejemplos de Mensajes ---")
    
    gm.enviar_mensaje("Ana", "Beto", "¡Hola Beto!", "Saludo", 1)
    gm.enviar_mensaje("Beto", "Ana", "Hola Ana, ¿cómo estás?", "Saludo", 2)
    gm.enviar_mensaje("Ana", "Beto", "Bien, trabajando en Neo4j.", "Saludo", 3) 
    
    gm.enviar_mensaje("Beto", "Carlos", "Qué pasa Carlos", "Quedada", 1)
    gm.enviar_mensaje("Carlos", "Beto", "Todo bien Beto", "Quedada", 2)
    
    gm.enviar_mensaje("Gina", "Ian", "¿Tienes el reporte?", "Reporte Mensual", 1)
    gm.enviar_mensaje("Ian", "Gina", "Sí, te lo envío ahora.", "Reporte Mensual", 2)
    gm.enviar_mensaje("Gina", "Ian", "Gracias.", "Reporte Mensual", 3)

    print("\n--- Generando Ejemplos de Publicaciones ---")
    
    gp.crear_publicacion("Ana", "Actualización del Proyecto", "Estamos progresando mucho en TecnoSoluciones", menciones=["Beto"])
    gp.crear_publicacion("Gina", "Nuevo lanzamiento", "Gran trabajo del equipo de DataCorp", menciones=["Ian"])
    gp.crear_publicacion("Carlos", "Vacaciones", "Me voy a la playa", menciones=[])

    print("\n--- Ejemplos completados ---")


def menu_interactivo():
    gu = GestorUsuarios()
    gp = GestorPublicaciones()
    gm = GestorMensajes()
    gr = GestorRecomendaciones()
    
    while True:
        print("\n==============================================")
        print("       CONSOLA INTERACTIVA DE NEO4J")
        print("==============================================")
        print("1. Generar Ejemplos (Seed)")
        print("2. Crear Usuario")
        print("3. Crear Relación")
        print("4. Crear Publicación (Post)")
        print("--- Mensajería ---")
        print("5. Enviar Mensaje")
        print("6. Ver Conversación")
        print("7. Ver Mensajes Recientes")
        print("--- Recomendaciones y Consultas ---")
        print("8. Recomendar por Saltos (Amigos de amigos)")
        print("9. Recomendar por Interacción")
        print("10. Ver Colegas Del trabajo Mencionados en Posts")
        print("11. Ver Usuarios Mencionados (Todos)")
        print("--- Gestión ---")
        print("12. Limpiar Base de Datos")
        print("13. Salir")
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
                print("Tipos disponibles: AMISTAD, FAMILIA, ACADÉMICO, LABORAL")
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
                except Exception as e:
                    print(f"Error al crear post: {e}")
            case "5":
                remitente = input("Remitente: ")
                destinatario = input("Destinatario: ")
                contenido = input("Mensaje: ")
                asunto = input("Asunto (ej. Saludo, Trabajo): ")
                try:
                    gm.enviar_mensaje(remitente, destinatario, contenido, asunto, 1)
                except Exception as e:
                    print(f"Error al enviar mensaje: {e}")
            case "6":
                u1 = input("Usuario 1: ")
                u2 = input("Usuario 2: ")
                try:
                    msgs = gm.obtener_conversacion(u1, u2)
                    if not msgs:
                        print("No hay conversación encontrada.")
                    for m in msgs:
                        print(f"[{m['fecha']}] ({m.get('asunto', 'Sin Asunto')}) {m['remitente']}: {m['contenido']}")
                except Exception as e:
                    print(f"Error al obtener conversación: {e}")
            case "7":
                remitente = input("Remitente: ")
                destinatario = input("Destinatario: ")
                fecha = input("Fecha (YYYY-MM-DDTHH:MM:SS): ")
                try:
                    msgs = gm.obtener_mensajes_despues(remitente, destinatario, fecha)
                    for m in msgs:
                        print(f"[{m['fecha']}] {m['contenido']}")
                except Exception as e:
                    print(f"Error: {e}")
            case "8":
                usuario = input("Usuario para recomendar: ")
                try:
                    recs = gr.recomendar_por_saltos(usuario)
                    print("Recomendaciones:")
                    for r in recs:
                        print(f"- {r['recomendacion']} (vía {r['intermedio']}, saltos: {r['saltos']})")
                except Exception as e:
                    print(f"Error: {e}")
            case "9":
                usuario = input("Usuario para recomendar: ")
                try:
                    recs = gr.recomendar_por_interaccion(usuario)
                    print("Recomendaciones por interacción:")
                    for r in recs:
                        print(f"- {r['recomendacion']} (vía {r['via']})")
                except Exception as e:
                    print(f"Error: {e}")
            case "10":
                autor = input("Autor del post: ")
                try:
                    colegas = gp.obtener_colegas_trabajo_mencionados(autor)
                    print(f"Colegas mencionados por {autor}: {', '.join(colegas)}")
                except Exception as e:
                    print(f"Error: {e}")
            case "11":
                autor = input("Autor del post: ")
                try:
                    mencionados = gp.obtener_menciones(autor)
                    print(f"Usuarios mencionados por {autor}: {', '.join(mencionados)}")
                except Exception as e:
                    print(f"Error: {e}")
            case "12":
                confirmar = input("¿Seguro que quiere borrar TODA la base de datos? (s/n): ")
                if confirmar.lower() == 's':
                    limpiar_bd()
            case "13":
                print("Cerrando...")
                break
            case _:
                print("Opción no válida, intente de nuevo.")

if __name__ == "__main__":
    menu_interactivo()
