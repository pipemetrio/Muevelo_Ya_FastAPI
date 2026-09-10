# Retrospectiva Personal de Aprendizaje: Desarrollo y Despliegue de la API MuéveloYa

**Autor:** Andrés Felipe Vargas Metrio  
**Institución:** Servicio Nacional de Aprendizaje (SENA)  
**Centro de Formación:** Centro de Tecnología de la Manufactura Avanzada (CTMA)  
**Programa:** Análisis y Desarrollo de Software (ADSO)  
**Ficha:** 3169892  
**Instructor: *Mateo Arroyave* 
**Fecha:** 10 de septiembre de 2026  

---

## Resumen

El presente documento expone una introspección detallada sobre el recorrido formativo desarrollado durante las siete guías de aprendizaje aplicadas al backend del proyecto *MuéveloYa*. A través de un análisis honesto, se contrasta el nivel conceptual inicial con las competencias técnicas adquiridas al dominar la arquitectura de APIs REST con FastAPI, el manejo de bases de datos relacionales y el despliegue en la nube. Asimismo, se expone el mayor desafío técnico experimentado respecto al control de acceso y protocolos HTTP, las decisiones de arquitectura que reestructuraría en una nueva iteración del sistema, y la hoja de ruta establecida para abordar la inyección de dependencias, la separación de capas de datos y la adopción de contenedores en mi perfil profesional.

*Palabras clave:* Retrospectiva, FastAPI, SQLite, Nube, PaaS, SENA, Backend.

---

## 1. De Dónde Partí y Dónde Estoy Hoy: Evolución Técnica

Al dar inicio a la primera guía de aprendizaje de este ciclo, mi comprensión del desarrollo de software estaba fuertemente sesgada hacia la lógica de programación local y el maquetado de interfaces. Entendía la sintaxis fundamental de Python, sabía escribir funciones, manejar variables y ejecutar algunas consultas básicas en bases de datos relacionales. Sin embargo, conceptos fundamentales de la web como la diferencia entre una simple URL y un Endpoint, el ciclo de vida de una petición HTTP o la arquitectura cliente-servidor eran áreas puramente teóricas que no sabía cómo conectar en la práctica.

A lo largo del trabajo aplicado en las siete guías para la construcción de la API del proyecto *MuéveloYa*, mi aprendizaje evolucionó desde la ejecución de scripts sencillos hacia la arquitectura de un backend estructurado y listo para producción. Durante este proceso, adquirí y consolidé las siguientes competencias técnicas clave:

* **Arquitectura Web y FastAPI:** Comprendí que una *Ruta* es la dirección URL que identifica un recurso (como `/usuarios`), mientras que un *Endpoint* es el punto de comunicación exacto que combina esa ruta con un método HTTP específico (como `GET /usuarios` o `POST /usuarios`). Asimismo, aprendí a utilizar **Uvicorn** como servidor ASGI asíncrono para ejecutar la aplicación y a modularizar el código dividiendo las rutas en archivos independientes mediante **APIRouter**.
* **Validación de Datos con Pydantic:** Adopté el uso de esquemas derivados de `BaseModel` para definir la estructura estricta, el parseo y la validación de los datos que ingresan y salen de la API, garantizando que el servidor rechace datos mal estructurados automáticamente.
* **Manejo Estándar de Códigos de Estado HTTP:** Dejé de responder con mensajes informales y pasé a implementar códigos de estado exactos según la semántica web: `200 OK` para consultas o actualizaciones exitosas, `201 Created` para la creación de registros, `204 No Content` para eliminaciones, `400 Bad Request` para peticiones mal formuladas, `401 Unauthorized` por falta de autenticación, `403 Forbidden` cuando el usuario autenticado no posee los permisos de rol suficientes, y `404 Not Found` ante recursos inexistentes.
* **Persistencia Relacional y SQL:** Diseñé y conecté una base de datos relacional en **SQLite** contenida en un archivo físico `.db`. Aprendí a ejecutar operaciones CRUD mediante sentencias `INSERT INTO`, `SELECT`, `UPDATE` y `DELETE`, además de estructurar consultas con `LEFT JOIN` para combinar tablas basándome en llaves foráneas (`FOREIGN KEY`) sin perder registros de la tabla principal.
* **Computación en la Nube e Infraestructura:** Entendí el modelo de la nube como la disponibilidad bajo demanda de recursos informáticos mediante pago por uso. Identifiqué la diferencia entre modelos de servicio como **IaaS** (donde se administra el sistema operativo en hardware virtualizado), **PaaS** (plataforma donde el proveedor gestiona el entorno y el desarrollador solo despliega su código, tal como hicimos en Render), y **SaaS** (software listo para el usuario final). De igual forma, comprendí la distinción entre modelos de despliegue en nube pública, privada e híbrida.

Hoy no solo puedo escribir el código de una API, sino que entiendo todo el flujo: desde que la petición sale del cliente, pasa por el servidor ASGI, valida los datos con Pydantic, consulta la base de datos SQLite y retorna una respuesta HTTP adecuada desde un entorno desplegado en la nube.

---

## 2. El Concepto Más Complejo y Cómo Conseguí Resolverlo

El concepto que demandó el mayor esfuerzo de análisis, lectura y pruebas fallidas fue la **combinación entre la autenticación basada en Tokens JWT, el control de acceso basado en roles y su traducción a los códigos de error HTTP 401 y 403**.

