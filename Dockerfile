FROM openjdk:21-slim-bookworm

# Instalar Python y venv
RUN apt-get update && apt-get install -y python3 python3-pip python3-venv

WORKDIR /app

# Crear un entorno virtual
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Instalar dependencias de Python en el entorno virtual
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Configurar variables de entorno para Java y PySpark
ENV JAVA_HOME=/usr/local/openjdk-21
ENV PATH=$PATH:$JAVA_HOME/bin
ENV PYSPARK_PYTHON=$VIRTUAL_ENV/bin/python
ENV PYSPARK_DRIVER_PYTHON=$VIRTUAL_ENV/bin/python

# Comando para ejecutar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]