FROM python:3.9-slim-buster

# Instale as dependências do sistema
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Instale as dependências do Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copie o script Python e o arquivo .env para o container
COPY app.py /nytimes-scrapping/

# Defina o diretório de trabalho
WORKDIR /nytimes-scrapping

# Execute o script Python
CMD ["python", "app.py"]