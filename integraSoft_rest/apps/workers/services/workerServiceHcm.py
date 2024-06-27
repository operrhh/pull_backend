from ...services.globalService import GlobalService
from ..custom_exceptions import ExceptionWorkerHcm
from apps.parameters.models import Parameter, ParameterType
from ...utils import log_entry
from .workerServicePeopleSoft import WorkerServicePeopleSoft
from ..api.serializers import WorkerPeopleSoftSerializer, WorkerHcmSerializer

import requests
from django.http import HttpRequest, QueryDict
from django.test import RequestFactory
from datetime import datetime

from ..enums import companys as company_enum

class WorkerServiceHcm:
    def __init__(self):
        self.dic_parameter_type = {
            param.Description: param.id for param in ParameterType.objects.all()
        }

        self.dic_url = {
            param.FilterField3: param.Value for param in Parameter.objects
                .filter(ParameterTypeId=self.dic_parameter_type.get('url'))
                .filter(Enabled=True)
                .filter(FilterField1='url')
                .filter(FilterField2='hcm')
        }
        
        self.dic_size_request_hcm = {
            param.FilterField3: param.Value for param in Parameter.objects 
                .filter(ParameterTypeId=self.dic_parameter_type.get('size_request'))
                .filter(Enabled=True)
                .filter(FilterField1='size_request')
                .filter(FilterField2='hcm')
        }

        self.dic_size_request_integrasoft = {
            param.FilterField3: param.Value for param in Parameter.objects
                .filter(ParameterTypeId=self.dic_parameter_type.get('size_request'))
                .filter(Enabled=True)
                .filter(FilterField1='size_request')
                .filter(FilterField2='integrasoft')
        }

        self.global_service = GlobalService()
        self.peoplesoft_service = WorkerServicePeopleSoft()


        # Version
        self.version = None

        # Parametros que vienen en la request
        self.department_id_param_integrasoft: int = 0
        self.offset_param_integrasoft: int = 0
        self.last_offset_param_integrasoft: int = 0
        self.request = None


        # Parametros de uso general
        self.contador_registros: int = 0
        self.list_convert = []
        self.dic_centro_costo = {}
        self.list_convert_full: bool = False
        self.many_workers: bool = True
        self.excluded_items: int = 0
        self.res = {}

        # Parametros para la paginacion de hcm
        self.limit_hcm = int(self.dic_size_request_hcm.get('worker')) # Este parametro es para la cantidad de registros que se retornan en hcm
        self.has_more = False
        self.total_results: int = 0

        # Parametros para la paginacion de integraSoft
        self.limit_integrasoft = int(self.dic_size_request_integrasoft.get('worker')) # Este parametro es para la cantidad de registros que se retornan en integraSoft
        self.offset_more_integrasoft = False

    def get_workers_hcm(self, request):
        try:
            self.request = request
            params = self.params_definition(request)
            response = self.global_service.generate_request(request=request,url=self.dic_url.get('worker'), params=params)
            if response:
                if response.get('count') != 0:
                    items = response.get('items')
                    self.has_more = response.get('hasMore')
                    workers = self.convert_data_many(items)

                    print("Tamaño de la lista: ", len(self.list_convert))

                    if self.list_convert_full == False and self.has_more == True:
                        self.offset_more_integrasoft = True
                        return self.get_workers_hcm(request)
                    
                    self.res = {
                        'items': workers,
                        'next': self.contador_registros if self.has_more else 0,
                        'count': len(workers),
                        'has_more': self.has_more,
                        'limit': self.limit_hcm,
                        'url': self.get_link_request(request)
                    }  
                else:
                    self.res = {
                        'items': [],
                        'next': 0,
                        'count': 0,
                        'has_more': False,
                        'limit': self.limit_hcm,
                        'url': self.get_link_request(request)
                    } 
            else:
                raise ExceptionWorkerHcm('Error al consultar workers')          
            
            log_entry(request.user, 'INFO', 'get workers hcm', 'Se ha consultado workers exitosamente')
            
            return self.res
        except Exception as e:
            raise Exception(e) from e


    def get_worker_hcm(self, request):
        try:
            self.request = request

            self.version = self.request.GET.get('version', None)
            params = self.params_definition(request)



            if self.version:
                response = self.global_service.generate_request(request=request,url=self.dic_url.get('worker'), params=params,version=self.version)
            else:
                response = self.global_service.generate_request(request=request,url=self.dic_url.get('worker'), params=params)

            if response:
                if response.get('count') != 0:
                    item = response.get('items')

                    if self.version:
                        return item
                    else:
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
            response = self.global_service.generate_request(request=self.request,url=self.dic_url.get('department'),params=params)
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
        salary = self.get_salary_hcm(last_assignment['AssignmentId'])
        last_assignment['SalaryAmount'] = salary

        # Se obtiene el manager valido de last_assignment
        managers = last_assignment.get('managers', {}).get('items', [])
        manager = self.get_work_relationship_manager(managers)

        if manager:
            manager_number = self.convert_manager_assignment_number(manager['ManagerAssignmentNumber'])
            last_assignment['Manager'] = manager_number
            last_assignment['manager_detail'] = manager
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
            response = self.global_service.generate_request(request=self.request,url=self.dic_url.get('salary'),params=params)
            if response:
                if response.get('count') != 0:
                    salary = response.get('items')[0]

                    log_entry(self.request.user, 'INFO', 'get salary hcm', 'Se ha consultado salary exitosamente')

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
                # print("No | ", self.contador_registros , " | ", result.get('PersonNumber'), " | ", work_names[0]['DisplayName'], " | ", assignments[0]['DepartmentName'])
                return None

        # Datos de la persona
        worker_data: dict = {}
        worker_data['person_number'] = result.get('PersonNumber')
        worker_data['display_name'] = work_names[0]['DisplayName']
        worker_data['department_name'] = assignments[0]['DepartmentName'] if assignments[0]['DepartmentName'] else None

        # print("Si | ", self.contador_registros , " | ", worker_data['person_number'], " | ", worker_data['display_name'], " | ", worker_data['department_name'])

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
            else:
                self.excluded_items += 1
        return self.list_convert

    def params_definition(self, request):
        """
        Constructs the query parameters based on the request parameters.

        Args:
            request: The request object containing the query parameters.

        Returns:
            A dictionary containing the constructed query parameters.
        """
        self.many_workers = request.GET.get('manyWorkers', 'True').lower() == 'true'

        person_number = request.GET.get('personNumber', None)
        first_name = request.GET.get('firstName', None)
        last_name = request.GET.get('lastName', None)
        legislation_code = request.GET.get('legislationCode', 'CL')
        self.department_id_param_integrasoft = int(request.GET.get('department', 0))

        self.offset_param_integrasoft = int(request.GET.get('offset', 0))
        self.offset_param_integrasoft = self.offset_param_integrasoft - 1

        self.last_offset_param_integrasoft = self.offset_param_integrasoft

        query_params = ''
        conditions_added = False
        AND_CONDITION = ' AND '

        if person_number:
            query_params += f"upper(PersonNumber) like '{person_number.upper()}%'"
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

            if self.version is None:
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
                
                # print("Contador de registros: ", self.contador_registros)

            params['orderBy'] = 'PersonNumber:desc'
        else:
            params['offset'] = 0

        log_entry(request.user, 'INFO', 'get workers hcm (params definition)', f'Parametros de la consulta: {params}')
        return params

    def get_worker_lov(self, person_id:int):
        params = {}
        params['q'] = f"PersonId = '{person_id}'"
        try:
            response = self.global_service.generate_request(request=self.request,url=self.dic_url.get('worker_lov'),params=params)
            if response:
                if response.get('count') != 0:
                    worker = response.get('items')[0]
                    return worker
                else:
                    raise ExceptionWorkerHcm('No se han encontrado workers')
        except Exception as e:
            raise Exception(e) from e


