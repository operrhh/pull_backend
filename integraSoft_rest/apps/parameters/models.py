from django.db import models
from django.utils import timezone
from datetime import timedelta

# Create your models here.
from django.db import models

def default_validity_end_date():
    return timezone.now() + timedelta(days=365)

class Parameter(models.Model):
    Enabled = models.BooleanField(default=True)
    ValidityStartDate = models.DateTimeField(default=timezone.now)
    ValidityEndDate = models.DateTimeField(default=default_validity_end_date)
    FilterField1 = models.CharField(max_length=100, blank=True)
    FilterField2 = models.CharField(max_length=100, blank=True)
    FilterField3 = models.CharField(max_length=100, blank=True)
    Value = models.CharField(max_length=400,blank=False, null=False)
    ParameterTypeId = models.ForeignKey('ParameterType', on_delete=models.CASCADE, db_column='ParameterTypeId')

    class Meta:
        db_table = 'Parameter'

class ParameterType(models.Model):
    Description = models.TextField(blank=False, null=False)

    class Meta:
        db_table = 'ParameterType'