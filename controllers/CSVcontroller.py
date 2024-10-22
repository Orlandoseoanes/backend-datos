from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import shutil
import os
from services import DataFrameService
router = APIRouter()

UPLOAD_DIR = "uploads/"

@router.post("/upload-file/")
async def upload_file(file: UploadFile = File(...)):
    # Asegúrate de que el directorio de uploads exista
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    file_location = os.path.join(UPLOAD_DIR, file.filename)

    try:
        # Guarda el archivo subido
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)

        return {"message": f"File '{file.filename}' uploaded successfully to '{UPLOAD_DIR}'."}

    except Exception as e:
        if os.path.exists(file_location):
            os.remove(file_location)  # Limpia el archivo subido en caso de fallo
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    

@router.get("/analizar")
async def analizar_file():
    # Listar archivos en la carpeta de subida
    files = os.listdir(UPLOAD_DIR)
    
    if not files:
        raise HTTPException(status_code=404, detail="No files found in the uploads directory.")
    
    # Tomar el primer archivo de la lista
    file_name = files[0]
    file_location = os.path.join(UPLOAD_DIR, file_name)
    
    try:
        # Llamar a la función que procesa el archivo Excel
        DataFrameService.process_excel_file(file_location)

        return {"message": f"All sheets except 'Sistemas' have been removed from '{file_name}', and new columns 'CICLO' and 'Semestre' have been added."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
