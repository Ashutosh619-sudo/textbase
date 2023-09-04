import os
from twilio.rest import Client
import openai
import sys
import importlib
from textbase.models import OpenAI

class Whatsapp:

    message_history = []
    SYSTEM_PROMPT = "You are a whatsapp chatbot, talk and answer everything the user asks."

    @classmethod
    def send_message(cls,message,from_number):

        from_phone_number = os.environ.get("PHONE_NUMBER_FROM")
        account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
        token = os.environ.get("TWILIO_TOKEN")
        client = Client(account_sid,token)

        client.messages.create(
        from_=f'whatsapp:{from_phone_number}',
        body=message,
        to=from_number
        )

        cls.message_history.append({'role':'assistant','content':[{'data_type':'STRING','value':message}]})
    
    @classmethod
    def receive_message(cls,message,from_number):

        cls.message_history.append({'role':'user','content':[{'data_type':'STRING','value':message}]})

        bot_response = OpenAI.generate(
        system_prompt=cls.SYSTEM_PROMPT,
        message_history=cls.message_history,
        model="gpt-3.5-turbo",
        )
        cls.send_message(bot_response,from_number)
