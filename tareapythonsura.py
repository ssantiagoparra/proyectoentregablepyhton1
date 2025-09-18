# --- Configuración MySQL ---
# PARTE DE PARRA
import mysql.connector

class DBManager:
    def __init__(self, host='localhost', user='root', password='', database='biblioteca_sura'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conn = None
        self.cursor = None

    def conectar(self):
        self.conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.conn.cursor()

    def crear_bd_si_no_existe(self):
        temp_conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password
        )
        temp_cursor = temp_conn.cursor()
        temp_cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
        temp_conn.close()

    def crear_tablas(self):
        self.conectar() 
        #--------------------------------------------------
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS usuario (
            id INT PRIMARY KEY AUTO_INCREMENT,
            nombre VARCHAR(100),
            telefono VARCHAR(20),
            email VARCHAR(100)
        )''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS libro (
            id INT PRIMARY KEY AUTO_INCREMENT,
            titulo VARCHAR(100),
            autor VARCHAR(100),
            genero VARCHAR(50),
            disponible BOOLEAN
        )''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS revista (
            id INT PRIMARY KEY AUTO_INCREMENT,
            titulo VARCHAR(100),
            editorial VARCHAR(100),
            categoria VARCHAR(50),
            disponible BOOLEAN
        )''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS dispositivo (
            id INT PRIMARY KEY AUTO_INCREMENT,
            tipo VARCHAR(50),
            marca VARCHAR(50),
            modelo VARCHAR(50),
            disponible BOOLEAN
        )''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS prestamo (
            id INT PRIMARY KEY AUTO_INCREMENT,
            id_usuario INT,
            tipo_objeto VARCHAR(20),
            id_objeto INT,
            tipo_prestamo VARCHAR(20),
            fecha_prestamo VARCHAR(20),
            activo BOOLEAN
        )''')
        self.conn.commit()
        #-----------------------------------------------------------
    def cerrar(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
from datetime import datetime
import re
import csv

# Clase Usuario
class Usuario:
    def __init__(self, id_usuario, nombre, telefono, email):
        self.id = id_usuario
        self.nombre = nombre
        self.telefono = telefono
        self.email = email

    def __str__(self):
        return f"ID: {self.id} | Nombre: {self.nombre} | Tel: {self.telefono} | Email: {self.email}"

    @staticmethod
    def validar_email(email):
        return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email)

    @staticmethod
    def validar_telefono(telefono):
        # Permite números de 7 a 15 dígitos, opcionalmente con +
        return re.match(r"^\+?\d{7,15}$", telefono)

    @staticmethod
    def validar_nombre(nombre):
        # Permite letras, espacios y tildes, mínimo 2 caracteres
        return re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ ]{2,}$", nombre)
    #-----------------------------------------------------------------
# Clase Libro
class Libro:
    def __init__(self, id_libro, titulo, autor, genero):
        self.id = id_libro
        self.titulo = titulo
        self.autor = autor
        self.genero = genero
        self.disponible = True

    def __str__(self):
        estado = "Disponible" if self.disponible else "Prestado"
        return f"ID: {self.id} | Título: {self.titulo} | Autor: {self.autor} | Estado: {estado}"

# Clase Revista
class Revista:
    def __init__(self, id_revista, titulo, editorial, categoria):
        self.id = id_revista
        self.titulo = titulo
        self.editorial = editorial
        self.categoria = categoria
        self.disponible = True

    def __str__(self):
        estado = "Disponible" if self.disponible else "Prestado"
        return f"ID: {self.id} | Título: {self.titulo} | Editorial: {self.editorial} | Estado: {estado}"

# Clase Dispositivo
class Dispositivo:
    def __init__(self, id_disp, tipo, marca, modelo):
        self.id = id_disp
        self.tipo = tipo
        self.marca = marca
        self.modelo = modelo
        self.disponible = True
#----------------------------------------------------------------------------
def __str__(self):
        estado = "Disponible" if self.disponible else "Prestado"
        return f"ID: {self.id} | Tipo: {self.tipo} | Marca: {self.marca} | Modelo: {self.modelo} | Estado: {estado}"
 
# Clase Prestamo
class Prestamo:
    def __init__(self, id_prestamo, id_usuario, tipo_objeto, id_objeto, tipo_prestamo):
        self.id = id_prestamo
        self.id_usuario = id_usuario
        self.tipo_objeto = tipo_objeto # libro, revista, dispositivo
        self.id_objeto = id_objeto
        self.tipo_prestamo = tipo_prestamo # corto, largo, institucional, etc.
        self.fecha_prestamo = datetime.now().strftime("%d/%m/%Y")
        self.activo = True
 
    def __str__(self):
        estado = "Activo" if self.activo else "Devuelto"
        return f"ID: {self.id} | Usuario: {self.id_usuario} | Objeto: {self.tipo_objeto}-{self.id_objeto} | Tipo: {self.tipo_prestamo} | Fecha: {self.fecha_prestamo} | Estado: {estado}"
 
# Clase Biblioteca
class Biblioteca:
    def __init__(self):
        self.usuarios = []
        self.libros = []
        self.revistas = []
        self.dispositivos = []
        self.prestamos = []
        self.id_usuario = 1
        self.id_libro = 1
        self.id_revista = 1
        self.id_disp = 1
        self.id_prestamo = 1
          # Métodos CRUD para Usuario
    def crear_usuario(self, nombre, telefono, email):
        if not Usuario.validar_nombre(nombre):
            print("Nombre inválido. Solo letras y espacios, mínimo 2 caracteres.")
            return None
        if not Usuario.validar_telefono(telefono):
            print("Teléfono inválido. Debe ser numérico, entre 7 y 15 dígitos.")
            return None
        if not Usuario.validar_email(email):
            print("Email inválido.")
            return None
        db = DBManager()
        db.conectar()
        db.cursor.execute("INSERT INTO usuario (nombre, telefono, email) VALUES (%s, %s, %s)", (nombre, telefono, email))
        db.conn.commit()
        db.cerrar()
        print("Usuario registrado correctamente en la base de datos.")
        return True
 
    def consultar_usuario(self, id_usuario):
        db = DBManager()
        db.conectar()
        db.cursor.execute("SELECT * FROM usuario WHERE id=%s", (id_usuario,))
        usuario = db.cursor.fetchone()
        db.cerrar()
        return usuario
 
    def actualizar_usuario(self, id_usuario, nombre=None, telefono=None, email=None):
        usuario = self.consultar_usuario(id_usuario)
        if usuario:
            if nombre:
                usuario.nombre = nombre
            if telefono:
                usuario.telefono = telefono
            if email and Usuario.validar_email(email):
                usuario.email = email
            return usuario
        return None
def borrar_usuario(self, id_usuario):
        self.usuarios = [u for u in self.usuarios if u.id != id_usuario]
 
    # Métodos CRUD para Libro
    def crear_libro(self, titulo, autor, genero):
        if not titulo or len(titulo) < 2:
            print("Título inválido. Debe tener al menos 2 caracteres.")
            return None
        if not autor or not Usuario.validar_nombre(autor):
            print("Autor inválido. Solo letras y espacios.")
            return None
        if not genero or len(genero) < 2:
            print("Género inválido. Debe tener al menos 2 caracteres.")
            return None
        db = DBManager()
        db.conectar()
        db.cursor.execute("INSERT INTO libro (titulo, autor, genero, disponible) VALUES (%s, %s, %s, %s)", (titulo, autor, genero, True))
        db.conn.commit()
        db.cerrar()
        print("Libro registrado correctamente en la base de datos.")
        return True
 
    def consultar_libro(self, id_libro):
        db = DBManager()
        db.conectar()
        db.cursor.execute("SELECT * FROM libro WHERE id=%s", (id_libro,))
        libro = db.cursor.fetchone()
        db.cerrar()
        return libro
 def actualizar_libro(self, id_libro, titulo=None, autor=None, genero=None):
        libro = self.consultar_libro(id_libro)
        if libro:
            if titulo:
                libro.titulo = titulo
            if autor:
                libro.autor = autor
            if genero:
                libro.genero = genero
            return libro
        return None
 
    def borrar_libro(self, id_libro):
        self.libros = [l for l in self.libros if l.id != id_libro]
 
    # Métodos CRUD para Revista
    def crear_revista(self, titulo, editorial, categoria):
        if not titulo or len(titulo) < 2:
            print("Título inválido. Debe tener al menos 2 caracteres.")
            return None
        if not editorial or not Usuario.validar_nombre(editorial):
            print("Editorial inválida. Solo letras y espacios.")
            return None
        if not categoria or len(categoria) < 2:
            print("Categoría inválida. Debe tener al menos 2 caracteres.")
            return None
        db = DBManager()
        db.conectar()
        db.cursor.execute("INSERT INTO revista (titulo, editorial, categoria, disponible) VALUES (%s, %s, %s, %s)", (titulo, editorial, categoria, True))
        db.conn.commit()
        db.cerrar()
#PARTE MATIAS
        print("Revista registrada correctamente en la base de datos.")
        return True
 
    def consultar_revista(self, id_revista):
        db = DBManager()
        db.conectar()
        db.cursor.execute("SELECT * FROM revista WHERE id=%s", (id_revista,))
        revista = db.cursor.fetchone()
        db.cerrar()
        return revista
 
    def actualizar_revista(self, id_revista, titulo=None, editorial=None, categoria=None):
        revista = self.consultar_revista(id_revista)
        if revista:
            if titulo:
                revista.titulo = titulo
            if editorial:
                revista.editorial = editorial
            if categoria:
                revista.categoria = categoria
            return revista
        return None
 
    def borrar_revista(self, id_revista):
        self.revistas = [r for r in self.revistas if r.id != id_revista]
 

 #-----------------------------------------------------------
    # Métodos CRUD para Dispositivo
    def crear_dispositivo(self, tipo, marca, modelo):
        if not tipo or len(tipo) < 2:
            print("Tipo inválido. Debe tener al menos 2 caracteres.")
            return None
        if not marca or not Usuario.validar_nombre(marca):
            print("Marca inválida. Solo letras y espacios.")
            return None
        if not modelo or len(modelo) < 2:
            print("Modelo inválido. Debe tener al menos 2 caracteres.")
            return None
        db = DBManager()
        db.conectar()
        db.cursor.execute("INSERT INTO dispositivo (tipo, marca, modelo, disponible) VALUES (%s, %s, %s, %s)", (tipo, marca, modelo, True))
        db.conn.commit()
        db.cerrar()
        print("Dispositivo registrado correctamente en la base de datos.")
        return True
 
    def consultar_dispositivo(self, id_disp):
        db = DBManager()
        db.conectar()
        db.cursor.execute("SELECT * FROM dispositivo WHERE id=%s", (id_disp,))
        disp = db.cursor.fetchone()
        db.cerrar()
        return disp
 
    def actualizar_dispositivo(self, id_disp, tipo=None, marca=None, modelo=None):
        disp = self.consultar_dispositivo(id_disp)
        if disp:
            if tipo:
                disp.tipo = tipo
            if marca:
                disp.marca = marca
            if modelo:
                disp.modelo = modelo
            return disp
        return None
        def borrar_dispositivo(self, id_disp):
        self.dispositivos = [d for d in self.dispositivos if d.id != id_disp]
 
    # Métodos CRUD para Prestamo
    def crear_prestamo(self, id_usuario, tipo_objeto, id_objeto, tipo_prestamo):
        db = DBManager()
        db.conectar()
        db.cursor.execute("INSERT INTO prestamo (id_usuario, tipo_objeto, id_objeto, tipo_prestamo, fecha_prestamo, activo) VALUES (%s, %s, %s, %s, %s, %s)", (id_usuario, tipo_objeto, id_objeto, tipo_prestamo, datetime.now().strftime("%d/%m/%Y"), True))
        # Marcar objeto como no disponible si es libro, revista o dispositivo
        if tipo_objeto == 'libro':
            db.cursor.execute("UPDATE libro SET disponible=0 WHERE id=%s", (id_objeto,))
        elif tipo_objeto == 'revista':
            db.cursor.execute("UPDATE revista SET disponible=0 WHERE id=%s", (id_objeto,))
        elif tipo_objeto == 'dispositivo':
            db.cursor.execute("UPDATE dispositivo SET disponible=0 WHERE id=%s", (id_objeto,))
        db.conn.commit()
        db.cerrar()
        print("Préstamo registrado correctamente en la base de datos.")
        return True
 
    def consultar_prestamo(self, id_prestamo):
        db = DBManager()
        db.conectar()
        db.cursor.execute("SELECT * FROM prestamo WHERE id=%s", (id_prestamo,))
        prestamo = db.cursor.fetchone()
        db.cerrar()
        return prestamo
 
    def actualizar_prestamo(self, id_prestamo, tipo_prestamo=None, activo=None):
        prestamo = self.consultar_prestamo(id_prestamo)
        if prestamo:
            if tipo_prestamo:
                prestamo.tipo_prestamo = tipo_prestamo
            if activo is not None:
                prestamo.activo = activo
            return prestamo
        return None
         def borrar_prestamo(self, id_prestamo):
        self.prestamos = [p for p in self.prestamos if p.id != id_prestamo]
 
    def mostrar_menu(self):
        print("\n=== BIBLIOTECA ===")
        print("1. Registrar usuario")
        print("2. Registrar libro")
        print("3. Registrar revista")
        print("4. Registrar dispositivo")
        print("5. Ver usuarios")
        print("6. Ver libros")
        print("7. Ver revistas")
        print("8. Ver dispositivos")
        print("9. Crear préstamo de libro")
        print("10. Crear préstamo de revista")
        print("11. Crear préstamo de dispositivo")
        print("12. Devolver libro")
        print("13. Devolver revista")
        print("14. Devolver dispositivo")
        print("15. Ver préstamos")
        print("16. Exportar préstamos a CSV")
        print("17. Salir")
        opcion = input("Opción: ")
        return opcion
 
    def ejecutar(self):
        while True:
            opcion = self.mostrar_menu()
            if opcion == '1':
                nombre = input("Nombre: ")
                telefono = input("Teléfono: ")
                email = input("Email: ")
                self.crear_usuario(nombre, telefono, email)

           #PARTE JOANOTTI
            elif opcion == '2':
                titulo = input("Título: ")
                autor = input("Autor: ")
                genero = input("Género: ")
                self.crear_libro(titulo, autor, genero)
            elif opcion == '3':
                titulo = input("Título: ")
                editorial = input("Editorial: ")
                categoria = input("Categoría: ")
                self.crear_revista(titulo, editorial, categoria)
            elif opcion == '4':
                tipo = input("Tipo: ")
                marca = input("Marca: ")
                modelo = input("Modelo: ")
                self.crear_dispositivo(tipo, marca, modelo)
            elif opcion == '5':
                self.ver_usuarios()
            elif opcion == '6':
                self.ver_libros()
            elif opcion == '7':
                self.ver_revistas()
            elif opcion == '8':
                self.ver_dispositivos()
            elif opcion == '9':
                self.crear_prestamo_objeto('libro')
            elif opcion == '10':
                self.crear_prestamo_objeto('revista')
            elif opcion == '11':
                self.crear_prestamo_objeto('dispositivo')
            elif opcion == '12':
                self.devolver_objeto('libro')
            elif opcion == '13':
                self.devolver_objeto('revista')
            elif opcion == '14':
                self.devolver_objeto('dispositivo')
            elif opcion == '15':
                self.ver_prestamos()
            elif opcion == '16':
                self.exportar_prestamos_csv()
            elif opcion == '17':
                print("¡Adiós!")
                break
            else:
                print("Opción inválida")
            input("\nPresiona Enter para continuar...")

def crear_prestamo_objeto(self, tipo_objeto):
        db = DBManager()
        db.conectar()
        db.cursor.execute("SELECT * FROM usuario")
        usuarios = db.cursor.fetchall()
        if not usuarios:
            print("No hay usuarios registrados")
            db.cerrar()
            return
        db.cursor.execute(f"SELECT * FROM {tipo_objeto} WHERE disponible=1")
        objetos_disponibles = db.cursor.fetchall()
        if not objetos_disponibles:
            print(f"No hay {tipo_objeto}s disponibles")
            db.cerrar()
            return
        print("Usuarios:")
        for u in usuarios:
            print(f"{u[0]}. {u[1]}")
        id_usuario = int(input("ID del usuario: "))
        usuario = next((u for u in usuarios if u[0] == id_usuario), None)
        if not usuario:
            print("Usuario no encontrado")
            db.cerrar()
            return
        print(f"{tipo_objeto.capitalize()}s disponibles:")
        for o in objetos_disponibles:
            nombre = o[1] if tipo_objeto != 'dispositivo' else o[3]
            print(f"{o[0]}. {nombre}")
        id_objeto = int(input(f"ID del {tipo_objeto}: "))
        objeto = next((o for o in objetos_disponibles if o[0] == id_objeto), None)
        if not objeto:
            print(f"{tipo_objeto.capitalize()} no encontrado")
            db.cerrar()
            return
        db.cursor.execute("INSERT INTO prestamo (id_usuario, tipo_objeto, id_objeto, tipo_prestamo, fecha_prestamo, activo) VALUES (%s, %s, %s, %s, %s, %s)", (id_usuario, tipo_objeto, id_objeto, 'corto', datetime.now().strftime("%d/%m/%Y"), True))
        db.cursor.execute(f"UPDATE {tipo_objeto} SET disponible=0 WHERE id=%s", (id_objeto,))
        db.conn.commit()
        print(f"Préstamo de {tipo_objeto} creado correctamente en la base de datos.")
        db.cerrar()

def devolver_objeto(self, tipo_objeto):
        db = DBManager()
        db.conectar()
        db.cursor.execute(f"SELECT * FROM prestamo WHERE activo=1 AND tipo_objeto=%s", (tipo_objeto,))
        prestamos_activos = db.cursor.fetchall()
        if not prestamos_activos:
            print(f"No hay préstamos activos de {tipo_objeto}")
            db.cerrar()
            return
        print(f"Préstamos activos de {tipo_objeto}:")
        for p in prestamos_activos:
            db.cursor.execute("SELECT nombre FROM usuario WHERE id=%s", (p[1],))
            usuario = db.cursor.fetchone()
            nombre_objeto = None
            if tipo_objeto == 'libro':
                db.cursor.execute("SELECT titulo FROM libro WHERE id=%s", (p[3],))
                nombre_objeto = db.cursor.fetchone()
            elif tipo_objeto == 'revista':
                db.cursor.execute("SELECT titulo FROM revista WHERE id=%s", (p[3],))
                nombre_objeto = db.cursor.fetchone()
            elif tipo_objeto == 'dispositivo':
                db.cursor.execute("SELECT modelo FROM dispositivo WHERE id=%s", (p[3],))
                nombre_objeto = db.cursor.fetchone()
            if nombre_objeto and usuario:
                print(f"{p[0]}. {nombre_objeto[0]} - {usuario[0]}")
        id_prestamo = int(input("ID del préstamo: "))
        prestamo = next((p for p in prestamos_activos if p[0] == id_prestamo), None)
        if not prestamo:
            print("Préstamo no encontrado")
            db.cerrar()
            return
        db.cursor.execute("UPDATE prestamo SET activo=0 WHERE id=%s", (id_prestamo,))
        db.cursor.execute(f"UPDATE {tipo_objeto} SET disponible=1 WHERE id=%s", (prestamo[3],))
        db.conn.commit()
        print(f"{tipo_objeto.capitalize()} devuelto exitosamente")
        db.cerrar()






