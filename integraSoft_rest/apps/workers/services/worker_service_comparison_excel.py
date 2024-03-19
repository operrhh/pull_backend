from .worker_service_comparison import WorkerServiceComparison
from openpyxl import Workbook
from openpyxl.styles import PatternFill
from io import BytesIO
from django.http import HttpResponse


class WorkerServiceComparisonExcel:
    def __init__(self):
        self.worker_comparison = WorkerServiceComparison()
        self.color_true = '00FF00'
        self.color_false = 'FC371B'
        self.color_detail_wsdl = '94B4FF'
        self.color_detail_peoplesoft = 'D98FF5'


    def run(self, request):
        try:

            workers = self.worker_comparison.get_workers_comparison(request=request)
            workers_data = workers['category']['personal_data']['data']
            workers_not_found = workers['not_found']['data']

            # Crear un libro de Excel y agregar una hoja de trabajo
            wb = Workbook()
            ws = wb.active
            ws.title = 'Workers'
            ws.append([
                'Person Number',
                'Nombre',
                'Nombre Detalle Hcm',
                'Nombre Detalle Peoplesoft',
                'Correo',
                'Correo Detalle Hcm',
                'Correo Detalle Peoplesoft',
                'Direccion',
                'Direccion Detalle Hcm',
                'Direccion Detalle Peoplesoft',
                'Ciudad',
                'Ciudad Detalle Hcm',
                'Ciudad Detalle Peoplesoft'
            ])
            

            for idx, worker in enumerate(workers_data, start=2):
                ws.append([
                    worker['person_number'], #1
                    worker['name'], #2
                    worker['name_wsdl'], #3
                    worker['name_peoplesoft'], #4
                    worker['email'], #5
                    worker['email_wsdl'], #6
                    worker['email_peoplesoft'], #7
                    worker['address'], #8
                    worker['address_wsdl'], #9
                    worker['address_peoplesoft'], #10
                    worker['city'], #11
                    worker['city_wsdl'], #12
                    worker['city_peoplesoft'] #13
                ])

                # Agregar color a las celdas

                # Nombre
                if worker['name'] == True:
                    cell_color = ws.cell(row=idx, column=2)
                    cell_color.fill = PatternFill(start_color=self.color_true, end_color=self.color_true, fill_type='solid')
                else:
                    cell_color = ws.cell(row=idx, column=2)
                    cell_color.fill = PatternFill(start_color=self.color_false, end_color=self.color_false, fill_type='solid')
                
                cell_color = ws.cell(row=idx, column=3)
                cell_color.fill = PatternFill(start_color=self.color_detail_wsdl, end_color=self.color_detail_wsdl, fill_type='solid')
                cell_color = ws.cell(row=idx, column=4)
                cell_color.fill = PatternFill(start_color=self.color_detail_peoplesoft, end_color=self.color_detail_peoplesoft, fill_type='solid')


                # Email
                if worker['email'] == True: 
                    cell_color = ws.cell(row=idx, column=5)
                    cell_color.fill = PatternFill(start_color=self.color_true, end_color=self.color_true, fill_type='solid')
                else:
                    cell_color = ws.cell(row=idx, column=5)
                    cell_color.fill = PatternFill(start_color=self.color_false, end_color=self.color_false, fill_type='solid')

                cell_color = ws.cell(row=idx, column=6)
                cell_color.fill = PatternFill(start_color=self.color_detail_wsdl, end_color=self.color_detail_wsdl, fill_type='solid')
                cell_color = ws.cell(row=idx, column=7)
                cell_color.fill = PatternFill(start_color=self.color_detail_peoplesoft, end_color=self.color_detail_peoplesoft, fill_type='solid')


                # Address                
                if worker['address'] == True:
                    cell_color = ws.cell(row=idx, column=8)
                    cell_color.fill = PatternFill(start_color=self.color_true, end_color=self.color_true, fill_type='solid')
                else:
                    cell_color = ws.cell(row=idx, column=8)
                    cell_color.fill = PatternFill(start_color=self.color_false, end_color=self.color_false, fill_type='solid')

                cell_color = ws.cell(row=idx, column=9)
                cell_color.fill = PatternFill(start_color=self.color_detail_wsdl, end_color=self.color_detail_wsdl, fill_type='solid')
                cell_color = ws.cell(row=idx, column=10)
                cell_color.fill = PatternFill(start_color=self.color_detail_peoplesoft, end_color=self.color_detail_peoplesoft, fill_type='solid')

                # City
                if worker['city'] == True:
                    cell_color = ws.cell(row=idx, column=11)
                    cell_color.fill = PatternFill(start_color=self.color_true, end_color=self.color_true, fill_type='solid')
                else:
                    cell_color = ws.cell(row=idx, column=11)
                    cell_color.fill = PatternFill(start_color=self.color_false, end_color=self.color_false, fill_type='solid')

                cell_color = ws.cell(row=idx, column=12)
                cell_color.fill = PatternFill(start_color=self.color_detail_wsdl, end_color=self.color_detail_wsdl, fill_type='solid')
                cell_color = ws.cell(row=idx, column=13)
                cell_color.fill = PatternFill(start_color=self.color_detail_peoplesoft, end_color=self.color_detail_peoplesoft, fill_type='solid')



            # Crear otra hoja de trabajo
            ws2 = wb.create_sheet(title='Not Found')

            # Puedes agregar datos a la nueva hoja de trabajo si lo deseas
            ws2.append(['Person Number'])

            for idx, worker in enumerate(workers_not_found, start=2):
                ws2.append([
                    worker['person_number']
                ])                

            
            # Crear un objeto de BytesIO para almacenar el archivo en memoria
            excel_file = BytesIO()

            # Guardar el libro de Excel en el objeto BytesIO
            wb.save(excel_file)

            # Configurar la respuesta HTTP para devolver el archivo Excel
            response = HttpResponse(
                excel_file.getvalue(),
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )

            # Configurar el encabezado de la respuesta HTTP
            response['Content-Disposition'] = 'attachment; filename=workers.xlsx'
            
            return response
        except Exception as e:
            raise Exception(e) from e