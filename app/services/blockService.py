from .jsonService import JsonService
import json
import datetime
import hashlib

class BlockService:
    def __init__(self, json_path="app/database/chain.json"):
        # Inicializa o arquivo de banco de dados, se ainda não existir
        self.json_path = json_path
        self.chain = JsonService.load_json(self.json_path)

    @staticmethod
    def _calculate_hash(block):
        """Calcula o hash de um bloco."""
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @staticmethod
    def _create_genesis_block():
        """Cria o bloco gênesis."""
        genesis_block = {
            "previous_hash": "00000000000000000000000000000000",
            "data": {
                "client": "PetroLocus",
                "description": "Registro de jazidas de Petróleo",
                "security_protocols": ["HTTP/JSON"],
                "consensus_mechanism": "Majority Consensus",
                "technology_integration": ["Drones", "navios"],
                "mapping": "Geografico",
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        }

        genesis_block["hash"] = BlockService._calculate_hash(genesis_block)
        return genesis_block

    def find_block(self, identifier:str) -> dict:
        """
        Busca um bloco na blockchain pelo identificador.
        """
        for block in self.chain:
            if block["data"].get("identifier") == identifier:
                return block
        print(f"Nenhum bloco encontrado com o identifier: {identifier}")
        return None    
        
    def add_block(self, new_data: dict):
        """
        Adiciona um novo bloco à blockchain.

        Se não houver blocos existentes, cria o bloco gênesis.
        Caso contrário, utiliza o hash do último bloco como previous_hash.
        """
        """
        Adiciona um novo bloco à blockchain.
        """
        if not self.chain:  # Se a blockchain está vazia
            print("Debug: Criando bloco genenis...")
            genesis_block = self._create_genesis_block()
            self.chain.append(genesis_block)
            print("Debug: Bloco gênesis criado com sucesso")
            JsonService.save_json(self.json_path, self.chain)

        # Adiciona um novo bloco
        print("Debug: Adicionando novo bloco...")
        previous_hash = self.chain[-1]["hash"]
        new_block = {
            "data": new_data,
            "previous_hash": previous_hash
        }
        new_block["hash"] = self._calculate_hash(new_block)
        self.chain.append(new_block)

    
        # Salva a blockchain
        JsonService.save_json(self.json_path, self.chain)
        print(f"Debug: Novo bloco adicionado com sucesso")