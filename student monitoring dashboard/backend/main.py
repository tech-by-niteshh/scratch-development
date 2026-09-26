from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import fastapi
import telebot
import sqlite3
import uvicorn
import dotenv
import os
import html

dotenv.load_dotenv()

bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))
app = fastapi.FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # local development ke liye
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class contactFormData(BaseModel):
    full_name: str
    email: str
    category: str
    message: str

def sendContactToTelegram(name: str, email: str, category:str , message:str):
    name = html.escape(name)
    email = html.escape(email)
    category = html.escape(category)
    message = html.escape(message)

    msg = f"""✅ 𝖮𝗇𝖾 𝗆𝗈𝗋𝖾 𝖢𝗈𝗇𝗍𝖺𝖼𝗍 𝖿𝗈𝗋𝗆 𝗌𝗎𝖻𝗆𝗂𝗍𝗍𝖾𝖽
    <blockquote>𝚂𝚝𝚞𝚍𝚎𝚗𝚝 𝚖𝚘𝚗𝚒𝚝𝚘𝚛𝚒𝚗𝚐 𝚜𝚢𝚜𝚝𝚎𝚖 𝙰𝚕𝚎𝚛𝚝</blockquote>

    <b>Name</b> : {name}
    <b>E-mail</b> : {email}{email}
    <b>Category</b> : {category}

    {message}"""

    bot.send_message(7701460651, msg, parse_mode="html")
    return True

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS contactData (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            category TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
    )
    conn.commit()
    conn.close()

init_db() # Initialising database




@app.get("/")
def home():
    return {
        "message": "Server is working..",
        "page": "opne index.html"
    }


# FOR INDEX.HTML 

@app.post("/contact")
def handleContactForm(details: contactFormData):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    insert_query = """
        INSERT INTO contactData(name, email, category, message)
        VALUES (?, ?, ?, ?)
"""

    cursor.execute(insert_query, (
        details.full_name,
        details.email,
        details.category,
        details.message
    ))

    conn.commit()
    conn.close()
    sendContactToTelegram(details.full_name, details.email, details.category, details.message)
    
    return {
        "status": "success",
        "Message":"Everything is working correct",
        "data":details
            }


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
    print("Application started successfully..")
    print("Telegram Bot started successfully..")