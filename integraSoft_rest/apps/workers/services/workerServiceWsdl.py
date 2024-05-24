from zeep import Client, Transport
from requests import Session
from requests.auth import HTTPBasicAuth
import pandas as pd
import io


class WorkerServiceWsdl:
    def __init__(self):
        # URL del archivo WSDL
        # self.wsdl_url = 'https://hcoa-test.fa.us2.oraclecloud.com:443/xmlpserver/services/ExternalReportWSSService?WSDL'
        self.wsdl_url = 'https://hcoa.fa.us2.oraclecloud.com:443/xmlpserver/services/ExternalReportWSSService?WSDL'

    def get_workers_wsdl(self):
        workers = self.run_report()

        res = {
            'count':len(workers),
            'result': workers
        }

        return res

    def run_report(self):

        nuevos_nombres = {
            'PERSON_NUMBER':'person_number',
            'START_DATE':'start_date',
            'DISPLAY_NAME':'display_name',
            'EMAIL_EMPLID':'email_emplid',
            'JOB_CODE':'job_code',
            'JOB_NAME':'job_name',
            'LEGAL_ENTITY_NAME':'legal_entity_name',
            'HDR_PERSON_LOCATION':'hdr_person_location',
            'HDR_INTERNAL_LOCATION_CODE':'hdr_internal_location_code',
            'HDR_PERSON_DEPARTMENT':'hdr_person_department',
            'ID_JEFE':'id_jefe',
            'NOMBRE_JEFE':'nombre_jefe',
            'EMAIL_MANAGER':'email_manager',
            'SALARY_AMOUNT':'salary_amount',
            'ADDRESS_TYPE':'address_type',
            'ADDRESS_LINE_1':'address_line_1',
            'ADDRESS_LINE_2':'address_line_2',
            'ADDRESS_LINE_3':'address_line_3',
            'ADDRESS_LINE_4':'address_line_4',
            'TOWN_OR_CITY':'town_or_city',
            'FIRST_NAME':'first_name',
            'LAST_NAME':'last_name',
            'MIDDLE_NAMES':'middle_names',
            # 'FLEX_CONTEXT_DEPARTMENT':'flex_context_department',
            'CCU_CODIGO_CENTRO_COSTO':'ccu_codigo_centro_costo',
            # 'CCU_TIPO_CENTRO_COSTO':'ccu_tipo_centro_costo',
        }

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
                                            # 40 50 60 61 63 71 80 81 83 90 96
                                    # '00 - Compañía Cervecerías Unidas S.A.', LISTO
                                    # '07 - La Barra S.A.', LISTO
                                    # '11 - Compañía Industrial Cervecera S.A.', NOOOO
                                    # '16 - Saenz Briones y CIA S.A.I.C.', NOOOO
                                    # '22- Bebidas Bolivianas BBO S.A.', NOOOO
                                    # '23 - Cervecera CCU Chile Ltda.', NOOOO
                                    # '25 - CCU Uruguay S.A.', NOOOO
                                    # '31 - Fábrica de Envases Plásticos S.A.', # LISTO (3 registros NOT FOUND)
                                    # '32 - Transportes CCU Ltda.',
                                    # '35 - Bebidas del Paraguay SA', NOOOO
                                    # '36 - Distribuidora del Paraguay SA', NOOOO
                                    '40 - Financiera CRECCU S.A.',
                                    # '45 - Vitivinícola del Maipo S.A.', NOOOO
                                    # '46 - Viña del Mar de Casablanca S.A.', NOOOO
                                    # '47 - Viña Misiones de Rengo S.A.', NOOOO
                                    # '48 - Viñas Orgánicas VSPT S.A.', NOOOO
                                    # '50 - Viña San Pedro Tarapacá S.A.',
                                    # '51 - Viña Santa Helena S.A.',
                                    # '52 - Finca La Celia S.A.', NOOOO
                                    # '53 - Viña Altair S.A.', NOOOO
                                    # '56 - Viña Valles de Chile S.A.', NOOOO
                                    # '58 - Viña Altair II S.A.', NOOOO
                                    # '59 - Viña Tabalí S.A.', NOOOO
                                    # '60 - Cervecera Austral S.A.',
                                    # '61 - Comercial Patagona Ltda.',
                                    # '63 - Compañía Cervecera Kunstmann S.A.',
                                    # '70 - Pisconor S.A.', NOOOO
                                    # '71 - Compañía Pisquera de Chile S.A.',
                                    # '80 - Aguas CCU-Nestle Chile S.A',
                                    # '81 - Manantial S.A.',
                                    # '83 - Bebidas Ecusa SPA',
                                    # '90 - Embotelladoras Chilenas Unidas S.A.',
                                    # '92 - Transportes ECUSA S.A.', NOOOO
                                    # '93 - Vending y Servicios CCU Ltda.', NOOOO
                                    # '96 - Comercial CCU S.A.',
                                    # '97 - Foods Cia de Alimentos CCU S.A.', NOOOO
                                    # '99 - Promarca S.A.' NOOOO
                                ]
                            }
                        }
                    ]
                },
                # 'reportAbsolutePath': '/~MCASTROFOX/IntegraSoftTest/Informacion Empleados.xdo',
                # 'reportAbsolutePath': '/~OPERRHH@CCU.CL/IntegraSoftTest/Informacion Empleados.xdo',
                'reportAbsolutePath': '/~operrhh@ccu.cl/IntegraSoftTest/Informacion Empleados.xdo',
                    
                'sizeOfDataChunkDownload': -1,
                'byPassCache': False,
                'flattenXML': False,
            },
            'appParams': '?'
        }

        try:
            # Crea un cliente SOAP dentro de un administrador de contexto
            with Session() as session:
                session.auth = HTTPBasicAuth('operrhh@ccu.cl', 'Op$r22.8')
                print("Cliente creado correctamente")
                transport = Transport(session=session)
                with Client(wsdl=self.wsdl_url, transport=transport) as client:
                    service = client.bind('ExternalReportWSSService', 'ExternalReportWSSService')
                    result = service.runReport(reportRequest=payload['reportRequest'], appParams=payload['appParams'])
                    print("Reporte ejecutado correctamente")
                    
                    # Leer el archivo Excel directamente desde los datos binarios
                    df = pd.read_excel(io.BytesIO(result["reportBytes"]), header=1)

                    # Renombrar las columnas
                    df = df.rename(columns=nuevos_nombres)

                    # Filtrar los registros que no tienen el campo Puesto
                    df_filtrado = df[df['job_name'].notnull()]

                    # Sustituir los valores nulos en el campo Email por 'No tiene correo'
                    df_filtrado.loc[df_filtrado['email_emplid'].isnull(), 'email_emplid'] = 'NA'

                    # Reemplazar los NaN por None
                    df_filtrado = df_filtrado.where(pd.notna(df_filtrado), None)

                    # Crear una lista de diccionarios a partir del DataFrame
                    res = df_filtrado.to_dict(orient='records')

                    return res
    
        except Exception as e:
            print("Error al crear el cliente:", e)
