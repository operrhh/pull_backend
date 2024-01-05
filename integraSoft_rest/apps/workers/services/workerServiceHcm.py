from ...services.globalService import GlobalService
from ..custom_exceptions import ExceptionJson, ExceptionWorkerHcm
from apps.parameters.models import Parameter, ParameterType

class WorkerServiceHcm:
    def __init__(self):
        self.dic_parameter_type = {param.Description: param.id for param in ParameterType.objects.all()}
        self.dic_url = {param.FilterField3: param.Value for param in Parameter.objects  .filter(ParameterTypeId=self.dic_parameter_type.get('url'))
                                                                                        .filter(Enabled=True)
                                                                                        .filter(FilterField1='url')
                                                                                        .filter(FilterField2='hcm')}
        self.global_service = GlobalService()

        # Parametros que vienen en la request
        self.department_id_param_integrasoft: int = 0
        self.offset_param_integrasoft: int = 0
        self.last_offset_param_integrasoft: int = 0

        # Parametros de uso general
        self.contador_registros: int = 0
        self.list_convert = []
        self.dic_centro_costo = {}
        self.list_convert_full: bool = False
        self.many_workers: bool = True

        # Parametros para la paginacion de hcm
        self.limit_hcm = 20
        self.has_more = False
        self.total_results: int = 0

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
                    self.total_results = response.get('totalResults')
                    workers = self.convert_data_many(items)

                    print("Tamaño de la lista: ", len(self.list_convert))

                    if self.list_convert_full == False and self.has_more == True:
                        self.offset_more_integrasoft = True
                        self.get_workers_hcm(request)
                else:
                    raise ExceptionWorkerHcm('No se han encontrado worker')
            else:
                raise ExceptionWorkerHcm('Error al consultar workers')
            
            # res = self.create_data_worker_return(workers)

            res = {
                'items': workers,
                'next': self.contador_registros if self.has_more else 0,
                'previous': self.last_offset_param_integrasoft,
                'count': len(workers),
                'has_more': self.has_more,
                'total_results': self.total_results,
                'limit': self.limit_hcm,
                'url': self.get_link_request(request)
            }

            return res
        except Exception as e:
            raise Exception(e) from e

    def create_data_worker_return(self, worker_data):
        if self.has_more:
            res = {
                'items': worker_data,
                'next_offset': self.contador_registros,
                'count': len(worker_data),
                'has_more': self.has_more
            }
        else:
            res = {
                'items': worker_data,
                'next_offset': 1,
                'count': len(worker_data),
                'has_more': self.has_more
            }
        return res

    def get_worker_hcm(self, request):
        params = self.params_definition(request)
        try:
            response = self.global_service.generate_request(self.dic_url.get('worker'), params)
            if response:
                if response.get('count') != 0:
                    item = response.get('items')
                    worker = self.convert_data(item[0])
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
        # if centro_costo == None:
        #     centro_costo = 'No asignado'
        self.insert_centro_costo_dic(department_id,centro_costo)
        return centro_costo

    def create_worker_data_details(self, result):
        worker_data: dict = {
                'person_id': result.get('PersonId'),
                'person_number': result.get('PersonNumber'),
                'date_of_birth': result.get('DateOfBirth'),
                'date_of_death': result.get('DateOfDeath'),
                'country_of_birth': result.get('CountryOfBirth'),
                'region_of_birth': result.get('RegionOfBirth'),
                'town_of_birth': result.get('TownOfBirth'),
                'created_by': result.get('CreatedBy'),
                'creation_date': result.get('CreationDate'),
                'last_updated_by': result.get('LastUpdatedBy'),
                'last_update_date': result.get('LastUpdateDate'),
                'names': result.get('names').get('items', []),
                'emails': result.get('emails').get('items', []),
                'addresses': result.get('addresses').get('items', []),
                'phones': result.get('phones').get('items', []),
                'work_relationships': [], # Realizamos un trabajo adicional para obtener los assignments
                'links': result.get('links', [])
            }
        
        work_relationships = result.get('workRelationships', {}).get('items', [])

        # Se obtiene el ultimo work_relationship
        last_work_relationship = self.get_last_work_relationship(work_relationships)

        # Se obtiene assignment de last_work_relationship
        last_assignment = last_work_relationship.get('assignments').get('items', [])[0]

        # Se obtiene el deparment_id de last_assignment
        assignments_department_id = last_assignment['DepartmentId']

        if assignments_department_id != None:
            # Se obtiene el centro_costo de deparment_id en el diccionario o se consulta en hcm
            centro_costo = self.dic_centro_costo.get(assignments_department_id)
            if not centro_costo:
                centro_costo = self.get_centro_costo_hcm(assignments_department_id)
            last_assignment['CcuCodigoCentroCosto'] = centro_costo
        else:
            last_assignment['CcuCodigoCentroCosto'] = None

        # Se obtiene el salario de last_assignment
        salary_decimal = self.get_salary_hcm(last_assignment['AssignmentId'])
        salary = str(int(salary_decimal))
        last_assignment['SalaryAmount'] = salary

        # Se obtiene el manager valido de last_assignment
        managers = last_assignment.get('managers', {}).get('items', [])
        manager = self.get_work_relationship_manager(managers)

        if manager:
            manager_number = self.convert_manager_assignment_number(manager['ManagerAssignmentNumber'])
            last_assignment['Manager'] = manager_number
        else:
            last_assignment['Manager'] = None

        # Borramos los valores no utilizados
        del last_assignment['managers']
        del last_work_relationship['assignments']

        last_work_relationship['assignment'] = last_assignment

        worker_data['work_relationships'].append(last_work_relationship)

        return worker_data

    def get_link_request(self,request):
        return request.build_absolute_uri()

    def convert_manager_assignment_number(self, manager_assignment_number):
        manager_number = ''
        for i in manager_assignment_number:
            if i != '_':
                manager_number += i
            else:
                return manager_number

    def get_salary_hcm(self,assignmentd_id):
        params = {}
        params['q'] = f"AssignmentId={assignmentd_id}"
        params['orderBy'] = 'DateTo:desc'
        try:
            response = self.global_service.generate_request(self.dic_url.get('salary'),params=params)
            if response:
                if response.get('count') != 0:
                    salary = response.get('items')[0]
                    return salary.get('SalaryAmount')
                else:
                    return 0
        except Exception as e:
            raise Exception(e) from e

    def get_work_relationship_manager(self, managers):
        # Se ordenan los managers por fecha de inicio
        managers_ordenados = sorted(managers, key=lambda k: k['EffectiveStartDate'], reverse=True)
        # Se toma el primer manager que es el mas reciente
        for manager in managers_ordenados:
            if manager['ManagerType'] == 'LINE_MANAGER':
                return manager
        return None

    def get_last_work_relationship(self, work_relationships):
        # Se ordenan los work_relationships por fecha de inicio
        work_relationships_ordenados = sorted(work_relationships, key=lambda k: k['StartDate'], reverse=True)
        # Se toma el primer work_relationship que es el mas reciente
        return work_relationships_ordenados[0]

    def create_worker_data_many(self, result):
        work_relationships = result.get('workRelationships', {}).get('items', [])

        # Se obtiene el ultimo work_relationship
        last_work_relationship = self.get_last_work_relationship(work_relationships)

        assignments = last_work_relationship.get('assignments', {}).get('items', [])

        work_names = result.get('names', {}).get('items', [])

        # Si hay department id, se filtra por el
        if self.department_id_param_integrasoft != 0:
            if assignments[0]['DepartmentId'] != self.department_id_param_integrasoft:
                print("No | ", self.contador_registros , " | ", result.get('PersonNumber'), " | ", work_names[0]['DisplayName'], " | ", assignments[0]['DepartmentName'])
                return None

        # Datos de la persona
        worker_data: dict = {}
        worker_data['person_number'] = result.get('PersonNumber')
        worker_data['display_name'] = work_names[0]['DisplayName']
        worker_data['department_name'] = assignments[0]['DepartmentName'] if assignments[0]['DepartmentName'] else None

        print("Si | ", self.contador_registros , " | ", worker_data['person_number'], " | ", worker_data['display_name'], " | ", worker_data['department_name'])

        return worker_data

    def create_worker_data(self, result):
        if self.many_workers:
            return self.create_worker_data_many(result)
        else:
            return self.create_worker_data_details(result)

    def convert_data(self, item):
        worker_data = self.create_worker_data(item)
        if worker_data:
            self.list_convert.append(worker_data)
        return worker_data

    def convert_data_many(self, items):
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
        self.many_workers = request.query_params.get('manyWorkers', 'True').lower() == 'true'

        person_number = request.query_params.get('personNumber', None)
        first_name = request.query_params.get('firstName', None)
        last_name = request.query_params.get('lastName', None)
        legislation_code = request.query_params.get('legislationCode', 'CL')
        self.department_id_param_integrasoft = int(request.query_params.get('department', 0))

        # self.offset_param_integrasoft = int(request.query_params.get('offset', 1))
        self.offset_param_integrasoft = int(request.query_params.get('offset', 0))
        self.offset_param_integrasoft = self.offset_param_integrasoft - 1

        self.last_offset_param_integrasoft = self.offset_param_integrasoft

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
            params['totalResults'] = 'true'
        else:
            params['expand'] = 'names,emails,addresses,phones,workRelationships.assignments,workRelationships.assignments.managers'

        params['limit'] = self.limit_hcm

        if self.many_workers:
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
        else:
            params['offset'] = 0

        print("Parametros de la consulta: ", params)
        return params