from fastapi import FastAPI, File, UploadFile, Form,Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from textbase.message import Message
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware
import sys
import logging
from typing import List
import importlib
from textbase.models import OpenAI
import openai
from textbase.integration.whatsapp import Whatsapp
from textbase.integration.SMS import SMS

logging.basicConfig(level=logging.INFO)

load_dotenv()

OpenAI.api_key = "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"

from textbase.message import Message

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:4000",
    "http://localhost:5173",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/twilio/recieve-whatsapp/")
async def receive_whatsapp(request: Request):
        
    twilio_data = await request.form()
    from_number = twilio_data["From"]
    message = twilio_data["Body"]
    
    Whatsapp.receive_message(message,from_number)

@app.post("/twilio/receive-sms/")
async def receive_sms(request: Request):
    
    twilio_data = await request.form()
    from_number = twilio_data["From"]
    message = twilio_data["Body"]


    return SMS.receive_message(message,from_number)



app.mount(
    "/static",
    StaticFiles(directory="dist/", html=True),
    name="static",
)
