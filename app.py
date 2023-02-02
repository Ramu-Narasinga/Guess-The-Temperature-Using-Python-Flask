import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
import pandas
import csv
import random

result = pandas.read_csv('temperature.csv')

print(result)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Q#qwe121dvj)sndh'

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    with open('temperature.csv') as f:
      reader = csv.reader(f)
      chosen_row = random.choice(list(reader))
      print(chosen_row)
    return render_template('index.html', randomDate=chosen_row)

def save_user_guess(guessed_temp, actual_temp, dt):
  conn = get_db_connection()
  conn.execute('INSERT INTO user_guesses (guessed_temp, actual_temp, dt) VALUES (?, ?, ?)',
              (guessed_temp, actual_temp, dt))
  conn.commit()
  conn.close()

@app.route('/result', methods=('GET', 'POST'))
def compareTemperatures():
  # print(request.form['guess-temperature'], "date::", request.form['date'])
  with open('temperature.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    foundRowInCsv = [row for row in reader if row['dt'] == request.form['date']]
    actualTemp = [foundRowInCsv[0]['dt'], foundRowInCsv[0]['dt_iso'], foundRowInCsv[0]['temp'] ]

    print("found temp", actualTemp)
    if actualTemp[2] == request.form['guess-temperature']:
      flash('You guessed it correctly')
    elif request.form['guess-temperature'] < actualTemp[2]:
      flash('You guessed lower value, increase value')
    elif request.form['guess-temperature'] > actualTemp[2]:
      flash('You guessed higher value, decrease value')

    save_user_guess(request.form['guess-temperature'], actualTemp[2], foundRowInCsv[0]['dt'])
  return render_template('index.html', randomDate=actualTemp)

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