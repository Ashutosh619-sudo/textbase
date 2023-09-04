import os
from twilio.rest import Client
import openai
from textbase.models import OpenAI
from twilio.twiml.messaging_response import MessagingResponse

class SMS:

    message_history = []
    SYSTEM_PROMPT = "You are a SMS chatbot, talk and answer everything the user asks."

    @classmethod
    def receive_message(cls,message,from_number):
        cls.message_history.append({'role':'user','content':[{'data_type':'STRING','value':message}]})

        bot_response = OpenAI.generate(
        system_prompt=cls.SYSTEM_PROMPT,
        message_history=cls.message_history,
        model="gpt-3.5-turbo",
        )  

        cls.message_history.append({'role':'assistant','content':[{'data_type':'STRING','value':bot_response}]})
        
        resp = MessagingResponse()
        resp.message(bot_response)
        return str(resp)
