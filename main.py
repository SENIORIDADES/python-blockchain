from flask import Flask
from routes import register_routes

app = Flask(_name_)

register_routes(app)

if _name_ == "_main_":
  app.run(debug=True, host="0.0.0.0", port=5000)