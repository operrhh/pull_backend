from rest_framework.pagination import PageNumberPagination
from apps.parameters.models import Parameter, ParameterType

class CustomPaginationPeopleSoft(PageNumberPagination):

    def __init__(self):
        super().__init__()
        self.setup_parameters()

    def setup_parameters(self):
        # Obtener el ID del tipo de parámetro para 'size_request'
        parameter_type_id = ParameterType.objects.filter(Description='size_request').values_list('id', flat=True).first()

        # Obtener el tamaño de la solicitud de PeopleSoft de la tabla de parámetros
        parameter = Parameter.objects.filter(
            ParameterTypeId=parameter_type_id,
            Enabled=True,
            FilterField1='size_request',
            FilterField2='peoplesoft',
            FilterField3='worker'
        ).first()
        
        # Configurar el tamaño de la página
        if parameter:
            self.page_size = int(parameter.Value)  # Tamaño de la página
        else:
            # Si no se encuentra el parámetro, usar un valor predeterminado
            self.page_size = 10  # Valor predeterminado

        self.page_size_query_param = 'page_size'
        self.max_page_size = 1000  # Número máximo de elementos por página