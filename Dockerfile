# Usar uma imagem base do Python
FROM python:3.8-slim

# Definir o diretório de trabalho no container
WORKDIR /app

# Copiar os arquivos da aplicação para o diretório de trabalho
COPY . /app

# Instalar as dependências da aplicação
RUN pip install --no-cache-dir -r requirements.txt

# Expor a porta em que a aplicação será executada (caso aplicável)
EXPOSE 5500

# Comando para rodar a aplicação
CMD ["python", "app.py"]
