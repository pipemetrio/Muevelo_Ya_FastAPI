# Actividades de reflexión inicial - Lluvia de ideas

## 1. Situaciones o problemas identificados

Al observar situaciones cotidianas que actualmente pueden manejarse sin un sistema especializado, se identificaron las siguientes necesidades:

1. **Conseguir servicios de transporte de objetos y mudanzas:** muchas personas necesitan transportar objetos, muebles o pertenencias, pero no cuentan con un vehículo adecuado y deben buscar un transportista por conocidos, grupos de mensajería o publicaciones.

2. **Problemas con las nomenclaturas de las casas:** en algunas zonas puede ser complicado identificar correctamente una dirección o explicar cómo llegar a un lugar, especialmente cuando las nomenclaturas no son claras o no se encuentran fácilmente.

3. **Publicidad para un negocio nuevo:** un negocio que acaba de iniciar puede tener dificultades para darse a conocer y encontrar usuarios, especialmente cuando todavía no cuenta con una plataforma propia para mostrar sus servicios.

4. **Organización de pedidos de un negocio de comidas:** un negocio pequeño puede recibir pedidos por diferentes medios, como llamadas o mensajes, haciendo más difícil llevar un control de los pedidos realizados, los datos del usuario y su estado.

5. **Control de préstamos de objetos o materiales:** un grupo, negocio o institución puede llevar el registro de préstamos manualmente, por ejemplo mediante apuntes o archivos separados, lo que puede dificultar saber quién tiene un objeto, cuándo debe devolverlo o si ya fue entregado.

## 2. Problema seleccionado

De las situaciones anteriores se escogió el problema de **conseguir un servicio de transporte de objetos y mudanzas**, ya que es una situación que puede presentarse con frecuencia y que resulta difícil de resolver rápidamente cuando una persona no tiene un vehículo adecuado.

Actualmente, una persona que necesita transportar un objeto puede tener que preguntar a conocidos si conocen algún transportista, buscar en grupos de redes sociales o mensajería, o contactar diferentes servicios hasta encontrar uno disponible. Este proceso puede tomar tiempo y no garantiza que el vehículo encontrado tenga las características necesarias para transportar el objeto.

El problema afecta principalmente a las personas que necesitan mover objetos de un lugar a otro o realizar una mudanza y no cuentan con un vehículo propio. También puede afectar a pequeños transportistas que ofrecen este tipo de servicios, porque pueden tener dificultades para encontrar personas que necesiten sus servicios.

Al no existir un sistema centralizado, se puede complicar la búsqueda de un transportista disponible, conocer qué tipo de vehículo tiene, organizar las direcciones de origen y destino y llevar un seguimiento del servicio solicitado.

Por esta razón se plantea **MueveloYa**, una aplicación orientada a facilitar la conexión entre personas que necesitan transportar objetos y personas que ofrecen servicios de transporte. La propuesta busca reunir la solicitud y gestión de estos servicios en un mismo lugar. Esta idea coincide con la definición inicial del proyecto de facilitar el acceso a servicios de mudanza y transporte de objetos.

## 3. Entidades identificadas

Para que el sistema pueda gestionar este problema, debe almacenar información relacionada con las personas que utilizan el servicio, los vehículos disponibles y las solicitudes de transporte.

Entre las entidades que podrían formar parte del sistema se encuentran:

- **Usuario:** persona que necesita solicitar un servicio de transporte.
- **Transportista:** persona que ofrece el servicio de transporte.
- **Vehículo:** vehículo utilizado para transportar los objetos.
- **Dirección:** lugares relacionados con el servicio, como el origen y el destino.
- **Servicio:** solicitud de transporte realizada por un usuario.
- **ObjetoTransporte:** objetos que deben ser transportados.
- **Asignación:** relación entre un servicio, un transportista y un vehículo.
- **Pago:** información relacionada con el pago de un servicio.

## 4. Actores y permisos

El sistema tendrá diferentes actores de acuerdo con las necesidades del negocio.

**Usuario**

El usuario podrá registrarse y acceder al sistema para solicitar y consultar sus servicios de transporte. También podrá proporcionar la información necesaria para realizar una solicitud, como los lugares de origen y destino y los objetos que necesita transportar.

Sus principales permisos serán:

- Registrarse.
- Consultar sus servicios.
- Crear una solicitud de transporte.
- Modificar la información de sus solicitudes cuando corresponda.
- Consultar el estado de sus servicios.

Estas acciones se permiten porque corresponden directamente a las necesidades de la persona que está solicitando el servicio.

**Transportista**

El transportista será quien ofrezca el servicio de transporte. Podrá consultar las asignaciones que le correspondan y conocer la información necesaria para realizar el servicio.

Sus permisos estarán relacionados con:

- Consultar los servicios que tenga asignados.
- Consultar la información necesaria para realizar un servicio.
- Actualizar el estado de un servicio que esté atendiendo.

Esto permite que el transportista gestione únicamente los servicios que le corresponden.

**Administrador**

El administrador tendrá el mayor nivel de control sobre el sistema. Podrá gestionar la información general y realizar operaciones que no deberían estar disponibles para cualquier usuario.

Entre sus permisos estarán:

- Consultar información general.
- Crear y modificar registros administrativos.
- Gestionar usuarios y servicios.
- Eliminar información cuando sea necesario.

La eliminación se reserva al administrador porque es una operación que puede afectar información importante del sistema y no debería quedar disponible para cualquier usuario.

## 5. Alcance del proyecto

La aplicación se llamará **MueveloYa** y tendrá como objetivo facilitar la búsqueda y gestión de servicios de transporte de objetos y mudanzas.

**Frase de alcance:**

> **«Mi API permite a usuarios y transportistas gestionar solicitudes y servicios de transporte, de modo que puedan facilitar la organización y realización de mudanzas y transporte de objetos.»**

El proyecto tendrá un alcance pequeño para poder terminarlo y probarlo correctamente. La guía establece precisamente que el proyecto debe evitar convertirse en una aplicación demasiado grande y centrarse en un alcance cerrado y terminado.

## Versión 2 — Funciones fuera del alcance inicial

Las siguientes funciones no formarán parte de la primera versión:

- Sistema de pagos reales.
- Suscripciones.
- Chat entre usuarios y transportistas.
- Notificaciones.
- Sistema avanzado de calificaciones y reseñas.
- Seguimiento GPS en tiempo real.
- Integración con mapas.
- Cálculo automático de precios.
- Aplicación móvil.
- Sistema avanzado de promociones y publicidad.
