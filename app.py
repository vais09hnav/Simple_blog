from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Initialize the database
def init_db():
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Home route - Display all blog posts
@app.route('/')
def index():
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    c.execute('SELECT id, title, content, created_at FROM posts ORDER BY created_at DESC')
    posts = c.fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

# Route to display the post submission form
@app.route('/add')
def add_post():
    return render_template('add_post.html')

# Route to handle the form submission and add a new blog post
@app.route('/add_post', methods=['POST'])
def save_post():
    title = request.form['title']
    content = request.form['content']
    
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    c.execute('INSERT INTO posts (title, content, created_at) VALUES (?, ?, ?)', 
              (title, content, datetime.now()))
    conn.commit()
    conn.close()
    
    return redirect(url_for('index'))

# Initialize the database when the script runs
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
