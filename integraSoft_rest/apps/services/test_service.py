from apps.parameters.models import Parameter

class GlobalService:
    def __init__(self):
        # self.dic_params = Parameter.objects.filter(FilterField1='authorization').filter(FilterField2='hcm').filter(FilterField3 = 'user').first()
        self.dic_user = {param.FilterField3: param.Value for param in Parameter.objects.filter(FilterField1='authorization').filter(FilterField2='hcm').filter(FilterField3 = 'user')}
        self.dic_pass = {param.FilterField3: param.Value for param in Parameter.objects.filter(FilterField1='authorization').filter(FilterField2='hcm').filter(FilterField3 = 'pass')}
    
    def generate_request(self):
        print(self.dic_user)
        print(self.dic_pass)