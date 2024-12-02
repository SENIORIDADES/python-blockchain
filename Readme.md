![Wallpapper](https://private-user-images.githubusercontent.com/126973782/391306771-f01bcb18-b13a-4037-adf0-e66d9090a7a1.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MzMxMDg3NTksIm5iZiI6MTczMzEwODQ1OSwicGF0aCI6Ii8xMjY5NzM3ODIvMzkxMzA2NzcxLWYwMWJjYjE4LWIxM2EtNDAzNy1hZGYwLWU2NmQ5MDkwYTdhMS5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjQxMjAyJTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI0MTIwMlQwMzAwNTlaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT1kYzY2YjhlN2RkMTM4MzdiYmIwZGQ5YjMyODM3NDQ5OTY0MWZlOGRkMjA1MzMwOGNjYjg1ODU1NjU1MzMyZjg4JlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.hS0VQLURMWVnWgG1Tsh4YTLb7GCBrMRyHxqaBB7fOKk)

<table>
  <tr>
    <td>
      Status : Concluido ✔️ 
    </td>
    <td>
      <img align="center" alt="Ally-Bootstrap" height="20" width="110" src="https://img.shields.io/badge/version-1.0-purple">
    </td>
  </tr>
</table>

## Proposta de projeto

> O objetivo desse projeto foi construir uma blockchain capaz de armazenar dados de mineração extraidos por agentes(drones e navios). Petrolocus, nosso cliente, solicitou a criação da rede afim de documentar seus pontos de mineração em um sistema imutavel.

## Dados do projeto

- Titulo: Petrochain;
- Tipo: Aplicação backend;
- Stakeholder: Biopark Educação, Petrolocus.

## Tecnologias utilizadas

<table>
  <tr>
    <td>
      <img align="center" alt="Ally-Bootstrap" height="30" width="170" src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white">   
    </td>
    <td>
      <img align="center" alt="Ally-CSS" height="30" width="170" src="https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white&backgroundColor=white))">
    </td>
    <td>
      <img align="center" alt="Ally-Bootstrap" height="30" width="170" src="https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white&backgroundColor=white))">    
    </td>
  </tr>
</table>

### Como rodar:
```sh
cd /

cd home

mkdir blockchain

cd blockchain

git clone https://github.com/SENIORIDADES/python-blockchain.git

cd python-blockchain

cd app

code . #Para abrir o código no vscode

# Verifique se você esta na pasta correta ls na lista deve aparecer o arquivo dockerfile, estando na pasta correta execute:

docker build --no-cache  --build-arg UID=$(id -u) --build-arg GID=$(id -g) -t petrochain_v1 .

docker images #Para verificar se sua imagem subiu com sucesso. Deverá exibir algo como:

 REPOSITORY      TAG      IMAGE ID      CREATED        SIZE

 petrochain_v1  latest  a1b2c3d4e5f6  2 minutes ago   500MB 

execute o main.py
```

### Como testar:

> Utilizando o [insomnia]([URL](https://insomnia.rest)) é possivel testar as rotas.

```yml
docker_url: <endereço-python-server>:5000
```
- Para adicionar agentes:
```python
# Endpoint para adicionar um novo agente.
[POST] docker_url/newAgent
    Corpo da Requisição:
    {
        "identifier": "identificador_do_novo_agente"
    }
```
- Para adicionar blocos:
```python
# Endpoint para atualizar informações de um agente existente.
[PUT] docker_url/updateAgent
    Corpo da Requisição:
    {
        "identifier": "identificador_do_agente"
    }
```

### Ver oque foi salvo:

```sh
# Execute os comandos na sequência:

docker ps #Lista todos containers

docker exec -it <container_name> /bin/bash # Entra dentro do container

cd database # Navega até o diretório

vim chain.json # Abre o arquivo no terminal

# Com esses passos você pode verificar sua chain
```
### Observações
  - Todo o projeto foi criado e testado utilizando WSL e insomnia;
  - Em caso de erros com o diretório, reinicie o vscode;
  - ![Documento 📄](https://drive.google.com/file/d/1beSAXPtCxDlW30BVIGFmyBzj3gJt0AXm/view?usp=sharing)
  - ![Figma 🖥️](https://www.figma.com/proto/qNjYpo9nwQRPvgBS2nznHp/Petrochain?node-id=1-3&node-type=canvas&t=8nSn6xiesmVJqQQq-1&scaling=min-zoom&content-scaling=fixed&page-id=0%3A1)
  - ![Youtube ▶️](https://youtu.be/cBIKng548y0?si=i-8w9tyF5YGfzAp9)


### Versões:

```python
python=3.9-slim
flask=2.2.3
werkzeug=2.2.3
docker=7.1.0
requests=2.32.3
python-dotenv=1.0.1
pip=24.3.1
```
## Autores
<p>
  <img src="https://github.com/devpisa.png?size=400" width="40" height="40">
  <img src="https://github.com/gustavocortelassi.png?size=400" width="40" height="40">
  <img src="https://github.com/KronosZbr.png?size=400" width="40" height="40">
  <img src="https://github.com/Kainak.png?size=400" width="40" height="40">
  <img src="https://github.com/MatheusMorilha.png?size=400" width="40" height="40">
</p>

**Projeto criado com objetivos educacionais e dados fictícios, podem haver bugs.* **Não deverá ser usado para fins comerciais.*