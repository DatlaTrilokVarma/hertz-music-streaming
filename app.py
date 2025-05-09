import os
import logging
from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Initialize SQLAlchemy
db = SQLAlchemy()

# Create the Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "mtunes-secret-key")

# Import MySQL configuration
from config import SQLALCHEMY_DATABASE_URI

# Configure MySQL database
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize database with app
db.init_app(app)

# Configure session
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False
Session(app)

# Import routes
from routes import auth, songs, playlists, users

# Register blueprints
app.register_blueprint(auth.bp)
app.register_blueprint(songs.bp)
app.register_blueprint(playlists.bp)
app.register_blueprint(users.bp)

# Initialize database and load sample data
with app.app_context():
    import models
    db.create_all()
    models.init_sample_data()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
