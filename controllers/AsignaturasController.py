from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import shutil
import os
from services import DataFrameService
from entitys.general import materias_periodos,semestres,Ciclos

router = APIRouter()

UPLOAD_DIR = "uploads/"


@router.get("/")
async def get_all_materias():
    return materias_periodos

@router.get("/Semestre/{semestre}")
async def get_asignaturas(semestre: str):
    asignaturas = DataFrameService.get_asignaturas_por_semestre(semestre)
    if not asignaturas:
        raise HTTPException(status_code=404, detail=f"No asignaturas found for ciclo '{semestre}'.")
    return {"semestre": semestre, "asignaturas": asignaturas}


@router.get("/{materia}/{fechaInicial}/{fechaFinal}")
async def get_comparativa_materia(materia: str, fecha_inicial: str, fecha_final: str):
    try:
        folder = 'uploads'
        files = [f for f in os.listdir(folder) if f.endswith('.csv')]
        
        if len(files) != 1:
            raise HTTPException(
                status_code=400,
                detail="Debe haber exactamente un archivo CSV en la carpeta /uploads"
            )
        
        file_path = os.path.join(folder, files[0])
        
        # Obtener los datos usando el servicio
        result = DataFrameService.get_data(materia, fecha_inicial, fecha_final, file_path)
        
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


