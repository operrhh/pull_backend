from django.db import connections
import cx_Oracle
from ..custom_exceptions import ExceptionDepartmentPeopleSoft
from ..models import Department

class DepartmentServicePeopleSoft:

    def __init__(self):

        self.departments: list[Department] = []

    def get_departments(self, request):

        name = request.query_params.get('name', None)

        try:
            with connections['people_soft'].cursor() as cursor:
                out_cur = cursor.connection.cursor()
                cursor.callproc("SP_GET_DEPARTMENTS", [out_cur, name])
                if out_cur:
                    items = [res for res in out_cur]
                    if len(items) > 0:
                        self.convert_data(items)
                        return self.departments
                    else:
                        raise ExceptionDepartmentPeopleSoft('No se han encontrado departments')
                else:
                    raise ExceptionDepartmentPeopleSoft('No se han encontrado departments')
        except cx_Oracle.DatabaseError as e:
            print('Error de la base de datos:', e)

    def create_department_data(self, data):
        department = Department(
                        dept_id=data[0], 
                        name=data[1]
                    )
        self.departments.append(department)

    def validate_none(self,obj):
        if isinstance(obj, None.__class__):
            return True

    def convert_data(self, data):
        return [self.create_department_data(result) for result in data]