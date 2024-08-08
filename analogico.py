import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import re

load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=google_api_key)
model = genai.GenerativeModel('gemini-pro')

def get_analogical_definition(word):
   prompt = f"""Você é um dicionário analógico da língua portuguesa. Responda sempre em português do Brasil. Para a palavra '{word}', forneça uma definição analógica estruturada nas seguintes categorias:

Analogias: até 40 itens, separados por ponto e vírgula.
Verbos: exatamente 30 itens, separados por ponto e vírgula.
Adjetivos: até 40 itens, separados por ponto e vírgula.
Advérbios: até 40 itens, separados por ponto e vírgula.
Frases: 10 frases completas, separadas por ponto e vírgula.

Não repita palavras ou frases. Se não houver itens suficientes, deixe o restante em branco.
"""

    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Ocorreu um erro ao processar sua solicitação: {str(e)}")
        return None

def parse_response(response):
    categories = ['Analogias', 'Verbos', 'Adjetivos', 'Advérbios', 'Frases']
    parsed = {}
    
    for category in categories:
        pattern = f"{category}:(.+?)(?={('|'.join(categories))}:|$)"
        match = re.search(pattern, response, re.DOTALL)
        if match:
            if category == 'Frases':
                items = [item.strip() for item in match.group(1).split(';') if item.strip()]
            else:
                items = [item.strip() for item in match.group(1).split(';') if item.strip()]
                items = list(dict.fromkeys(items))
            parsed[category] = items
        else:
            parsed[category] = []
    
    return parsed

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
                    st.write(f"{item}")
            else:
                st.write(", ".join(items))

if not google_api_key:
    st.error("A chave API do Google não está definida. Por favor, configure a variável de ambiente GOOGLE_API_KEY.")
