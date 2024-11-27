import mysql.connector
from mysql.connector import Error


def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost", database="dreamteam_db", user="root", password="472215"
        )
        if connection.is_connected():
            print("Conexão com o banco de dados estabelecida.")
            return connection
    except Error as e:
        print(f"Error ao tentar criar conexão com o banco de dados: {e}.")


def close_connection(connection):
    if connection.is_connected():
        connection.close()
        print("Conexão finalizada com o banco de dados.")
