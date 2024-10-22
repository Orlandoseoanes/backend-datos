from entitys.general import materias_periodos,semestres,Ciclos,Areas
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

    # Insertar tres nuevas columnas al inicio
    sheet.insert_cols(1, 3)

    # Agregar los encabezados en la fila 3
    sheet.cell(row=3, column=1, value="Ciclo")
    sheet.cell(row=3, column=2, value="Semestre")
    sheet.cell(row=3, column=3, value="Area")

    # Llenar las columnas
    for row in range(4, sheet.max_row + 1):
        asignatura = sheet.cell(row=row, column=4).value  # La columna de asignaturas ahora es la 4
        if asignatura is None:
            continue

        # Inicializar variables de control
        ciclo_found = False
        semestre_found = False
        areas_found = False

        # Limpiar el nombre de la asignatura
        asignatura = str(asignatura).strip()

        # Buscar y asignar el ciclo
        for ciclo, asignaturas in Ciclos.items():
            if asignatura in asignaturas:
                sheet.cell(row=row, column=1, value=ciclo)
                ciclo_found = True
                break
        if not ciclo_found:
            sheet.cell(row=row, column=1, value="N/A")

        # Buscar y asignar el semestre
        for semestre, asignaturas in materias_periodos.items():
            if asignatura in asignaturas:
                sheet.cell(row=row, column=2, value=semestre)
                semestre_found = True
                break
        if not semestre_found:
            sheet.cell(row=row, column=2, value="N/A")

        # Buscar y asignar el área
        for area, asignaturas in Areas.items():
            if asignatura in asignaturas:
                sheet.cell(row=row, column=3, value=area)
                areas_found = True
                break
        if not areas_found:
            sheet.cell(row=row, column=3, value="N/A")

    # Modificar la fila 3 con los valores del vector semestre
    for col_index, semestre in enumerate(semestres, start=5):
        sheet.cell(row=3, column=col_index, value=semestre)

    # Guardar el archivo modificado
    workbook.save(file_location)

    # Convertir a CSV con formato específico
    csv_file_location = file_location.replace('.xlsx', '.csv')
    
    with open(csv_file_location, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        
        for row_idx, row in enumerate(sheet.iter_rows(values_only=True)):
            formatted_row = []
            for col_idx, cell in enumerate(row, start=1):
                # Manejar valores numéricos
                if col_idx >= 5 and row_idx >= 3:  # Datos numéricos desde la columna 4
                    try:
                        if cell is None or (isinstance(cell, str) and cell.strip() == ''):
                            formatted_value = '0'
                        elif isinstance(cell, (int, float)):
                            # Convertir a porcentaje y redondear a 3 decimales
                            value = float(cell)
                            if abs(value) < 1e-10:
                                formatted_value = '0'
                            else:
                                formatted_value = f"{value * 100:.3f}"
                        else:
                            # Intentar convertir strings que puedan ser números
                            value = float(str(cell).replace('%', '').strip())
                            formatted_value = f"{value:.3f}"
                    except (ValueError, TypeError):
                        formatted_value = '0'
                else:
                    # Valores no numéricos
                    formatted_value = str(cell) if cell is not None else ''
                
                formatted_row.append(formatted_value)
            
            # Escribir la fila solo si tiene contenido
            if any(cell.strip() != '' for cell in formatted_row):
                writer.writerow(formatted_row)
    
    # Borrar el archivo Excel original
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
        
        # Leer el archivo CSV
        with open(file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            
            # Saltar las dos primeras líneas de encabezado
            next(csv_reader)  # Saltar "EVOLUCION ASIGNATURAS CON MAYOR TASA DE MORTALIDAD"
            next(csv_reader)  # Saltar "INGENIERIA DE SISTEMAS"
            
            # Leer la línea de encabezados (tercera línea)
            headers = next(csv_reader)
            
            # Encontrar los índices de las columnas para el rango de fechas
            fechas_indices = []
            for i, header in enumerate(headers):
                if header in semestres:
                    if fecha_inicial <= header <= fecha_final:
                        fechas_indices.append(i)
            
            if not fechas_indices:
                raise ValueError("No se encontraron las fechas especificadas en el archivo")
            
            # Buscar la materia en el archivo
            for row in csv_reader:
                if len(row) < 3:  # Saltar filas vacías o mal formadas
                    continue
                    
                # La materia puede estar en diferentes posiciones según el formato
                asignatura_actual = None
                ciclo = row[0].strip()
                area = row[2].strip() if len(row) > 2 else ""
                
                # Extraer la asignatura del formato del archivo
                for campo in row:
                    if materia in campo:
                        asignatura_actual = materia
                        break
                
                if asignatura_actual == materia:
                    # Extraer los datos del rango solicitado
                    datos_rango = []
                    for idx in fechas_indices:
                        try:
                            if idx < len(row):
                                valor = row[idx].strip()
                                if valor == '' or valor == 'None':
                                    datos_rango.append(0.0)
                                else:
                                    # Eliminar el símbolo de porcentaje si existe y convertir a float
                                    valor = valor.replace('%', '').strip()
                                    datos_rango.append(float(valor))
                            else:
                                datos_rango.append(0.0)
                        except (ValueError, IndexError):
                            datos_rango.append(0.0)
                    
                    # Construir la respuesta
                    fechas_rango = [headers[i] for i in fechas_indices]
                    return {
                        "ciclo": ciclo,
                        "semestre": row[1] if len(row) > 1 else "semestre-desconocido",
                        "area": area,
                        "materia": materia,
                        "fechas": fechas_rango,
                        "datos": datos_rango
                    }
            
            # Si no se encuentra la materia
            raise ValueError(f"No se encontró la asignatura: {materia}")
            
    except Exception as e:
        raise ValueError(f"Error al procesar los datos: {str(e)}")
    
