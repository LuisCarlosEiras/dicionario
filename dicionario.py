import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# Carrega as variáveis de ambiente
load_dotenv()

class GroqAPI:
    def __init__(self, model_name: str):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model_name = model_name

    def get_response(self, messages):
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=0,
                max_tokens=4096,
                stream=False,
                stop=None,
            )
            # Debug: Imprimir a resposta completa para verificar a estrutura
            st.write(response)
            
            # Acesso à resposta com verificação
            if response.choices and hasattr(response.choices[0], 'message') and hasattr(response.choices[0].message, 'content'):
                return response.choices[0].message.content
            else:
                return "Resposta inválida ou estrutura inesperada."
        except Exception as e:
            st.error(f"Erro ao obter resposta da API: {e}")
            return "Erro ao obter resposta da API."

class Message:
    system_prompt = "Por favor, escreva todas as respostas em português do Brasil, usando o formato de analogia com categorias como Substantivos, Verbos, Adjetivos, Advérbios e Frases."

    def __init__(self):
        if "messages" not in st.session_state:
            st.session_state.messages = [{"role": "system", "content": self.system_prompt}]

    def add(self, role: str, content: str):
        st.session_state.messages.append({"role": role, "content": content})

    def get_messages(self):
        return st.session_state.messages

class ModelSelector:
    def __init__(self):
        self.models = ["llama3-70b-8192", "llama3-8b-8192", "mixtral-8x7b-32768", "gemma-7b-it"]

    def select(self):
        with st.sidebar:
            st.sidebar.title("Dicionário Analógico da Língua Portuguesa")
            return st.selectbox("Selecione um modelo:", self.models)

def main():
    st.title("Dicionário Analógico da Língua Portuguesa")
    user_input = st.text_input("Digite uma palavra ou conceito:")
    model_selector = ModelSelector()
    selected_model = model_selector.select()
    message = Message()

    if user_input:
        groq_api = GroqAPI(selected_model)
        
        # Adiciona a mensagem do usuário ao histórico
        message.add("user", user_input)
        
        # Obtém a resposta da API
        response = groq_api.get_response(message.get_messages())
        
        # Adiciona a resposta ao histórico
        message.add("assistant", response)
        
        # Exibe a resposta formatada
        st.subheader(f"Analogia para '{user_input}':")
        st.write(response)

if __name__ == "__main__":
    main()
 
