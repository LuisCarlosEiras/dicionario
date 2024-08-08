import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import re
from googletrans import Translator

# Carrega as variáveis de ambiente
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

# Verifica se a chave da API está definida
if not google_api_key:
    st.error("A chave API do Google não está definida. Por favor, configure a variável de ambiente GOOGLE_API_KEY.")
    st.stop()

# Configura a API da Google Generative AI
genai.configure(api_key=google_api_key)

# Configura o tradutor
translator = Translator()

# Função para obter a definição analógica
def get_analogical_definition(word):
    prompt_text = f"""
You are an analogical dictionary of the Portuguese language. Always respond in Portuguese (Brazil). For the word '{word}', provide an analogical definition structured in the following categories:

Analogies: up to 40 items, separated by semicolons. Whenever possible, include terms from current science and technology.
Verbs: exactly 30 items, separated by semicolons. Whenever possible, include terms from current science and technology.
Adjectives: up to 40 items, separated by semicolons. Whenever possible, include terms from current science and technology.
Adverbs: up to 40 items, separated by semicolons. Whenever possible, include terms from current science and technology.
Sentences: 10 complete sentences, separated by semicolons. Whenever possible, use terms from current science and technology.

Do not repeat words or sentences. If there are not enough items, leave the 
