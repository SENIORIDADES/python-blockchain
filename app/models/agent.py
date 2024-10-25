from typing import List, Dict

class Agent:
    def __init__(self, identifier: str, public_key: str,
                 agent_type: str = None, issued_hashes: List[Dict] = None,
                 location: List[Dict] = None, metadata: List[Dict] = None):
        self.identifier = identifier
        self.public_key = public_key
        self.agent_type = agent_type if agent_type is not None else {} 
        self.issued_hashes = issued_hashes if issued_hashes is not None else []
        self.location = location if location is not None else []
        self.metadata = metadata if metadata is not None else []

    def to_dict(self):
        return {
            "identifier": self.identifier,
            "public_key": self.public_key,
            "agent_type": self.agent_type,
            "issued_hashes": self.issued_hashes,
            "location": self.location, 
            "metadata": self.metadata        
        }
