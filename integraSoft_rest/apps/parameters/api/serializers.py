from rest_framework import serializers
from apps.parameters.models import Parameter, ParameterType

class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = '__all__'
    
    def create(self, validated_data):
        parameter = Parameter(**validated_data)
        parameter.save()
        return parameter
    
    def update(self, instance, validated_data):
        update_parameter = super().update(instance, validated_data)
        update_parameter.save()
        return update_parameter

class ParameterTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParameterType
        fields = '__all__'
    
    def create(self, validated_data):
        parameterType = ParameterType(**validated_data)
        parameterType.save()
        return parameterType
    
    def update(self, instance, validated_data):
        update_parameterType = super().update(instance, validated_data)
        update_parameterType.save()
        return update_parameterType