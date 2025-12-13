# Proyecto de Ampliación de Bases de Datos - Neo4j

¡Hola! Este es nuestro proyecto para la práctica de Neo4j. Aquí le explicamos brevemente cómo funciona y qué necesita para ejecutarlo sin problemas.

## ¿Qué hace este código?
Hemos creado una pequeña red social simulada donde gestionamos:
- **Usuarios** (Personas, Empresas, Centros Educativos).
- **Relaciones** (Amistad, Familia, Trabajo, Estudios).
- **Interacciones** (Mensajes privados y Publicaciones en el muro).
- **Recomendaciones** (Sugerencias de amistad basadas en amigos en común o interacciones).

Todo esto se conecta a una base de datos **Neo4j** para guardar y consultar la información de forma gráfica.

## ¿Cómo ejecutarlo?

Para que el código funcione en su ordenador, necesita seguir estos sencillos pasos:

### 1. Configurar las credenciales
El proyecto necesita conectarse a su base de datos Neo4j. Tiene dos opciones para hacerlo:

**Opción A (Recomendada): Usar archivo .env**
Cree un archivo llamado `.env` en la misma carpeta que estos archivos y ponga sus claves dentro siguiendo este formato:

```env
NEO4J_CONN_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=su_contraseña_aqui
```

**Opción B (Más fácil): Escribirlas directamente en el código**
Si le resulta más cómodo, puede abrir el archivo `connection.py` y escribir sus claves directamente en el código. Solo tiene que sustituir las llamadas a `os.getenv(...)` por sus datos reales entre comillas.

> **Nota:** Si su base de datos no se llama `neo4j` (que es la por defecto), tendrá que cambiar el nombre en los archivos de código donde aparece `database="neo4j"`.

### 2. Iniciar el programa
Una vez configurado, simplemente ejecute el archivo principal:

```bash
uv run main.py
```
(O `python main.py` si no usa `uv`)

### 3. Usar la consola
Al iniciar, verá un menú muy sencillo en la consola. Seleccione la opción **1** para cargar los datos de prueba (nuestros usuarios y relaciones de ejemplo) y ver cómo se llena la base de datos mágicamente.

¡Esperamos que le guste!
