import hashlib
from typing import List, Dict

class Block:
    def __init__(self, version:str, timestamp:str, 
                 previous_hash:str, nonce:str, 
                 hash_value:str, data:List[Dict]):        
        self.version = version
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash_value = hash_value
        self.data = data

    def to_hash(block):
        hash = hashlib.sha256()
        hash.update((block).encode('utf-8'))
        return hash.hexdigest()