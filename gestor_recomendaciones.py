from conexion import obtener_conexion

class GestorRecomendaciones:
    def __init__(self):
        self.driver = obtener_conexion().obtener_driver()

    def recomendar_por_saltos(self, usuario_inicio, max_saltos=3):

        consulta = (
            "MATCH (u1:Persona {nombre: $nombre})-[r1]-(u2:Persona) "
            f"MATCH (u2)-[r2*1..{max_saltos}]-(u3:Persona) "
            "WHERE u1 <> u3 AND NOT (u1)--(u3) "
            "RETURN u2.nombre AS intermedio, u3.nombre AS recomendacion, length(r2) AS saltos "
            "ORDER BY saltos ASC"
        )
        resultado, resumen, llaves = self.driver.execute_query(consulta, nombre=usuario_inicio, database="neo4j")
        return [registro.data() for registro in resultado]

    def recomendar_por_interaccion(self, usuario_inicio, min_mensajes=2):    
        consulta = (
            "MATCH (u1:Persona {nombre: $nombre})-[r1:ENVIO_MENSAJE]-(u2:Persona) "
            "WITH u1, u2, count(r1) as cuenta_msg_1_2 "
            "WHERE cuenta_msg_1_2 > $min_msg "
            
            "MATCH (u2)-[r2:ENVIO_MENSAJE]-(u3:Persona) "
            "WHERE u1 <> u3 AND NOT (u1)--(u3) "
            "WITH u1, u2, u3, cuenta_msg_1_2, count(r2) as cuenta_msg_2_3 "
            "WHERE cuenta_msg_2_3 > $min_msg "
            
            "RETURN u3.nombre AS recomendacion, u2.nombre AS via, "
            "cuenta_msg_1_2, cuenta_msg_2_3 "
            "ORDER BY cuenta_msg_1_2 DESC, cuenta_msg_2_3 DESC"
        )
        resultado, resumen, llaves = self.driver.execute_query(consulta, nombre=usuario_inicio, min_msg=min_mensajes, database="neo4j")
        return [registro.data() for registro in resultado]
