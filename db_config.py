"""Database configuration for MySQL-compatible setup."""
import os

def get_mysql_compatible_sql(table_name, operation):
    """Return MySQL-compatible SQL statements."""
    # Dictionary of create table statements for MySQL
    create_statements = {
        "users": """CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;""",
        
        "songs": """CREATE TABLE `songs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `artist` varchar(255) NOT NULL,
  `album` varchar(255) DEFAULT NULL,
  `genre` varchar(100) DEFAULT NULL,
  `duration` int DEFAULT NULL,
  `file_path` varchar(500) NOT NULL,
  `album_cover` varchar(500) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;""",
        
        "playlists": """CREATE TABLE `playlists` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `user_id` int NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `playlists_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;""",
        
        "playlist_songs": """CREATE TABLE `playlist_songs` (
  `playlist_id` int NOT NULL,
  `song_id` int NOT NULL,
  `added_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`playlist_id`,`song_id`),
  KEY `song_id` (`song_id`),
  CONSTRAINT `playlist_songs_ibfk_1` FOREIGN KEY (`playlist_id`) REFERENCES `playlists` (`id`) ON DELETE CASCADE,
  CONSTRAINT `playlist_songs_ibfk_2` FOREIGN KEY (`song_id`) REFERENCES `songs` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;""",
        
        "history": """CREATE TABLE `history` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `song_id` int NOT NULL,
  `played_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `song_id` (`song_id`),
  CONSTRAINT `history_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `history_ibfk_2` FOREIGN KEY (`song_id`) REFERENCES `songs` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;""",
        
        "ratings": """CREATE TABLE `ratings` (
  `user_id` int NOT NULL,
  `song_id` int NOT NULL,
  `rating` int NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`,`song_id`),
  KEY `song_id` (`song_id`),
  CONSTRAINT `ratings_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `ratings_ibfk_2` FOREIGN KEY (`song_id`) REFERENCES `songs` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;""",
        
        "subscriptions": """CREATE TABLE `subscriptions` (
  `user_id` int NOT NULL,
  `level` varchar(50) NOT NULL,
  `start_date` datetime DEFAULT CURRENT_TIMESTAMP,
  `end_date` datetime DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  CONSTRAINT `subscriptions_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;"""
    }
    
    # Dictionary of drop table statements for MySQL
    drop_statements = {
        "users": "DROP TABLE IF EXISTS `users`;",
        "songs": "DROP TABLE IF EXISTS `songs`;",
        "playlists": "DROP TABLE IF EXISTS `playlists`;",
        "playlist_songs": "DROP TABLE IF EXISTS `playlist_songs`;",
        "history": "DROP TABLE IF EXISTS `history`;",
        "ratings": "DROP TABLE IF EXISTS `ratings`;",
        "subscriptions": "DROP TABLE IF EXISTS `subscriptions`;"
    }
    
    # Return the appropriate SQL statement
    if operation == "create":
        return create_statements.get(table_name, "")
    elif operation == "drop":
        return drop_statements.get(table_name, "")
    else:
        return ""

def get_database_url():
    """Get the database URL from environment variables."""
    # Check if running in Replit with PostgreSQL
    db_url = os.environ.get('DATABASE_URL')
    if db_url and db_url.startswith('postgresql://'):
        return db_url
    
    # For MySQL
    mysql_host = os.environ.get('MYSQL_HOST', 'localhost')
    mysql_user = os.environ.get('MYSQL_USER', 'root')
    mysql_password = os.environ.get('MYSQL_PASSWORD', '')
    mysql_db = os.environ.get('MYSQL_DB', 'mtunes')
    
    # Fall back to SQLite for development
    sqlite_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mtunes.db')
    return f"sqlite:///{sqlite_path}"