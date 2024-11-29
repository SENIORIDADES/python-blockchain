from flask import Blueprint, request, jsonify
from http import HTTPStatus
from services import jsonService

mine_routes = Blueprint('mine', __name__)
update_chain_routes = Blueprint('updateChain', __name__)

@mine_routes.route("/mine", methods=["POST"])
def mine():
    """
    Recebe dados via POST, processa e retorna uma resposta.
    """
    print(f"Dados recebidos")
    try:
        dados = request.json  # Obtém os dados do corpo da requisição
        print(f"Dados recebidos: {dados}")

        return jsonify({
            "approved": True,
            "message": "Recebido com sucesso"
        }), HTTPStatus.ACCEPTED
    except Exception as e:
        # Caso ocorra algum erro, retornamos a resposta com erro.
        return jsonify({
            "approved": False,
            "message": str(e)
        }), HTTPStatus.BAD_REQUEST

@update_chain_routes.route('/updateChain', methods=['POST'])
def update_chain():
    data = request.json

    filename = jsonService.JsonService.search_json('app/database', 'chain.json')

    if 'chain' in data:
        jsonService.JsonService.save_json(filename, data)
        return {
            "message": "Agente atualizado com sucesso"
        }, HTTPStatus.ACCEPTED
    return {
        "message": "Dados invalidos"
    }, HTTPStatus.BAD_REQUEST
