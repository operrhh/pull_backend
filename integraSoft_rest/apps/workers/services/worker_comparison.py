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

    def __init__(self, person_number: str):
        self.person_number: str = self.format_person_number( person_number)

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

    def compare_workers(self, workers_peoplesoft: List[WorkerFormatComparison], workers_wsdl: List[WorkerFormatComparison], main: str):
        try:
            i = 0
            p = 0
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
                        print(f'{i} | {person_number}')

                        #Comparamos los valores de la categoria Datos Personales
                        self.compare_workers_personal_data(wr_ps, wsdl_dic[person_number])



                print('Total de usuarios Peoplesoft: ', p)
                print('End for')

            # if main == 'wsdl':
            #     peoplesoft_dic = {getattr(obj,"person_number"):obj for obj in workers_peoplesoft}
            #     for wr_wsdl in workers_wsdl:
            #         person_number = getattr(wr_wsdl, "person_number")
            #         if person_number in peoplesoft_dic:
            #             i += 1
            #             print(f'{i} | {person_number}')

            return 'ok'
        except Exception as e:
            raise Exception(e) from e

    def compare_workers_personal_data(self, worker_peoplesoft: WorkerFormatComparison, worker_wsdl: WorkerFormatComparison):
        return 'ok'

    def format_workers_by_peoplesoft(self, workers: list):
        try:
            new_workers = []
            for worker in workers:
                wr = WorkerFormatComparison(
                    person_number=worker['emplid']
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
                wr = WorkerFormatComparison(
                    person_number=worker['person_number']
                )
                new_workers.append(wr)

            return new_workers
        except Exception as e:
            raise Exception(e) from e    