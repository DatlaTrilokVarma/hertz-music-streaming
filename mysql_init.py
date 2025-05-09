"""
MySQL database initialization script for MTunes.

This script creates the MySQL database and tables for MTunes.
Run this script before starting the application when using MySQL.

Usage:
    python mysql_init.py
"""
import os
import pymysql
from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB, MYSQL_PORT, SAMPLE_SONGS

def create_mysql_tables():
    """Create MySQL tables for MTunes."""
    try:
        # Connect to MySQL server
        connection = pymysql.connect(
            host=MYSQL_HOST,
            port=int(MYSQL_PORT),
            user=MYSQL_USER,
            password=MYSQL_PASSWORD
        )
        
        with connection.cursor() as cursor:
            # Create database if it doesn't exist
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_DB}")
            print(f"Database '{MYSQL_DB}' created or already exists.")
            
            # Use the database
            cursor.execute(f"USE {MYSQL_DB}")
            
            # Create users table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(100) NOT NULL UNIQUE,
                email VARCHAR(255) NOT NULL UNIQUE,
                password_hash VARCHAR(255) NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """)
            
            # Create songs table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS songs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                artist VARCHAR(255) NOT NULL,
                album VARCHAR(255),
                genre VARCHAR(100),
                duration INT,
                file_path VARCHAR(500) NOT NULL,
                album_cover VARCHAR(500),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """)
            
            # Create playlists table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS playlists (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                user_id INT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
            """)
            
            # Create playlist_songs table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS playlist_songs (
                playlist_id INT NOT NULL,
                song_id INT NOT NULL,
                added_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (playlist_id, song_id),
                FOREIGN KEY (playlist_id) REFERENCES playlists(id) ON DELETE CASCADE,
                FOREIGN KEY (song_id) REFERENCES songs(id) ON DELETE CASCADE
            )
            """)
            
            # Create history table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                song_id INT NOT NULL,
                played_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (song_id) REFERENCES songs(id) ON DELETE CASCADE
            )
            """)
            
            # Create ratings table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS ratings (
                user_id INT NOT NULL,
                song_id INT NOT NULL,
                rating INT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (user_id, song_id),
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (song_id) REFERENCES songs(id) ON DELETE CASCADE
            )
            """)
            
            # Create subscriptions table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS subscriptions (
                user_id INT NOT NULL PRIMARY KEY,
                level VARCHAR(50) NOT NULL,
                start_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                end_date DATETIME,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
            """)
            
            # Insert sample songs if songs table is empty
            cursor.execute("SELECT COUNT(*) FROM songs")
            song_count = cursor.fetchone()[0]
            
            if song_count == 0:
                print("Inserting sample songs...")
                for song in SAMPLE_SONGS:
                    # Using the local file paths for audio and images
                    cursor.execute("""
                    INSERT INTO songs (title, artist, album, genre, duration, file_path, album_cover)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (
                        song["title"],
                        song["artist"],
                        song["album"],
                        song["genre"],
                        song["duration"],
                        song["file_path"],  # Local file path to the MP3
                        song["album_cover"] # Local file path to the album cover
                    ))
            
            # Insert sample user if users table is empty
            cursor.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]
            
            if user_count == 0:
                print("Inserting sample user...")
                cursor.execute("""
                INSERT INTO users (username, email, password_hash)
                VALUES (%s, %s, %s)
                """, (
                    "demo",
                    "demo@example.com",
                    "pbkdf2:sha256:150000$PBKDF2SHAidentifierforemail$dd29aaad91c2e9e1dae3aa50f0454e42e33cb16be9e5ac10f9a5c47de842e09c"
                ))
                
                # Get the user ID
                cursor.execute("SELECT id FROM users WHERE username = 'demo'")
                user_id = cursor.fetchone()[0]
                
                # Create a sample playlist
                cursor.execute("""
                INSERT INTO playlists (name, user_id)
                VALUES (%s, %s)
                """, (
                    "My Favorites",
                    user_id
                ))
                
                # Get the playlist ID
                cursor.execute("SELECT id FROM playlists WHERE name = 'My Favorites' AND user_id = %s", (user_id,))
                playlist_id = cursor.fetchone()[0]
                
                # Add sample songs to the playlist
                cursor.execute("SELECT id FROM songs LIMIT 3")
                sample_song_ids = cursor.fetchall()
                
                for song_id in sample_song_ids:
                    cursor.execute("""
                    INSERT INTO playlist_songs (playlist_id, song_id)
                    VALUES (%s, %s)
                    """, (
                        playlist_id,
                        song_id[0]
                    ))
            
            connection.commit()
            print("MySQL tables created successfully.")
    
    except pymysql.MySQLError as e:
        print(f"Error while connecting to MySQL: {e}")
    
    finally:
        if 'connection' in locals():
            connection.close()
            print("MySQL connection closed.")

if __name__ == "__main__":
    print("Initializing MySQL database for MTunes...")
    create_mysql_tables()
    print("""
MySQL database initialized.

To run MTunes with MySQL:
1. Ensure MySQL server is running
2. Set the following environment variables:
   - MYSQL_HOST (default: localhost)
   - MYSQL_USER (default: root)
   - MYSQL_PASSWORD
   - MYSQL_DB (default: mtunes)
   - MYSQL_PORT (default: 3306)
3. Run the Flask application: python main.py

Demo account:
- Username: demo
- Password: password
""")