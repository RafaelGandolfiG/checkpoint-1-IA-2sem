# app/chain.py

import os

from dotenv import load_dotenv

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from app.prompts import SYSTEM_PROMPT_GAMES, ANALISE_PROMPT_GAMES

from app.schemas import AnaliseConsulta

# ============================================================
# CARREGAMENTO DAS VARIÁVEIS DE AMBIENTE
# ============================================================

load_dotenv()


OLLAMA_HOST = os.getenv("OLLAMA_HOST", "https://ollama.com")

OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY", "")

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma4:cloud")


# Verifica se a chave foi configurada no .env
if not OLLAMA_API_KEY:
    raise RuntimeError(
        "OLLAMA_API_KEY não encontrada. "
        "Crie um arquivo .env baseado no .env.example "
        "e adicione sua chave da Ollama Cloud."
    )


# Disponibiliza as configurações para o ChatOllama
os.environ["OLLAMA_HOST"] = OLLAMA_HOST
os.environ["OLLAMA_API_KEY"] = OLLAMA_API_KEY


# ============================================================
# FUNÇÃO PARA CRIAR O MODELO
# ============================================================


def criar_llm(temperatura=0.7):
    """
    Cria uma instância do ChatOllama utilizando
    o modelo definido no arquivo .env.
    """

    llm = ChatOllama(
        model=OLLAMA_MODEL,
        base_url=OLLAMA_HOST,
        temperature=temperatura,
        num_predict=512,
    )

    return llm


# ============================================================
# MODELO UTILIZADO PARA O CHAT
# ============================================================

llm_chat = criar_llm(temperatura=0.7)


# ============================================================
# MODELO UTILIZADO PARA A ANÁLISE ESTRUTURADA
# ============================================================

llm_analise = criar_llm(temperatura=0.2)


# ============================================================
# PYDANTIC OUTPUT PARSER
# ============================================================

parser_analise = PydanticOutputParser(pydantic_object=AnaliseConsulta)


# ============================================================
# CHAT PROMPT TEMPLATE
# ============================================================

prompt_analise = ChatPromptTemplate.from_messages(
    [("system", SYSTEM_PROMPT_GAMES), ("human", ANALISE_PROMPT_GAMES)]
)


# Adiciona automaticamente ao prompt as instruções
# de formatação geradas pelo PydanticOutputParser
prompt_analise = prompt_analise.partial(
    instrucoes_formato=(parser_analise.get_format_instructions())
)


# ============================================================
# CHAIN LCEL
# ============================================================

chain_analise = prompt_analise | llm_analise | parser_analise


# ============================================================
# FUNÇÃO PARA ANALISAR A CONSULTA
# ============================================================


def analisar_consulta(pergunta):
    """
    Analisa a mensagem do usuário utilizando
    a chain LCEL e retorna um objeto AnaliseConsulta.
    """

    resultado = chain_analise.invoke({"pergunta": pergunta})

    return resultado


# ============================================================
# ALIAS UTILIZADO PELO CONTEXT_ROT.PY
# ============================================================

llm = llm_chat


# ============================================================
# TESTE DA CHAIN
# ============================================================


def testar_chain():
    """
    Executa um teste simples da análise estruturada.
    """

    pergunta = (
        "Quero um RPG difícil para jogar sozinho no PC. "
        "Você pode me recomendar algum?"
    )

    resultado = analisar_consulta(pergunta)

    print("\n==========================================")

    print("       ANÁLISE ESTRUTURADA")

    print("==========================================\n")

    print(f"Dentro do domínio: " f"{resultado.dentro_dominio}")

    print(f"Assunto: " f"{resultado.assunto}")

    print(f"Tipo de consulta: " f"{resultado.tipo_consulta}")

    print(f"Jogo mencionado: " f"{resultado.jogo_mencionado}")

    print("Precisa de contexto adicional: " f"{resultado.precisa_contexto_adicional}")

    print(f"Resumo: " f"{resultado.resumo}")


# ============================================================
# EXECUÇÃO DIRETA PARA TESTE
# ============================================================

if __name__ == "__main__":
    testar_chain()
