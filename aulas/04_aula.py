from pathlib import Path
import pickle

import streamlit as st
from unidecode import unidecode

PASTA_MENSAGENS = Path(__file__).parent / 'mensagens'
PASTA_MENSAGENS.mkdir(exist_ok=True)


def le_mensagens_armazendas(usuario, conversando_com):
    nome_arquivo = nome_arquivo_armazenado(usuario, conversando_com)
    if (PASTA_MENSAGENS / nome_arquivo).exists():
        with open(PASTA_MENSAGENS / nome_arquivo, 'rb') as f:
            return pickle.load(f)
    else:
        return []

def armazena_mensagens(usuario, conversando_com, mensagens):
    nome_arquivo = nome_arquivo_armazenado(usuario, conversando_com)
    with open(PASTA_MENSAGENS / nome_arquivo, 'wb') as f:
        pickle.dump(mensagens, f)

def nome_arquivo_armazenado(usuario, conversando_com):
    nome_arquivo = [usuario, conversando_com]
    nome_arquivo.sort()
    nome_arquivo = [u.replace(' ', '_') for u in nome_arquivo]
    nome_arquivo = [unidecode(u) for u in nome_arquivo]
    return '&'.join(nome_arquivo).lower()


def pag_login():
    st.header('💬 Bem-vindo ao Streamlit Messenger', divider=True)
    tab1, tab2 = st.tabs(['Entrar', 'Cadastrar'])

    with tab1.form(key='login'):
        nome = st.text_input('Digite seu nome de usuario')
        senha = st.text_input('Digite sua senha')
        st.form_submit_button('Entrar')
    
    with tab2.form(key='cadastro'):
        nomes= st.text_input('Cadastre um novo nome de usuário')
        senha = st.text_input('Cadastre uma nova senha')
        st.form_submit_button('Cadastrar')

def pagina_chat():
    st.title('💬 Asimov Chat')
    st.divider()

    usuario_logado = 'ADRIANO'
    conversando_com = 'RODRIGO'
    mensagens = le_mensagens_armazendas(usuario_logado, conversando_com)

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
        armazena_mensagens(usuario_logado, conversando_com, mensagens)

def main():
    if not 'pagina_atual' in st.session_state:
        st.session_state['pagina_atual'] = 'login'

    if st.session_state['pagina_atual'] == 'login':
        pag_login()
    elif st.session_state['pagina_atual'] == 'chat':
        pagina_chat()


if __name__ == '__main__':
    main()