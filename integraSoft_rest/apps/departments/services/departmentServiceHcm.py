from ...services.globalService import GlobalService
from ...parameters.models import Parameter, ParameterType
from ..models import Department
from ...utils import log_entry


class DepartmentServiceHcm():
    def __init__(self):
        self.dic_parameter_type = {param.Description: param.id for param in ParameterType.objects.all()}
        self.dic_url = {param.FilterField3: param.Value for param in Parameter.objects  .filter(ParameterTypeId=self.dic_parameter_type.get('url'))
                                                                                        .filter(Enabled=True)
                                                                                        .filter(FilterField1='url')
                                                                                        .filter(FilterField2='hcm')}
        self.global_service = GlobalService()

        self.departments: list[Department] = []

        self.offset: int = 0
        self.limit: int = 50 # Número de elementos por página
        self.total_results: int = 0
        self.has_more: bool = True
        self.contador_registros: int = -1
        self.conditions_added = False

        self.last_offset: int = 0

    def get_departments(self,request):
        params = self.params_definition(request)
        try:
            response = self.global_service.generate_request(request=request, url=self.dic_url.get('department'), params=params)
            if response:
                if response.get('count') != 0:
                    items = response.get('items')
                    self.has_more = response.get('hasMore')
                    self.convert_departments(items)
                else:
                    raise Exception('No se encontraron departments')
            else:
                raise Exception('Error al consultar departments')

            res = {
                'items': self.departments,
                'next': self.contador_registros if self.has_more else 0,
                'count': len(self.departments),                
                'has_more': self.has_more,
                'limit': self.limit,
                'url': self.get_link_request(request)
            }

            log_entry(request.user, 'INFO', 'GET Departments hcm', 'Se ha consultado Departments exitosamente')

            return res
        except Exception as e:
            raise Exception(e) from e
        
    def get_link_request(self,request):
        return request.build_absolute_uri()

    def params_definition(self, request):
        self.offset = int(request.query_params.get('offset', self.offset))
        self.offset = self.offset - 1

        self.last_offset = self.offset

        if self.offset != 0:
            self.contador_registros = self.offset
            self.offset += 1

        name = request.query_params.get('name') if request.query_params.get('name') else None

        if name:
            query_name = f"upper(Name) like '%{name.upper()}%'"
            self.conditions_added = True

        query = "SetCode in ('CHILE','GRALS') AND departmentsEFF.CategoryCode='DEPARTMENT' AND ActiveStatus='A'"

        if self.conditions_added:
            query += f" AND {query_name}"

        params = {}
        params['q'] = query
        params['fields'] = 'OrganizationId,Name,departmentsDFF'
        params['onlyData'] = 'true'
        params['totalResults'] = 'true'
        params['limit'] = self.limit
        params['offset'] = self.offset
        return params

    def convert_departments(self, items):
        for item in items:
            department = Department()
            department.dept_id = item.get('OrganizationId')
            department.name = item.get('Name')
            department.ccu_codigo_centro_costo = self.filter_centro_costo(item)
            self.departments.append(department)
            self.contador_registros += 1

            # print(f'{self.contador_registros} - {department.dept_id} - {department.name} - {department.ccu_codigo_centro_costo}')
    
    def filter_centro_costo(self, department):
        centro_costo = department.get('departmentsDFF').get('items')[0].get('ccuCodigoCentroCosto')
        if centro_costo == None:
            centro_costo = department.get('Name').split(' ')[0]

        return centro_costo