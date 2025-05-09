import datetime
import os
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func
from app import db
from flask_sqlalchemy import SQLAlchemy

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    # Relationships
    playlists = db.relationship("Playlist", back_populates="user", cascade="all, delete-orphan")
    history_entries = db.relationship("History", back_populates="user", cascade="all, delete-orphan")
    ratings = db.relationship("Rating", back_populates="user", cascade="all, delete-orphan")
    subscription = db.relationship("Subscription", back_populates="user", uselist=False, cascade="all, delete-orphan")
    
    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def get_by_id(cls, user_id):
        return cls.query.get(user_id)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Song(db.Model):
    __tablename__ = 'songs'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    artist = db.Column(db.String(255), nullable=False)
    album = db.Column(db.String(255))
    genre = db.Column(db.String(100))
    duration = db.Column(db.Integer)  # in seconds
    file_path = db.Column(db.String(500), nullable=False)  # Path to the MP3 file
    album_cover = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    # Relationships
    playlist_songs = db.relationship("PlaylistSong", back_populates="song", cascade="all, delete-orphan")
    history_entries = db.relationship("History", back_populates="song", cascade="all, delete-orphan")
    ratings = db.relationship("Rating", back_populates="song", cascade="all, delete-orphan")
    
    @classmethod
    def get_all(cls):
        return cls.query.all()
    
    @classmethod
    def get_by_id(cls, song_id):
        return cls.query.get(song_id)
    
    @classmethod
    def search(cls, query):
        if not query:
            return []
        search_term = f"%{query.lower()}%"
        return cls.query.filter(
            db.or_(
                func.lower(cls.title).like(search_term),
                func.lower(cls.artist).like(search_term),
                func.lower(cls.album).like(search_term)
            )
        ).all()
    
    def to_dict(self):
        """Convert song object to dictionary for JSON response"""
        return {
            'id': self.id,
            'title': self.title,
            'artist': self.artist,
            'album': self.album,
            'duration': self.duration,
            'file_path': self.file_path,
            'album_cover': self.album_cover
        }

class Playlist(db.Model):
    __tablename__ = 'playlists'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    # Relationships
    user = db.relationship("User", back_populates="playlists")
    playlist_songs = db.relationship("PlaylistSong", back_populates="playlist", cascade="all, delete-orphan")
    
    @classmethod
    def get_by_user(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()
    
    @classmethod
    def get_by_id(cls, playlist_id):
        return cls.query.get(playlist_id)
    
    def add_song(self, song_id):
        # Check if song is already in playlist
        existing = PlaylistSong.query.filter_by(playlist_id=self.id, song_id=song_id).first()
        if not existing:
            playlist_song = PlaylistSong(playlist_id=self.id, song_id=song_id)
            db.session.add(playlist_song)
            db.session.commit()
            return True
        return False
    
    def remove_song(self, song_id):
        playlist_song = PlaylistSong.query.filter_by(playlist_id=self.id, song_id=song_id).first()
        if playlist_song:
            db.session.delete(playlist_song)
            db.session.commit()
            return True
        return False
    
    def get_songs(self):
        """Get all songs in this playlist"""
        playlist_songs = PlaylistSong.query.filter_by(playlist_id=self.id).all()
        song_ids = [ps.song_id for ps in playlist_songs]
        return Song.query.filter(Song.id.in_(song_ids)).all()
    
    def to_dict(self):
        """Convert playlist to dictionary for JSON response"""
        return {
            'id': self.id,
            'name': self.name,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat(),
            'songs': [song.to_dict() for song in self.get_songs()]
        }

class PlaylistSong(db.Model):
    __tablename__ = 'playlist_songs'
    
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlists.id'), primary_key=True)
    song_id = db.Column(db.Integer, db.ForeignKey('songs.id'), primary_key=True)
    added_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    # Relationships
    playlist = db.relationship("Playlist", back_populates="playlist_songs")
    song = db.relationship("Song", back_populates="playlist_songs")

class Rating(db.Model):
    __tablename__ = 'ratings'
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    song_id = db.Column(db.Integer, db.ForeignKey('songs.id'), primary_key=True)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    # Relationships
    user = db.relationship("User", back_populates="ratings")
    song = db.relationship("Song", back_populates="ratings")
    
    @classmethod
    def get_by_user_and_song(cls, user_id, song_id):
        return cls.query.filter_by(user_id=user_id, song_id=song_id).first()
    
    @classmethod
    def get_average_for_song(cls, song_id):
        result = db.session.query(func.avg(cls.rating)).filter_by(song_id=song_id).scalar()
        return float(result) if result else 0

class History(db.Model):
    __tablename__ = 'history'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    song_id = db.Column(db.Integer, db.ForeignKey('songs.id'), nullable=False)
    played_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    # Relationships
    user = db.relationship("User", back_populates="history_entries")
    song = db.relationship("Song", back_populates="history_entries")
    
    @classmethod
    def get_by_user(cls, user_id, limit=20):
        return cls.query.filter_by(user_id=user_id).order_by(cls.played_at.desc()).limit(limit).all()
    
    @classmethod
    def add_entry(cls, user_id, song_id):
        entry = cls(user_id=user_id, song_id=song_id)
        db.session.add(entry)
        db.session.commit()
        return entry
    
    def to_dict(self):
        """Convert history entry to dictionary for JSON response"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'song': self.song.to_dict() if self.song else None,
            'played_at': self.played_at.isoformat()
        }

class Subscription(db.Model):
    __tablename__ = 'subscriptions'
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    level = db.Column(db.String(50), nullable=False)  # "free", "premium"
    start_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    user = db.relationship("User", back_populates="subscription")
    
    @classmethod
    def get_by_user(cls, user_id):
        return cls.query.filter_by(user_id=user_id).first()
    
    def is_active(self):
        if not self.end_date:
            return True
        return self.end_date > datetime.datetime.utcnow()

# Function to initialize sample data in the database
def init_sample_data():
    # Check if songs already exist
    if Song.query.count() > 0:
        return
        
    from config import SAMPLE_SONGS
    
    # Add sample songs from config
    songs = []
    for song_data in SAMPLE_SONGS:
        song = Song(
            title=song_data["title"],
            artist=song_data["artist"],
            album=song_data["album"],
            genre=song_data["genre"],
            duration=song_data["duration"],
            file_path=song_data["file_path"],     # Direct URLs to royalty-free MP3s
            album_cover=song_data["album_cover"]  # Direct URLs to placeholder images
        )
        songs.append(song)
        db.session.add(song)
    
    db.session.commit()
    
    # If no users exist, create a sample user
    if User.query.count() == 0:
        sample_user = User(
            username="demo",
            email="demo@example.com"
        )
        sample_user.set_password("password")
        db.session.add(sample_user)
        db.session.commit()
        
        # Create a sample playlist for the user
        if sample_user.id:
            sample_playlist = Playlist(
                name="My Favorites",
                user_id=sample_user.id
            )
            db.session.add(sample_playlist)
            db.session.commit()
            
            # Add some songs to the playlist
            if songs and sample_playlist.id:
                for i in range(min(3, len(songs))):
                    sample_playlist.add_song(songs[i].id)
