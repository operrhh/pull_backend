import json
from ...services.globalService import GlobalService
from ..custom_exceptions import ExceptionJson, ExceptionWorkerHcm
from apps.parameters.models import Parameter, ParameterType
from apps.utils import log_entry

class WorkerServiceHcm:
    def __init__(self):
        self.dic_parameter_type = {param.Description: param.id for param in ParameterType.objects.all()}
        self.dic_url = {param.FilterField3: param.Value for param in Parameter.objects  .filter(ParameterTypeId=self.dic_parameter_type.get('url'))
                                                                                        .filter(Enabled=True)
                                                                                        .filter(FilterField1='url')
                                                                                        .filter(FilterField2='hcm')}
        self.global_service = GlobalService()

    def get_workers_hcm(self, request):
        params = self.params_definition(request)
        response = self.global_service.generate_request(self.dic_url.get('worker'), params)
        if response:
            if response.get('count') != 0:
                items = response.get('items')               
                workers = self.convert_data(items)
                return workers
            else:
                raise ExceptionWorkerHcm('No se han encontrado usuarios')
        else:
            raise ExceptionWorkerHcm('Error al consultar usuarios')

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
                
                # if 'phones' in body_json:

                return {'message': 'Worker actualizado correctamente'}

            except Exception as e:
                raise Exception(e) from e

    def params_definition(self,request):
        person_number = request.query_params.get('personNumber', None)
        name = request.query_params.get('name', None)
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
            query_params += f"upper(names.DisplayName) like '%{name.upper()}%'"
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
        print(f'Query params: {query_params}')
        params = {}
        if query_params != '':
            params['q'] = query_params
        params['expand'] = 'names,emails,addresses,phones,workRelationships.assignments'
        print(f'Params: {params}')

        return params

    def create_worker_data(self,result):
        return {
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
                'work_relationships': result.get('workRelationships').get('items', []),
                'links': result.get('links', [])
            }

    def convert_data(self,data):
        if isinstance(data, list):
            return [self.create_worker_data(result) for result in data]
        else:
            return self.create_worker_data(data)