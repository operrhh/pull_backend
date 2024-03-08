from zeep import Client, Transport
from requests import Session
from requests.auth import HTTPBasicAuth
import pandas as pd
import io

# URL del archivo WSDL
wsdl_url = 'https://hcoa-test.fa.us2.oraclecloud.com:443/xmlpserver/services/ExternalReportWSSService?WSDL'

payload = {
    'reportRequest': {
        'attributeFormat': 'xlsx',
        'parameterNameValues': {
            'item': [
                {
                    'multiValuesAllowed': '?',
                    'name': 'Empresa',
                    'refreshParamOnChange': '?',
                    'selectAll': '?',
                    'templateParam': '?',
                    'useNullForAll': '?',
                    'values': {
                        'item': [
                            '00 - Compañía Cervecerías Unidas S.A.',
                            # '11 - Compañía Industrial Cervecera S.A.',
                            # '16 - Saenz Briones y CIA S.A.I.C.',
                            # '22- Bebidas Bolivianas BBO S.A.'
                        ]
                    }
                }
            ]
        },
        'reportAbsolutePath': '/~MCASTROFOX/IntegraSoftTest/Informacion Empleados.xdo',
        'sizeOfDataChunkDownload': -1,
        'byPassCache': False,
        'flattenXML': False,
    },
    'appParams': '?'
}

def run_report_final():
    try:
        # Crea un cliente SOAP dentro de un administrador de contexto
        with Session() as session:
            session.auth = HTTPBasicAuth('mcastrofox', 'Feb.2023')
            transport = Transport(session=session)
            with Client(wsdl=wsdl_url, transport=transport) as client:
                service = client.bind('ExternalReportWSSService', 'ExternalReportWSSService')
                result = service.runReport(reportRequest=payload['reportRequest'], appParams=payload['appParams'])
                
                # Leer el archivo Excel directamente desde los datos binarios
                df = pd.read_excel(io.BytesIO(result["reportBytes"]), header=1)

                # Mostrar los datos utilizando Pandas
                print(df[['Id Empleado', 'Nombre Empleado','E-mail Empleado','Puesto','Unidad de Negocio']])

                # workers = [{
                #     'id': row['Id Empleado'],
                #     'name': row['Nombre Empleado'],
                #     'email': row['E-mail Empleado'],
                #     'position': row['Puesto'],
                #     'business_unit': row['Unidad de Negocio']
                # } for index, row in df.iterrows()]
                
                # print(workers)

    except Exception as e:
        print("Error al crear el cliente:", e)    

if __name__ == "__main__":
    #test_webservice()
    # test_webservice_calculator()
    run_report_final()
    
    