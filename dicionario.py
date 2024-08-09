import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

class GroqAPI:
    def __init__(self, model_name: str):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model_name = model_name

    def _response(self, message):
        return self.client.chat.completions.create(
            model=self.model_name,
            messages=message,
            temperature=0,
            max_tokens=4096,
            stream=True,
            stop=None,
        )

    def response_stream(self, message):
        response_text = ""
        for chunk in self._response(message):
            if 'content' in chunk.choices[0].delta:
                response_text += chunk.choices[0].delta.content
                yield chunk.choices[0].delta.content
        return response_text

class Message:
    system_prompt = "Por favor, escreva todas as respostas em português do Brasil, usando o formato de analogia com categorias como Substantivos, Verbos, Adjetivos, Advérbios e Frases."

    def __init__(self):
        if "messages" not in st.session_state:
            st.session_state.messages = [{"role": "system", "content": self.system_prompt}]

    def add(self, role: str, content: str):
        st.session_state.messages.append({"role": role, "content": content})

    def display_chat_history(self):
        for message in st.session_state.messages:
            if message["role"] == "system":
                continue
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    def display_stream(self, generator):
        response_text = ""
        for response in generator:
            response_text += response
            st.write(response)  # Exibe cada parte do stream em tempo real
        st.session_state.messages.append({"role": "assistant", "content": response_text})
        return response_text

class ModelSelector:
    def __init__(self):
        self.models = ["llama3-70b-8192", "llama3-8b-8192", "mixtral-8x7b-32768", "gemma-7b-it"]

    def select(self):
        with st.sidebar:
            st.sidebar.title("Dicionário Analógico da Língua Portuguesa")
            return st.selectbox("Selecione um modelo:", self.models)

def main():
    user_input = st.text_input("Digite uma palavra ou conceito:")
    model = ModelSelector()
    selected_model = model.select()

    message = Message()

    if user_input:
        llm = GroqAPI(selected_model)
        message.add("user", user_input)
        message.display_chat_history()

        st.title("Dicionário Analógico da Língua Portuguesa")

        # Gera uma única resposta para todas as categorias
        full_response = " ".join(list(llm.response_stream(st.session_state.messages)))
        
        # Exibe a resposta completa, que deve incluir todas as categorias
        st.write(full_response)

if __name__ == "__main__":
    main()
