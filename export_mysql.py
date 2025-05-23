#!/usr/bin/env python3
"""
Hertz MySQL Export Utility

This script will export data from the Hertz application to a MySQL database.
It reads configuration from the .env file and generates SQL statements to populate a MySQL database.

Usage:
    python export_mysql.py > hertz_data.sql
"""

import os
import sys
from dotenv import load_dotenv
import sqlite3
from app import app, db
import models

# Load environment variables from .env file
load_dotenv()

def get_db_connection():
    """Get a connection to the SQLite database."""
    sqlite_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hertz.db')
    conn = sqlite3.connect(sqlite_path)
    conn.row_factory = sqlite3.Row
    return conn

def export_data_to_mysql():
    """Export data from SQLite to MySQL-compatible SQL statements."""
    conn = get_db_connection()
    
    # Print SQL statements header
    print("-- Hertz MySQL Data Export")
    print("-- Generated by export_mysql.py")
    print("-- This script contains INSERT statements for the Hertz database")
    print("\n")
    print("USE hertz;\n")
    
    # Export users
    print("-- Users data")
    users = conn.execute('SELECT * FROM users').fetchall()
    for user in users:
        cols = ', '.join(user.keys())
        placeholders = ', '.join(['%s'] * len(user))
        sql = f"INSERT INTO users ({cols}) VALUES ("
        values = []
        for k in user.keys():
            if user[k] is None:
                values.append("NULL")
            elif isinstance(user[k], (int, float)):
                values.append(str(user[k]))
            else:
                values.append(f"'{user[k]}'")
        sql += ', '.join(values) + ");"
        print(sql)
    print("\n")
    
    # Export songs
    print("-- Songs data")
    songs = conn.execute('SELECT * FROM songs').fetchall()
    for song in songs:
        cols = ', '.join(song.keys())
        values = []
        for k in song.keys():
            if song[k] is None:
                values.append("NULL")
            elif isinstance(song[k], (int, float)):
                values.append(str(song[k]))
            else:
                values.append(f"'{song[k].replace("'", "''")}'")
        sql = f"INSERT INTO songs ({cols}) VALUES ({', '.join(values)});"
        print(sql)
    print("\n")
    
    # Export playlists
    print("-- Playlists data")
    playlists = conn.execute('SELECT * FROM playlists').fetchall()
    for playlist in playlists:
        cols = ', '.join(playlist.keys())
        values = []
        for k in playlist.keys():
            if playlist[k] is None:
                values.append("NULL")
            elif isinstance(playlist[k], (int, float)):
                values.append(str(playlist[k]))
            else:
                values.append(f"'{playlist[k]}'")
        sql = f"INSERT INTO playlists ({cols}) VALUES ({', '.join(values)});"
        print(sql)
    print("\n")
    
    # Export playlist_songs
    print("-- Playlist songs data")
    playlist_songs = conn.execute('SELECT * FROM playlist_songs').fetchall()
    for ps in playlist_songs:
        cols = ', '.join(ps.keys())
        values = []
        for k in ps.keys():
            if ps[k] is None:
                values.append("NULL")
            elif isinstance(ps[k], (int, float)):
                values.append(str(ps[k]))
            else:
                values.append(f"'{ps[k]}'")
        sql = f"INSERT INTO playlist_songs ({cols}) VALUES ({', '.join(values)});"
        print(sql)
    print("\n")
    
    # Export ratings
    print("-- Ratings data")
    ratings = conn.execute('SELECT * FROM ratings').fetchall()
    for rating in ratings:
        cols = ', '.join(rating.keys())
        values = []
        for k in rating.keys():
            if rating[k] is None:
                values.append("NULL")
            elif isinstance(rating[k], (int, float)):
                values.append(str(rating[k]))
            else:
                values.append(f"'{rating[k]}'")
        sql = f"INSERT INTO ratings ({cols}) VALUES ({', '.join(values)});"
        print(sql)
    print("\n")
    
    # Export history
    print("-- Play history data")
    history = conn.execute('SELECT * FROM history').fetchall()
    for h in history:
        cols = ', '.join(h.keys())
        values = []
        for k in h.keys():
            if h[k] is None:
                values.append("NULL")
            elif isinstance(h[k], (int, float)):
                values.append(str(h[k]))
            else:
                values.append(f"'{h[k]}'")
        sql = f"INSERT INTO history ({cols}) VALUES ({', '.join(values)});"
        print(sql)
    print("\n")
    
    # Export subscriptions
    print("-- Subscriptions data")
    subscriptions = conn.execute('SELECT * FROM subscriptions').fetchall()
    for sub in subscriptions:
        cols = ', '.join(sub.keys())
        values = []
        for k in sub.keys():
            if sub[k] is None:
                values.append("NULL")
            elif isinstance(sub[k], (int, float)):
                values.append(str(sub[k]))
            else:
                values.append(f"'{sub[k]}'")
        sql = f"INSERT INTO subscriptions ({cols}) VALUES ({', '.join(values)});"
        print(sql)
    
    conn.close()

if __name__ == "__main__":
    with app.app_context():
        export_data_to_mysql()