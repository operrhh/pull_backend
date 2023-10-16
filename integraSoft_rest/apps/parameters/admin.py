from django.contrib import admin
from apps.parameters.models import Parameter, ParameterType

# Register your models here.
admin.site.register(Parameter)
admin.site.register(ParameterType)