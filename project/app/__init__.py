from flask import Flask

# Import your blueprints
from .consensus import consensus_bp

def create_app():
    """
    Factory function to create and configure the Flask application.
    """
    app = Flask(__name__)

    # Register blueprints
    app.register_blueprint(consensus_bp)

    return app

