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
        self.has_more = True
        self.workers_list = []
        self.limit = 10
        self.offset = 0
        self.cont_limit = self.limit

    def get_workers_hcm(self, request):
        params = self.params_definition(request)
        response = self.global_service.generate_request(self.dic_url.get('worker'), params)
        if response:
            if response.get('count') != 0:
                items = response.get('items')
                workers = self.convert_data(items)
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

    def get_centro_costo_hcm(self,department_id):
        params = {}
        params['q'] = f"departmentsEFF.CategoryCode='DEPARTMENT' and OrganizationId={department_id}"
        params['expand'] = 'departmentsDFF'
        response = self.global_service.generate_request(self.dic_url.get('department'),params=params)
        if response:
            if response.get('count') != 0:
                items = response.get('items')[0]
                department_dff = items.get('departmentsDFF').get('items')[0]
                centro_costo = department_dff.get('ccuCodigoCentroCosto')
                return centro_costo
            else:
                raise ExceptionWorkerHcm('No se han encontrado departamentos')

    def params_definition(self,request):
        person_number = request.query_params.get('personNumber', None)
        name = request.query_params.get('name', None)
        last_name = request.query_params.get('lastName', None)
        bussines_unit = request.query_params.get('bussinesUnit', None)
        department = request.query_params.get('department', None)

        query_params = ''
        conditions_added = False

        if person_number:
            query_params += f"PersonNumber like '{person_number}%'"
            conditions_added = True
        if name:
            if conditions_added:
                query_params += ' AND '
            query_params += f"upper(names.FirstName) like '%{name.upper()}%'"
            conditions_added = True
        if last_name:
            if conditions_added:
                query_params += ' AND '
            query_params += f"upper(names.LastName) like '%{last_name.upper()}%'"
            conditions_added = True
        if bussines_unit:
            if conditions_added:
                query_params += ' AND '
            query_params += f'workRelationships.assignments.BusinessUnitId = {bussines_unit}'
            conditions_added = True
        if department:
            if conditions_added:
                query_params += ' AND '
            query_params += f'workRelationships.assignments.DepartmentId = {department}'
        params = {}
        if query_params != '':
            print(query_params)
            params['q'] = query_params
        params['expand'] = 'names,emails,addresses,phones,workRelationships.assignments'

        return params

    def pagination_definition(self,params):
        params['limit'] = self.cont_limit
        params['offset'] = self.offset
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

        for relationship in work_relationships:
            assignments = relationship.get('assignments', {}).get('items', [])
            department_id = assignments[0]['DepartmentId']
            centro_costo = self.get_centro_costo_hcm(department_id)
            assignments[0]['CcuCodigoCentroCosto'] = centro_costo
            relationship['assignments'] = assignments
            worker_data['work_relationships'].append(relationship)
        
        return worker_data

    def convert_data(self,data):
        if isinstance(data, list):
            return [self.create_worker_data(result) for result in data]
        else:
            return self.create_worker_data(data)