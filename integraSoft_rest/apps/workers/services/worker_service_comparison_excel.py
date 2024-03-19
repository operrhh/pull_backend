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

    def run(self, request):
        try:

            workers = self.worker_comparison.get_workers_comparison(request=request)

            # Crear un libro de Excel y agregar una hoja de trabajo
            wb = Workbook()
            ws = wb.active
            ws.title = 'Workers'
            ws.append(['Person Number', 'Nombre', 'Correo Electrónico', 'Direccion', 'Ciudad'])

            for idx, worker in enumerate(workers['category']['personal_data']['data'], start=2):
                ws.append([
                    worker['person_number'],
                    worker['name'],
                    worker['email'],
                    worker['address'],
                    worker['city']
                ])

                if worker['name'] == True:
                    cell_color = ws.cell(row=idx, column=2)
                    cell_color.fill = PatternFill(start_color=self.color_true, end_color=self.color_true, fill_type='solid')
                else:
                    cell_color = ws.cell(row=idx, column=2)
                    cell_color.fill = PatternFill(start_color=self.color_false, end_color=self.color_false, fill_type='solid')
                
                if worker['email'] == True:
                    cell_color = ws.cell(row=idx, column=3)
                    cell_color.fill = PatternFill(start_color=self.color_true, end_color=self.color_true, fill_type='solid')
                else:
                    cell_color = ws.cell(row=idx, column=3)
                    cell_color.fill = PatternFill(start_color=self.color_false, end_color=self.color_false, fill_type='solid')
                
                if worker['address'] == True:
                    cell_color = ws.cell(row=idx, column=4)
                    cell_color.fill = PatternFill(start_color=self.color_true, end_color=self.color_true, fill_type='solid')
                else:
                    cell_color = ws.cell(row=idx, column=4)
                    cell_color.fill = PatternFill(start_color=self.color_false, end_color=self.color_false, fill_type='solid')
                
                if worker['city'] == True:
                    cell_color = ws.cell(row=idx, column=5)
                    cell_color.fill = PatternFill(start_color=self.color_true, end_color=self.color_true, fill_type='solid')
                else:
                    cell_color = ws.cell(row=idx, column=5)
                    cell_color.fill = PatternFill(start_color=self.color_false, end_color=self.color_false, fill_type='solid')
            
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