from fastapi import FastAPI,APIRouter
from controllers import CSVcontroller, CiclosController, AsignaturasController,SemestreController,AreasController
router = APIRouter()

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(CSVcontroller.router, prefix="/csv", tags=["CSV"])
app.include_router(CiclosController.router, prefix="/ciclos", tags=["Ciclos"])
app.include_router(AsignaturasController.router, prefix="/Asignaturas", tags=["Asignaturas"])
app.include_router(SemestreController.router, prefix="/semestres", tags=["semestres"])
app.include_router(AreasController.router, prefix="/areas", tags=["areas"])



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)