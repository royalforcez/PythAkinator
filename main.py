import requests
from bs4 import BeautifulSoup
from ollama import chat
from ollama import ChatResponse
from ollama import generate
import ollama 

response = ollama.chat(model='gemma3:12b', messages=[
  {
    'role': 'user',
    'content': 'We want to play a game like Akinator, I think about something, and you are asking me questions to find out what it is. And I can answer only "yes" or "no".',
  },
])
print(response['message']['content'])