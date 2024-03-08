import cx_Oracle
import requests
import base64

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

def test_request():
    # Configuración de la petición basada en tu información
    url = "https://hcoa-test.fa.us2.oraclecloud.com:443/xmlpserver/services/rest/v1"
    credentials = "mcastrofox:Feb.2023"
    encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/vnd.oracle.adf.resourceitem+json",
        "REST-Framework-Version": "4",
    }
    # Intento de petición
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print("Petición exitosa!")
            # Aquí puedes agregar más código para procesar la respuesta si lo deseas
        else:
            response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Error al realizar la petición:", e)


if __name__ == "__main__":
    test_db_connection()
    #test_request()
    #test_webservice_calculator()
