import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO user_guesses (guessed_temp, actual_temp, dt) VALUES (?, ?, ?)",
            (12, 4.2, 283996800)
            )

connection.commit()
connection.close()