import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import re

# Carrega as variáveis de ambiente
load_dotenv()

# Configura a API do Google Gemini-Pro
google_api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=google_api_key)
model = genai.GenerativeModel('gemini-pro')

def get_analogical_definition(word):
    prompt = f"""Você é um dicionário analógico da língua portuguesa. Responda sempre em português do Brasil. Forneça uma definição analógica para a palavra: {word}
    É CRUCIAL que você estruture sua resposta EXATAMENTE nas seguintes categorias, usando exatamente estes títulos:
    Analogias:
    Verbos:
    Adjetivos:
    Advérbios:
    Frases:
    Para a categoria Verbos, forneça até 30 itens separados por ponto e vírgula.
    Para todas as outras categorias, forneça até 20 itens separados por ponto e vírgula.
    Não repita palavras ou frases em nenhuma categoria. Se não houver itens suficientes para uma categoria, deixe o restante em branco.
    Exemplo de formato da resposta:
    Analogias: item1; item2; item3; ...
    Verbos: verbo1; verbo2; verbo3; ...
    Adjetivos: adjetivo1; adjetivo2; adjetivo3; ...
    Advérbios: advérbio1; advérbio2; advérbio3; ...
    Frases: frase1; frase2; frase3; ...
    Forneça uma definição analógica para a palavra: {word}
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
            items = [item.strip() for item in match.group(1).split(';') if item.strip()]
            # Remove duplicates while preserving order
            items = list(dict.fromkeys(items))
            parsed[category] = items
        else:
            parsed[category] = []
    
    return parsed

st.title("Dicionário Analógico da Língua Portuguesa")
st.write("""
Se num dicionário comum se procura o significado exato de uma palavra, neste Dicionário Analógico se procura o inverso: o máximo de significados de uma palavra.
""")

word = st.text_input("Digite uma palavra para ver suas analogias:")

if word:
    with st.spinner('Buscando definição analógica...'):
        definition = get_analogical_definition(word)
    if definition:
        parsed_definition = parse_response(definition)
        for category, items in parsed_definition.items():
            st.subheader(category)
            st.write(", ".join(items))

# Adicione isso no final do seu script para verificar se a chave API está definida
if not google_api_key:
    st.error("A chave API do Google não está definida. Por favor, configure a variável de ambiente GOOGLE_API_KEY.")
