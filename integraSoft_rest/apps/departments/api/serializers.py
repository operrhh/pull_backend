from rest_framework import serializers
from apps.departments.models import Department
from rest_framework.utils.urls import replace_query_param, remove_query_param


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['dept_id', 'name', 'ccu_codigo_centro_costo']

class DepartmentHcmSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    totalResults = serializers.IntegerField(source='total_results')
    hasMore = serializers.BooleanField(source='has_more')
    next = serializers.SerializerMethodField()
    previous = serializers.SerializerMethodField()
    items = DepartmentSerializer(many=True)
    limit = serializers.IntegerField()
    url = serializers.CharField(max_length=100)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.pop('url', None)
        data.pop('limit', None)
        return data

    def get_next(self, obj):
        _next = obj.get('next') + 1 # Agregamos 1 para que el offset sea legible para el usuario

        if obj.get('has_more') == True:
            return replace_query_param(obj.get('url'), 'offset', _next)
        return None
    
    def get_previous(self, obj):
        _previous = obj.get('previous') + 1 # Agregamos 1 para que el offset sea legible para el usuario

        if _previous == 0:
            return None
        elif (_previous - obj.get('count')) <= 0:
            return remove_query_param(obj.get('url'), 'offset')
        elif (obj.get('has_more') == False):
            return replace_query_param(obj.get('url'), 'offset', (_previous - obj.get('limit')))
        else:
            return replace_query_param(obj.get('url'), 'offset', (_previous - obj.get('count')))