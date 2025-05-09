-- Hertz MySQL Database Schema
-- This script creates the database structure for the Hertz application
-- Compatible with MySQL/MariaDB

-- Create database if it doesn't exist
CREATE DATABASE IF NOT EXISTS hertz;
USE hertz;

-- Drop tables if they exist (for clean installation)
DROP TABLE IF EXISTS history;
DROP TABLE IF EXISTS ratings;
DROP TABLE IF EXISTS playlist_songs;
DROP TABLE IF EXISTS playlists;
DROP TABLE IF EXISTS subscriptions;
DROP TABLE IF EXISTS songs;
DROP TABLE IF EXISTS users;

-- Users table
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(100) NOT NULL UNIQUE,
  email VARCHAR(255) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Songs table
CREATE TABLE songs (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  artist VARCHAR(255) NOT NULL,
  album VARCHAR(255),
  genre VARCHAR(100),
  duration INT, -- in seconds
  file_path VARCHAR(500) NOT NULL, -- Path to the MP3 file
  album_cover VARCHAR(500),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Playlists table
CREATE TABLE playlists (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  user_id INT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Playlist_songs table (junction between playlists and songs)
CREATE TABLE playlist_songs (
  playlist_id INT NOT NULL,
  song_id INT NOT NULL,
  added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (playlist_id, song_id),
  FOREIGN KEY (playlist_id) REFERENCES playlists(id) ON DELETE CASCADE,
  FOREIGN KEY (song_id) REFERENCES songs(id) ON DELETE CASCADE
);

-- Ratings table
CREATE TABLE ratings (
  user_id INT NOT NULL,
  song_id INT NOT NULL,
  rating INT NOT NULL, -- 1-5 stars
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (user_id, song_id),
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY (song_id) REFERENCES songs(id) ON DELETE CASCADE
);

-- History table (play history)
CREATE TABLE history (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  song_id INT NOT NULL,
  played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY (song_id) REFERENCES songs(id) ON DELETE CASCADE
);

-- Subscriptions table
CREATE TABLE subscriptions (
  user_id INT PRIMARY KEY,
  level VARCHAR(50) NOT NULL, -- "free", "premium"
  start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  end_date TIMESTAMP NULL,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Insert sample songs data
INSERT INTO songs (title, artist, album, genre, duration, file_path, album_cover) VALUES
('Shape of You', 'Ed Sheeran', 'Divide', 'Pop', 234, '/static/audio/shape_of_you.mp3', '/static/images/covers/divide.jpg'),
('Blinding Lights', 'The Weeknd', 'After Hours', 'Synthwave', 200, '/static/audio/blinding_lights.mp3', '/static/images/covers/after_hours.jpg'),
('Believer', 'Imagine Dragons', 'Evolve', 'Rock', 204, '/static/audio/believer.mp3', '/static/images/covers/evolve.jpg'),
('Tera Ban Jaunga', 'Akhil Sachdeva', 'Kabir Singh', 'Romantic', 254, '/static/audio/tera_ban_jaunga.mp3', '/static/images/covers/kabir_singh.jpg'),
('Tum Hi Ho', 'Arijit Singh', 'Aashiqui 2', 'Romantic', 262, '/static/audio/tum_hi_ho.mp3', '/static/images/covers/aashiqui_2.jpg'),
('Senorita', 'Shawn Mendes', 'Shawn Mendes', 'Latin Pop', 191, '/static/audio/senorita.mp3', '/static/images/covers/shawn_mendes.jpg');

-- Create a demo user (username: demo, password: password)
INSERT INTO users (username, email, password_hash) VALUES
('demo', 'demo@example.com', 'pbkdf2:sha256:260000$XNQO9Zoaj3yFQiSv$f52a7c2c3b5eea5ff4e391050f64de9fdff54e079d1898cbe6da779b103ac34f');

-- Create subscription for demo user
INSERT INTO subscriptions (user_id, level) VALUES (1, 'free');

-- Create a sample playlist for demo user
INSERT INTO playlists (name, user_id) VALUES ('My Favorites', 1);

-- Add songs to the demo playlist
INSERT INTO playlist_songs (playlist_id, song_id) VALUES 
(1, 1), -- Shape of You
(1, 3), -- Believer
(1, 5); -- Tum Hi Ho