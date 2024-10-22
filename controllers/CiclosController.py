from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import shutil
import os
from services import DataFrameService
from entitys.general import materias_periodos,semestres,Ciclos

router = APIRouter()

UPLOAD_DIR = "uploads/"


#@router.get("/allciclos")
#async def get_all_ciclos():
#    return Ciclos



@router.get("/")
async def get_ciclos():
    return {"ciclos": list(Ciclos.keys())}

@router.get("/{ciclo}")
async def get_all_ciclos(ciclo: str):
    asignaturas = DataFrameService.get_asignaturas_por_ciclo(ciclo)
    if not asignaturas:
        raise HTTPException(status_code=404, detail=f"No asignaturas found for ciclo '{ciclo}'.")
    return {"ciclo": ciclo, "asignaturas": asignaturas}

