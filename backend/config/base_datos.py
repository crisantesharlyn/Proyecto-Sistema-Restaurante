"""
Conexión simple a PostgreSQL.
A diferencia del Singleton con pool que usábamos con Flask, aquí cada
función que necesita hablar con la base de datos pide una conexión
nueva con obtener_conexion() y la cierra cuando termina. Es el mismo
patrón que usa el profesor en config/base_datos.py de 'semana-14'.
"""
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()


def obtener_conexion():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "restaurante"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", ""),
        cursor_factory=RealDictCursor,
    )
