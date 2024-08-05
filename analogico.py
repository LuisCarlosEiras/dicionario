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

    Para cada categoria, forneça EXATAMENTE 20 itens separados por vírgula. Se não houver 20 itens para uma categoria, crie variações para chegar a 20.

    Exemplo de formato da resposta:
    Analogias: item1; item2; item3; item4; item5; item6; item7; item8; item9; item10; item11; item12; item13; item14; item15; item16; item17; item18; item19; item20
    Verbos: verbo1; verbo2; verbo3; verbo4; verbo5; verbo6; verbo7; verbo8; verbo9; verbo10; verbo 11; verbo12; verbo 13; verbo14; verbo15; verbo16; verbo17; verbo18; verbo19; verbo20
    Adjetivos: adjetivo1; adjetivo2; adjetivo3; adjetivo4; adjetivo5; adjetivo6; adjetivo7; adjetivo8; adjetivo9; adjetivo10
    Advérbios: advérbio1; advérbio2; advérbio3; advérbio4; advérbio5; advérbio6; advérbio7; advérbio8; advérbio9; advérbio10
    Frases: frase1; frase2; frase3; frase4; frase5; frase6; frase7; frase8; frase9; frase10

    Forneça uma definição analógica para a palavra: {word}
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um assistente especializado em fornecer definições analógicas em português."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            n=1,
            temperature=0.3,
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
            # Ensure we have exactly 10 items
            items = (items * ((10 + len(items) - 1) // len(items)))[:10]
            parsed[category] = items
        else:
            parsed[category] = ['N/A'] * 10
    
    return parsed

st.title("Dicionário Analógico da Língua Portuguesa")

st.write("""
Se num dicionário comum se procura o significado exato de uma palavra, neste Dicionário Analógico se procura o inverso: o máximo de significados de uma palavra.
""")

word = st.text_input("Digite uma palavra para buscar sua definição analógica:")

if word:
    with st.spinner('Buscando definição analógica...'):
        definition = get_analogical_definition(word)
    if definition:
        parsed_definition = parse_response(definition)
        for category, items in parsed_definition.items():
            st.subheader(category)
            st.write(", ".join(items))

# Adicione isso no final do seu script para verificar se a chave API está definida
if not openai.api_key:
    st.error("A chave API do OpenAI não está definida. Por favor, configure a variável de ambiente OPENAI_API_KEY.")
