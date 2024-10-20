FROM jupyter/pyspark-notebook:latest

USER root

# Instalar dependencias adicionales
RUN apt-get update && apt-get install -y \
    python3-venv \
    gcc \
    libc6-dev

# Crear y activar entorno virtual
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /app

# Copiar y instalar requisitos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Configurar variables de entorno para PySpark
ENV PYSPARK_PYTHON=$VIRTUAL_ENV/bin/python
ENV PYSPARK_DRIVER_PYTHON=$VIRTUAL_ENV/bin/python
ENV PYSPARK_SUBMIT_ARGS="--master local[*] pyspark-shell"

# Asegurarse de que los scripts tengan permisos de ejecución
RUN chmod +x /app/*.py

# Comando para ejecutar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]