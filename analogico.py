import streamlit as st
import openai
from dotenv import load_dotenv
import os
import re

# Carrega as variáveis de ambiente
load_dotenv()

# Configura a API do OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_analogical_definition(word):
    prompt = f"""Você é um dicionário analógico da língua portuguesa. Forneça uma definição analógica para a palavra: {word}

    É CRUCIAL que você estruture sua resposta EXATAMENTE nas seguintes categorias, usando exatamente estes títulos:

    Analogias:
    Verbos:
    Adjetivos:
    Advérbios:
    Frases:

    Para a categoria Verbos, forneça EXATAMENTE 30 itens separados por ponto e vírgula.
    Para todas as outras categorias, forneça EXATAMENTE 20 itens separados por ponto e vírgula.
    Se não houver itens suficientes para uma categoria, repita os itens existentes ou crie variações para chegar ao número necessário.

    Exemplo de formato da resposta:
    Analogias: item1; item2; item3; ...; item20
    Verbos: verbo1; verbo2; verbo3; ...; verbo30
    Adjetivos: adjetivo1; adjetivo2; adjetivo3; ...; adjetivo20
    Advérbios: advérbio1; advérbio2; advérbio3; ...; advérbio20
    Frases: frase1; frase2; frase3; ...; frase20

    Forneça uma definição analógica para a palavra: {word}
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um assistente especializado em fornecer definições analógicas em português."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=3500,
            n=1,
            temperature=0.7,
        )
        return response.choices[0].message['content'].strip()
    except openai.error.OpenAIError as e:
        st.error(f"Ocorreu um erro ao processar sua solicitação: {str(e)}")
        return None

def parse_response(response):
    categories = ['Analogias', 'Verbos', 'Adjetivos', 'Advérbios', 'Frases']
    parsed = {}
    
    for i, category in enumerate(categories):
        if i < len(categories) - 1:
            pattern = f"{category}:(.+?)(?={categories[i+1]}:)"
        else:
            pattern = f"{category}:(.+)"
        
        match = re.search(pattern, response, re.DOTALL)
        if match:
            items = [item.strip() for item in match.group(1).split(';') if item.strip()]
            # Ensure we have the correct number of items
            if category == 'Verbos':
                items = (items * ((30 + len(items) - 1) // len(items)))[:30]
            else:
                items = (items * ((20 + len(items) - 1) // len(items)))[:20]
            parsed[category] = items
        else:
            parsed[category] = ['N/A'] * (30 if category == 'Verbos' else 20)
    
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
            st.subheader(f"{category} ({len(items)})")
            st.write(", ".join(items))

# Adicione isso no final do seu script para verificar se a chave API está definida
if not openai.api_key:
    st.error("A chave API do OpenAI não está definida. Por favor, configure a variável de ambiente OPENAI_API_KEY.")
