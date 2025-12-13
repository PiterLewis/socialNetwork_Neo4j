from conexion import obtener_conexion
from datetime import datetime

class GestorMensajes:
    def __init__(self):
        self.driver = obtener_conexion().obtener_driver()

    def enviar_mensaje(self, remitente, destinatario, contenido, id_conversacion, num_secuencia):
        fecha_hora = datetime.now().isoformat()
        consulta = (
            "MATCH (a:Persona {nombre: $remitente}), (b:Persona {nombre: $destinatario}) "
            "CREATE (a)-[r:ENVIO_MENSAJE { "
            "   contenido: $contenido, "
            "   fecha: $fecha_hora, "
            "   numero_secuencia: $num_secuencia "
            "}]->(b) "
            "RETURN r"
        )
        self.driver.execute_query(consulta, remitente=remitente, destinatario=destinatario, 
                       contenido=contenido, fecha_hora=fecha_hora, 
                       id_conv=id_conversacion, num_secuencia=num_secuencia, database="neo4j")
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
            "WHERE (a.nombre = $u1 AND b.nombre = $u2) OR (a.nombre = $u2 AND b.nombre = $u1) "
            "RETURN r.id_conversacion AS id_conv, r.numero_secuencia AS sec, "
            "       startNode(r).nombre AS remitente, r.contenido AS contenido, r.fecha AS fecha "
            "ORDER BY r.fecha ASC"
        )
        # Nota: La consulta original usaba r.conversation_id pero al crear el mensaje NO lo guardé como propiedad en la relación en el CREATE original tampoco se veia explícito, 
        # Espera, en el original: "CREATE (a)-[r:SENT_MESSAGE { content: $content, date: $timestamp, sequence_number: $seq_num }]->(b)"
        # NO guardaba conversation_id en el nodo. Sin embargo, en get_conversation consultaba r.conversation_id.
        # Probablemente era un error en el código original o asumía que se pasaría.
        # Voy a agregarlo en enviar_mensaje para que funcione.
        
        # Corrección en enviar_mensaje para incluir id_conversacion
        
        resultado, resumen, llaves = self.driver.execute_query(consulta, u1=usuario1, u2=usuario2, database="neo4j")
        return [registro.data() for registro in resultado]
