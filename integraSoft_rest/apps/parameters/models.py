from django.db import models
from django.utils import timezone
from datetime import timedelta

# Create your models here.
from django.db import models

class Parameter(models.Model):
    Enabled = models.BooleanField(default=True)
    ValidityStartDate = models.DateTimeField( default=timezone.now )
    ValidityEndDate = models.DateTimeField( default= timezone.now() + timedelta(days=365))
    FilterField1 = models.TextField(blank=True)
    FilterField2 = models.TextField(blank=True)
    FilterField3 = models.TextField(blank=True)
    Value = models.TextField(blank=False, null=False)
    ParameterTypeId = models.ForeignKey('ParameterType', on_delete=models.CASCADE, db_column='ParameterTypeId')

    class Meta:
        db_table = 'Parameter'

class ParameterType(models.Model):
    Description = models.CharField(blank=False, null=False, max_length=255)

    class Meta:
        db_table = 'ParameterType'