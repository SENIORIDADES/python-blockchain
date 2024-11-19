import docker
import requests
import asyncio
import aiohttp
import os

class DockerContainer():
    
    def __init__(self):
       self.agent = docker.from_env()
       self.hostname = os.getenv("HOSTNAME")
       self.network_name = "blockchain"

    @staticmethod
    async def _propagate_hash(self, dados):
        agents = self.agent.containers.list()
        async with aiohttp.ClientSession() as session:
            for agent in agents:
                try:
                    ip_address = agent.attrs['NetworkSettings']['Networks'][self.network_name]['IPAddress']
                    url = f"http://{ip_address}:5000/nome_do_endpoint_salvar_json"
                    await session.post(url,json=dados, timeout=5)
                    print(f"Hash salvo com sucesso para o agente {agent.name}")
                except aiohttp.ClientError as e:
                    print(f"Erro ao salvar hash do agent {agent.name}:{e}")

    @staticmethod
    def _abort(self, dados):
        pass

    async def send_broadcast(self, dados: dict):
        agents = self.client.containers.list()
        all_agents = len(agents)
        required_votes = all_agents // 2 + 1
        approved = 0
        rejected = 0

        async with aiohttp.ClientSession() as session:
            tasks = []

            for agent in agents:
                if agent.id == self.client.containers.get(self.hostname).id:
                    continue

                ip_address = agent.attrs['NetworkSettings']['Networks'][self.network_name]['IpAddress']
                url = f"http://{ip_address}:5000/isValid"
                tasks.append(self._send_request(session, url, dados))

            results = await asyncio.gather(*tasks, return_exceptions=True)

            for result in results:
                if isinstance(result, dict) and result.get("approved"):
                    approved += 1
                else:
                    rejected += 1
                
                if approved >= required_votes:
                    print("Debug: Consenso aprovado! Salvando o hash...")
                    self._save_to_local_storage(dados)
                    return
                elif rejected >= required_votes:
                    print("Debug: Consenso rejeitado. Abortando...")
                    self._abort(dados)
                    return

            
    
         


