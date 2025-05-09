"""Database configuration for Hertz."""
import os

# MySQL Configuration
MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
MYSQL_DB = os.environ.get('MYSQL_DB', 'hertz')
MYSQL_PORT = os.environ.get('MYSQL_PORT', '3306')

# SQLAlchemy Database URI
# When running locally, use this MySQL URI configuration:
SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"

# For development on Replit, we'll use SQLite as a fallback
# But in production, ensure you use MySQL as specified in the URI above
import os
if not os.path.exists('/var/run/mysqld/mysqld.sock'):
    # If MySQL is not available, use SQLite for development
    sqlite_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hertz.db')
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{sqlite_path}"

# Sample Song Data - using royalty free music with local file paths
# These are placeholder songs matching the requested titles, but with royalty-free audio
SAMPLE_SONGS = [
    {
        "title": "Shape of You",
        "artist": "Ed Sheeran",
        "album": "Divide",
        "genre": "Pop",
        "duration": 234,
        "file_path": "/static/audio/shape_of_you.mp3",
        "album_cover": "/static/images/covers/divide.jpg"
    },
    {
        "title": "Blinding Lights",
        "artist": "The Weeknd",
        "album": "After Hours",
        "genre": "Synthwave",
        "duration": 200,
        "file_path": "/static/audio/blinding_lights.mp3",
        "album_cover": "/static/images/covers/after_hours.jpg"
    },
    {
        "title": "Believer",
        "artist": "Imagine Dragons",
        "album": "Evolve",
        "genre": "Rock",
        "duration": 204,
        "file_path": "/static/audio/believer.mp3",
        "album_cover": "/static/images/covers/evolve.jpg"
    },
    {
        "title": "Tera Ban Jaunga",
        "artist": "Akhil Sachdeva",
        "album": "Kabir Singh",
        "genre": "Romantic",
        "duration": 254,
        "file_path": "/static/audio/tera_ban_jaunga.mp3",
        "album_cover": "/static/images/covers/kabir_singh.jpg"
    },
    {
        "title": "Tum Hi Ho",
        "artist": "Arijit Singh",
        "album": "Aashiqui 2",
        "genre": "Romantic",
        "duration": 262,
        "file_path": "/static/audio/tum_hi_ho.mp3",
        "album_cover": "/static/images/covers/aashiqui_2.jpg"
    },
    {
        "title": "Senorita",
        "artist": "Shawn Mendes",
        "album": "Shawn Mendes",
        "genre": "Latin Pop",
        "duration": 191,
        "file_path": "/static/audio/senorita.mp3",
        "album_cover": "/static/images/covers/shawn_mendes.jpg"
    }
]