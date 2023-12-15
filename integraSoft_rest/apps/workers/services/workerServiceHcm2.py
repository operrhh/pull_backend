import json
from ...services.globalService import GlobalService
from ..custom_exceptions import ExceptionJson, ExceptionWorkerHcm
from apps.parameters.models import Parameter, ParameterType

class WorkerServiceHcm2:
    def __init__(self):
        self.dic_parameter_type = {param.Description: param.id for param in ParameterType.objects.all()}
        self.dic_url = {param.FilterField3: param.Value for param in Parameter.objects  .filter(ParameterTypeId=self.dic_parameter_type.get('url'))
                                                                                        .filter(Enabled=True)
                                                                                        .filter(FilterField1='url')
                                                                                        .filter(FilterField2='hcm')}
        self.global_service = GlobalService()
    
        # Parametros de uso general

        # Parametros que vienen en la request
        self.department_id_param_integrasoft = 0
        self.offset_param_integrasoft = 0


        self.contador_registros = 0
        self.list_convert = []
        self.dic_centro_costo = {}
        self.list_convert_full = False
        self.many_workers = True

        # Parametros para la paginacion de hcm
        self.limit_hcm = 10
        self.has_more = False

        # Parametros para la paginacion de integraSoft
        self.offset_more_integrasoft = False
        self.limit_integrasoft = 20

    def get_workers_hcm(self, request):
        params = self.params_definition(request)
        try:
            response = self.global_service.generate_request(self.dic_url.get('worker'), params)
            if response:
                if response.get('count') != 0:
                    items = response.get('items')
                    self.has_more = response.get('hasMore')
                    workers = self.convert_data(items)
                    print("Tamaño de la lista: ", len(self.list_convert))
                    if self.list_convert_full == False and self.has_more == True:
                        self.offset_more_integrasoft = True
                        self.get_workers_hcm(request)

                    if self.has_more:
                        res = {
                            'items': workers,
                            'next_offset': self.contador_registros,
                            'count': len(workers),
                            'has_more': self.has_more
                        }
                    else:
                        res = {
                            'items': workers,
                            'next_offset': 1,
                            'count': len(workers),
                            'has_more': self.has_more
                        }                        

                    return res
                else:
                    raise ExceptionWorkerHcm('No se han encontrado worker')
            else:
                raise ExceptionWorkerHcm('Error al consultar workers')
        except Exception as e:
            raise Exception(e) from e
        
    def get_worker_hcm(self, request):
        params = self.params_definition(request)
        try:
            response = self.global_service.generate_request(self.dic_url.get('worker'), params)
            if response:
                if response.get('count') != 0:
                    items = response.get('items')
                    worker = self.convert_data(items)
                    return worker
                else:
                    raise ExceptionWorkerHcm('No se han encontrado worker')
            else:
                raise ExceptionWorkerHcm('Error al consultar workers')
        except Exception as e:
            raise Exception(e) from e

    def insert_centro_costo_dic(self,department_id,centro_costo):
        self.dic_centro_costo[department_id] = centro_costo

    def get_department_hcm(self,department_id):
        params = {}
        params['q'] = f"departmentsEFF.CategoryCode='DEPARTMENT' and OrganizationId={department_id}"
        params['expand'] = 'departmentsDFF'
        try:
            response = self.global_service.generate_request(self.dic_url.get('department'),params=params)
            if response:
                if response.get('count') != 0:
                    department = response.get('items')[0]
                    return department
                else:
                    raise ExceptionWorkerHcm('No se han encontrado departamentos')
        except Exception as e:
            raise Exception(e) from e

    def get_centro_costo_hcm(self,department_id):

        department = self.get_department_hcm(department_id)

        department_dff = department.get('departmentsDFF').get('items')[0]
        centro_costo = department_dff.get('ccuCodigoCentroCosto')
        if centro_costo == None:
            centro_costo = 'No asignado'
        self.insert_centro_costo_dic(department_id,centro_costo)
        return centro_costo

    def create_worker_data_details(self, result):
        return result
    
    def create_worker_data_many(self, result):
        work_relationships = result.get('workRelationships', {}).get('items', [])

        # Se ordenan los work_relationships por fecha de inicio
        work_relationships_ordenados = sorted(work_relationships, key=lambda k: k['StartDate'], reverse=True)

        # Se toma el primer work_relationship que es el mas reciente
        work_relationships = work_relationships_ordenados[0]

        assignments = work_relationships.get('assignments', {}).get('items', [])

        work_names = result.get('names', {}).get('items', [])

        # Datos de la persona
        worker_data: dict = {}
        worker_data['person_number'] = result.get('PersonNumber')
        worker_data['display_name'] = work_names[0]['DisplayName']
        worker_data['department_name'] = assignments[0]['DepartmentName']

        # Si hay department id, se filtra por el
        if self.department_id_param_integrasoft != 0:
            if assignments[0]['DepartmentId'] != self.department_id_param_integrasoft:
                print("No | ", self.contador_registros , " | ", worker_data['person_number'], " | ", worker_data['display_name'], " | ", worker_data['department_name'])
                return None

        print("Si | ", self.contador_registros , " | ", worker_data['person_number'], " | ", worker_data['display_name'], " | ", worker_data['department_name'])

        return worker_data

    def create_worker_data(self, result):
        if self.many_workers:
            return self.create_worker_data_many(result)
        else:
            return self.create_worker_data_details(result)

    def convert_data(self, items):
        for result in items:
            self.contador_registros += 1
            worker_data = self.create_worker_data(result)
            if worker_data:
                self.list_convert.append(worker_data)
                if len(self.list_convert) == self.limit_integrasoft:
                    self.list_convert_full = True
                    break
        return self.list_convert

    def params_definition(self, request):
        """
        Constructs the query parameters based on the request parameters.

        Args:
            request: The request object containing the query parameters.

        Returns:
            A dictionary containing the constructed query parameters.
        """
        person_number = request.query_params.get('personNumber', None)
        first_name = request.query_params.get('firstName', None)
        last_name = request.query_params.get('lastName', None)
        legislation_code = request.query_params.get('legislationCode', 'CL')
        self.department_id_param_integrasoft = int(request.query_params.get('department', 0))
        self.many_workers = bool(request.query_params.get('manyWorkers', True))
        self.offset_param_integrasoft = int(request.query_params.get('offset', 1))

        query_params = ''
        conditions_added = False
        AND_CONDITION = ' AND '

        if person_number:
            query_params += f"PersonNumber like '{person_number}%'"
            conditions_added = True
        if first_name:
            if conditions_added:
                query_params += AND_CONDITION
            query_params += f"upper(names.FirstName) like '%{first_name.upper()}%'"
            conditions_added = True
        if last_name:
            if conditions_added:
                query_params += AND_CONDITION
            query_params += f"upper(names.LastName) like '%{last_name.upper()}%'"
            conditions_added = True
        if legislation_code:
            if conditions_added:
                query_params += AND_CONDITION
            query_params += f"workRelationships.LegislationCode = '{legislation_code}'"
            conditions_added = True
        if self.department_id_param_integrasoft != 0:
            if conditions_added:
                query_params += AND_CONDITION
            query_params += f'workRelationships.assignments.DepartmentId = {self.department_id_param_integrasoft}'
        params = {}
        if query_params != '':
            params['q'] = query_params

        if self.many_workers:
            params['expand'] = 'names,workRelationships.assignments'
            params['onlyData'] = 'true'
        else:
            params['expand'] = 'names,emails,addresses,phones,workRelationships.assignments'

        params['limit'] = self.limit_hcm

        if self.offset_more_integrasoft:
            params['offset'] = self.contador_registros + 1
        else:
            if self.offset_param_integrasoft == 1:
                params['offset'] = 0
                self.contador_registros = -1
            else:
                params['offset'] = self.offset_param_integrasoft + 1
                self.contador_registros = self.offset_param_integrasoft
            
            print("Contador de registros: ", self.contador_registros)

        params['orderBy'] = 'PersonId:desc'

        print("Parametros de la consulta: ", params)
        return params