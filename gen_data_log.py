import sqlite3

con = sqlite3.connect('Project_Electrician/data_log.db')

cur = con.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS data_log
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            skin TEXT,
            wins INTEGER,
            lose INTEGER)''')

[print(el) for el in cur.execute('SELECT * FROM data_log').fetchall()]

cur.execute('''DELETE FROM data_log''')

con.commit()

cur.close()
