import os
import sqlite3
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler

TOKEN = os.getenv("BOT_TOKEN")

conn = sqlite3.connect("reminders.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS reminders (
    user_id INTEGER,
    message TEXT,
    remind_time TEXT
)
""")
conn.commit()

scheduler = AsyncIOScheduler()
scheduler.start()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 Welcome to AMU X R5NAK\n\nUse:\n/add YYYY-MM-DD HH:MM Message"
    )

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_id = update.effective_user.id
        date = context.args[0]
        time = context.args[1]
        message = " ".join(context.args[2:])
        remind_time = f"{date} {time}"
        dt = datetime.strptime(remind_time, "%Y-%m-%d %H:%M")

        cursor.execute(
            "INSERT INTO reminders VALUES (?, ?, ?)",
            (user_id, message, remind_time)
        )
        conn.commit()

        scheduler.add_job(
            lambda: app.bot.send_message(chat_id=user_id, text=f"🔔 Reminder:\n{message}"),
            "date",
            run_date=dt
        )

        await update.message.reply_text("⏰ Reminder set!")

    except:
        await update.message.reply_text(
            "❌ Format:\n/add 2026-03-05 19:00 Study Physics"
        )

async def list_reminders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    cursor.execute(
        "SELECT message, remind_time FROM reminders WHERE user_id=?",
        (user_id,)
    )
    rows = cursor.fetchall()

    if not rows:
        await update.message.reply_text("📭 No reminders found.")
    else:
        text = "📋 Your Reminders:\n\n"
        for r in rows:
            text += f"{r[1]} → {r[0]}\n"
        await update.message.reply_text
