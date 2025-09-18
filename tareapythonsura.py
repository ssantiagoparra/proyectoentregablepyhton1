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








