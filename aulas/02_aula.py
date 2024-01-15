import streamlit as st

MENSAGENS_FICT = [{'nome_usuario': 'ADRIANO',
                   'conteudo': 'Olá, Juli'},
                   {'nome_usuario': 'JULIANO',
                   'conteudo': 'Olá, Adri'},]

def pagina_chat():
    st.title('💬 Asimov Chat')
    st.divider()

    if not 'mensagens' in st.session_state:
        st.session_state['mensagens'] = MENSAGENS_FICT
    
    mensagens = st.session_state['mensagens']
    usuario_logado = 'ADRIANO'

    for mensagem in mensagens:
        nome_usuario = 'user' if mensagem['nome_usuario'] == usuario_logado else mensagem['nome_usuario']
        avatar = None if mensagem['nome_usuario'] == usuario_logado else '😎'
        chat = st.chat_message(nome_usuario, avatar=avatar)
        chat.markdown(mensagem['conteudo'])
    
    nova_mensagem = st.chat_input('Digite uma mensagem')
    if nova_mensagem:
        nova_dict_mensagem = {'nome_usuario': usuario_logado,
                              'conteudo': nova_mensagem}
        chat = st.chat_message('user')
        chat.markdown(nova_dict_mensagem['conteudo'])
        mensagens.append(nova_dict_mensagem)
        st.session_state['mensagens'] = mensagens


def main():
    pagina_chat()


if __name__ == '__main__':
    main()