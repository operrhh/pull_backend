import json
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

        # Parametrps de uso general
        self.dic_centro_costo = {}
        self.list_convert = []
        self.list_convert_full = False
        self.department_id = 0
        self.contador_registros = 0

        # Parametros para la paginacion de hcm
        self.limit_hcm = 20
        self.offset_hcm = 0
        self.has_more = False

        # Parametros para la paginacion de integraSoft
        self.pagination_integrasoft = 0
        self.limit_integrasoft = 20
        self.offset_param_integrasoft = 0
        self.offset_more_integrasoft = False

    def get_workers_hcm(self, request):
        params = self.params_definition(request)
        response = self.global_service.generate_request(self.dic_url.get('worker'), params)
        if response:
            if response.get('count') != 0:
                items = response.get('items')
                self.has_more = response.get('hasMore')
                workers = self.convert_data(items)
                print("Tamaño de la lista: ", len(self.list_convert))
                if self.list_convert_full == False and self.has_more == True:
                    self.offset_hcm = self.contador_registros
                    self.offset_more_integrasoft = True
                    self.get_workers_hcm(request)
                return workers
            else:
                raise ExceptionWorkerHcm('No se han encontrado worker')
        else:
            raise ExceptionWorkerHcm('Error al consultar workers')

    def update_worker_hcm(self, body, worker):
            try:
                body_json = json.loads(body.decode('utf-8'))
            except json.JSONDecodeError as e:
                raise ExceptionJson('Json enviado invalido')

            try:
                if 'worker' in body_json:
                    link_worker = worker.get('link')
                    json_worker = body_json['worker'][0]
                    print(json_worker)

                    response = self.global_service.generate_request(link_worker,body_data=json_worker)
                    if response:
                        print("Worker actualizado correctamente")

                if 'names' in body_json:
                    link_name = worker.get('names')[0].get('link')
                    json_name = body_json['names'][0]
                    response = self.global_service.generate_request(link_name, body_data=json_name)
                    if response:
                        print("Name actualizado correctamente")

                if 'addresses' in body_json:
                    link_address = worker.get('addresses')[0].get('link')
                    json_address = body_json['addresses'][0]
                    response = self.global_service.generate_request(link_address, body_data=json_address)
                    if response:
                        print("Address actualizado correctamente")

                if 'emails' in body_json:
                    for email_json in body_json['emails']:
                        for email_worker in worker.get('emails'):
                            if email_json.get('idEmail') == email_worker.get('email_address_id'):
                                link_email = email_worker.get('link')
                                response = self.global_service.generate_request(link_email, body_data=email_json.get('content'))
                                if response:
                                    print("Email actualizado correctamente")

                if 'workRelationships' in body_json:
                    for workrelationship_json in body_json['workRelationships']:
                        if workrelationship_json.get('assignments'):
                            link_assignment = worker.get('work_relationships')[0].get('assignments')[0].get('link')
                            assignment_json = workrelationship_json.get('assignments')[0]

                            response = self.global_service.generate_request(link_assignment, body_data=assignment_json)
                            if response:
                                print("assignment actualizado correctamente")

                        link_workrelationship = worker.get('work_relationships')[0].get('link')
                        workrelationship_json.pop('assignments', None)

                        response = self.global_service.generate_request(link_workrelationship, body_data=workrelationship_json)
                        if response:
                            print("workRelationship actualizado correctamente")                

                if 'phones' in body_json and len(worker.get('phones')) > 0:
                    for phone_json in body_json['phones']:
                            for phone_worker in worker.get('phones'):
                                if phone_json.get('idPhone') == phone_worker.get('phone_id'):
                                    link_phone = phone_worker.get('link')
                                    response = self.global_service.generate_request(link_phone, body_data=phone_json.get('content'))
                                    if response:
                                        print("Phone actualizado correctamente")
                elif 'phones' in body_json and not worker.get('phones'):
                    link_phone = worker.get('phones')[0].get('link')
                    phone_json = body_json['phones'][0]
                    response = self.global_service.generate_request(link_phone, body_data=phone_json)
                    if response:
                        print("Phone actualizado correctamente")

                # if 'phones' in body_json:
                #     for phone_json in body_json['phones']:
                #         for phone_worker in worker.get('phones'):
                #             if phone_json.get('idPhone') == phone_worker.get('phone_id'):
                #                 link_phone = phone_worker.get('link')
                #                 response = self.global_service.generate_request(link_phone, body_data=phone_json.get('content'))
                #                 if response:
                #                     print("Phone actualizado correctamente")

                return {'message': 'Worker actualizado correctamente'}

            except Exception as e:
                raise Exception(e) from e

    def create_worker_hcm(self, body):
        try:
            print(body)
        except Exception as e:
            raise Exception(e) from e

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

    def insert_centro_costo_dic(self,department_id,centro_costo):
        self.dic_centro_costo[department_id] = centro_costo
        #print(self.dic_centro_costo)

    def params_definition(self,request):
        person_number = request.query_params.get('personNumber', None)
        first_name = request.query_params.get('firstName', None)
        last_name = request.query_params.get('lastName', None)
        self.department_id = int(request.query_params.get('department', 0))

        self.offset_param_integrasoft = int(request.query_params.get('offset', 0))

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
        if self.department_id != 0:
            if conditions_added:
                query_params += AND_CONDITION
            query_params += f'workRelationships.assignments.DepartmentId = {self.department_id}'
        params = {}
        if query_params != '':
            #print(query_params)
            params['q'] = query_params
        params['expand'] = 'names,emails,addresses,phones,workRelationships.assignments'
        params['limit'] = self.limit_hcm

        if self.offset_more_integrasoft:
            params['offset'] = self.contador_registros
        else:
            params['offset'] = self.offset_param_integrasoft
            self.contador_registros = self.offset_param_integrasoft

        return params

    def create_worker_data(self,result):
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

        work_relationships_ordenados = sorted(work_relationships, key=lambda k: k['StartDate'], reverse=True)

        work_relationships = work_relationships_ordenados[0]

        assignments = work_relationships.get('assignments', {}).get('items', [])
        assignments_department_id = assignments[0]['DepartmentId']

        # Si se esta filtrando por departamento
        if self.department_id != 0:
            # Si el departamento del worker es igual al departamento filtrado
            if self.department_id == assignments_department_id:
                print( str(self.contador_registros) + " | " + result.get('PersonNumber') + " | Si")
                centro_costo = self.dic_centro_costo.get(assignments_department_id)
                if not centro_costo:
                    centro_costo = self.get_centro_costo_hcm(assignments_department_id)
                assignments[0]['CcuCodigoCentroCosto'] = centro_costo
                work_relationships['assignments'] = assignments
                worker_data['work_relationships'].append(work_relationships)

                return worker_data
            else:
                print( str(self.contador_registros) + " | " + result.get('PersonNumber') + " | No")
                return None
        else:
            print( str(self.contador_registros) + " | " + result.get('PersonNumber') + " | Si")
            centro_costo = self.dic_centro_costo.get(assignments_department_id)
            if not centro_costo:
                centro_costo = self.get_centro_costo_hcm(assignments_department_id)

            assignments[0]['CcuCodigoCentroCosto'] = centro_costo

            salary = self.get_salary_hcm(assignments[0]['AssignmentId'])
            
            assignments[0]['SalaryAmount'] = salary

            work_relationships['assignments'] = assignments
            worker_data['work_relationships'].append(work_relationships)

            return worker_data

    def convert_data(self,data):
        if isinstance(data, list):
            for result in data:
                if len(self.list_convert) == self.limit_integrasoft:
                    self.list_convert_full = True
                    break
                else:
                    self.contador_registros = self.contador_registros + 1 #Contador de registros
                    worker_data = self.create_worker_data(result)
                    if worker_data:
                        self.list_convert.append(worker_data)
            return self.list_convert
        else:
            return self.create_worker_data(data)