from flask import Flask
from routes import register_routes
import os

app = Flask(__name__)

register_routes(app)

if __name__ == "__main__":
  print(f"O diretório: {os.getcwd()}")
  app.run(debug=True, host="0.0.0.0", port=5000)