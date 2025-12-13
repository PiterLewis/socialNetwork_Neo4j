# Proyecto de Ampliación de Bases de Datos - Neo4j

¡Hola! Este es nuestro proyecto para la práctica de Neo4j. Aquí le explicamos brevemente cómo funciona y qué necesita para ejecutarlo sin problemas.

## ¿Qué hace este código?
Hemos creado una pequeña red social simulada donde gestionamos:

### 1. Gestión de Usuarios y Relaciones
- **Usuarios**: Podemos crear personas, empresas y centros educativos.
- **Relaciones**: Conectamos a los usuarios mediante relaciones de:
    - Amistad (`AMISTAD`)
    - Familia (`FAMILIA`)
    - Trabajo (`LABORAL`)
    - Estudios (`ACADÉMICO`)

### 2. Interacciones Sociales
- **Mensajería Privada**: Los usuarios pueden enviarse mensajes entre sí, creando hilos de conversación.
- **Publicaciones (Posts)**: Los usuarios pueden publicar en su muro y **mencionar** a otros usuarios.

### 3. Sistema de Recomendaciones
El sistema es inteligente y puede sugerir nuevos amigos basándose en:
- **Saltos**: "Amigos de amigos" (o amigos de amigos de amigos...).
- **Interacción**: Personas con las que interactúas mucho pero aún no sigues.

Todo esto se conecta a una base de datos **Neo4j** para guardar y consultar la información de forma gráfica.

## ¿Cómo ejecutarlo?

Para que el código funcione en su ordenador, necesita seguir estos sencillos pasos:

### 1. Instalar dependencias
Antes de nada, necesitamos instalar las librerías necesarias. Puede hacerlo de dos formas:

**Opción A: Usando pip (Estándar)**
```bash
pip install -r requirements.txt
```

**Opción B: Usando uv (Moderno)**
Si utiliza `uv`, puede instalar todo rápidamente con:
```bash
uv add python-dotenv neo4j
```


### 2. Configurar las credenciales
El proyecto necesita conectarse a su base de datos Neo4j. Tiene dos opciones para hacerlo:

**Opción A: Usar archivo .env**
Cree un archivo llamado `.env` en la misma carpeta que estos archivos y ponga sus claves dentro siguiendo este formato:

```env
NEO4J_CONN_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=su_contraseña_aqui
```

**Opción B (Más fácil): Escribirlas directamente en el código**
Si le resulta más cómodo, puede abrir el archivo `connection.py` y escribir sus claves directamente en el código. Solo tiene que sustituir las llamadas a `os.getenv(...)` por sus datos reales entre comillas.

> **Nota:** Si su base de datos no se llama `neo4j` (que es la por defecto), tendrá que cambiar el nombre en los archivos de código donde aparece `database="neo4j"`.

### 3. Iniciar el programa
Una vez configurado, simplemente ejecute el archivo principal:

```bash
uv run main.py
```
(O `python main.py` si no usa `uv`)

### 4. Usar la consola
Al iniciar, verá un menú interactivo en la consola. Seleccione la opción **1** para acceder a todas las herramientas disponibles. A continuación detallamos qué hace cada opción:

1. **Generar Ejemplos (Seed)**: 
   - Carga automáticamente un conjunto de usuarios (Ana, Beto, Carlos...), relaciones, mensajes y publicaciones de prueba.
   - **Nota**: Borra la base de datos antes de cargar los nuevos datos para evitar duplicados.

2. **Crear Usuario**: 
   - Le pedirá el **nombre** del usuario.
   - Le pedirá el **tipo** de usuario (puede ser `Persona`, `Empresa` o `CentroEducativo`). Si pulsa Enter, por defecto será `Persona`.

3. **Crear Relación**: 
   - Le pedirá el nombre del **primer usuario**.
   - Le pedirá el nombre del **segundo usuario**.
   - Le pedirá el **tipo de relación** (`AMISTAD`, `FAMILIA`, `ACADÉMICO`, `LABORAL`).

4. **Crear Publicación (Post)**: 
   - Le pedirá el nombre del **autor**.
   - Le pedirá el **título** y el **contenido** del post.
   - Le pedirá si quiere **mencionar** a alguien (escriba los nombres separados por comas).
   - **Importante**: El sistema verificará si los usuarios mencionados existen. Si no existen, le avisará y no creará el post.

5. **Limpiar Base de Datos**: 
   - Borra **todos** los nodos y relaciones de la base de datos. Úselo con precaución.

6. **Salir**: Cierra el programa.

¡Esperamos que le guste!
