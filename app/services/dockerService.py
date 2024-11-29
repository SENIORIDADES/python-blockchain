import docker
import requests
import os
from http import HTTPStatus 
from dotenv import load_dotenv
from dotenv import load_dotenv
from .jsonService import JsonService
from docker.errors import NotFound

load_dotenv()

class DockerService:
    def __init__(self):
        self.client = docker.from_env()  # Usando a API do Docker
        self.network_name = os.getenv("NETWORK_NAME")  # Carrega o nome da rede
        self.hostname = os.getenv("HOSTNAME")
        self.filename = JsonService.search_json('app/database', 'chain.json') # Carrega o nome do container atual
        self.chain = JsonService.load_json(self.filename)

    def container_exists(self, identifier: str) -> bool:
        try:
            container = self.client.containers.get(f"agent_{identifier}")
            return True
        except NotFound:
            return False

    def start_container(self, identifier: str):
        """
        Inicia um container para o agente fornecido.

        :param identifier: Identificador único do agente.
        """
        container_name = f"agent_{identifier}"  # Nome do container baseado no identificador
        if self.container_exists(identifier):
            container = self.client.containers.get(container_name)
            if container.status != "running":
                container.start()
            else:
                return container
        try:
            container = self.client.containers.run(
                "petrochain_v1",  
                name=container_name,
                command="python3 main.py",
                ports={'5001/tcp': 5000},
                detach=True,  # Faz o container rodar em segundo plano
                environment={"IDENTIFIER": identifier}
            )
            print(f"Debug: Container {container_name} iniciado com sucesso.")
            return container
        except Exception as e:
            print(f"Erro ao iniciar container para o agente {identifier}: {str(e)}")

    def find_container(self, identifier: str) -> docker.models.containers.Container:
        """
        Busca o container pelo identificador fornecido.

        :param identifier: Identificador único do agente.
        :return: O container encontrado ou None caso não exista.
        """
        try:
            containers = self.client.containers.list(all=True) 
            container_name = f"agent_{identifier}"

            for container in containers:
                if container_name in container.name:
                    return container  
            return None

        except docker.errors.DockerException as e:
            raise Exception(f"Erro ao comunicar com o Docker: {str(e)}")


    async def send_broadcast(self, data: dict , identifier:str):
        """
        Envia um broadcast para todos os containers e aguarda o consenso.

        :param dados: Dados a serem enviados no broadcast.
        """      
        agents = self.client.containers.list()  # Lista todos os containers
        all_agents = len(agents)  # Total de containers 
        current_agent = identifier
        required_votes = all_agents // 2 + 1  # Número mínimo de votos para o consenso
        approved = 0
        rejected = 0

        for agent in agents:
            if agent.id == current_agent:
                continue  # Ignora o container atual     
            
            ip_address = agent.attrs['NetworkSettings']['Networks'][self.network_name]['IPAddress']  
            url = f"http://{ip_address}:5001/mine"  # URL de validação no container
            print(f"Debug: Tentando conectar ao URL: {url}")
            
            # Realiza a requisição HTTP diretamente dentro do loop, de forma síncrona
            response= requests.post(url, json=data)
            if response.status_code == HTTPStatus.ACCEPTED:
                result = response.json()  # Processa a resposta como JSON
                print(f"Resultado: {result}")
            else:
                result = {"approved": False}  # Caso o status não seja OK, assume rejeição
                print(f"Resultado: {result}")

            # Processa o resultado da requisição
            if isinstance(result, dict) and result.get("approved"):  # Se aprovado
                approved += 1
            else:
                rejected += 1  # Caso contrário, rejeitado

            # Verifica se o consenso foi alcançado
            if approved >= required_votes:
                ("Debug: Consenso aprovado! Salvando o hash...")
                self.chain.append(data)
                JsonService.save_json(self.filename, data)
                
                for agent in agents:
                    ip_address = agent.attrs['NetworkSettings']['Networks'][self.network_name]['IPAddress']  
                    url = f"http://{ip_address}:5001/updateChain"  # URL de validação no container

                    response = requests.post(url, json={'chain':self.chain})
                    
                    if response.status_code == HTTPStatus.ACCEPTED:
                        print(f"Chain atualizada no agente {agent.id}")
                    else:
                        print(f"Debug: Erro ao atualizar a chain no agente {agent.id}")
                return  # Encerra o processo após consenso aprovado
            elif rejected >= required_votes:
                print("Debug: Consenso rejeitado. Abortando...")
                break  # Interrompe o processo após o número necessário de rejeições