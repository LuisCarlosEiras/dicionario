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
        # Adiciona uma mensagem de depuração para o prompt
        st.write("Prompt enviado para a API:")
        st.write(prompt_text)
        
        response = genai.generate_text(prompt=prompt_text)
        
        # Adiciona uma mensagem de depuração para a resposta
        st.write("Resposta recebida da API:")
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

# Função para analisar a resposta gerada
def parse_response(response):
    categories = ['Analogias', 'Verbos', 'Adjetivos', 'Advérbios', 'Frases']
    parsed = {}

    for category in categories:
        pattern = f"{category}:(.+?)(?=({'|'.join(categories)}):|$)"
        match = re.search(pattern, response, re.DOTALL)
        if match:
            items = [item.strip() for item in match.group(1).split(';') if item.strip()]
            items = list(dict.fromkeys(items))  # Remove duplicatas
            parsed[category] = items
        else:
            parsed[category] = []

    return parsed

# Interface do Streamlit
st.title("Dicionário Analógico da Língua Portuguesa")
st.write("""
Num dicionário comum se procura o significado exato de uma palavra. Neste **Dicionário Analógico** se procura o inverso: o máximo de significados de uma palavra.
""")

word = st.text_input("Digite uma palavra para ver suas analogias:")

if word:
    with st.spinner('Buscando definição analógica...'):
        definition = get_analogical_definition(word)
    if definition:
        parsed_definition = parse_response(definition)
        for category, items in parsed_definition.items():
            st.subheader(category)
            if category == 'Frases':
                for item in items:
                    st.write(f"- {item}")
            else:
                st.write(", ".join(items))
