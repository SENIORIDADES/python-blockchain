from ..models.block_model import Block
import datetime

class BlockService:
    def __init__(self):
        self.blocks = []

    def create_genesis_block(self, version, previous_hash, nonce, score, network):
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

        
        hash_value = Block(version, timestamp, data, previous_hash, nonce).calculate_hash()
        genesis_block = Block(version, timestamp, data, previous_hash, nonce, hash_value)
        
        self.blocks.append(genesis_block)
        return genesis_block
