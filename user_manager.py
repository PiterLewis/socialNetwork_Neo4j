from connection import obtener_conexion
# Nota: connection.py ahora exporta obtener_conexion y la clase Conexion

class GestorUsuarios:
    def __init__(self):
        self.driver = obtener_conexion().obtener_driver()

    def crear_usuario(self, nombre, tipo_usuario="Persona"):
        """
        tipo_usuario puede ser 'Persona', 'Empresa', o 'CentroEducativo'
        """
        consulta = (
            f"MERGE (u:{tipo_usuario} {{nombre: $nombre, tipo: $tipo_usuario}}) "
            "RETURN u"
        )
        # Nota: He agregado 'tipo' como propiedad para persistir el string original si necesario, 
        # pero principalmente cambiamos el Label del nodo.
        # En el código original era MERGE (u:{user_type} {name: $name})
        # Ahora será MERGE (u:{tipo_usuario} {nombre: $nombre})
        
        consulta = (
            f"MERGE (u:{tipo_usuario} {{nombre: $nombre}}) "
            "RETURN u"
        )
        
        resultado, resumen, llaves = self.driver.execute_query(consulta, nombre=nombre, database="neo4j")
        return resultado[0]

    def crear_relacion(self, nombre1, nombre2, tipo_relacion):
        """
        tipo_relacion: 'AMIGO', 'FAMILIA', 'ACADEMICO', 'TRABAJO'
        """
        tipos_validos = ['AMIGO', 'FAMILIA', 'ACADEMICO', 'TRABAJO']
        if tipo_relacion not in tipos_validos:
            raise ValueError(f"Tipo de relación inválido. Debe ser uno de {tipos_validos}")

        consulta = (
            "MATCH (a {nombre: $nombre1}), (b {nombre: $nombre2}) "
            f"MERGE (a)-[r:{tipo_relacion}]->(b) "
            "RETURN r"
        )
        resultado, resumen, llaves = self.driver.execute_query(consulta, nombre1=nombre1, nombre2=nombre2, database="neo4j")
        return resultado[0]

    def obtener_amigos_y_familia(self, nombre):
        consulta = (
            "MATCH (u:Persona {nombre: $nombre})-[r:AMIGO|FAMILIA]-(pariente) "
            "RETURN pariente.nombre AS nombre, type(r) AS relacion"
        )
        resultado, resumen, llaves = self.driver.execute_query(consulta, nombre=nombre, database="neo4j")
        return [registro.data() for registro in resultado]

    def obtener_familia_de_familia(self, nombre):
        consulta = (
            "MATCH (u:Persona {nombre: $nombre})-[:FAMILIA]-(f)-[:FAMILIA]-(fof) "
            "WHERE fof <> u "
            "RETURN DISTINCT fof.nombre AS nombre"
        )
        resultado, resumen, llaves = self.driver.execute_query(consulta, nombre=nombre, database="neo4j")
        return [registro["nombre"] for registro in resultado]