# POST Assignment Name HCM

    def update_assignment_name_hcm(self, request):
        try:
            worker_hcm = self.get_worker_hcm(request)[0]
            if worker_hcm:
                work_relationships = worker_hcm.get('workRelationships', {}).get('items', [])
                last_work_relationship = self.get_last_work_relationship(work_relationships)

                assignments = last_work_relationship.get('assignments', {}).get('items', [])
                assignment = assignments[0]
                assignment_link = assignment.get('@context').get('links')[0].get('href')
                effdt = assignment.get('EffectiveStartDate')

                job_id = assignment.get('JobId')
                job = self.get_job_hcm(job_id)
                if job:
                    job_name = job.get('Name')
                else:
                    raise ExceptionWorkerHcm('No se ha encontrado Job en hcm')

                res = self.update_assignment_name_hcm_data(assignment_link, job_name, effdt)

                return res
            else:
                raise ExceptionWorkerHcm('No se ha encontrado worker en hcm')
        except Exception as e:
            raise Exception(e) from e

    def update_assignment_name_hcm_data(self, assignment_hcm, job_name, effdt):
        try:
            body_data = {
                "ActionCode":"DP_DTA",
                "AssignmentName": job_name
            }

            response = self.global_service.generate_request(request=self.request, url=assignment_hcm, body_data=body_data, range_start_date=effdt,method='PATCH',version=self.version)
            if response:
                return response
            else:
                raise ExceptionWorkerHcm('Error al actualizar assignment name')
        except Exception as e:
            raise Exception(e) from e

    def get_job_hcm(self, job_id):
        params = {}
        params['q'] = f"JobId = '{job_id}'"
        try:
            response = self.global_service.generate_request(request=self.request,url=self.dic_url.get('job'),params=params)
            if response:
                if response.get('count') != 0:
                    job = response.get('items')[0]
                    return job
                else:
                    raise ExceptionWorkerHcm('No se han encontrado jobs')
        except Exception as e:
            raise Exception(e) from e


