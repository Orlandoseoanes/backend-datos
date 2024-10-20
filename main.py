from fastapi import FastAPI, File, UploadFile, HTTPException
from controllers import  CSVcontroller
import python_multipart

app = FastAPI()


app.include_router(CSVcontroller.router,prefix="/loadfile",tags=["loadfile"])

