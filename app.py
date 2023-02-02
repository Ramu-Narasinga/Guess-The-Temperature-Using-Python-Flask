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
  with open('temperature.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    foundRowInCsv = [row for row in reader if row['dt'] == request.form['date']]
    actualTemp = [foundRowInCsv[0]['dt'], foundRowInCsv[0]['dt_iso'], foundRowInCsv[0]['temp'] ]

    print("actual temp", actualTemp[2], "guessTemp:", request.form['guess-temperature'])
    save_user_guess(request.form['guess-temperature'], actualTemp[2], foundRowInCsv[0]['dt'])

    guessedTemp = request.form['guess-temperature']

    if guessedTemp == actualTemp[2]:
      flash('You guessed it correctly, Congratulations. You won!')
    
    if guessedTemp < actualTemp[2]:
      flash('You guessed lower value, increase value')
    
    if guessedTemp > actualTemp[2]:
      flash('You guessed higher value, decrease value')

  return render_template('index.html', randomDate=actualTemp)
