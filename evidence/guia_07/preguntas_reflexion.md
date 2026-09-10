# GA7-AA1-EV01 - Reflexión: de «en mi máquina funciona» a «cualquiera puede usarlo»

## Diferencias entre el Entorno Local y el Entorno Productivo

- **Quién puede llamarla:** En el computador local solo la puede llamar el propio desarrollador (`127.0.0.1`) y en un servidor público la puede consumir cualquier persona o aplicación con acceso a internet mediante la URL pública.

- **Quién puede leer el código:** En la máquina local el código reside únicamente en el disco duro personal, pero en el servidor productivo el código pasa a estar en un repositorio remoto (como GitHub) y en el entorno del proveedor de nube, expuesto a ser visto si el repositorio es público.

- **Cuántas personas la usan a la vez:** En local la usa una sola persona para pruebas y en producción el servidor debe procesar múltiples peticiones simultáneas de varios usuarios al mismo tiempo.

- **Quién reinicia el servidor:** En local el servidor lo enciende o apaga el desarrollador desde su terminal y en la nube lo gestiona la infraestructura de la plataforma de forma automática cuando detecta fallos, reinicios o inactividad.

- **Qué pasa si se cae a las 3 de la mañana:** En el entorno local no ocurre nada porque nadie más la está usando, pero en un servidor público el servicio queda inaccesible para los usuarios reales hasta que la plataforma o el desarrollador resuelvan la caída.

- **Dónde quedan los datos:** En local los datos se almacenan en el disco duro físico del computador y en Render los datos quedan dentro del contenedor efímero del servidor, perdiéndose en cada reinicio.

- **Quién paga el servicio:** En el entorno local se asume únicamente el consumo eléctrico del equipo y en producción el costo depende del plan contratado con el proveedor de nube.

- **Qué sabe el usuario cuando algo falla:** En local el desarrollador lee la linea completa del error en la terminal (_traceback_) y en producción el usuario solo debe recibir respuestas HTTP estándar (como 400, 401, 500) para no revelar detalles internos ni vulnerabilidades de la infraestructura.

---

## Auditoría de secretos en el repositorio

- **Clave secreta JWT (`SECRET_KEY`):**
- **Estado:** La clave para firmar y validar tokens JWT se encontraba escrita como una constante de texto directamente dentro de `security.py`.

- **Gravedad y justificación:** Es un riesgo de gravedad **Crítica**. Al estar expuesto en el repositorio, cualquier persona puede tomar la clave de `security.py`, fabricar tokens JWT con rol de administrador y acceder a operaciones sensibles dentro de la API sin requerir credenciales reales.

- **Historial del archivo de base de datos (`.db`):**
- **Estado:** El archivo `mueveloya.db` estuvo incluido dentro del árbol de trabajo en la raíz del proyecto y en el historial de commits de Git.

- **Análisis de riesgo:** Aunque se añada `mueveloya.db` al `.gitignore`, el archivo sigue existiendo en el historial de commits anteriores de Git. Un atacante puede inspeccionar la historia del repositorio, descargar el `.db` y extraer usuarios, servicios, transportistas o contraseñas encriptadas guardadas durante las pruebas.

- **Datos sensibles y rutas en el código:**
- **Estado:** Se identificaron datos de prueba en la inicialización (correos, contraseñas de demostración para login) y configuraciones con rutas de archivos del sistema operativo local dentro de `database/database.py` y `main.py`.

- **Análisis de riesgo:** Las rutas locales impiden que la aplicación inicie correctamente en el sistema operativo del contenedor de Render, mientras que los datos de prueba en texto plano ofrecen información sobre los patrones de prueba usados en el sistema.

---

## Modelo de Configuración por Entorno (Twelve-Factor App - III)

El principio III de la metodología _Twelve-Factor App_ exige la separación total entre la configuración del sistema y el código fuente. La configuración varía según el entorno (desarrollo, pruebas, producción), mientras que el código permanece idéntico en todos los escenarios.

- **Ejemplo en el proyecto:** En lugar de escribir la constante `SECRET_KEY = "clave_de_prueba"` en `seguridad.py`, la aplicación invoca `os.getenv("SECRET_KEY")`. En el equipo local se lee la variable desde un archivo `.env` mediante `python-dotenv`, mientras que en Render la clave se inyecta directamente desde el panel de control de la plataforma.

---

## Análisis de Límites del Plan Gratuito de Render

- **Suspensión por inactividad:** Tras 15 minutos sin tráfico, Render suspende la ejecución del servicio para conservar recursos.

- **Respuesta en frío:** La primera petición enviada a una instancia en reposo tarda aproximadamente 60 segundos en responder mientras el contenedor vuelve a iniciar.

- **Disco efímero:** Toda modificación realizada en el sistema de archivos del contenedor (como la creación de registros en SQLite) se elimina cada vez que el servidor se reinicia o se despliega una nueva versión.

---

## Impacto en la Base de Datos SQLite y Soluciones

- **Impacto:** Al reiniciar el servicio en Render, el archivo `.db` se destruye y la aplicación pierde todos los datos registrados por los usuarios.

- **Solución 1 (Siembra automática de datos):** Configurar la función `sembrar_datos()` para que se ejecute automáticamente al arrancar el servidor si detecta que la base de datos está vacía, asegurando la creación de las tablas y del usuario administrador base.

- **Solución 2 (Migración a base de datos gestionada):** Conectar la API a un servicio de base de datos externo como PostgreSQL (mediante Render o Supabase), ajustando únicamente la cadena de conexión en las variables de entorno sin modificar la lógica interna.
