# Usa una imagen base oficial de Python con el tag slim para una imagen ligera
FROM python:3.9-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el archivo de requerimientos (requirements.txt) a la imagen
COPY requirements.txt .

# Instalar las dependencias desde requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código de la aplicación
COPY . .

# Exponer el puerto en el que se ejecutará la app (8000 para FastAPI)
EXPOSE 8000

# Comando para iniciar la aplicación
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
