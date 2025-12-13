from connection import obtener_conexion
from datetime import datetime

class GestorPublicaciones:
    def __init__(self):
        self.driver = obtener_conexion().obtener_driver()

    def crear_publicacion(self, nombre_autor, titulo, cuerpo, menciones=None):
        fecha_hora = datetime.now().isoformat()
        if menciones is None:
            menciones = []
        
        # Si no hay menciones, manejar sin ellas
        if not menciones:
            consulta = (
                "MATCH (u:Persona {nombre: $autor}) "
                "CREATE (p:Publicacion {titulo: $titulo, cuerpo: $cuerpo, fecha: $fecha_hora}) "
                "CREATE (u)-[:PUBLICO]->(p) "
                "RETURN p"
            )
            self.driver.execute_query(consulta, autor=nombre_autor, titulo=titulo, cuerpo=cuerpo, fecha_hora=fecha_hora, menciones=menciones, database="neo4j")
        else:
            # Validar menciones
            usuarios_faltantes = []
            for nombre_mencionado in menciones:
                consulta_check = "MATCH (u:Persona {nombre: $nombre}) RETURN u"
                resultado, _, _ = self.driver.execute_query(consulta_check, nombre=nombre_mencionado, database="neo4j")
                if not resultado:
                    usuarios_faltantes.append(nombre_mencionado)
            
            if usuarios_faltantes:
                raise ValueError(f"Los siguientes usuarios mencionados no existen: {', '.join(usuarios_faltantes)}")

            consulta = (
                "MATCH (u:Persona {nombre: $autor}) "
                "CREATE (p:Publicacion {titulo: $titulo, cuerpo: $cuerpo, fecha: $fecha_hora}) "
                "CREATE (u)-[:PUBLICO]->(p) "
                "WITH p "
                "UNWIND $menciones AS nombre_coneccion "
                "MATCH (m:Persona {nombre: nombre_coneccion}) "
                "CREATE (p)-[:MENCIONA]->(m) "
                "RETURN p"
            )
            self.driver.execute_query(consulta, autor=nombre_autor, titulo=titulo, cuerpo=cuerpo, fecha_hora=fecha_hora, menciones=menciones, database="neo4j")
            
        print(f"Publicación creada por {nombre_autor}")

    def obtener_colegas_trabajo_mencionados(self, nombre_autor):
        consulta = (
            "MATCH (autor:Persona {nombre: $nombre})-[:PUBLICO]->(p:Publicacion)-[:MENCIONA]->(mencionado:Persona) "
            "WHERE (autor)-[:TRABAJO]-(mencionado) "
            "RETURN DISTINCT mencionado.nombre AS nombre"
        )
        resultado, resumen, llaves = self.driver.execute_query(consulta, nombre=nombre_autor, database="neo4j")
        return [registro["nombre"] for registro in resultado]
