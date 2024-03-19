from .workerServicePeopleSoft import WorkerServicePeopleSoft
from .workerServiceWsdl import WorkerServiceWsdl
from typing import List
from ..models import WorkerFormatComparison


# Clase que se encarga de comparar los trabajadores de peoplesoft con los trabajadores de wsdl
class WorkerServiceComparison:
    def __init__(self):
        self.worker_service_peoplesoft = WorkerServicePeopleSoft()
        self.worker_service_wsdl = WorkerServiceWsdl()

    def get_workers_comparison(self, request):
        try:
            workers_peoplesoft = self.worker_service_peoplesoft.get_workers_peoplesoft(request=request)
            workers_wsdl = self.worker_service_wsdl.get_workers_wsdl()

            workers_peoplesoft_format = self.format_workers_by_peoplesoft(workers_peoplesoft)
            workers_wsdl_format = self.format_workers_by_wsdl(workers_wsdl)

            res = self.compare_workers(workers_peoplesoft_format, workers_wsdl_format, 'peoplesoft')

            return res
        except Exception as e:
            raise Exception(e) from e

    def format_workers_by_peoplesoft(self, workers: list):
        try:
            new_workers = []
            for worker in workers:
                wr = WorkerFormatComparison(
                    person_number = worker['emplid'],
                    name = worker['name'],
                    email = worker['email'],
                    address1 = worker['address1'],
                    city = worker['city']
                )
                new_workers.append(wr)

            return new_workers
        except Exception as e:
            raise Exception(e) from e

    def format_workers_by_wsdl(self, workers: list):
        try:
            new_workers = []
            workers = workers['result']
            for worker in workers:

                name_format = self.get_complete_name(worker['first_name'], worker['last_name'], worker['middle_names'])

                wr = WorkerFormatComparison(
                    person_number = worker['person_number'],
                    name = name_format,
                    email = worker['email_emplid'],
                    address1 = worker['address_line_1'],
                    city = worker['town_or_city']
                )
                new_workers.append(wr)

            return new_workers
        except Exception as e:
            raise Exception(e) from e

    def get_complete_name(self, first_name: str, last_name: str, middle_names: str):
        
        if first_name == None:
            first_name = ''
        else:
            first_name = first_name.split(' ')

        if last_name == None:
            last_name = ''
        else:
            last_name = last_name.split(' ')
        
        if middle_names == None:
            middle_names = ''
        else:
            middle_names = middle_names.split(' ')

        first_name = self.format_name(first_name)
        last_name = self.format_name(last_name)
        middle_names = self.format_name(middle_names)
        complete_name = f"{first_name}{last_name}{middle_names}"

        return complete_name

    def format_name(self, list_name: list):
        clean_name = ''
        for name in list_name:
            if name != '':
                clean_name += f"{name} "
        return clean_name

    def compare_workers(self, workers_peoplesoft: List[WorkerFormatComparison], workers_wsdl: List[WorkerFormatComparison], main: str):
        try:
            i = 0
            c = 0
            res = {}

            list_personal_data = []
            list_work_relationship = []
            list_worker_not_found = []

            if main == 'peoplesoft':

                # Crea un diccionario con los atributos person_number de los objetos de workers_wsdl
                wsdl_dic = {getattr(obj,"person_number"):obj for obj in workers_wsdl}


                for wr_ps in workers_peoplesoft:
                    # Obtiene el valor del atributo person_number del objeto wr_ps
                    person_number = getattr(wr_ps, "person_number")

                    # Si el valor de person_number se encuentra en el diccionario wsdl_dic
                    if person_number in wsdl_dic:
                        i += 1

                        # Comparamos los valores de la categoria Datos Personales

                        res_personal_data = self.compare_workers_personal_data(wr_ps, wsdl_dic[person_number])

                        if res_personal_data != None:
                            list_personal_data.append(res_personal_data)
                        else:
                            c += 1
                    else:
                        not_found = {
                            'person_number': person_number
                        }

                        list_worker_not_found.append(not_found)

                res = {
                    'category':{
                        'personal_data': {
                            "count": len(list_personal_data),
                            "data": list_personal_data
                        },
                        'work_relationship': {
                            "count": len(list_work_relationship),
                            "data": list_work_relationship
                        }
                    },
                    'not_found': {
                        "count": len(list_worker_not_found),
                        "data": list_worker_not_found
                    }
                }

                print('Total de usuarios Peoplesoft: ', len(workers_peoplesoft))
                print('Total de usuarios Wsdl: ', len(workers_wsdl))
                print('Total de usuarios PeopleSoft encontrados en Cloud : ', i)
                print('Total de usuarios PeopleSoft no encontrados en Cloud : ', len(list_worker_not_found))
                print('Total de usuarios PeopleSoft encontrados en Cloud sin diferencias : ', c)
                print('Total de usuarios PeopleSoft encontrados en Cloud con diferencias : ', len(list_personal_data))
                
                

            # if main == 'wsdl':
            #     peoplesoft_dic = {getattr(obj,"person_number"):obj for obj in workers_peoplesoft}
            #     for wr_wsdl in workers_wsdl:
            #         person_number = getattr(wr_wsdl, "person_number")
            #         if person_number in peoplesoft_dic:
            #             i += 1
            #             print(f'{i} | {person_number}')

            return res
        except Exception as e:
            raise Exception(e) from e

    def compare_workers_personal_data(self, worker_peoplesoft: WorkerFormatComparison, worker_wsdl: WorkerFormatComparison):
        try:
            print('')
            print('===================================')
            print(f'Person number : {worker_peoplesoft.person_number}')
            print('===================================')

            # if worker_peoplesoft.person_number == '16770555-3':
            #     print('')
            
            name = self.compare_workers_personal_data_names(worker_peoplesoft.name, worker_wsdl.name)
            email = self.compare_workers_personal_data_email(worker_peoplesoft.email, worker_wsdl.email)
            address = self.compare_workers_personal_data_address(worker_peoplesoft.address1, worker_wsdl.address1)
            city = self.compare_workers_personal_data_city(worker_peoplesoft.city, worker_wsdl.city)

            if name == False or email == False or address == False or city == False:
                personal_data = {
                    'person_number': worker_peoplesoft.person_number,
                    'name': name,
                    'email': email,
                    'address': address,
                    'city': city
                }
                return personal_data
            else:
                return None

        except Exception as e:
            raise Exception(e) from e

    def compare_workers_personal_data_city(self, city_peoplesoft: str, city_wsdl: str):
        try:        
            # if city_peoplesoft != None:
            #     city_peoplesoft = city_peoplesoft.replace(' ', '').upper()
            #     if city_peoplesoft == '':
            #         city_peoplesoft = None
            # if city_wsdl != None:
            #     city_wsdl = city_wsdl.replace(' ', '').upper()
            #     if city_wsdl == '':
            #         city_wsdl = None

            # Limpiar y convertir las ciudades a mayúsculas
            city_peoplesoft = city_peoplesoft.strip().upper() if city_peoplesoft is not None else None
            city_wsdl = city_wsdl.strip().upper() if city_wsdl is not None else None

            city_peoplesoft = None if city_peoplesoft == '' else city_peoplesoft
            city_wsdl = None if city_wsdl == '' else city_wsdl

            if city_peoplesoft == city_wsdl :
                print('Las ciudades coinciden')
            else:
                print('Las ciudades no coinciden')

            print('Peoplesoft: ', city_peoplesoft)
            print('Wsdl      : ', city_wsdl)
            print('-----------------------------------')

            return city_peoplesoft == city_wsdl
        except Exception as e:
            raise Exception(e) from e

    def compare_workers_personal_data_address(self, address_peoplesoft: str, address_wsdl: str):
        try:
            address_peoplesoft = address_peoplesoft.replace(' ', '').upper()
            address_wsdl = address_wsdl.replace(' ', '').upper()

            if address_peoplesoft == address_wsdl:
                print('Las direcciones coinciden')
                print('Peoplesoft: ', address_peoplesoft)
                print('Wsdl      : ', address_wsdl)
                print('-----------------------------------')
                return True
            else:
                print('Las direcciones no coinciden')
                print('Peoplesoft: ', address_peoplesoft)
                print('Wsdl      : ', address_wsdl)
                print('-----------------------------------')
                return False
        except Exception as e:
            raise Exception(e) from e

    def compare_workers_personal_data_email(self, email_peoplesoft: str, email_wsdl: str):
        try:
            if email_peoplesoft == email_wsdl:
                print('Los email coinciden')
                print('Peoplesoft: ', email_peoplesoft)
                print('Wsdl      : ', email_wsdl)
                print('-----------------------------------')
                return True
            else:
                print('Los email no coinciden')
                print('Peoplesoft: ', email_peoplesoft)
                print('Wsdl      : ', email_wsdl)
                print('-----------------------------------')
                return False

        except Exception as e:
            raise Exception(e) from e

    def compare_workers_personal_data_names(self, name_peoplesoft: str, name_wsdl: str):
        try:
            name_peoplesoft = name_peoplesoft.replace(' ', '').upper()
            name_wsdl = name_wsdl.replace(' ', '').upper()

            if name_peoplesoft == name_wsdl:
                print('Los nombres coinciden')
                print('Peoplesoft: ', name_peoplesoft)
                print('Wsdl      : ', name_wsdl)
                print('-----------------------------------')
                return True
            else:
                print('Los nombres no coinciden')
                print('Peoplesoft: ', name_peoplesoft)
                print('Wsdl      : ', name_wsdl)
                print('-----------------------------------')
                return False

        except Exception as e:
            raise Exception(e) from e