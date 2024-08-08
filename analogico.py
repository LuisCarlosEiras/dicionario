import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import re

# Carrega as variáveis de ambiente
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

# Verifica se a chave da API está definida
if not google_api_key:
    st.error("A chave API do Google não está definida. Por favor, configure a variável de ambiente GOOGLE_API_KEY.")
    st.stop()

# Configura a API da Google Generative AI
genai.configure(api_key=google_api_key)
model = genai.GenerativeModel('gemini-pro')

# Função para obter a definição analógica
def get_analogical_definition(word):
    prompt_text = f"""
Você é um dicionário analógico da língua portuguesa. Responda sempre em português do Brasil. Para a palavra '{word}', forneça uma definição analógica estruturada nas seguintes categorias:

Analogias: até 40 itens, separados por ponto e vírgula. Sempre que possível, inclua termos da ciência e tecnologia atuais.
Verbos: exatamente 30 itens, separados por ponto e vírgula. Sempre que possível, inclua termos da ciência e tecnologia atuais.
Adjetivos: até 40 itens, separados por ponto e vírgula. Sempre que possível, inclua termos da ciência e tecnologia atuais.
Advérbios: até 40 itens, separados por ponto e vírgula. Sempre que possível, inclua termos da ciência e tecnologia atuais.
Frases: 10 frases completas, separadas por ponto e vírgula. Sempre que possível, utilize termos da ciência e tecnologia atuais.

Não repita palavras ou frases. Se não houver itens suficientes, deixe o restante em branco.
"""

    try:
        response = model.generate_content(content=prompt_text)
        return response.text
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
