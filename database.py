import sqlite3

conn = sqlite3.connect('fratachos_army.db')
c = conn.cursor()

# Tabla de superhéroes
c.execute('''CREATE TABLE IF NOT EXISTS superheroes
             (id INTEGER PRIMARY KEY, name TEXT, power_level INTEGER, image_url TEXT)''')

# Tabla de jugadores
c.execute('''CREATE TABLE IF NOT EXISTS players
             (user_id INTEGER PRIMARY KEY, points INTEGER, last_points_reset TEXT, team TEXT)''')

conn.commit()
conn.close()