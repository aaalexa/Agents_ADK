FROM python:3.12-slim

# Variables de entorno para evitar prompts de Python y asegurar UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV LANG=C.UTF-8

# Instala dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Crea el directorio de la app
WORKDIR /app

# Copia los archivos de requirements y los instala
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia el resto del código de la app
COPY app/ .

# Expone el puerto (ajusta si usas otro)
EXPOSE 8001

# Comando para correr FastAPI con Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]