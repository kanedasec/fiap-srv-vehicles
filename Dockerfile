# Dockerfile
FROM python:3.13-slim

WORKDIR /app

# Instalar dependências do sistema necessárias para psycopg2
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Tornar o diretório /app visível para imports Python
ENV PYTHONPATH=/app

# Copiar requirements e instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo o código da aplicação
COPY . .

# Expôr porta do FastAPI
EXPOSE 8000

# Corrigimos o caminho para src.main:app
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
