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
                    address2= worker['address2'],
                    city = worker['city'],
                    location_code = worker['location'],
                    codigo_centro_costo = worker['deptid']
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
                    address2 = worker['address_line_2'],
                    city = worker['town_or_city'],
                    location_code = worker['hdr_internal_location_code'],
                    codigo_centro_costo = worker['ccu_codigo_centro_costo']
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
            a = 0
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

                        # Comparamos los valores de la categoria Relación Laboral
                        res_work_relationship = self.compare_workers_work_relationship(wr_ps, wsdl_dic[person_number])

                        if res_work_relationship != None:
                            list_work_relationship.append(res_work_relationship)
                        else:
                            a += 1

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
                print('Total de usuarios PeopleSoft encontrados en Cloud sin diferencias PERSONAL_DATA : ', c)
                print('Total de usuarios PeopleSoft encontrados en Cloud sin diferencias WORK_RELATIONSHIP : ', a)
                print('Total de usuarios PeopleSoft encontrados en Cloud con diferencias PERSONAL_DATA: ', len(list_personal_data))
                print('Total de usuarios PeopleSoft encontrados en Cloud con diferencias WORK_RELATIONSHIP: ', len(list_work_relationship))

                
                

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


    # Compara los datos personales de los trabajadores

    def compare_workers_personal_data(self, worker_peoplesoft: WorkerFormatComparison, worker_wsdl: WorkerFormatComparison):
        try:
            # print('')
            # print('===================================')
            # print(f'Person number : {worker_peoplesoft.person_number}')
            # print('===================================')

            # if worker_peoplesoft.person_number == '16770555-3':
            #     print('')
            
            name = self.compare_workers_personal_data_names(worker_peoplesoft.name, worker_wsdl.name)
            email = self.compare_workers_personal_data_email(worker_peoplesoft.email, worker_wsdl.email)
            address_1 = self.compare_workers_personal_data_address(worker_peoplesoft.address1, worker_wsdl.address1)
            address_2 = self.compare_workers_personal_data_address(worker_peoplesoft.address2, worker_wsdl.address2)
            city = self.compare_workers_personal_data_city(worker_peoplesoft.city, worker_wsdl.city)

            if name == False or email == False or address_1 == False or address_2 == False or city == False:
                personal_data = {
                    'person_number': worker_peoplesoft.person_number,
                    'name': name,
                    'name_peoplesoft': worker_peoplesoft.name,
                    'name_wsdl': worker_wsdl.name,
                    'email': email,
                    'email_peoplesoft': worker_peoplesoft.email,
                    'email_wsdl': worker_wsdl.email,
                    'address_1': address_1,
                    'address_1_peoplesoft': worker_peoplesoft.address1,
                    'address_1_wsdl': worker_wsdl.address1,
                    'address_2': address_2,
                    'address_2_peoplesoft': worker_peoplesoft.address2,
                    'address_2_wsdl': worker_wsdl.address2,
                    'city': city,
                    'city_peoplesoft': worker_peoplesoft.city,
                    'city_wsdl': worker_wsdl.city,
                }
                return personal_data
            else:
                return None

        except Exception as e:
            raise Exception(e) from e

    def compare_workers_personal_data_city(self, city_peoplesoft: str, city_wsdl: str):
        try:
            city_peoplesoft = city_peoplesoft.strip().replace(' ', '').upper() if city_peoplesoft is not None else None
            city_wsdl = city_wsdl.strip().replace(' ', '').upper() if city_wsdl is not None else None

            city_peoplesoft = None if city_peoplesoft == '' else city_peoplesoft
            city_wsdl = None if city_wsdl == '' else city_wsdl

            # if city_peoplesoft == city_wsdl :
            #     print('Las ciudades coinciden')
            # else:
            #     print('Las ciudades no coinciden')

            # print('Peoplesoft: ', city_peoplesoft)
            # print('Wsdl      : ', city_wsdl)
            # print('-----------------------------------')

            return city_peoplesoft == city_wsdl
        except Exception as e:
            raise Exception(e) from e

    def compare_workers_personal_data_address(self, address_peoplesoft: str, address_wsdl: str):
        try:
            address_peoplesoft = address_peoplesoft.strip().replace(' ', '').upper() if address_peoplesoft is not None else None
            address_wsdl = address_wsdl.strip().replace(' ', '').upper() if address_wsdl is not None else None

            address_peoplesoft = None if address_peoplesoft == '' else address_peoplesoft
            address_wsdl = None if address_wsdl == '' else address_wsdl

            # if address_peoplesoft == address_wsdl:
            #     print('Las direcciones coinciden')
            # else:
            #     print('Las direcciones no coinciden')

            # print('Peoplesoft: ', address_peoplesoft)
            # print('Wsdl      : ', address_wsdl)
            # print('-----------------------------------')

            return address_peoplesoft == address_wsdl
        except Exception as e:
            raise Exception(e) from e

    def compare_workers_personal_data_email(self, email_peoplesoft: str, email_wsdl: str):
        try:
            # if email_peoplesoft == email_wsdl:
            #     print('Los correos coinciden')
            # else:
            #     print('Los correos no coinciden')
            
            # print('Peoplesoft: ', email_peoplesoft)
            # print('Wsdl      : ', email_wsdl)
            # print('-----------------------------------')

            return email_peoplesoft == email_wsdl

        except Exception as e:
            raise Exception(e) from e

    def compare_workers_personal_data_names(self, name_peoplesoft: str, name_wsdl: str):
        try:
            name_peoplesoft = name_peoplesoft.replace(' ', '').upper()
            name_wsdl = name_wsdl.replace(' ', '').upper()

            # if name_peoplesoft == name_wsdl:
            #     print('Los nombres coinciden')
            # else:
            #     print('Los nombres no coinciden')

            
            # print('Peoplesoft: ', name_peoplesoft)
            # print('Wsdl      : ', name_wsdl)
            # print('-----------------------------------')

            return name_peoplesoft == name_wsdl

        except Exception as e:
            raise Exception(e) from e


    # Compara la relacion laboral de los trabajadores

    def compare_workers_work_relationship(self, worker_peoplesoft: WorkerFormatComparison, worker_wsdl: WorkerFormatComparison):
        try:
            location_code = self.compare_workers_work_relationship_location_code(worker_peoplesoft.location_code, worker_wsdl.location_code)
            codigo_centro_costo = self.compare_workers_work_relationship_codigo_centro_costo(worker_peoplesoft.ccu_codigo_centro_costo, worker_wsdl.ccu_codigo_centro_costo)

            if location_code == False or codigo_centro_costo == False:
                work_relationship = {
                    'person_number': worker_peoplesoft.person_number,
                    'location_code': location_code,
                    'location_code_peoplesoft': worker_peoplesoft.location_code,
                    'location_code_wsdl': worker_wsdl.location_code,
                    'codigo_centro_costo': codigo_centro_costo,
                    'codigo_centro_costo_peoplesoft': worker_peoplesoft.ccu_codigo_centro_costo,
                    'codigo_centro_costo_wsdl': worker_wsdl.ccu_codigo_centro_costo,
                }
                return work_relationship
            else:
                return None
        except Exception as e:
            raise Exception(e) from e

    def compare_workers_work_relationship_location_code(self, location_code_peoplesoft: str, location_code_wsdl: str):
        try:
            location_code_peoplesoft = location_code_peoplesoft.strip().replace(' ', '').upper() if location_code_peoplesoft is not None else None
            location_code_wsdl = location_code_wsdl.strip().replace(' ', '').upper() if location_code_wsdl is not None else None

            location_code_peoplesoft = None if location_code_peoplesoft == '' else location_code_peoplesoft
            location_code_wsdl = None if location_code_wsdl == '' else location_code_wsdl

            # if location_code_peoplesoft == location_code_wsdl:
            #     print('Los codigos de localizacion coinciden')
            # else:
            #     print('Los codigos de localizacion no coinciden')

            # print('Peoplesoft: ', location_code_peoplesoft)
            # print('Wsdl      : ', location_code_wsdl)
            # print('-----------------------------------')

            return location_code_peoplesoft == location_code_wsdl
        except Exception as e:
            raise Exception(e) from e

    def compare_workers_work_relationship_codigo_centro_costo(self, codigo_centro_costo_peoplesoft: str, codigo_centro_costo_wsdl: str):
        try:
            codigo_centro_costo_peoplesoft = codigo_centro_costo_peoplesoft.strip().replace(' ', '').upper() if codigo_centro_costo_peoplesoft is not None else None
            codigo_centro_costo_wsdl = codigo_centro_costo_wsdl.strip().replace(' ', '').upper() if codigo_centro_costo_wsdl is not None else None

            codigo_centro_costo_peoplesoft = None if codigo_centro_costo_peoplesoft == '' else codigo_centro_costo_peoplesoft
            codigo_centro_costo_wsdl = None if codigo_centro_costo_wsdl == '' else codigo_centro_costo_wsdl

            if codigo_centro_costo_peoplesoft == codigo_centro_costo_wsdl:
                print(f'Los codigos de centro de costo coinciden: {codigo_centro_costo_peoplesoft} | {codigo_centro_costo_wsdl}')
            # else:
            #     print('Los codigos de centro de costo no coinciden')

            # print('Peoplesoft: ', codigo_centro_costo_peoplesoft)
            # print('Wsdl      : ', codigo_centro_costo_wsdl)
            # print('-----------------------------------')
            


            return codigo_centro_costo_peoplesoft == codigo_centro_costo_wsdl
        except Exception as e:
            raise Exception(e) from e

    def exist_worker(self, workers_ps, workers_wsdl):
        try:
            ps = '18558627-8'

            for worker_ps in workers_ps:
                if worker_ps.person_number == ps:
                    print('Exist in peoplesoft')
            
            for worker_wsdl in workers_wsdl:
                if worker_wsdl.person_number == ps:
                    print('Exist in wsdl')

        except Exception as e:
            raise Exception(e) from e