Al comienzo del módulo, me resultaba muy difícil diferenciar operativamente cuándo una petición debía ser rechazada con un código `401 Unauthorized` y cuándo con un `403 Forbidden`. Se me complicaba entender cómo el servidor tomaba el token enviado en la cabecera de la petición, verificaba su firma y expiración, y luego evaluaba si el rol del usuario (por ejemplo, *Cliente* o *Transportista*) tenía la jerarquía necesaria para acceder a un endpoint reservado para un *Administrador*.

Para superar este obstáculo conceptual y práctico, implementé una metodología de estudio basada en la experimentación directa:

1. **Pruebas Aisladas en Swagger UI (`/docs`):** Utilicé la documentación interactiva generada por FastAPI para monitorear las respuestas en tiempo real. Ejecuté peticiones intencionales sin incluir el token para observar la respuesta `401 Unauthorized`, y posteriormente envié peticiones con tokens de usuarios normales hacia rutas administrativas para confirmar la respuesta `403 Forbidden`.
2. **Mapeo de Rutas y Métodos:** Creé un cuadro comparativo donde asocié cada Endpoint con su respectivo nivel de acceso y el código HTTP esperado ante un fallo. Esto me ayudó a visualizar la lógica de seguridad antes de escribir las funciones de validación.
3. **Depuración mediante Bitácora y Logs:** Al revisar la consola del servidor Uvicorn ante cada fallo de prueba, pude rastrear los errores de desencriptación de tokens y corregir la lectura de variables de entorno críticas como la `SECRET_KEY`.

Comprender esta diferencia me permitió asegurar la API de *MuéveloYa* de forma profesional, garantizando que cada endpoint responda exactamente según los estándares de la industria.

---

## 3. ¿Qué Haría Distinto si Empezara el Proyecto de Nuevo?

Realizando una autoevaluación honesta sobre el desarrollo de las siete guías, existen dos decisiones técnicas de diseño y metodología que reestructuraría radicalmente si iniciara el proyecto desde cero:

En primer lugar, **separaría la capa de acceso a datos de las funciones de los endpoints desde la primera guía**. Al inicio del proyecto, escribí consultas SQL manuales e interacciones con SQLite directamente dentro de las funciones de las rutas en los archivos de `APIRouter`. Aunque esto funcionó para entender el flujo inicial, con el crecimiento del proyecto provocó un acoplamiento innecesario entre la lógica HTTP y la persistencia de datos, haciendo que el código fuera más denso y difícil de leer. Si empezara de nuevo, implementaría un patrón donde la base de datos se gestione en un módulo independiente.

En segundo lugar, **diseñaría una arquitectura basada en un ORM desde el comienzo en lugar de ejecutar sentencias SQL en texto plano**. Si bien trabajar con comandos `INSERT`, `SELECT`, `UPDATE` y `DELETE` directamente fortaleció mis bases en bases de datos relacionales, también introdujo riesgo de errores sintácticos y limitó la portabilidad del sistema. Utilizar un ORM desde el primer día habría simplificado la creación de modelos de datos y facilitado la migración de la base de datos hacia un entorno de producción más robusto.

---

## 4. Próximo Paso Concreto en mi Formación

Como estudiante que cursa el 6.° trimestre del programa ADSO y se prepara para asumir retos en el entorno laboral, reconozco que la finalización del despliegue en Render es la base sobre la cual debo construir un perfil backend más avanzado. Mi siguiente paso concreto de formación está enfocado en tres pilares técnicos interconectados: **la inyección de dependencias con `Depends` en FastAPI, la migración a un ORM como SQLAlchemy y el empaquetamiento de la aplicación utilizando contenedores con Docker**.

Actualmente, el proyecto *MuéveloYa* funciona bajo un modelo PaaS en Render utilizando un archivo físico de SQLite. No obstante, para escalar a un nivel profesional, mi hoja de ruta inmediata contempla:

* **Implementar `Depends` de FastAPI:** Utilizar el sistema de inyección de dependencias para gestionar la apertura, entrega y cierre automático de las conexiones a la base de datos en cada petición HTTP, reduciendo la duplicación de código en las rutas.
* **Migrar la Persistencia a SQLAlchemy:** Sustituir las ejecuciones directas de cadenas SQL por modelos relacionales definidos como clases de Python. Esto me permitirá mapear los datos de forma orientada a objetos y habilitará la posibilidad de conectar el sistema a motores más potentes como PostgreSQL.
* **Contenedorización con Docker:** Empaquetar la aplicación FastAPI junto con sus dependencias y variables de entorno dentro de un contenedor. Esto garantizará la portabilidad total del sistema, eliminando el problema de "funciona en mi máquina pero no en el servidor" y preparando el proyecto para despliegues en infraestructuras IaaS o plataformas orquestadas.

Con la ruta trazada a través de estas siete guías y las bases adquiridas en el SENA, asumo el compromiso de aplicar estos conceptos avanzados en mis próximos desarrollos para responder con solvencia a las exigencias del mercado tecnológico.

---

## Referencias

* Ramírez, A. (2024). *Desarrollo de APIs RESTful con Python y FastAPI*. Editorial TEK.
* Servicio Nacional de Aprendizaje (SENA). (2026). *Guías de Aprendizaje GA7: Implementación y Despliegue de Servicios Web*. Centro de Tecnología de la Manufactura Avanzada (CTMA).
* Tiangolo, S. (2025). *FastAPI Documentation: Big Applications - Multiple Files, APIRouter and Dependencies*. https://fastapi.tiangolo.com/tutorial/bigger-applications/git 