## Análisis de datos 

1. Crear el entorno virtual
```
python3 -m venv venv(Nombre de tu entorno)
```

2. Activar el entorno virtual
Linux
```
source venv/bin/activate
```
windows
```
venv\Scripts\activate
```

3. Installar dependencias
```
pip install -r requeriments.txt
```

## Ambiente en Docker
Si desea correr el ambiente en un contenedor de docker puede utilizar el docker compose 
```
docker compose up --build
```
Esto para que te cree una imagen en un contenedor de docker por si te quieres saltar los pasos anteriormente nombrados
