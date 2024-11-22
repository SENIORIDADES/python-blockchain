import docker
import os
import requests
from flask import request

class DockerService:
    def __init__(self):
        self.client = docker.from_env()  # Usando a API do Docker

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
