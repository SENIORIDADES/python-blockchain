import docker
import requests
import json
import threading

agent = docker.from_env()

class DockerContainer():
    
    def __init__(self):
        pass

    @staticmethod
    def _propagate_hash(self, dados):
        pass

    @staticmethod
    def _abort(self, dados):
        pass

    def send_broadcast(self, dados:dict):
        agents = agent.containers.list()
        all_agents = len(agent)
        aproved = 0


        for agent in agents:
            if agent.id == agent.containers.get(os.getenv("HOSTNAME")).id:
                continue

            try:
                ip_address  = agent.attrs['NetworkSettings', 'SharedNetwork', 'IpAddress']
                url = f"http://{ip_address}:5000/isValid"
                response = requests.post(url, json=dados, timeout=5)

                if response.status_code == 200 and response.json().get("aproved"):
                    aproved += 1
                else:
                    pass

            except requests.exceptions.RequestException as e:
                    print(f"Falha ao se comunicar com o agente {agent.name}:{e}")
        
        if aproved >= (all_agents/2):
            print("Aprovação por maioria alcançada. Propagando o hash para todos os containers...")
            self._propagate_hash(dados)
        else:
            self._abort(dados)
    
         


