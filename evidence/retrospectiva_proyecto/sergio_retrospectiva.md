# Retrospectiva MueveloYa FastAPI Sergio Andrés López Sepúlveda

**1. Lo que sabía antes y lo que sé hacer hoy**

Al comenzar este proceso formativo en las primeras guías, mi conocimiento sobre desarrollo backend era bastante básico: sabía entender por encima cómo funcionaban los endpoints y cómo estructurar una API REST sencilla para probarla en mi computador.

Hoy, tras completar el desarrollo de **MuéveloYa** y recorrer las siete guías, logré avanzar a un nivel mucho más completo y cercano a lo que exige el trabajo real:

- **Seguridad y autenticación:** Aprendí a encriptar contraseñas usando `bcrypt` para no guardarlas en texto plano y a implementar autenticación por tokens JWT para identificar a los usuarios.

- **Control de acceso y roles:** Aprendí a proteger los endpoints para que solo las personas con permisos (como el administrador) puedan ejecutar acciones críticas como borrar o modificar datos, respondiendo con los códigos correctos como 401 y 403.

- **Estructura y documentación de la API:** Aprendí a organizar el código de forma modular dividiendo todo en carpetas para routers (`usuario.py`, `servicio.py`, etc.), esquemas y base de datos, además de generar la documentación interactiva en Swagger (`/docs`).

- **Preparación y despliegue en la nube:** Aprendí a sacar la API de mi computador local, manejar la configuración con variables de entorno para proteger las claves secretas y desplegar el servicio en la plataforma Render para que quede disponible en internet.

---

**2. El concepto que más me costó y cómo lo resolví**

El concepto más difícil de todo el proyecto no fue la inyección de dependencias, sino **todo el tema de la seguridad con JWT y el cifrado de contraseñas** en el archivo `security.py`.

Al principio era muy confuso entender cómo se conectaban todas las piezas: recibir la contraseña, encriptarla, verificarla contra la base de datos `mueveloya.db`, generar la firma del token con un tiempo de expiración y luego pedir y validar ese token en cada petición para dar o denegar el acceso.

Lo resolví **analizando el flujo exacto del código paso a paso**: me puse a seguir el camino que hace el dato desde que el usuario envía sus datos en el endpoint de login, viendo qué función procesa la clave, cómo se arma el token y cómo la API revisa ese token en las rutas protegidas. Al entender esa secuencia lógica dentro del código, el tema me quedó totalmente claro.

---

**3. Qué haría distinto si empezara el proyecto de nuevo**

Si fuera a iniciar **MuéveloYa** desde cero con la experiencia que tengo hoy, cambiaría dos cosas fundamentales en la forma de trabajar:

- **Planear la seguridad antes de programar:** En lugar de crear todos los endpoints y dejar la seguridad para el final, prepararía desde el primer día la protección de los routers y la definición de roles antes de escribir las rutas de negocio.

- **Mayor orden en la arquitectura:** Mantendría una separación mucho más estricta de las cosas para no tener lógica acumulada en una sola ubicación, organizando de forma más limpia la base de datos, las utilidades de seguridad y las rutas para que el código fuera más fácil de mantener.

---

**4. Mi siguiente paso concreto como desarrollador**

Mi siguiente objetivo para seguir creciendo como desarrollador es aprender a fondo la **inyección de dependencias con `Depends` en FastAPI**.

Es un tema que me parece muy interesante porque permite reutilizar código de forma adecuada, manejar las conexiones a la base de datos de manera limpia y validar permisos de usuario sin tener que repetir lógica en cada endpoint. Dominar esto me ayudará a escribir un código backend mucho más profesional y estructurado.
