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
    pagina_chat()


if __name__ == '__main__':
    main()