from connection import obtener_conexion
from datetime import datetime

class GestorMensajes:
    def __init__(self):
        self.driver = obtener_conexion().obtener_driver()

    def enviar_mensaje(self, remitente, destinatario, contenido, asunto, num_secuencia):
        fecha_hora = datetime.now().isoformat()
        consulta = (
            "MATCH (a:Persona {nombre: $remitente}), (b:Persona {nombre: $destinatario}) "
            "CREATE (a)-[r:ENVIO_MENSAJE { "
            "   contenido: $contenido, "
            "   fecha: $fecha_hora, "
            "   asunto: $asunto, "
            "   numero_secuencia: $num_secuencia "
            "}]->(b) "
            "RETURN r"
        )
        self.driver.execute_query(consulta, remitente=remitente, destinatario=destinatario, 
                       contenido=contenido, fecha_hora=fecha_hora, 
                       asunto=asunto, num_secuencia=num_secuencia, database="neo4j")
        print(f"Mensaje enviado de {remitente} a {destinatario}")

    def obtener_mensajes_despues(self, remitente, destinatario, fecha_str):
        consulta = (
            "MATCH (a:Persona {nombre: $remitente})-[r:ENVIO_MENSAJE]->(b:Persona {nombre: $destinatario}) "
            "WHERE r.fecha > $fecha "
            "RETURN r.contenido AS contenido, r.fecha AS fecha"
        )
        resultado, resumen, llaves = self.driver.execute_query(consulta, remitente=remitente, destinatario=destinatario, fecha=fecha_str, database="neo4j")
        return [registro.data() for registro in resultado]

    def obtener_conversacion(self, usuario1, usuario2):
        consulta = (
            "MATCH (a:Persona)-[r:ENVIO_MENSAJE]-(b:Persona) "
            "WHERE (a.nombre = $u1 AND b.nombre = $u2) "
            "RETURN DISTINCT r.asunto AS asunto, r.numero_secuencia AS sec, "
            "       startNode(r).nombre AS remitente, r.contenido AS contenido, r.fecha AS fecha "
            "ORDER BY r.fecha ASC"
        )
        
        resultado, resumen, llaves = self.driver.execute_query(consulta, u1=usuario1, u2=usuario2, database="neo4j")
        return [registro.data() for registro in resultado]
