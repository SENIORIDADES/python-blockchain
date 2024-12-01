# app/routes/__init__.py
from .agentRoute import login_routes, add_agent_routes, update_agents_routes
from .mineRoute import mine_routes, update_chain_routes

# Referenciando as rotas para modularização
def register_routes(app):
    app.register_blueprint(login_routes, url_prefix='')
    app.register_blueprint(add_agent_routes, url_prefix='')
    app.register_blueprint(update_agents_routes, url_prefix='')
    app.register_blueprint(mine_routes, url_prefix='')
    app.register_blueprint(update_chain_routes, url_prefix='')
