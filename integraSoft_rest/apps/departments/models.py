from django.db import models

class Department(models.Model):
    dept_id = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    ccu_codigo_centro_costo = models.CharField(max_length=50)

    def __init__(self, dept_id=None, name=None, ccu_codigo_centro_costo=None):
        self.dept_id = dept_id
        self.name = name
        self.ccu_codigo_centro_costo = ccu_codigo_centro_costo

    def __str__(self):
        return self.name