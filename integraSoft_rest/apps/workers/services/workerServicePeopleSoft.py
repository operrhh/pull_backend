from django.db import connections
import cx_Oracle 

from ..custom_exceptions import ExceptionWorkerPeopleSoft

class WorkerServicePeopleSoft:

    def get_workers_peoplesoft(self):
        try:
            with connections['people_soft'].cursor() as cursor:
                out_cur = cursor.connection.cursor()
                cursor.callproc("GET_WORKERS", [out_cur])

                if out_cur:
                    workers = [res for res in out_cur]
                    return workers
                else:
                    raise ExceptionWorkerPeopleSoft('No se han encontrado usuarios')
        except cx_Oracle.DatabaseError as e:
            print('Error de la base de datos:', e)

    def get_worker_peoplesoft(self, pk):
        try:
            with connections['people_soft'].cursor() as cursor:
                out_cur = cursor.connection.cursor()
                cursor.callproc("GET_WORKER", [pk, out_cur])

                if out_cur:
                    worker = [res for res in out_cur]
                    return worker
                else:
                    raise ExceptionWorkerPeopleSoft('No se han encontrado usuarios')
        except cx_Oracle.DatabaseError as e:
            print('Error de la base de datos:', e)

    # def get_product(self):
    #     try:
    #         with connections['people_soft_luky'].cursor() as cursor:
    #             out_cur = cursor.connection.cursor()
    #             cursor.callproc("SP_GET_PRODUCTS", [out_cur])
                
    #             lista = [res for res in out_cur]
    #         return lista
    #     except cx_Oracle.DatabaseError as e:
    #         print('Error de la base de datos:', e)