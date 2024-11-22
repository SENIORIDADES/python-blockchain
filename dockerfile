# Usando uma imagem base com Python 3.9 slim
FROM python:3.9-slim

# Atualizando o repositório e instalando pacotes necessários
RUN apt-get update && apt-get install -y \
    vim \
    curl \
    python3-pip \
    && apt-get clean

# Definindo o diretório de trabalho no container
WORKDIR /app

# Copiando o arquivo de dependências antes do código
COPY requirements.txt /app/

# Criando um ambiente virtual para o Python
RUN python3 -m venv /app/venv

# Instalando as dependências dentro do ambiente virtual
RUN /app/venv/bin/pip install --no-cache-dir -r requirements.txt

# Copiando o código-fonte para o diretório de trabalho no container
COPY . /app

# Adicionando o ambiente virtual ao PATH
ENV PATH="/app/venv/bin:$PATH"

# Expondo a porta para o servidor Flask
EXPOSE 5000

# Comando para rodar a aplicação
CMD ["python3", "main.py"]