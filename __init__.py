from flask import Flask
from .consensus import consensus_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(consensus_bp, url_prefix='/market/technical')
    return app

