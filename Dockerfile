# Usa una imagen base oficial de Python con el tag slim para una imagen ligera
FROM python:3.10-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el archivo de requerimientos (requirements.txt) a la imagen
COPY requirements.txt .

# Instalar las dependencias desde requirements.txt
# Incluye la instalación de build-essential para compilar algunas dependencias
RUN apt-get update && apt-get install -y build-essential && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get remove -y build-essential && apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

# Copiar el resto del código de la aplicación
COPY . .

# Instalar Gunicorn
RUN pip install gunicorn

# Exponer el puerto en el que se ejecutará la app (8000 para FastAPI)
EXPOSE 8080

# Comando para iniciar la aplicación
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Comando para iniciar la aplicación con Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "main:app"]
#CMD ["gunicorn", "--bind", "0.0.0.0:8080", "-w", "4", "main:app"]
