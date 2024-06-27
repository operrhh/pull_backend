from rest_framework import status

import requests
import base64
import cx_Oracle
from ..parameters.models import Parameter, ParameterType
from ..utils import log_entry
from datetime import datetime

class GlobalService:
    def __init__(self):
        self.dic_parameter_type = {param.Description: param.id for param in ParameterType.objects.all()}
        self.dic_authorization = {param.FilterField3: param.Value for param in Parameter.objects.filter(ParameterTypeId=self.dic_parameter_type.get('authorization'))
                                                                                                .filter(Enabled=True)
                                                                                                .filter(FilterField1='authorization')
                                                                                                .filter(FilterField2='hcm')}
        self.dic_people_soft = {param.FilterField3: param.Value for param in Parameter.objects  .filter(ParameterTypeId=self.dic_parameter_type.get('authorization'))
                                                                                                .filter(Enabled=True)
                                                                                                .filter(FilterField1='authorization')
                                                                                                .filter(FilterField2='people_soft')}

    def generate_request(self, request, url, params={}, body_data={}, method='', range_start_date='', version = ''):
        credentials = f"{self.dic_authorization.get('user')}:{self.dic_authorization.get('pass')}"
        encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
        
        if version == '':
            version = '4'

        headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/vnd.oracle.adf.resourceitem+json",
            "REST-Framework-Version": version,
        }
        if body_data:

            if method == 'POST':
                #Obtenemos fecha actual
                now = datetime.now()
                # date_time = now.strftime("%Y-%m-%d")

                headers['Effective-of'] = f"RangeStartDate={range_start_date};"
                try:
                    response = requests.post(url, headers=headers, json=body_data)

                    if response.status_code == 201:
                        return response.json()
                    else:
                        response.raise_for_status()
                except requests.exceptions.RequestException as e:
                    raise Exception(response.text) from e
                
            if method == 'PATCH':
                headers['Effective-of'] = f"RangeMode=UPDATE;RangeStartDate={range_start_date}"
                try:
                    response = requests.patch(url, headers=headers, json=body_data)

                    if response.status_code == 200:
                        return response.json()
                    else:
                        return response.raise_for_status()
                except requests.exceptions.RequestException as e:
                    raise Exception(response.text) from e
        else:
            try:
                response = requests.get(url, headers=headers, params=params)
                log_entry(request.user, 'INFO', 'globalService', 'URL: ' + response.url)
                if response.status_code == 200:
                    return response.json()
                else:
                    response.raise_for_status()
            except requests.exceptions.RequestException as e:
                raise Exception(response.text) from e