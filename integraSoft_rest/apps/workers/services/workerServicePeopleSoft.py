from django.db import connections
import cx_Oracle
import json
from datetime import datetime
from ...utils import log_entry

from ..custom_exceptions import ExceptionWorkerPeopleSoft

class WorkerServicePeopleSoft:

    def __init__(self):
        self.field_names = [
            'emplid', 'birthdate', 'birthplace', 'country_nm_format', 'name', 'name_prefix', 'last_name', 'first_name',
            'middle_name', 'second_last_name', 'country', 'address1', 'address2', 'address3', 'address4', 'city',
            'county', 'state', 'email', 'email_type', 'home_phone', 'national_id_type', 'national_id', 'sex', 'mar_status', 'highest_educ_lvl',
            'orig_hire_dt', 'per_org', 'cmpny_seniority_dt', 'service_dt', 'last_increase_dt', 'business_title',
            'effdt', 'hire_dt', 'supervisor_id', 'business_unit', 'business_unit_descr', 'deptid','dept_descr', 'jobcode', 'action',
            'action_dt', 'action_reason', 'location', 'job_entry_dt', 'dept_entry_dt', 'reg_temp', 'full_part_time',
            'company', 'paygroup', 'empl_type', 'holiday_schedule', 'std_hours', 'reg_region', 'jobtitle', 'jobtitle_abbrv',
            'deptname', 'deptname_abbrv', 'rehire_dt', 'work_phone', 'nid_country'
        ]

    def get_workers_peoplesoft(self, request):

        person_number = request.query_params.get('personNumber', None)
        first_name = request.query_params.get('firstName', None)
        last_name = request.query_params.get('lastName', None)
        department = request.query_params.get('department', None)

        try:
            with connections['people_soft'].cursor() as cursor:
                out_cur = cursor.connection.cursor()
                cursor.callproc("SP_GET_WORKERS", [out_cur, person_number, first_name, last_name, department])
                if out_cur:
                    items = [res for res in out_cur]
                    if len(items) > 0:
                        workers = self.convert_data(items)

                        log_entry(request.user, 'INFO', 'get_workers_peoplesoft', 'Se ha consultado workers exitosamente')

                        return workers
                    else:
                        raise ExceptionWorkerPeopleSoft('No se han encontrado workers')
                else:
                    raise ExceptionWorkerPeopleSoft('No se han encontrado workers')
        except cx_Oracle.DatabaseError as e:
            print('Error de la base de datos:', e)

    def get_worker_peoplesoft(self, request, pk):
        try:
            with connections['people_soft'].cursor() as cursor:
                out_cur = cursor.connection.cursor()
                cursor.callproc("SP_GET_WORKER", [out_cur, pk])

                if out_cur:
                    items = out_cur.fetchone()
                    worker = self.convert_data(items)

                    log_entry(request.user, 'INFO', 'get_worker_peoplesoft', 'Se ha consultado worker exitosamente')

                    return worker
                else:
                    raise ExceptionWorkerPeopleSoft('No se han encontrado workers')
        except cx_Oracle.DatabaseError as e:
            print('Error de la base de datos:', e)

    def update_worker_peoplesoft(self, request):
        # Crear un diccionario con los nombres de los atributos y sus valores
        params = {field: request.data.get(field, None) for field in self.field_names}
        try:
            with connections['people_soft'].cursor() as cursor:
                cursor.callproc("SP_INSERT_WORKER", [[params[param] for param in self.field_names]])
        except cx_Oracle.DatabaseError as e:
            print('Error de la base de datos:', e)

    def create_worker_data(self, data):
        worker_data = {}
        for i, field_name in enumerate(self.field_names):
            if not self.validate_none(data[i]):
                if field_name in ['birthdate', 'birthplace', 'orig_hire_dt', 'cmpny_seniority_dt', 'service_dt',
                                  'last_increase_dt', 'effdt', 'hire_dt', 'action_dt', 'job_entry_dt', 'dept_entry_dt', 'rehire_dt'] and not isinstance(data[i], str):
                    worker_data[field_name] = self.serialize_datetime(data[i])
                else:
                    worker_data[field_name] = data[i]
            else:
                worker_data[field_name] = None
        return worker_data

    def convert_data(self, data):
        if isinstance(data, list):
            return [self.create_worker_data(result) for result in data]
        else:
            return self.create_worker_data(data)

    def validate_none(self,obj):
        if isinstance(obj, None.__class__):
            return True

    def serialize_datetime(self,obj):
        if isinstance(obj, datetime):
            #return obj.isoformat()
            return obj.strftime('%Y-%m-%d')
        raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")