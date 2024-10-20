from fastapi import FastAPI
from controllers import CSVcontroller

app = FastAPI()

# Cambia esta línea
app.include_router(CSVcontroller.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)