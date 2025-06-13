from flask import Flask, render_template, request, redirect, url_for
from slugify import slugify
import sqlite3
import time
from urllib.parse import quote

DB_PATH = 'lyrics.db'

app = Flask(__name__)

# --- Database Setup
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS songs (
            id INTEGER PRIMARY KEY,
            artist TEXT,
            title TEXT,
            url TEXT,
            timestamp REAL
        )
    ''')
    conn.commit()
    conn.close()

# --- Fetch or Generate Lyrics URL
def make_lyrics_url(artist, title):
    # Percent‑encode Unicode
    safe_artist = quote(artist, safe='')
    safe_title  = quote(title, safe='')
    return f"https://example-lyrics-site.com/lyrics/{safe_artist}/{safe_title}/"

# --- Add entry
def add_song(artist, title):
    url = make_lyrics_url(artist, title)
    ts = time.time()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO songs (artist, title, url, timestamp) VALUES (?, ?, ?, ?)',
              (artist, title, url, ts))
    conn.commit()
    conn.close()
    return url

# --- Search & List
def get_songs(order='date', keyword=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    query = 'SELECT artist, title, url, timestamp FROM songs'
    params = []
    if keyword:
        query += ' WHERE artist LIKE ? OR title LIKE ?'
        kw = f"%{keyword}%"
        params.extend([kw, kw])
    if order == 'alpha':
        query += ' ORDER BY artist COLLATE NOCASE, title COLLATE NOCASE'
    else:
        query += ' ORDER BY timestamp DESC'
    c.execute(query, params)
    rows = c.fetchall()
    conn.close()
    return rows

# --- Routes
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        artist = request.form['artist'].strip()
        title  = request.form['title'].strip()
        add_song(artist, title)
        return redirect(url_for('library'))
    return render_template('index.html')

@app.route('/library')
def library():
    order   = request.args.get('order', 'date')
    keyword = request.args.get('search', None)
    songs   = get_songs(order, keyword)
    return render_template('library.html', songs=songs, order=order, search=keyword)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)