from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from services import DataFrameService
from entitys.general import Areas
from typing import List, Dict, Optional

router = APIRouter()

UPLOAD_DIR = "uploads/"



@router.get("/", description="Este metodo devuelve todos las areas")
async def get_areas():
    return {"Areas": list(Areas.keys())}



@router.get("/{areas}", description="Este metodo devuelve todas las asignaturas de un area especifica")
async def get_all_areas(areas: str):
    asignaturas = DataFrameService.get_asignaturas_por_area(areas)
    if not asignaturas:
        raise HTTPException(status_code=404, detail=f"No asignaturas found for ciclo '{areas}'.")
    return {"areas": areas, "asignaturas": asignaturas}



@router.get("/tasa-mortandad/{areas}", description="Este método devuelve la tasa de mortandad de todos los años de un ciclo específico.")
async def get_tasa_mortandad(areas: str):
    try:
        data = DataFrameService.get_tasa_mortandad_areas(areas)
        
        if data is None:  # Verificamos específicamente si es None
            raise HTTPException(
                status_code=404, 
                detail=f"No se encontraron datos para el ciclo {areas}"  # Removido las comillas simples
            )
        
        return {"areas": areas, "data": data}
    
    except FileNotFoundError:
        raise HTTPException(
            status_code=500, 
            detail="Archivo no encontrado en el directorio uploads/"
        )
    except HTTPException as http_ex:
        # Propagar excepciones HTTP sin modificar
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error al procesar la solicitud: {str(e)}"
        )
    
@router.get("/tasa-mortandad/{areas}/filtrada/{semestre1}/{semestre2}", 
            description="Este método devuelve la tasa de mortandad de todos los años de un areas específico filtrada por dos semestres.")
async def get_tasa_mortandad_filtrada(areas: str, semestre1: str, semestre2: str):
    # Lista de semestres válidos
    semestres_validos = [
        "2017-1", "2017-2", "2018-1", "2018-2", 
        "2019-1", "2019-2", "2020-1", "2020-2", 
        "2021-1", "2021-2", "2022-1", "2022-2", 
        "2023-1", "2023-2", "2024-1"
    ]

    # Validar que los semestres estén en la lista de semestres válidos
    if semestre1 not in semestres_validos or semestre2 not in semestres_validos:
        raise HTTPException(
            status_code=400,
            detail="Semestres inválidos proporcionados."
        )

    # Asegurarse de que semestre1 sea anterior a semestre2
    if semestres_validos.index(semestre1) > semestres_validos.index(semestre2):
        raise HTTPException(
            status_code=400,
            detail="El semestre inicial no puede ser posterior al semestre final."
        )

    try:
        # Obtener los datos de la tasa de mortalidad
        data = DataFrameService.get_tasa_mortandad_areas(areas)

        if data is None:  # Verificamos específicamente si es None
            raise HTTPException(
                status_code=404, 
                detail=f"No se encontraron datos para el areas {areas}"
            )

        # Filtrar los datos según el rango de semestres
        filtered_data = []
        for row in data:
            filtered_row = {
                "areas": areas,
                "semestre": semestre1 + " a " + semestre2,
                "area": "Ingenieria_Aplicada",  # Reemplaza esto según tus necesidades
                "materia": row["Asignatura"],
                "fechas": [],
                "datos": []
            }

            # Recorrer los semestres válidos y agregar los datos filtrados
            for semestre in semestres_validos:
                if semestre1 <= semestre <= semestre2:
                    if semestre in row:
                        filtered_row["fechas"].append(semestre)
                        filtered_row["datos"].append(row[semestre])

            # Agregar solo si hay datos en el rango
            if filtered_row["fechas"]:
                filtered_data.append(filtered_row)

        if not filtered_data:
            raise HTTPException(
                status_code=404,
                detail=f"No se encontraron datos para el ciclo {areas} en el rango de semestres especificado"
            )

        return filtered_data  # Retorna la lista de datos filtrados

    except FileNotFoundError:
        raise HTTPException(
            status_code=500, 
            detail="Archivo no encontrado en el directorio uploads/"
        )
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error al procesar la solicitud: {str(e)}"
        )



