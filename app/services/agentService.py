import hashlib
import re
import datetime
from typing import Optional, Dict
from app.models import Agent
from .jsonService import JsonService

class AgentService:

    @staticmethod
    def search_agent(identifier: str) -> Optional[Dict]:
        """Busca agente pelo identificador e opcionalmente pela chave pública."""

        # Buscando o arquivo JSON que armazena os agentes
        filename = JsonService.search_json('app/database', 'storage.json')
        if not filename:
            print("Debug: Arquivo não encontrado.")
            return None

        # Carregando os agentes existentes do arquivo JSON
        agents = JsonService.load_json(filename)

        print(f"Debug: Procurando agente com identificador {identifier}...")

        # Iterando sobre os agentes para encontrar o correspondente
        for agent in agents:
            if agent['identifier'] == identifier:
                    print(f"Debug: Agente encontrado: {agent}")
                    return agent

        print("Debug: Agente não encontrado.")
        return None

    @staticmethod
    def classify_agent(identifier: str) -> Optional[str]:
        """Classificando o agente com base no formato do identificador."""
        print(f"Debug: Classificando agente com identificador {identifier}...")
        
        # Verifica se o identificador segue o formato esperado
        if not re.match(r'^[ND]\d{5,6}', identifier):
            print("Debug: Formato de identificador inválido.")
            return None

        # Classificando o agente como "Navio" ou "Drone" baseado no identificador
        if re.match(r'^N\d{5}$', identifier):
            print(f"Debug: O agente {identifier} foi classificado como 'Navio'.")
            return "Ship"
        if re.match(r'^D\d{6}$', identifier):
            print(f"Debug: O agente {identifier} foi classificado como 'Drone'.")
            return "Drone"

    @staticmethod
    def hashe_genereted(identifier: str) -> Optional[str]:
        """Gerando um hash SHA-256 baseado no identificador."""
        print(f"Debug: Gerando hash para o identificador {identifier}...")
        
        generated_key = hashlib.sha256()
        generated_key.update(identifier.encode('utf-8'))
        hash_value = generated_key.hexdigest()
        
        print(f"Debug: Hash gerado: {hash_value}")
        return hash_value

    @staticmethod
    def check_agent_exists(identifier:str) -> bool:
        try:
            existing_agent = AgentService.search_agent(identifier)
            return existing_agent is not None
        except Exception as e:
            print(f"Erro ao verificar existência do agente: {e}")
            return False

    @staticmethod
    def add_agent(identifier: str) -> Dict:
        """
        Adiciona um novo agente com o identificador e chave pública especificados.
        Retorna um dicionário com o status do processo.
        """

        # Verificando se o agente já existe
        if AgentService.check_agent_exists(identifier):
            print(f"Debug: Agente com identificador {identifier} já existe.")
            return {
                "success": False,
                "data": {},
                "error": f"Agente com identificador {identifier} já existe."
            }

        # Validando e gerando os dados do novo agente
        try:
            public_key = AgentService.hashe_genereted(identifier)
            if not public_key:
                return {
                    "success": False,
                    "data": {},
                    "error": "Erro ao gerar chave pública."
                }

            agent_type = AgentService.classify_agent(identifier)
            if not agent_type:
                return {
                    "success": False,
                    "data": {},
                    "error": "Identificador inválido ou não reconhecido."
                }
            print(f"Debug: Gerando dados...")
            print(f"Debug: Dados gerados com sucesso: {agent_type}, {public_key}")
        except Exception as e:
            print(f"Erro ao processar dados do agente: {e}")
            return {
                "success": False,
                "data": {},
                "error": "Erro ao processar dados do agente."
            }

        # Criando a instância do agente
        new_agent = Agent(
            identifier=identifier,
            public_key=public_key,
            metadata={
                "agent_type": agent_type,
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "location": "",
                "geolocation": {"latitude": None, "longitude": None},
            },
        )
        print(f"Debug: Novo agente criado...")

        # Buscando e atualizando o arquivo JSON
        try:
            filename = JsonService.search_json('app/database', 'storage.json')
            if not filename:
                return {
                    "success": False,
                    "data": {},
                    "error": "Arquivo de agentes não encontrado."
                }

            agents = JsonService.load_json(filename)
            agents.append(new_agent.to_dict())
            JsonService.save_json(filename, agents)
            print(f"Debug: Agente salvo com sucesso.")
        except Exception as e:
            print(f"Erro ao manipular arquivo JSON: {e}")
            return {
                "success": False,
                "data": {},
                "error": "Erro ao manipular arquivo JSON."
            }

        # Retorna o novo agente como um dicionário
        return {
            "success": True,
            "data": new_agent.to_dict(),
            "error": ""
        }


