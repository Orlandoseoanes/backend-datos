from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from services import DataFrameService
from entitys.general import Areas
from typing import List, Dict, Union, Optional
import os

router = APIRouter()


@router.get("/masperdidas",
            description="Este método devuelve las tasas de mortandad más altas por semestre",
            response_model=List[Dict[str, Union[str, float]]])
async def get_mas_perdidas():
    try:
        directorio_uploads = "uploads"
        resultados = DataFrameService.cargar_y_analizar_datos(
            directorio_uploads)
        return resultados

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error inesperado: {str(e)}"
        )


@router.get("/tasas-mortalidad-ciclo/{ciclo}",
            description="Este método devuelve las tasas de mortandad más altas por semestre",
            response_model=List[Dict[str, Union[str, float]]])
async def get_tasas_mortalidad(ciclo: str):
    try:
        directorio_uploads = "uploads"
        resultados = DataFrameService.obtener_tasas_mortalidad_por_ciclo(
            directorio_uploads, ciclo)
        return resultados
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error inesperado: {str(e)}"
        )


@router.get("/tasas-mortalidad-area/{area}",
            description="Este método devuelve las tasas de mortandad más altas por semestre",
            response_model=List[Dict[str, Union[str, float]]])
async def get_tasas_mortalidad_area(area: str):
    try:
        directorio_uploads = "uploads"
        resultados = DataFrameService.obtener_tasas_mortalidad_por_area(
            directorio_uploads, area)
        return resultados
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error inesperado: {str(e)}"
        )