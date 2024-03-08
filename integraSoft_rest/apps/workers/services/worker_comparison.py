from .workerServicePeopleSoft import WorkerServicePeopleSoft
from .workerServiceWsdl import WorkerServiceWsdl
from typing import List

class WorkerFormatComparison:
    def __init__(self, person_number):
        self.person_number = person_number

class WorkerComparison:
    def __init__(self):
        self.worker_service_peoplesoft = WorkerServicePeopleSoft()
        self.worker_service_wsdl = WorkerServiceWsdl()

    def get_workers_comparison(self, request):
        workers_peoplesoft = self.worker_service_peoplesoft.get_workers_peoplesoft(request=request)
        workers_wsdl = self.worker_service_wsdl.get_workers_wsdl()

        workers_peoplesoft_format = self.format_workers_by_peoplesoft(workers_peoplesoft)
        workers_wsdl_format = self.format_workers_by_wsdl(workers_wsdl)

        res = self.compare_workers(workers_peoplesoft_format, workers_wsdl_format, 'peoplesoft')

        return res

    def compare_workers(self, workers_peoplesoft: List[WorkerFormatComparison], workers_wsdl: List[WorkerFormatComparison], main: str):
        if main == 'peoplesoft':
            wsdl_dic = {getattr(obj,"person_number"):obj for obj in workers_wsdl}
            for wr_ps in workers_peoplesoft:
                person_number = getattr(wr_ps, "person_number")
                if person_number in wsdl_dic:
                    print('Coincide')


    def format_workers_by_peoplesoft(self, workers: list):
        new_workers = []
        for worker in workers:
            wr = WorkerFormatComparison(
                person_number=worker['emplid']
            )
            new_workers.append(wr)

        return new_workers

    def format_workers_by_wsdl(self, workers: list):
        new_workers = []
        for worker in workers:
            wr = WorkerFormatComparison(
                person_number=worker['person_number']
            )
            new_workers.append(wr)

        return new_workers