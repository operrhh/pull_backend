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
                    person_number = str(worker['emplid']),
                    name = str(worker['name']),
                    email = str(worker['email']),
                    address1 = str(worker['address1']),
                    address2= str(worker['address2']),
                    city = str(worker['city']),
                    phone= str(worker['phone']),
                    location_code = str(worker['location']),
                    codigo_centro_costo = str(worker['deptid']),
                    job_name= str(worker['job_descr']),
                    job_code = str(worker['jobcode']),
                    manager_id= str(worker['supervisor_id'])
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
                codigo_centro_costo_format = self.get_codigos_centro_costo(worker['ccu_codigo_centro_costo'])

                wr = WorkerFormatComparison(
                    person_number = str(worker['person_number']),
                    name = str(name_format),
                    email = str(worker['email_emplid']),
                    address1 = str(worker['address_line_1']),
                    address2 = str(worker['address_line_2']),
                    city = str(worker['town_or_city']),
                    phone= ' ',
                    location_code = str(worker['hdr_internal_location_code']),
                    codigo_centro_costo = str(codigo_centro_costo_format),
                    job_name= str(worker['job_name']),
                    job_code = str(worker['job_code']),
                    manager_id= str(worker['id_jefe'])
                )

                new_workers.append(wr)

            return new_workers
        except Exception as e:
            raise Exception(e) from e

    def get_codigos_centro_costo(self, codigo:str):
        try:
            codigo_split = codigo.split('_')
            if len(codigo_split) == 2 and codigo_split[1] != '':
                return codigo_split[1]
            else:
                return None
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


    # Compara los trabajadores de peoplesoft con los trabajadores de wsdl

    def existe_duplicado_rut(self, lista_workers:WorkerFormatComparison):
        diccionario_ruts = {}
        for worker in lista_workers:
            if worker.person_number in diccionario_ruts:
                diccionario_ruts[worker.person_number].append(worker)
            else:
                diccionario_ruts[worker.person_number] = [worker]
        return {rut: workers for rut, workers in diccionario_ruts.items() if len(workers) > 1}

    def validando_duplicados(self, lista_workers:WorkerFormatComparison):
        duplicados_por_rut = self.existe_duplicado_rut(lista_workers)

        print('-------------------------------')
        if duplicados_por_rut:
            print("Se encontraron duplicados de Rut:")
            for rut, workers in duplicados_por_rut.items():
                print(f"Rut: {rut}, Objetos con este Rut: {[worker.name for worker in workers]}")
        else:
            print("No se encontraron duplicados de Rut.")
        print('-------------------------------\n')


    def compare_workers(self, workers_peoplesoft: List[WorkerFormatComparison], workers_wsdl: List[WorkerFormatComparison], main: str):
        try:
            i = 0
            c = 0
            a = 0
            res = {}

            not_consulted_wsdl = {}

            list_personal_data = []
            list_work_relationship = []
            list_worker_not_found = []

            if main == 'peoplesoft':

                # Crea un diccionario con los atributos person_number de los objetos de workers_wsdl
                wsdl_dic = {getattr(obj,"person_number"):obj for obj in workers_wsdl}


                for obj in wsdl_dic:
                    not_consulted_wsdl[obj] = False

                print('-------------------------------')
                print(f'Tamaño de  workers_wsdl {len(workers_wsdl)}')
                print(f'Tamaño de  workers_peoplesoft {len(workers_peoplesoft)}')
                print(f'Tamaño de  wsdl_dic {len(wsdl_dic)}')
                print(f'Tamaño de  not_consulted_wsdl {len(not_consulted_wsdl)}')
                print('-------------------------------\n')
                
                self.validando_duplicados(workers_wsdl)



                for wr_ps in workers_peoplesoft:
                    # Obtiene el valor del atributo person_number del objeto wr_ps
                    person_number_peoplesoft = getattr(wr_ps, "person_number")

                    # Si el valor de person_number se encuentra en el diccionario wsdl_dic
                    if person_number_peoplesoft in wsdl_dic:
                        i += 1

                        not_consulted_wsdl[person_number_peoplesoft] = True

                        # Comparamos los valores de la categoria Datos Personales
                        res_personal_data = self.compare_workers_personal_data(wr_ps, wsdl_dic[person_number_peoplesoft])
                        if res_personal_data != None:
                            list_personal_data.append(res_personal_data)
                        else:
                            c += 1

                        # Comparamos los valores de la categoria Relación Laboral
                        res_work_relationship = self.compare_workers_work_relationship(wr_ps, wsdl_dic[person_number_peoplesoft])
                        if res_work_relationship != None:
                            list_work_relationship.append(res_work_relationship)
                        else:
                            a += 1

                    else:
                        not_found = {
                            'person_number': person_number_peoplesoft
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

                print('-------------------------------')
                print('Total de usuarios Peoplesoft: ', len(workers_peoplesoft))
                print('Total de usuarios Wsdl: ', len(workers_wsdl))
                print('Total de usuarios PeopleSoft encontrados en Cloud : ', i)
                print('Total de usuarios PeopleSoft no encontrados en Cloud : ', len(list_worker_not_found))
                print('Total de usuarios PeopleSoft encontrados en Cloud sin diferencias PERSONAL_DATA : ', c)
                print('Total de usuarios PeopleSoft encontrados en Cloud sin diferencias WORK_RELATIONSHIP : ', a)
                print('Total de usuarios PeopleSoft encontrados en Cloud con diferencias PERSONAL_DATA: ', len(list_personal_data))
                print('Total de usuarios PeopleSoft encontrados en Cloud con diferencias WORK_RELATIONSHIP: ', len(list_work_relationship))
                print('-------------------------------\n')

                print('-------------------------------')
                print('Total de usuarios Cloud no existen en Peoplesoft')
                # Obtener solo los que tienen False
                for key in not_consulted_wsdl:
                    if not_consulted_wsdl[key] == False:
                        print(key)
                print('-------------------------------\n')
                
                

            # if main == 'wsdl':
            #     peoplesoft_dic = {getattr(obj,"person_number"):obj for obj in workers_peoplesoft}
            #     for wr_wsdl in workers_wsdl:
            #         person_number = getattr(wr_wsdl, "person_number")
            #         if person_number in peoplesoft_dic:
            #             i += 1
            #             print(f'{i} | {person_number}')

            return res
        except Exception as e:
            raise Exception(f" Location def_compare_workers | Error: {e}") from e


    # Compara los datos personales de los trabajadores

    def compare_workers_personal_data(self, worker_peoplesoft: WorkerFormatComparison, worker_wsdl: WorkerFormatComparison):
        try:

            if worker_wsdl.person_number == '12279172-6':
                print('Se encontro el trabajador 12279172-6 en wsdl')

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

            city_peoplesoft = self.clean_none(city_peoplesoft)
            city_wsdl = self.clean_none(city_wsdl)

            # city_peoplesoft = city_peoplesoft.strip().replace(' ', '').upper() if city_peoplesoft is not None else None
            # city_wsdl = city_wsdl.strip().replace(' ', '').upper() if city_wsdl is not None else None

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
            address_peoplesoft = self.clean_none(address_peoplesoft)
            address_wsdl = self.clean_none(address_wsdl)

            # address_peoplesoft = address_peoplesoft.strip().replace(' ', '').upper() if address_peoplesoft is not None else None
            # address_wsdl = address_wsdl.strip().replace(' ', '').upper() if address_wsdl is not None else None

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
            email_peoplesoft = self.clean_none(email_peoplesoft)
            email_wsdl = self.clean_none(email_wsdl)

            return email_peoplesoft == email_wsdl
            


            # if email_wsdl == 'No tiene correo':
            #     email_wsdl = None
            
            # if email_peoplesoft == 'NA':
            #     email_peoplesoft = None

            # if email_peoplesoft == None and email_wsdl == None:
            #     return False
            # else:
            #     return email_peoplesoft == email_wsdl

        except Exception as e:
            raise Exception(e) from e

    def compare_workers_personal_data_names(self, name_peoplesoft: str, name_wsdl: str):
        try:

            name_peoplesoft = self.clean_none(name_peoplesoft)
            name_wsdl = self.clean_none(name_wsdl)

            # name_peoplesoft = name_peoplesoft.replace(' ', '').upper()
            # name_wsdl = name_wsdl.replace(' ', '').upper()

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
            job_name = self.compare_workers_work_relationship_job_name(worker_peoplesoft.job_name, worker_wsdl.job_name)
            job_code = self.compare_workers_wort_relationship_job_code(worker_peoplesoft.job_code, worker_wsdl.job_code)
            manager_id = self.compare_workers_work_relationship_manager_id(worker_peoplesoft.manager_id, worker_wsdl.manager_id)

            if location_code == False or codigo_centro_costo == False:
                work_relationship = {
                    'person_number': worker_peoplesoft.person_number,
                    'location_code': location_code,
                    'location_code_peoplesoft': worker_peoplesoft.location_code,
                    'location_code_wsdl': worker_wsdl.location_code,
                    'codigo_centro_costo': codigo_centro_costo,
                    'codigo_centro_costo_peoplesoft': worker_peoplesoft.ccu_codigo_centro_costo,
                    'codigo_centro_costo_wsdl': worker_wsdl.ccu_codigo_centro_costo,
                    'job_name': job_name,
                    'job_name_peoplesoft': worker_peoplesoft.job_name,
                    'job_name_wsdl': worker_wsdl.job_name,
                    'job_code': job_code,
                    'job_code_peoplesoft': worker_peoplesoft.job_code,
                    'job_code_wsdl': worker_wsdl.job_code,
                    'manager_id': manager_id,
                    'manager_id_peoplesoft': worker_peoplesoft.manager_id,
                    'manager_id_wsdl': worker_wsdl.manager_id,
                }
                return work_relationship
            else:
                return None
        except Exception as e:
            raise Exception(e) from e

    def compare_workers_work_relationship_location_code(self, location_code_peoplesoft: str, location_code_wsdl: str):
        try:
            location_code_peoplesoft = self.clean_none(location_code_peoplesoft)
            location_code_wsdl = self.clean_none(location_code_wsdl)

            # location_code_peoplesoft = location_code_peoplesoft.strip().replace(' ', '').upper() if location_code_peoplesoft is not None else None
            # location_code_wsdl = location_code_wsdl.strip().replace(' ', '').upper() if location_code_wsdl is not None else None

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
            codigo_centro_costo_peoplesoft = self.clean_none(codigo_centro_costo_peoplesoft)
            codigo_centro_costo_wsdl = self.clean_none(codigo_centro_costo_wsdl)


            # codigo_centro_costo_peoplesoft = codigo_centro_costo_peoplesoft.strip().replace(' ', '').upper() if codigo_centro_costo_peoplesoft is not None else None
            # codigo_centro_costo_wsdl = codigo_centro_costo_wsdl.strip().replace(' ', '').upper() if codigo_centro_costo_wsdl is not None else None

            codigo_centro_costo_peoplesoft = None if codigo_centro_costo_peoplesoft == '' else codigo_centro_costo_peoplesoft
            codigo_centro_costo_wsdl = None if codigo_centro_costo_wsdl == '' else codigo_centro_costo_wsdl

            # if codigo_centro_costo_peoplesoft == codigo_centro_costo_wsdl:
            #     print(f'Los codigos de centro de costo coinciden: {codigo_centro_costo_peoplesoft} | {codigo_centro_costo_wsdl}')
            # else:
            #     print('Los codigos de centro de costo no coinciden')

            # print('Peoplesoft: ', codigo_centro_costo_peoplesoft)
            # print('Wsdl      : ', codigo_centro_costo_wsdl)
            # print('-----------------------------------')
            


            return codigo_centro_costo_peoplesoft == codigo_centro_costo_wsdl
        except Exception as e:
            raise Exception(e) from e

    def compare_workers_work_relationship_job_name(self, job_name_peoplesoft: str, job_name_wsdl: str):
        try:
            job_name_peoplesoft = self.clean_none(job_name_peoplesoft)
            job_name_wsdl = self.clean_none(job_name_wsdl)

            # job_name_peoplesoft = job_name_peoplesoft.strip().replace(' ', '').upper() if job_name_peoplesoft is not None else None
            # job_name_wsdl = job_name_wsdl.strip().replace(' ', '').upper() if job_name_wsdl is not None else None

            job_name_peoplesoft = None if job_name_peoplesoft == '' else job_name_peoplesoft
            job_name_wsdl = None if job_name_wsdl == '' else job_name_wsdl

            # if job_name_peoplesoft == job_name_wsdl:
            #     print('Los nombres de los cargos coinciden')
            # else:
            #     print('Los nombres de los cargos no coinciden')

            # print('Peoplesoft: ', job_name_peoplesoft)
            # print('Wsdl      : ', job_name_wsdl)
            # print('-----------------------------------')

            return job_name_peoplesoft == job_name_wsdl
        except Exception as e:
            raise Exception(e) from e

    def compare_workers_wort_relationship_job_code(self, job_code_peoplesoft: str, job_code_wsdl: str):
        try:
            job_code_peoplesoft = self.clean_none(job_code_peoplesoft)
            job_code_wsdl = self.clean_none(job_code_wsdl)

            # job_code_peoplesoft = job_code_peoplesoft.strip().replace(' ', '').upper() if job_code_peoplesoft is not None else None
            # job_code_wsdl = job_code_wsdl.strip().replace(' ', '').upper() if job_code_wsdl is not None else None

            job_code_peoplesoft = None if job_code_peoplesoft == '' else job_code_peoplesoft
            job_code_wsdl = None if job_code_wsdl == '' else job_code_wsdl

            # if job_code_peoplesoft == job_code_wsdl:
            #     print('Los codigos de los cargos coinciden')
            # else:
            #     print('Los codigos de los cargos no coinciden')

            # print('Peoplesoft: ', job_code_peoplesoft)
            # print('Wsdl      : ', job_code_wsdl)
            # print('-----------------------------------')

            return job_code_peoplesoft == job_code_wsdl
        except Exception as e:
            raise Exception(e) from e

    def compare_workers_work_relationship_manager_id(self, manager_id_peoplesoft: str, manager_id_wsdl: str):
        try:
            manager_id_peoplesoft = self.clean_none(manager_id_peoplesoft)
            manager_id_wsdl = self.clean_none(manager_id_wsdl)

            # manager_id_peoplesoft = manager_id_peoplesoft.strip().replace(' ', '').upper() if manager_id_peoplesoft is not None else None
            # manager_id_wsdl = manager_id_wsdl.strip().replace(' ', '').upper() if manager_id_wsdl is not None else None

            manager_id_peoplesoft = None if manager_id_peoplesoft == '' else manager_id_peoplesoft
            manager_id_wsdl = None if manager_id_wsdl == '' else manager_id_wsdl

            # if manager_id_peoplesoft == manager_id_wsdl:
            #     print('Los codigos de los jefes coinciden')
            # else:
            #     print('Los codigos de los jefes no coinciden')

            # print('Peoplesoft: ', manager_id_peoplesoft)
            # print('Wsdl      : ', manager_id_wsdl)
            # print('-----------------------------------')

            return manager_id_peoplesoft == manager_id_wsdl
        except Exception as e:
            raise Exception(e) from e


    def clean_none(self, value:str):
        value = value.strip().replace(' ', '').upper()

        if value == 'NONE':
            return None
        elif value == None:
            return None
        elif value == '':
            return None
        elif value == 'NA':
            return None
        else:
            return value

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
