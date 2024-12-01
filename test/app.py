from flask import Flask
from consensus import consensus_bp  # Import the Consensus Blueprint

app = Flask(__name__)

# Register the Consensus Blueprint
app.register_blueprint(consensus_bp)

if __name__ == "__main__":
    app.run(debug=True)

