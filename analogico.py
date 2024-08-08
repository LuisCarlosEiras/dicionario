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
    prompt_text = (
        f"You are an analogical dictionary of the Portuguese language. Always respond in Portuguese (Brazil). "
        f"For the word '{word}', provide an analogical definition structured in the following categories:\n\n"
        "Analogies: up to 40 items, separated by semicolons. Whenever possible, include terms from current science and technology.\n"
        "Verbs: exactly 30 items, separated by semicolons. Whenever possible, include terms from current science and technology.\n"
        "Adjectives: up to 40 items, separated by semicolons. Whenever possible, include terms from current science and technology.\n"
        "Adverbs: up to 40 items, separated by semicolons. Whenever possible, include terms from current science and technology.\n"
        "Sentences: 10 complete sentences, separated by semicolons. Whenever possible, use terms from current science and technology.\n\n"
        "Do not repeat words or sentences. If there are not enough items, leave the rest blank."
    )
    
    try:
        response = genai.generate_text(prompt=prompt_text)
        
        # Debug: Imprima a resposta completa
        st.write(response)
        
        # Verifica se há candidatos e se o primeiro candidato possui a chave 'output'
        if response.get('candidates') and len(response['candidates']) > 0 and 'output' in response['candidates'][0]:
            english_response = response['candidates'][0]['output']
            # Traduz a resposta para português
            translated_response = translator.translate(english_response, dest='pt').text
            return translated_response
        else:
            st.error("A resposta da API não contém dados esperados.")
            return None
            
    except Exception as e:
        st.error(f"Ocorreu um erro ao processar sua solicitação: {str(e)}")
        return None

