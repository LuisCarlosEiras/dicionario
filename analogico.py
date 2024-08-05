import streamlit as st
import openai
from dotenv import load_dotenv
import os

# Carrega as variáveis de ambiente
load_dotenv()

# Configura a API do OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_analogical_definition(word):
    prompt = f"""Você é um dicionário analógico da língua portuguesa. Forneça uma definição analógica para a palavra: {word}

    Exemplos de definições analógicas:

    Comparação: cotejo, cotejamento, homeose, relação, paralelo, semelhança = confronto, confrontação, acareação, meças, colação (ant.), conferência, conferição, equiparação, contraste, identidade, identificação, aferição, graduação, graduamento, equiparência, combinação, símile, similitude, similaridade, afinidade, analogia, alegoria; dessemelhança, diferença, diversidade, paralelismo. 
    Verbo: comparar, cotejar, igualar, confrontar, relacionar, contrapor, contrastar, colacionar, balançar, balancear, assemelhar, colocar nos pratos da balança, estabelecer confronto, estabelecer comparação, parva componere magnis, fazer cotejo, aferir; fazer um ou pôr em paralelo; equiparar, identificar, carear, acarear; concertar, contraprovar, conferir, opor, apodar, aquilatar, aferir por; pôr em face, apresentar em confronto. 
    Adjetivo: comparativo, comparador, cotejador, alegórico, umbrátil, afim, análogo; similar, idêntico, semelhante; diferente, diverso, dessemelhante. 
    Advérbio: comparativamente, & adj., em comparação, a par de.

    Probabilidade: possibilidade, admissibilidade, plausibilidade, aparência, perspectiva, indícios que deixam presumir a verdade, racionalidade, parecença; viso, vislumbre, aparência, indício de verdade; presunção; evidência presuntiva, circunstancial; credibilidade; aparência boa/favorável/alvissareira/promissora/razoável; aspecto promissor, prospecto, esperanças bem fundadas, conjectura provável, alternativa; expectativa, probabilismo, cálculo das possibilidades/de probabilidades. 
    Verbo: probabilizar, tornar (provável & adj.), ser (provável & adj.); ter seu lugar, dever, ter tudo para, estar com todo o jeito de, não haver razão para se perder a esperança, implicar; prometer bastante; levar jeito, ter toda probabilidade, parecer, ter boa perspectiva, ter expectativa de, aguardar; pressupor, contar com (crer). 
    Adjetivo: provável, probábil, verossímil, alvissareiro, opinável, opinativo, esperável, expectável, esperanço, plausível, especioso, ostensível, ostensivo, bem fundado, bem figurado, benetrovato, razoável, racional, racionável, (p. us.), crível, presumível, presuntivo, aparente, natural. 
    Advérbio: provavelmente & adj., com probabilidade, com toda a probabilidade, dez contra um, segundo as melhores aparências, prima facie, a todas as aparências. 
    Frases: Tudo indica que…; As aparências são a favor de…; Há motivos para crer/para esperar…; Militam muitas possibilidades em favor de…; Se non é vero é bene trovato. Não há motivos para se descrer.

    Forneça uma definição analógica para a palavra: {word}
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um assistente especializado em fornecer definições analógicas em português."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            n=1,
            temperature=0.3,
        )
        return response.choices[0].message['content'].strip()
    except openai.error.OpenAIError as e:
        st.error(f"Ocorreu um erro ao processar sua solicitação: {str(e)}")
        return None

st.title("Dicionário Analógico da Língua Portuguesa")

st.write("""
Se num dicionário comum se procura o significado exato de uma palavra, neste Dicionário Analógico se procura o inverso: o máximo de significados de uma palavra.
""")

word = st.text_input("Digite uma palavra para buscar sua definição analógica:")

if word:
    with st.spinner('Buscando definição analógica...'):
        definition = get_analogical_definition(word)
    if definition:
        st.write(definition)

# Adicione isso no final do seu script para verificar se a chave API está definida
if not openai.api_key:
    st.error("A chave API do OpenAI não está definida. Por favor, configure a variável de ambiente OPENAI_API_KEY.")
