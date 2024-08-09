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
