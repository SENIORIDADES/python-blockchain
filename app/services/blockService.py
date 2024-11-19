from app.models import Block
import datetime

class BlockService:
    def __init__(self):
        self.blocks = []

    @staticmethod
    def _generated_hash(previus_hash:str, agent:list[dict]):
        nonce = 0
        
        timestamp = datetime.datetime.now()
        data = agent
        timestamp = datetime.now


    @staticmethod
    def _create_genesis_block(version:str, previous_hash:str, 
                              nonce, score, network):
        timestamp = datetime.datetime.now()
        data = {
            "client": "PetroLocus",
            "description": "Registro de jazidas de petróleo",
            "security_protocols": ["HTTP/JSON"],
            "consensus_mechanism": "Delegated Proof of Stake",
            "technology_integration": ["Drones", "navios"],
            "mapping": "Geográfico",
            "delegates": network,
            "data_quality": score 
        }
        
        Block = []
        
        hash_value = Block(version, timestamp, data, previous_hash, nonce).calculate_hash()
        genesis_block = Block(version, timestamp, data, previous_hash, nonce, hash_value)
        
        Block.append(genesis_block)
        return genesis_block
