from flask import Flask
from market import market_bp  # Import your Blueprint

# Create the Flask application
app = Flask(__name__)

# Register the Blueprint
app.register_blueprint(market_bp)

# Start the server
if __name__ == "__main__":
    app.run(debug=True)

