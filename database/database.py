import sqlite3

DB_NAME = "mueveloYa.db"


def obtener_conexion():
    conexion = sqlite3.connect(DB_NAME, check_same_thread=False)
    conexion.row_factory = sqlite3.Row
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion


def crear_tablas():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Usuario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono TEXT NOT NULL,
            correo TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            rol TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Transportista (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            documento TEXT NOT NULL UNIQUE,
            telefono TEXT NOT NULL,
            activo INTEGER NOT NULL DEFAULT 1
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Vehiculo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            placa TEXT NOT NULL UNIQUE,
            tipo TEXT NOT NULL,
            capacidad_kg REAL NOT NULL,
            disponible INTEGER NOT NULL DEFAULT 1
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Direccion (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            alias TEXT NOT NULL,
            ciudad TEXT NOT NULL,
            barrio TEXT NOT NULL,
            direccion TEXT NOT NULL,
            usuario_id INTEGER NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuario(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Servicio (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            estado TEXT NOT NULL,
            descripcion TEXT,
            usuario_id INTEGER NOT NULL,
            direccion_origen_id INTEGER NOT NULL,
            direccion_destino_id INTEGER NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuario(id),
            FOREIGN KEY (direccion_origen_id) REFERENCES Direccion(id),
            FOREIGN KEY (direccion_destino_id) REFERENCES Direccion(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ObjetoTransporte (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            peso REAL NOT NULL,
            fragil INTEGER NOT NULL DEFAULT 0,
            servicio_id INTEGER NOT NULL,
            FOREIGN KEY (servicio_id) REFERENCES Servicio(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Asignacion (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha_asignacion TEXT NOT NULL,
            servicio_id INTEGER NOT NULL,
            transportista_id INTEGER NOT NULL,
            vehiculo_id INTEGER NOT NULL,
            FOREIGN KEY (servicio_id) REFERENCES Servicio(id),
            FOREIGN KEY (transportista_id) REFERENCES Transportista(id),
            FOREIGN KEY (vehiculo_id) REFERENCES Vehiculo(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Pago (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            valor REAL NOT NULL,
            metodo TEXT NOT NULL,
            pagado INTEGER NOT NULL DEFAULT 0,
            fecha_pago TEXT,
            servicio_id INTEGER NOT NULL,
            FOREIGN KEY (servicio_id) REFERENCES Servicio(id)
        )
    """)

    conexion.commit()
    conexion.close()

    print(f"[BD] Tablas verificadas en DB {DB_NAME}")


def sembrar_datos():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("SELECT COUNT(*) FROM Usuario")
    cantidad_usuarios = cursor.fetchone()[0]

    if cantidad_usuarios == 0:
        cursor.execute(
            """
            INSERT INTO Usuario
            (nombre, telefono, correo, password, rol)
            VALUES (?, ?, ?, ?, ?)
        """,
            ("Sergio Lopez", "3001234567", "sergio00@gmail.com", "$2b$12$e0...hash_de_ejemplo...", "admin"),
        )

        cursor.execute(
            """
            INSERT INTO Usuario
            (nombre, telefono, correo, password, rol)
            VALUES (?, ?, ?, ?, ?)
        """,
            ("Joel Buriticá", "3019876543", "joel@gmail.com", "$2b$12$e0...hash_de_ejemplo...", "admin"),
        )

        cursor.execute(
            """
            INSERT INTO Usuario
            (nombre, telefono, correo, password, rol)
            VALUES (?, ?, ?, ?, ?)
        """,
            ("Ousmane Dembele", "3154567890", "dembo@gmail.com", "$2b$12$e0...hash_de_ejemplo...", "cliente"),
        )

    cursor.execute("SELECT COUNT(*) FROM Transportista")
    cantidad_transportistas = cursor.fetchone()[0]

    if cantidad_transportistas == 0:
        cursor.execute(
            """
            INSERT INTO Transportista
            (nombre, documento, telefono, activo)
            VALUES (?, ?, ?, ?)
        """,
            ("Andrés Felipe", "12345678", "3115558899", 1),
        )

        cursor.execute(
            """
            INSERT INTO Transportista
            (nombre, documento, telefono, activo)
            VALUES (?, ?, ?, ?)
        """,
            ("Sergio Lopez", "98765432", "3124447788", 1),
        )

        cursor.execute(
            """
            INSERT INTO Transportista
            (nombre, documento, telefono, activo)
            VALUES (?, ?, ?, ?)
        """,
            ("Lionel Messi", "45678912", "3203332211", 0),
        )

    cursor.execute("SELECT COUNT(*) FROM Vehiculo")
    cantidad_vehiculos = cursor.fetchone()[0]

    if cantidad_vehiculos == 0:
        cursor.execute(
            """
            INSERT INTO Vehiculo
            (placa, tipo, capacidad_kg, disponible)
            VALUES (?, ?, ?, ?)
        """,
            ("ABC123", "Camión 3 toneladas", 3000, 1),
        )

        cursor.execute(
            """
            INSERT INTO Vehiculo
            (placa, tipo, capacidad_kg, disponible)
            VALUES (?, ?, ?, ?)
        """,
            ("XYZ789", "Camioneta", 1000, 1),
        )

        cursor.execute(
            """
            INSERT INTO Vehiculo
            (placa, tipo, capacidad_kg, disponible)
            VALUES (?, ?, ?, ?)
        """,
            ("DEF456", "Camión 5 toneladas", 5000, 0),
        )

    cursor.execute("SELECT COUNT(*) FROM Direccion")
    cantidad_direcciones = cursor.fetchone()[0]

    if cantidad_direcciones == 0:
        cursor.execute(
            """
            INSERT INTO Direccion
            (alias, ciudad, barrio, direccion, usuario_id)
            VALUES (?, ?, ?, ?, ?)
        """,
            ("Casa principal", "Bogotá", "Suba", "Calle 100 # 20-30", 1),
        )

        cursor.execute(
            """
            INSERT INTO Direccion
            (alias, ciudad, barrio, direccion, usuario_id)
            VALUES (?, ?, ?, ?, ?)
        """,
            ("Apartamento nuevo", "Bogotá", "Chapinero", "Carrera 15 # 80-25", 1),
        )

        cursor.execute(
            """
            INSERT INTO Direccion
            (alias, ciudad, barrio, direccion, usuario_id)
            VALUES (?, ?, ?, ?, ?)
        """,
            ("Casa Ana", "Bogotá", "Usaquén", "Carrera 7 # 120-15", 2),
        )

        cursor.execute(
            """
            INSERT INTO Direccion
            (alias, ciudad, barrio, direccion, usuario_id)
            VALUES (?, ?, ?, ?, ?)
        """,
            ("Oficina Ana", "Bogotá", "Centro", "Carrera 10 # 20-40", 2),
        )

    cursor.execute("SELECT COUNT(*) FROM Servicio")
    cantidad_servicios = cursor.fetchone()[0]

    if cantidad_servicios == 0:
        cursor.execute(
            """
            INSERT INTO Servicio
            (
                fecha,
                estado,
                descripcion,
                usuario_id,
                direccion_origen_id,
                direccion_destino_id
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            ("2026-08-15", "pendiente", "Mudanza de apartamento", 1, 1, 2),
        )

        cursor.execute(
            """
            INSERT INTO Servicio
            (
                fecha,
                estado,
                descripcion,
                usuario_id,
                direccion_origen_id,
                direccion_destino_id
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            (
                "2026-08-16",
                "en_ruta",
                "Traslado de muebles y electrodomésticos",
                2,
                3,
                4,
            ),
        )

    cursor.execute("SELECT COUNT(*) FROM ObjetoTransporte")
    cantidad_objetos = cursor.fetchone()[0]

    if cantidad_objetos == 0:
        cursor.execute(
            """
            INSERT INTO ObjetoTransporte
            (nombre, cantidad, peso, fragil, servicio_id)
            VALUES (?, ?, ?, ?, ?)
        """,
            ("Nevera", 1, 85.5, 1, 1),
        )

        cursor.execute(
            """
            INSERT INTO ObjetoTransporte
            (nombre, cantidad, peso, fragil, servicio_id)
            VALUES (?, ?, ?, ?, ?)
        """,
            ("Sofá", 1, 60, 0, 1),
        )

        cursor.execute(
            """
            INSERT INTO ObjetoTransporte
            (nombre, cantidad, peso, fragil, servicio_id)
            VALUES (?, ?, ?, ?, ?)
        """,
            ("Televisor", 1, 15, 1, 2),
        )

        cursor.execute(
            """
            INSERT INTO ObjetoTransporte
            (nombre, cantidad, peso, fragil, servicio_id)
            VALUES (?, ?, ?, ?, ?)
        """,
            ("Cajas", 10, 12.5, 0, 2),
        )

    cursor.execute("SELECT COUNT(*) FROM Asignacion")
    cantidad_asignaciones = cursor.fetchone()[0]

    if cantidad_asignaciones == 0:
        cursor.execute(
            """
            INSERT INTO Asignacion
            (
                fecha_asignacion,
                servicio_id,
                transportista_id,
                vehiculo_id
            )
            VALUES (?, ?, ?, ?)
        """,
            ("2026-08-14", 1, 1, 1),
        )

        cursor.execute(
            """
            INSERT INTO Asignacion
            (
                fecha_asignacion,
                servicio_id,
                transportista_id,
                vehiculo_id
            )
            VALUES (?, ?, ?, ?)
        """,
            ("2026-08-15", 2, 2, 2),
        )

    cursor.execute("SELECT COUNT(*) FROM Pago")
    cantidad_pagos = cursor.fetchone()[0]

    if cantidad_pagos == 0:
        cursor.execute(
            """
            INSERT INTO Pago
            (
                valor,
                metodo,
                pagado,
                fecha_pago,
                servicio_id
            )
            VALUES (?, ?, ?, ?, ?)
        """,
            (250000, "transferencia", 1, "2026-08-15", 1),
        )

        cursor.execute(
            """
            INSERT INTO Pago
            (
                valor,
                metodo,
                pagado,
                fecha_pago,
                servicio_id
            )
            VALUES (?, ?, ?, ?, ?)
        """,
            (180000, "efectivo", 0, None, 2),
        )

    conexion.commit()
    conexion.close()

    print("[BD] Datos iniciales insertados correctamente")


def inicializar_bd():
    crear_tablas()
    sembrar_datos()


if __name__ == "__main__":
    inicializar_bd()
