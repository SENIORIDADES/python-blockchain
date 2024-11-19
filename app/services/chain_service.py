from .blockService import BlockService
from app.models import Block

class Blockchain:
  def __init__(self):
    self.chain = [BlockService.create_genesis_block]

  def add_block(self, new_block):
    Block.new_block.previous_hash = self.chain[-1].hash
    Block.new_block.hash = new_block.calculate_hash()
    self.chain.append(Block.new_block)

def is_valid(self):
    for i in range(1, len(self.chain)):
        current_block = self.chain[i]
        previous_block = self.chain[i - 1]

        if current_block.hash != current_block.calculate_hash():
            return False
        
        if current_block.previous_hash != previous_block.hash:
            return False
            
    return True