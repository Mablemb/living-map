FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

# Instala dependências do Python primeiro para melhor cache
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código
COPY . .

# Comando padrão: script de entrada que roda migrações e depois o Gunicorn
CMD ["./entrypoint.sh"]
