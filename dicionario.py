import os
import streamlit as st
from pathlib import Path
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
        for chunk in self._response(message):
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

class Message:
    system_prompt = "Por favor, escreva todas as respostas em português do Brasil."

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
        with st.chat_message("assistant"):
            response_text = ""
            for response in generator:
                response_text += response
            st.write(response_text)

class ModelSelector:
    def __init__(self):
        self.models = ["llama3-70b-8192", "llama3-8b-8192", "mixtral-8x7b-32768", "gemma-7b-it"]

    def select(self):
        with st.sidebar:
            st.sidebar.title("Dicionário Analógico da Língua Portuguesa")
            return st.selectbox("Selecione um modelo:", self.models)

def main():
    user_input = st.text_input("Digite uma palavra:")
    model = ModelSelector()
    selected_model = model.select()

    message = Message()

    if user_input:
        llm = GroqAPI(selected_model)
        message.add("user", user_input)
        message.display_chat_history()

        analogias = list(llm.response_stream(message.add("assistant", user_input)))
        verbos = list(llm.response_stream(message.add("assistant", user_input)))
        adverbios = list(llm.response_stream(message.add("assistant", user_input)))
        adjetivos = list(llm.response_stream(message.add("assistant", user_input)))
        frases = list(llm.response_stream(message.add("assistant", user_input)))

        st.title("Dicionário Analógico da Língua Portuguesa")

        with st.expander("Analogias"):
            st.write(analogias)

        with st.expander("Verbos"):
            st.write(verbos)

        with st.expander("Advérbios"):
            st.write(adverbios)

        with st.expander("Adjetivos"):
            st.write(adjetivos)

        with st.expander("Frases"):
            st.write(frases)

if __name__ == "__main__":
    main()
