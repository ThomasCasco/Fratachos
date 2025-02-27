import sqlite3
import random
from datetime import datetime, timedelta

#imports de telegram.
from telegram import Update, Bot
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# Token del bot
TOKEN = '7756173232:AAGOL1tbScYCKrU5f5jYCwMMRheu2IEqAnM'


# Función para obtener la conexión a la base de datos
def get_db_connection():
    conn = sqlite3.connect('fratachos_army.db')
    return conn

def renew_points(user_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT last_points_reset FROM players WHERE user_id = ?", (user_id,))
    last_reset = c.fetchone()
    if last_reset is None:
        # nuevo jugador, cambiar insert en la nueva funcionabilidads
        c.execute(
            "INSERT INTO players (user_id, points, last_points_reset, team) VALUES (?, 500, ?, '[]')",
            (user_id, datetime.now().strftime("%Y-%m-%d"))
        )
    else:
        last_reset_date = datetime.strptime(last_reset[0], "%Y-%m-%d")
        if (datetime.now() - last_reset_date).days >= 1:
            c.execute(
                "UPDATE players SET points = 500, last_points_reset = ? WHERE user_id = ?",
                (datetime.now().strftime("%Y-%m-%d"), user_id)
            )
    conn.commit()
    conn.close()

# funcion de entrada
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    renew_points(user_id)
    await update.message.reply_text("¡Bienvenido a Fratacho's Army! Usa !heroe para reclutar un superhéroe.")

# funcion de heroe
async def heroe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    renew_points(user_id)
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT points FROM players WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    if not row:
       #fmensaje de error
        await update.message.reply_text("Primero usa /start para unirte al juego.")
        conn.close()
        return

    points = row[0]
    if points < 100:
        await update.message.reply_text("No tenés suficientes puntos. Volvé mañana para más.")
        conn.close()
        return

    # sacar un heroe al azar de la db
    c.execute("SELECT id, name, power_level, image_url FROM superheroes ORDER BY RANDOM() LIMIT 1")
    hero = c.fetchone()
    hero_id, hero_name, power_level, image_url = hero

    # chances de sacar un heroe segun el nivel de poder
    if power_level < 200:
        success_chance = 80
    elif power_level < 400:
        success_chance = 50
    else:
        success_chance = 20

    # Intento de reclutamiento
    if random.randint(1, 100) <= success_chance:
        c.execute("UPDATE players SET team = team || ? WHERE user_id = ?", (f"{hero_id},", user_id))
        await update.message.reply_photo(photo=image_url, caption=f"¡Reclutaste a {hero_name}!")
    else:
        await update.message.reply_text(f"No pudiste reclutar a {hero_name}. Seguí intentando.")

    # Sacarle puntos al jugador
    c.execute("UPDATE players SET points = points - 100 WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

def main() -> None:
    
    application = ApplicationBuilder().token(TOKEN).build()

    
    application.add_handler(CommandHandler("start", start))

    
    application.add_handler(MessageHandler(filters.Regex('^!heroe$'), heroe))

    
    application.run_polling()

if __name__ == '__main__':
    main()
