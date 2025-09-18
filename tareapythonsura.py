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