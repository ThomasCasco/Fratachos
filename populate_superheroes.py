import requests
import sqlite3

# Obtener datos de la API
response = requests.get('https://akabab.github.io/superhero-api/api/all.json')
heroes = response.json()

# Conectar a la base de datos
conn = sqlite3.connect('fratachos_army.db')
c = conn.cursor()

# Insertar héroes
for hero in heroes:
    power_level = sum(hero['powerstats'].values())  # Suma de estadísticas
    image_url = hero['images']['md']  # Imagen mediana
    c.execute("INSERT INTO superheroes (name, power_level, image_url) VALUES (?, ?, ?)",
              (hero['name'], power_level, image_url))

conn.commit()
conn.close()