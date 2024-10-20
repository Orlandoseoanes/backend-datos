from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import shutil
import os
from services.DataFrameService import data_frame_service

router = APIRouter()

UPLOAD_DIR = "uploads/"

@router.post("/upload-file/")
async def upload_file(file: UploadFile = File(...)):
    # Ensure the uploads directory exists
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    file_location = f"{UPLOAD_DIR}{file.filename}"

    try:
        # Save the uploaded file
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)

        # Load the file into the data frame service
        data_frame_service.load_data(file_location)

        return {"message": f"File '{file.filename}' uploaded and data loaded successfully."}

    except FileNotFoundError as fnf_error:
        raise HTTPException(status_code=404, detail=f"File not found: {str(fnf_error)}")

    except ValueError as val_error:
        raise HTTPException(status_code=400, detail=f"Data processing error: {str(val_error)}")

    except Exception as e:
        if os.path.exists(file_location):
            os.remove(file_location)  # Clean up the uploaded file in case of any failure
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@router.get("/analyze-data/")
async def analyze_data():
    try:
        # Perform analysis on the loaded DataFrame
        analysis_result = data_frame_service.analyze_data()

        # Return the result as JSON
        return JSONResponse(content=analysis_result.toPandas().to_dict())

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
