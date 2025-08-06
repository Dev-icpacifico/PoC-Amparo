# Imagen base con Python 3.11
FROM python:3.11-slim

# Información del autor
LABEL maintainer="Luis Pizarro"

# Crear directorio de trabajo
WORKDIR /app

# Copiar archivos del proyecto al contenedor
COPY . .

# Instalar dependencias
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Exponer el puerto que usará Uvicorn
EXPOSE 8000

# Comando para arrancar la API FastAPI
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]