from flask import Flask
from sma import sma_bp  # Import the SMA Blueprint

# Initialize the Flask application
app = Flask(__name__)

# Register the SMA Blueprint
app.register_blueprint(sma_bp)

# Start the Flask server
if __name__ == "__main__":
    app.run(debug=True)

