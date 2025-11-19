FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

# Instala dependências do Python primeiro para melhor cache
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código
COPY . .

# Comando para iniciar o servidor Django com Gunicorn no Render
CMD ["gunicorn", "living_map.wsgi:application", "--bind", "0.0.0.0:${PORT}"]
