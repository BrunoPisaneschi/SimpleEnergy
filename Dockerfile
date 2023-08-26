# Utilize uma imagem oficial do Python
FROM python:3.11-slim-buster

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

# Comando para executar a aplicação
CMD ["uvicorn", "main:app", "--workers", "5", "--host", "0.0.0.0", "--port", "8000"]
