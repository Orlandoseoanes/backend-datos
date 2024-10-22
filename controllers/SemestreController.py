from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import shutil
import os
from services import DataFrameService
from entitys.general import materias_periodos,semestres,Ciclos

router = APIRouter()

UPLOAD_DIR = "uploads/"

@router.get("/allsemestres")
async def get_all_semestres():
   return semestres

