from flask import Blueprint, request, jsonify
from http import HTTPStatus 
from app.services import AgentService
from ..services.locationService import LocationService
from ..services.blockService import BlockService
from ..services.dockerService import DockerService

# Definindo os blueprints para login e adicionar agente
login_routes = Blueprint('login', __name__)
add_agent_routes = Blueprint('add_agent', __name__)
update_agents_routes = Blueprint('update_agent',__name__)

# Rota para login
@login_routes.route('/login', methods=['POST'])
def login():
    """
    Endpoint para fazer login de um usuário.

    Corpo da Requisição:
    {
        "identifier": "identificador_do_usuario"
    }

    Respostas:
    - 200: Login bem-sucedido
    - 400: Identificador ou chave pública não fornecidos
    - 401: Identificador ou chave pública inválidos
    """
    data = request.json  # Obtém os dados da requisição

    identifier_request = data.get('identifier')  # Obtém o identificador do usuário

    if not identifier_request:
        # Se o identificador não for fornecido, retorna erro 400
        return jsonify({
            "Message": "Identificador não localizado"}), HTTPStatus.BAD_REQUEST
    
    # Tenta buscar o agente (usuário) com o identificador
    print("Debug: Fazendo busca local...") 
    agent = AgentService.search_agent(identifier_request)
    
    if agent is None:
        # Se o agente não for encontrado, retorna erro 401
        return jsonify({
            "Message": "Identificador não localizado"}), HTTPStatus.UNAUTHORIZED  
    
    print("Debug: Agente localizado...") 

    print("Debug: Iniciando busca na blockchain...")
    block_service = BlockService()
    agent_block = block_service.find_block(identifier_request)

    if agent_block is None:
            print("Debug: Agente não autorizado na blockchain...")
            # Se o agente não for encontrado, retorna erro 401
            return jsonify({"Message": "Agente não localizado na blockchain"}), HTTPStatus.UNAUTHORIZED   
        
    print("Debug: Agente localizado com sucesso!")
    print("Debug: Acessando a rede...")
    container_service = DockerService()
    container_service.find_container(identifier_request)
    print("Debug: Login bem-sucedido")
    # Retorna mensagem de sucesso no login
    return jsonify({"Message": "Login bem-sucedido"}), HTTPStatus.OK

# Rota para adicionar um novo agente
@add_agent_routes.route('/newAgent', methods=['POST'])
def add_agent():
    """
    Endpoint para adicionar um novo agente.

    Corpo da Requisição:
    {
        "identifier": "identificador_do_novo_agente"
    }

    Respostas:
    - 201: Agente adicionado com sucesso
    - 400: Identificador ou chave pública não fornecidos
    - 409: Agente já existe
    - 500: Ocorreu um erro
    """
    data = request.json  # Obtém os dados da requisição

    identifier_request = data.get('identifier')  # Obtém o identificador do agente
    if not identifier_request:
        # Se o identificador não for fornecido, retorna erro 400
        return jsonify({"Message": "Identificador não fornecido"}), HTTPStatus.BAD_REQUEST

    try:
        # Usando o serviço para adicionar o agente
        response = AgentService.add_agent(identifier_request)
        #Identificando a public_key para instaciar o bloco
    
        data = response['data']

        if not response["success"]:
            if "já existe" in response["error"]:
                print("Debug: Falha ao iniciar autenticação blockchain")
                return jsonify({"Message": response["error"]}), HTTPStatus.CONFLICT
            return jsonify({"Message": response["error"]}), HTTPStatus.BAD_REQUEST
        print("Debug: Iniciando autenticação blockchain...")
        block_service = BlockService()
        block_service.add_block(data)

        print("Debug: Acessando a rede...")
        container_service = DockerService()
        container_service.start_container(identifier_request)

        # Retorna os dados do agente criado com sucesso
        return jsonify(response["data"]), HTTPStatus.CREATED

    except Exception as e:
        # Se ocorrer um erro, retorna erro 500
        return jsonify({"Message": f"Ocorreu um erro: {str(e)}"}), HTTPStatus.INTERNAL_SERVER_ERROR

@update_agents_routes.route('/updateAgent', methods=['PUT'])
def update_agent():
    """
    Endpoint para atualizar informações de um agente existente.

    Corpo da Requisição:
    {
        "identifier": "identificador_do_agente",
    }

    Respostas:
    - 200: Agente atualizado com sucesso
    - 400: Dados inválidos ou não fornecidos
    - 404: Agente não encontrado
    - 500: Ocorreu um erro
    """
    data = request.json  # Obtém os dados da requisição
    
    identifier_request = data.get('identifier')  # Obtém o identificador do agente
    
    if not identifier_request:
        return jsonify({"Message": "Identificador não fornecido"}), HTTPStatus.BAD_REQUEST

    try:
        # Chama o serviço para recuperar as informações atualizadas do agente
        new_metadata_response = LocationService.locationService(identifier_request)

        # Verifica se a operação foi bem-sucedida
        if not new_metadata_response["success"]:
            return jsonify({"Message": new_metadata_response["error"]}), HTTPStatus.BAD_REQUEST
        
        new_metadata = new_metadata_response["data"]  # Extrai o metadata da resposta
        
        # Chama o serviço para atualizar as informações do agente
        response = AgentService.update_agent(identifier_request, new_metadata)
        
        if not response["success"]:
            print("Debug: Falha ao iniciar autenticação blockchain")
            return jsonify({"Message": response["error"]}), HTTPStatus.BAD_REQUEST 
        # Retorna a resposta de sucesso com os dados atualizados
        print("Debug: Iniciando autenticação blockchain...")
        block_service = BlockService()
        block_service.add_block(response["data"])
        return jsonify({"Message": "Agente atualizado com sucesso", 
                        "data": response["data"]}), HTTPStatus.OK

    except Exception as e:
        return jsonify({"Message": f"Ocorreu um erro: {str(e)}"}), HTTPStatus.INTERNAL_SERVER_ERROR
