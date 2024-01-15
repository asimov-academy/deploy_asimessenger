from pathlib import Path
import pickle

from unidecode import unidecode

PASTA_MENSAGENS = Path(__file__).parent / 'mensagens'
PASTA_MENSAGENS.mkdir(exist_ok=True)
PASTA_USUARIOS = Path(__file__).parent / 'usuarios'
PASTA_USUARIOS.mkdir(exist_ok=True)



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

def salvar_novo_usuario(nome, senha):
    nome_arquivo = unidecode(nome.replace(' ', '_').lower())
    if (PASTA_USUARIOS / nome_arquivo).exists():
        return False
    else:
        with open(PASTA_USUARIOS / nome_arquivo, 'wb') as f:
            pickle.dump({'nome_usuario': nome, 'senha': senha}, f)
        return True

def validacao_de_senha(nome, senha):
    nome_arquivo = unidecode(nome.replace(' ', '_').lower())
    if not (PASTA_USUARIOS / nome_arquivo).exists():
        return False
    else:
        with open(PASTA_USUARIOS / nome_arquivo, 'rb') as f:
            arquivo_senha = pickle.load(f)
        return arquivo_senha['senha'] == senha

def lista_usuarios():
    usuarios = list(PASTA_USUARIOS.glob('*'))
    usuarios = [u.stem.upper() for u in usuarios]
    return usuarios
