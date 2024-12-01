import json
import os
from typing import Optional, List, Dict
from datetime import datetime

class JsonService:
    @staticmethod
    def search_json(directory: str, filename: str) -> Optional[str]:
        """Buscando se o arquivo com o nome especificado existe no diretório."""
        print(f"Debug: Procurando pelo arquivo {filename} no diretório {directory}...")
        for root, __, files in os.walk(directory):
            if filename in files:
                print(f"Debug: Arquivo {filename} encontrado em {root}.")
                return os.path.join(root, filename)
        print(f"Debug: Arquivo {filename} não encontrado.")
        return None
    
    @staticmethod
    def load_json(filename: str) -> List[Dict]:
        """Carregando dados do arquivo JSON."""
        print(f"Debug: Carregando dados do arquivo {filename}...")
        if not os.path.exists(filename) or os.stat(filename).st_size == 0:
            print("Debug: Se o arquivo não existe ou está vazio. Se não existir, cria um novo arquivo vazio...")
            with open(filename, 'w') as file:
                json.dump([], file, indent=4)
            return []
        
        with open(filename, 'r') as file:
            try:
                data = json.load(file)
                print(f"Debug: {len(data)} registros carregados do arquivo.")
                return data
            except json.JSONDecodeError:
                print("Debug: Erro ao decodificar o arquivo JSON.")
                return []

    @staticmethod
    def get_last_coordinates(filename: str) -> Optional[tuple]:
        """Obtendo as últimas coordenadas do arquivo JSON."""
        print(f"Debug: Obtendo as coordenadas mais recentes do arquivo {filename}...")
        # Carregando os dados existentes e verificando se o agente já existe
        coordinates = JsonService.load_json(filename)

        if not coordinates:
            print("O arquivo Json está vazio.")
            return None
        
        # Ordenando as coordenadas pela data mais recente
        print("Ordenando coordenadas pela data mais recente...")
        sorted_coordinates = sorted(coordinates, 
          key=lambda x: datetime.strptime(x['metadata']['timestamp'], "%Y-%m-%d %H:%M:%S"), reverse=True)
        
        # Pegando a coordenada mais recente
        last_coordinates = sorted_coordinates[0]
        print(f"Última coordenada encontrada: {last_coordinates['metadata']['geolocation']}")
        
        # Verificando se 'geolocation' e as chaves necessárias existem no último agente
        if 'geolocation' in last_coordinates['metadata']:
            latitude = last_coordinates['metadata']['geolocation']['latitude']
            longitude = last_coordinates['metadata']['geolocation']['longitude']
            print(f"Coordenadas: Latitude: {latitude}, Longitude: {longitude}")
            return latitude, longitude
        else:
            print("Dados de geolocalização ausentes.")
            return None

    @staticmethod
    def save_json(filename: str, data: List[Dict]) -> None:
        """Salvando dados no arquivo JSON."""
        print(f"Salvando dados no arquivo {filename}...")
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
        print("Dados salvos com sucesso.")
