from .workerServicePeopleSoft import WorkerServicePeopleSoft
from .workerServiceWsdl import WorkerServiceWsdl
from typing import List

# Clase que se encarga de comparar los trabajadores de peoplesoft con los trabajadores de wsdl
class WorkerFormatComparison:

    # def __new__(cls, person_number: str):
    #     formatted_person_number = cls.format_person_number(person_number)
    #     instance = object.__new__(cls)
    #     instance.__init__(formatted_person_number)
    #     return instance

    def __init__(self, person_number: str, name: str = ''):
        self.person_number: str = self.format_person_number( person_number)
        self.name: str = name

    @staticmethod
    def format_person_number(person_number: str):
        if person_number:
            person_number = person_number.replace(' ', '')
        return person_number

class WorkerComparison:
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
                    name = worker['name']
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
                    name = name_format
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
            p = 0

            personal_data = []

            if main == 'peoplesoft':

                # Crea un diccionario con los atributos person_number de los objetos de workers_wsdl
                wsdl_dic = {getattr(obj,"person_number"):obj for obj in workers_wsdl}


                for wr_ps in workers_peoplesoft:
                    p += 1

                    # Obtiene el valor del atributo person_number del objeto wr_ps
                    person_number = getattr(wr_ps, "person_number")

                    # Si el valor de person_number se encuentra en el diccionario wsdl_dic
                    if person_number in wsdl_dic:
                        i += 1
                        print('-----------------------------------')
                        print(f'{i} | {person_number}')

                        # Comparamos los valores de la categoria Datos Personales
                        personal_data.append(self.compare_workers_personal_data(wr_ps, wsdl_dic[person_number]))


                categories = {
                    'personal_data': {
                        "count": len(personal_data),
                        "data": personal_data
                    }
                }

                print('Total de usuarios Peoplesoft: ', p)
                print('Total de usuarios Wsdl: ', len(workers_wsdl))
                print('End for')

            # if main == 'wsdl':
            #     peoplesoft_dic = {getattr(obj,"person_number"):obj for obj in workers_peoplesoft}
            #     for wr_wsdl in workers_wsdl:
            #         person_number = getattr(wr_wsdl, "person_number")
            #         if person_number in peoplesoft_dic:
            #             i += 1
            #             print(f'{i} | {person_number}')

            return categories
        except Exception as e:
            raise Exception(e) from e

    def compare_workers_personal_data(self, worker_peoplesoft: WorkerFormatComparison, worker_wsdl: WorkerFormatComparison):
        try:
            name = self.compare_workers_personal_data_names(worker_peoplesoft.name, worker_wsdl.name)

            personal_data = {
                'person_number': worker_peoplesoft.person_number,
                'name': name
            }
            return personal_data

        except Exception as e:
            raise Exception(e) from e


    def compare_workers_personal_data_names(self, name_peoplesoft: str, name_wsdl: str):
        try:
            name_peoplesoft = name_peoplesoft.replace(' ', '').upper()
            name_wsdl = name_wsdl.replace(' ', '').upper()

            if name_peoplesoft == name_wsdl:
                print('-----------------------------------')
                print('Los nombres coinciden')
                print('Peoplesoft: ', name_peoplesoft)
                print('Wsdl      : ', name_wsdl)
                print('-----------------------------------')
                return True
            else:
                print('-----------------------------------')
                print('Los nombres no coinciden')
                print('Peoplesoft: ', name_peoplesoft)
                print('Wsdl      : ', name_wsdl)
                print('-----------------------------------')
                return False

        except Exception as e:
            raise Exception(e) from e