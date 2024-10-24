from fastapi import FastAPI,APIRouter
from controllers import CSVcontroller, CiclosController, AsignaturasController,SemestreController,AreasController,ConsultasGenerales
router = APIRouter()
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


# Configura CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos
    allow_headers=["*"],  # Permite todos los encabezados
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(CSVcontroller.router, prefix="/csv", tags=["CSV"])
app.include_router(CiclosController.router, prefix="/ciclos", tags=["Ciclos"])
app.include_router(AsignaturasController.router, prefix="/Asignaturas", tags=["Asignaturas"])
app.include_router(SemestreController.router, prefix="/semestres", tags=["semestres"])
app.include_router(AreasController.router, prefix="/areas", tags=["areas"])
app.include_router(ConsultasGenerales.router, prefix="/ConsultasGenerales", tags=["ConsultasGenerales"])



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)