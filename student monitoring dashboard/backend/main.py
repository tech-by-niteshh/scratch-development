from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import fastapi
import telebot
import sqlite3
import pydantic
import uvicorn

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


@app.get("/")
def home():
    return {
        "message": "Server is working..",
        "page": "opne index.html"
    }


# FOR INDEX.HTML 

@app.post("/contact")
def handleContactForm(details: contactFormData):
    return {
        "Message":"Everything is working correct",
        "data":details
            }


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)