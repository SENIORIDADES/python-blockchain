# app/routes/__init__.py
from .agentRoute import login_routes, add_agent_routes

# Referenciando as rotas para modularização
def register_routes(app):
    app.register_blueprint(login_routes, url_prefix='')
    app.register_blueprint(add_agent_routes, url_prefix='')
