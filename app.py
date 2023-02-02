import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
import pandas
from faker import Faker

result = pandas.read_csv('temperature.csv')

print(result)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Q#qwe121dvj)sndh'

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

@app.route('/')
def index():
    fake = Faker()
    # used the stackoverflow answer to generate random date: https://stackoverflow.com/questions/553303/generate-a-random-date-between-two-other-dates
    randomDate = fake.date_time_between(start_date='-30y', end_date='now')
    return render_template('index.html', randomDate=randomDate)

@app.route('/result', methods=('GET', 'POST'))
def compareTemperatures():
  print(request.form['guess-temperature'])
  flash('Flash TITS')
  return redirect(url_for('index'))

@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
          title = request.form['title']
          content = request.form['content']

          if not title:
              flash('Title is required!')
          else:
              conn = get_db_connection()
              conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                          (title, content))
              conn.commit()
              conn.close()
              return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))