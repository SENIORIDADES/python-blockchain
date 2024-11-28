import docker
import aiohttp
import os
from http import HTTPStatus 
from dotenv import load_dotenv
from dotenv import load_dotenv
from .jsonService import JsonService

load_dotenv()

class DockerService:
    def __init__(self):
        self.client = docker.from_env()  # Usando a API do Docker
        self.network_name = os.getenv("NETWORK_NAME")  # Carrega o nome da rede
        self.hostname = os.getenv("HOSTNAME")          # Carrega o nome do container atual


    def start_container(self, identifier: str):
        """
        Inicia um container para o agente fornecido.

        :param identifier: Identificador único do agente.
        """
        try:
            container_name = f"agent_{identifier}"  # Nome do container baseado no identificador
            container = self.client.containers.run(
                "petrochain_v1",  
                name=container_name,
                detach=True,  # Faz o container rodar em segundo plano
                environment={"IDENTIFIER": identifier}
            )
            print(f"Debug: Container {container_name} iniciado com sucesso.")
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


    async def send_broadcast(self, dados: dict):
        """
        Envia um broadcast para todos os containers e aguarda o consenso.

        :param dados: Dados a serem enviados no broadcast.
        """
        print(f"Chegando aqui{dados}")
        agents = self.client.containers.list() # Lista todos os containers
        all_agents = len(agents)  # Total de containers
        print(f"Eu tenho {all_agents} agents")  
        required_votes = all_agents // 2 + 1  # Número mínimo de votos para o consenso
        approved = 0
        rejected = 0

        # Cria uma sessão assíncrona para as requisições HTTP
        async with aiohttp.ClientSession() as session:
            tasks = []

            for agent in agents:
                if agent.id == self.client.containers.get(self.hostname).id:
                    continue  # Ignora o container atual

                ip_address = agent.attrs['NetworkSettings']['Networks'][self.network_name]['IpAddress']
                url = f"http://{ip_address}/updateAgent"  # URL de validação no container

                # Realiza a requisição diretamente dentro do loop
                async with session.post(url, json=dados) as response:
                    if response.status == HTTPStatus.OK:
                        result = await response.json()  # Processa a resposta como JSON
                    else:
                        result = {"approved": False}  # Caso o status não seja OK, assume rejeição

                    # Processa o resultado da requisição
                    if isinstance(result, dict) and result.get("approved"):  # Se aprovado
                        approved += 1
                    else:
                        rejected += 1  # Caso contrário, rejeitado

                    filename = JsonService.search_json('app/database', 'chain.json')

                    # Verifica se o consenso foi alcançado
                    if approved >= required_votes:
                        print("Debug: Consenso aprovado! Salvando o hash...")
                        JsonService.save_json(filename, dados)
                        print("Debug: Salvando o hash...")
                        return  # Encerra o processo após consenso aprovado
                    elif rejected >= required_votes:
                        print("Debug: Consenso rejeitado. Abortando...")
                        break  # Interrompe o processo após o número necessário de rejeições