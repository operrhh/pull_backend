import cx_Oracle

def test_db_connection():
    # Configuración de la conexión basada en tu información
    dsn_str = cx_Oracle.makedsn("localhost", 0000, service_name="service_name")
    user = "user"
    password = "pass"

    # Intento de conexión
    try:
        with cx_Oracle.connect(user, password, dsn_str) as connection:
            print("Conexión exitosa!")
            # Aquí puedes agregar más código para realizar una consulta simple si lo deseas
    except cx_Oracle.DatabaseError as e:
        print("Error al conectarse a la base de datos:", e)

if __name__ == "__main__":
    test_db_connection()