# POST Worker HCM

    def create_worker_hcm(self, request):
        try:
            person_number = request.GET.get('personNumber', None)

            if person_number:
                res = self.get_workers_hcm(request)
                if res and res['count'] > 0:
                    raise ExceptionWorkerHcm('El worker ya existe')
                else:
                    worker = self.peoplesoft_service.get_workers_peoplesoft(request)
                    if worker:
                        worker_serializer = WorkerPeopleSoftSerializer(worker, many=True)
                        res = self.create_worker_hcm_data(request, worker_serializer.data)
            else:
                raise ExceptionWorkerHcm('El parametro personNumber es requerido')

        except Exception as e:
            raise Exception(e) from e
    
    def create_worker_hcm_data(self, request, worker):
        worker = worker[0]

        fake_request = self.create_fake_request(request, worker.get('supervisor_id'))

        # Crear variable que tenga la estructura de una request
        res_manager = self.get_workers_hcm(fake_request)

        if res_manager and res_manager['count'] > 0:
            manager = res_manager['items'][0]
        else:
            manager = None
        
        dt = str(manager.get("work_relationships")[0].get("StartDate"))
        dt_object = datetime.strptime(dt, '%Y-%m-%d')
        formatted_date_manager = dt_object.strftime('%d%m%Y')

        manager_assignment_number = manager.get("work_relationships")[0].get("assignment").get("AssignmentNumber")


        worker = self.create_worker_hcm_format_company(worker)

        try:
            body_data = {
                "PersonNumber": worker.get('emplid'),
                "DateOfBirth": worker.get('birthdate'),
                "CountryOfBirth": "CL",
                "legislativeInfo":[
                    {
                        "LegislationCode": "CL",
                        "Gender": worker.get('sex'),
                        "MaritalStatus": worker.get('mar_status'),
                    }
                ],
                "names":[
                    {
                        "LegislationCode": "CL",
                        "FirstName": worker.get('first_name'),
                        "LastName": worker.get('last_name'),
                        "PreviousLastName": worker.get('previous_last_name'),
                    }
                ],
                "addresses":[
                    {
                        "AddressType":"HOME",
                        "AddressLine1": worker.get('address1'),
                        "AddressLine2": worker.get('address2'),
                        "AddressLine3": worker.get('address3'),
                        "AddressLine4": worker.get('address4'),
                        "TownOrCity": worker.get('city'),
                        "Region1":"",
                        "Region2":"",
                        "Country":"CL",
                        "PostalCode":""
                    }
                ],
                "emails":[
                    {
                        "EmailType":"H1",
                        "EmailAddress": worker.get('email'),
                        "FromDate":worker.get('effdt'),
                        "PrimaryFlag": True
                    }
                ],
                "nationalIdentifiers":[
                    {
                        "LegislationCode":"CL",
                        "NationalIdentifierType":"NID",
                        "NationalIdentifierNumber": worker.get('emplid'),
                        "PrimaryFlag":True
                    }
                ],
                "workRelationships":[
                    {
                        "LegalEmployerName": f"{worker.get('company_code')} - {worker.get('company_descr')}",
                        "WorkerType":"E",
                        "StartDate":worker.get('effdt'),
                        "EnterpriseSeniorityDate":worker.get('effdt'),
                        "LegalEmployerSeniorityDate":worker.get('effdt'),
                        "PrimaryFlag": True,
                        "assignments":[
                            {
                                "BusinessUnitName": f"{worker.get('company_code')} - {worker.get('company_descr')} BU",
                                "ActionCode":"HIRE",
                                "ReasonCode":None,
                                "JobCode":worker.get('jobcode'),
                                "DepartmentName": f"{worker.get('deptid')} - {worker.get('dept_descr')}",
                                "LocationCode":worker.get('location'),
                                "AssignmentCategory":"FR",
                                "PermanentTemporary":"R",
                                "FullPartTime":"FULL_TIME",
                                "ManagerFlag":False,
                                "NormalHours":180,
                                "Frequency":"M",
                                #"WorkerCategory":worker.get('job_family'),
                                "CollectiveAgreementName": worker.get('labor_agreement'),
                                "UnionName":f"{worker.get('union_code')} - {worker.get('union_descr')}",
                                "LabourUnionMemberFlag":True,
                                "managers":[
                                    {
                                        #"ManagerAssignmentNumber":f'{manager.get("person_number")}_{worker.get("company_code")}_{formatted_date_manager}',
                                        "ManagerAssignmentNumber":manager_assignment_number,
                                        "ManagerType":"LINE_MANAGER",
                                        "ActionCode":"MANAGER_CHANGE",
                                        "ReasonCode":None,                                        
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }


            response = self.global_service.generate_request(request=self.request, url=self.dic_url.get('worker'), body_data=body_data, method='POST', range_start_date=worker.get('effdt'))
            if response:
                return response
            else:
                raise ExceptionWorkerHcm('Error al crear worker')            
        except Exception as e:
            raise Exception(e) from e
    
    def create_worker_hcm_format_company(self, worker):
        company_code = worker.get('company_code')
        
        company_detail = company_enum.get(company_code)

        worker['company_descr'] = company_detail

        return worker

    def create_fake_request(self, request, person_number):

        factory = RequestFactory()
        simulated_request = factory.get('/', data={'personNumber': person_number, 'manyWorkers': 'False'})

        simulated_request.query_params = simulated_request.GET
        simulated_request.user = request.user
        simulated_request.build_absolute_uri = request.build_absolute_uri


        # django_request = HttpRequest()
        # django_request.method = 'GET'
        # django_request.GET = QueryDict(f'personNumber={person_number}')

        return simulated_request

# POST Manager HCM

    def change_manager_hcm(self, request):
        try:
            worker_peoplesoft = self.peoplesoft_service.get_workers_peoplesoft(request)
            if worker_peoplesoft:
                worker_peoplesoft_serializer = WorkerPeopleSoftSerializer(worker_peoplesoft, many=True)
                worker_peoplesoft = worker_peoplesoft_serializer.data
            else:
                raise ExceptionWorkerHcm('No se ha encontrado worker en peoplesoft')
            
            person_number_manager = worker_peoplesoft[0].get('supervisor_id')
            manager_hcm = self.get_worker_with_fake_request(request, person_number_manager)
            if manager_hcm:
                manager_hcm_serializer = WorkerHcmSerializer(manager_hcm)
                manager_hcm = manager_hcm_serializer.data

            request_person_number_worker = request.GET.get('personNumber', None)
            worker_hcm = self.get_worker_with_fake_request(request, request_person_number_worker)
            if worker_hcm:
                worker_hcm_serializer = WorkerHcmSerializer(worker_hcm)
                worker_hcm = worker_hcm_serializer.data

            res = self.update_manager_hcm(manager_hcm, worker_hcm, worker_peoplesoft[0].get('effdt'))
            return res
        except Exception as e:
            raise Exception(e) from e

    def update_manager_hcm(self, manager_hcm, worker_hcm, effdt):
        try:

            manger_lov = self.get_worker_lov(int(manager_hcm.get('person_id')))

            payload  = {
                "ManagerAssignmentNumber": manger_lov.get('AssignmentNumber'),
                "ManagerType": "LINE_MANAGER",
                "ActionCode": "MANAGER_CHANGE",
                "ReasonCode": None,
            }


            url_change_manager = worker_hcm.get('work_relationships')[0].get('assignment').get('manager_detail').get('link')

            response = self.global_service.generate_request(request=self.request, url=url_change_manager, body_data=payload, range_start_date=effdt,method='PATCH')

            return response
        except Exception as e:
            raise Exception(e) from e

    def get_worker_with_fake_request(self, request, person_number):
        fake_request = self.create_fake_request(request, person_number)
        worker = self.get_worker_hcm(fake_request)
        return worker