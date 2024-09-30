from app.services.block_service import BlockService

if __name__ == "__main__":
    block_service = BlockService()

    version = "1.0"
    previous_hash = "0"
    nonce = 0
    score = 100  
    network = ["Genesis"] 

    genesis_block = block_service.create_genesis_block(version, previous_hash, nonce, score, network)

    print(f"Bloco gênese: {genesis_block.__dict__}")