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
        self.color_detail = '94B4FF'

    def run(self, request):
        try:

            workers = self.worker_comparison.get_workers_comparison(request=request)
            workers_data = workers['category']['personal_data']['data']

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
                    worker['name_hcm'], #3
                    worker['name_peoplesoft'], #4
                    worker['email'], #5
                    worker['email_hcm'], #6
                    worker['email_peoplesoft'], #7
                    worker['address'], #8
                    worker['address_hcm'], #9
                    worker['address_peoplesoft'], #10
                    worker['city'], #11
                    worker['city_hcm'], #12
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
                cell_color.fill = PatternFill(start_color=self.color_true, end_color=self.color_true, fill_type='solid')
                cell_color = ws.cell(row=idx, column=4)
                cell_color.fill = PatternFill(start_color=self.color_true, end_color=self.color_true, fill_type='solid')


                # Email
                if worker['email'] == True: 
                    cell_color = ws.cell(row=idx, column=5)
                    cell_color.fill = PatternFill(start_color=self.color_true, end_color=self.color_true, fill_type='solid')
                else:
                    cell_color = ws.cell(row=idx, column=5)
                    cell_color.fill = PatternFill(start_color=self.color_false, end_color=self.color_false, fill_type='solid')

                cell_color = ws.cell(row=idx, column=6)
                cell_color.fill = PatternFill(start_color=self.color_true, end_color=self.color_true, fill_type='solid')
                cell_color = ws.cell(row=idx, column=7)
                cell_color.fill = PatternFill(start_color=self.color_true, end_color=self.color_true, fill_type='solid')


                # Address                
                if worker['address'] == True:
                    cell_color = ws.cell(row=idx, column=8)
                    cell_color.fill = PatternFill(start_color=self.color_true, end_color=self.color_true, fill_type='solid')
                else:
                    cell_color = ws.cell(row=idx, column=8)
                    cell_color.fill = PatternFill(start_color=self.color_false, end_color=self.color_false, fill_type='solid')

                cell_color = ws.cell(row=idx, column=9)
                cell_color.fill = PatternFill(start_color=self.color_true, end_color=self.color_true, fill_type='solid')
                cell_color = ws.cell(row=idx, column=10)
                cell_color.fill = PatternFill(start_color=self.color_true, end_color=self.color_true, fill_type='solid')

                # City
                if worker['city'] == True:
                    cell_color = ws.cell(row=idx, column=11)
                    cell_color.fill = PatternFill(start_color=self.color_true, end_color=self.color_true, fill_type='solid')
                else:
                    cell_color = ws.cell(row=idx, column=11)
                    cell_color.fill = PatternFill(start_color=self.color_false, end_color=self.color_false, fill_type='solid')

                cell_color = ws.cell(row=idx, column=12)
                cell_color.fill = PatternFill(start_color=self.color_true, end_color=self.color_true, fill_type='solid')
                cell_color = ws.cell(row=idx, column=13)
                cell_color.fill = PatternFill(start_color=self.color_true, end_color=self.color_true, fill_type='solid')
                

            
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