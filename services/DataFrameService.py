from entitys.general import materias_periodos,semestres,Ciclos
from openpyxl import load_workbook
import os
from typing import List, Union
import csv


def process_excel_file(file_location: str):
    # Cargar el archivo Excel
    workbook = load_workbook(file_location)
    sheet = workbook['Sistemas']  # Acceder a la hoja 'Sistemas'

    # Borrar todas las hojas excepto 'Sistemas'
    sheet_names = workbook.sheetnames
    for sheet_name in sheet_names:
        if sheet_name != 'Sistemas':
            std = workbook[sheet_name]
            workbook.remove(std)

    # Insertar dos nuevas columnas en la posición 1 (Columna A y B)
    sheet.insert_cols(1)  # Para "Semestre"
    sheet.insert_cols(1)  # Para "CICLO"

    # Agregar las nuevas columnas "Semestre" y "CICLO" en la fila 3
    sheet.cell(row=3, column=1, value="CICLO")  # Columna A
    sheet.cell(row=3, column=2, value="Semestre")  # Columna B

    # Llenar las columnas "Semestre" y "CICLO"
    for row in range(4, sheet.max_row + 1):
        asignatura = sheet.cell(row=row, column=3).value
        semestre_found = False
        ciclo_found = False

        for ciclo, asignaturas in Ciclos.items():
            if asignatura in asignaturas:
                sheet.cell(row=row, column=1, value=ciclo)
                ciclo_found = True
                break

        if not ciclo_found:
            sheet.cell(row=row, column=1, value="N/A")

        for semestre, asignaturas in materias_periodos.items():
            if asignatura in asignaturas:
                sheet.cell(row=row, column=2, value=semestre)
                semestre_found = True
                break

        if not semestre_found:
            sheet.cell(row=row, column=2, value="N/A")

    # Modificar la fila 3 con los valores del vector semestre
    for col_index, semestre in enumerate(semestres, start=4):
        sheet.cell(row=3, column=col_index, value=semestre)

    # Guardar el archivo modificado
    workbook.save(file_location)

    # Convertir el archivo Excel a CSV con formato correcto para los ceros
    csv_file_location = file_location.replace('.xlsx', '.csv')

    with open(csv_file_location, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
        for row_idx, row in enumerate(sheet.iter_rows(values_only=True)):
            formatted_row = []
            for col_idx, cell in enumerate(row, start=1):
                # Para las columnas 4-18 (datos numéricos)
                if col_idx >= 4 and col_idx <= 18 and row_idx >= 3:  # Empezamos desde la fila 4 (índice 3)
                    if isinstance(cell, (int, float)):
                        # Multiplicar por 100 y redondear a 3 decimales
                        value = cell * 100 if abs(cell) >= 1e-10 else 0
                        formatted_value = round(value, 3)
                    else:
                        # Si no es número, intentar convertir
                        try:
                            if cell and str(cell).strip() != '':
                                value = float(str(cell).replace('%', '')) * 100
                                formatted_value = round(value, 3)
                            else:
                                formatted_value = 0
                        except (ValueError, TypeError):
                            formatted_value = cell
                else:
                    # Para las otras columnas (no numéricas)
                    if isinstance(cell, (int, float)) and abs(cell) < 1e-10:
                        formatted_value = 0
                    else:
                        formatted_value = cell
                        
                formatted_row.append(formatted_value)
            writer.writerow(formatted_row)
    
    # Borrar el archivo .xlsx original
    os.remove(file_location)

    return csv_file_location


def get_ciclo(asignatura: str):
    """
    Devuelve el ciclo correspondiente a una asignatura.
    """
    for ciclo, asignaturas in Ciclos.items():
        if asignatura in asignaturas:
            return ciclo
    return "N/A"

def get_asignaturas_por_ciclo(ciclo: str):
    """
    Devuelve las asignaturas correspondientes a un ciclo.
    """
    return Ciclos.get(ciclo, [])

def get_asignaturas_por_semestre(semestre: str):
    """
    Devuelve las asignaturas correspondientes a un ciclo.
    """
    return materias_periodos.get(semestre, [])


def get_data(materia: str, fecha_inicial: str, fecha_final: str, file_path: str) -> dict:
        try:
           
            
            # Validar fechas
            if fecha_inicial not in semestres or fecha_final not in semestres:
                raise ValueError("Las fechas deben estar en el rango permitido")
            
            if semestres.index(fecha_inicial) > semestres.index(fecha_final):
                raise ValueError("La fecha inicial debe ser anterior a la fecha final")
            
            # Índices para el rango de fechas
            inicio_idx = semestres.index(fecha_inicial) + 3  # +3 porque tenemos CICLO, Semestre, ASIGNATURA
            final_idx = semestres.index(fecha_final) + 3
            
            # Leer el archivo CSV
            with open(file_path, 'r', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                # Leer la primera fila para obtener los encabezados
                headers = next(csv_reader)
                
                # Buscar la materia línea por línea
                for row in csv_reader:
                    if row[2] == materia:  # La asignatura está en la columna 3 (índice 2)
                        # Extraer los datos del rango solicitado
                        datos_rango = []
                        for i in range(inicio_idx, final_idx + 1):
                            try:
                                # Convertir el valor a float, manejando casos especiales
                                valor = row[i].strip()
                                if valor == '' or valor == 'None':
                                    datos_rango.append(0.0)
                                else:
                                    # Eliminar el símbolo de porcentaje si existe
                                    valor = valor.replace('%', '').strip()
                                    datos_rango.append(float(valor))
                            except (ValueError, IndexError):
                                datos_rango.append(0.0)
                        
                        # Construir respuesta con toda la información de la materia
                        return {
                            "ciclo": row[0],
                            "semestre": row[1],
                            "materia": row[2],
                            "fechas": semestres[semestres.index(fecha_inicial):semestres.index(fecha_final) + 1],
                            "datos": datos_rango
                        }
                
                # Si no se encuentra la materia
                raise ValueError(f"No se encontró la asignatura: {materia}")
            
        except Exception as e:
            raise ValueError(f"Error al procesar los datos: {str(e)}")