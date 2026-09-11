# app/context_rot.py

import os

import pandas as pd
import matplotlib.pyplot as plt
import tiktoken

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from app.prompts import SYSTEM_PROMPT_GAMES, CONTEXT_ROT_PROMPT_GAMES

# ============================================================
# QUANTIDADES DE TURNOS UTILIZADAS NO EXPERIMENTO
# ============================================================

TURNOS_TESTE = [0, 20, 50, 100, 150]


# ============================================================
# INFORMAÇÕES IMPORTANTES
# ============================================================

INFORMACOES_IMPORTANTES = """
O usuário informou:

- Seu nome é Rafael.
- Sua plataforma principal é PC.
- Seu gênero favorito é RPG.
- Ele prefere jogos single-player.
- Ele prefere jogos difíceis e desafiadores.
"""


# ============================================================
# PERGUNTA FINAL
# ============================================================

PERGUNTA_TESTE = """
Com base exclusivamente no contexto fornecido, informe:

1. O nome do usuário.
2. Sua plataforma principal.
3. Seu gênero favorito.
4. Se ele prefere single-player ou multiplayer.
5. Que tipo de dificuldade ele prefere.
"""


# ============================================================
# TÓPICOS UTILIZADOS PARA AUMENTAR O CONTEXTO
# ============================================================

TOPICOS = [
    "FPS",
    "PvP",
    "PvE",
    "DLC",
    "ray tracing",
    "crossplay",
    "matchmaking",
    "roguelike",
    "mundo aberto",
    "jogos indie",
    "speedrun",
    "hitbox",
    "input lag",
    "RNG",
    "patches",
    "buff",
    "nerf",
    "quests",
    "lore",
    "grind",
]


# ============================================================
# CRIAÇÃO DE TURNOS ADICIONAIS
# ============================================================


def criar_turno(numero):
    """
    Cria informações adicionais relacionadas ao domínio
    de games para aumentar o tamanho e a complexidade
    do contexto.
    """

    topico = TOPICOS[numero % len(TOPICOS)]

    turno = f"""
Turno {numero + 1}

Usuário:
Explique o conceito de {topico} dentro do universo dos games.

Assistente:
O conceito de {topico} pode aparecer em diferentes tipos
de jogos e pode possuir características diferentes dependendo
do gênero, plataforma e estilo de gameplay.

Jogadores diferentes também podem interpretar ou utilizar
{topico} de maneiras diferentes.

Alguns jogadores preferem experiências competitivas,
enquanto outros preferem experiências mais focadas em
exploração ou narrativa.

Também existem diferenças relacionadas às plataformas.
Alguns jogadores utilizam computadores, enquanto outros
preferem consoles.

Dependendo do jogo, {topico} pode afetar diretamente
a estratégia utilizada pelo jogador, a dificuldade,
a progressão e a experiência geral durante a partida.

A importância de {topico} também pode variar de acordo
com o gênero do jogo e com os objetivos de cada jogador.
"""

    # --------------------------------------------------------
    # INFORMAÇÕES DE OUTROS JOGADORES
    # --------------------------------------------------------

    if numero % 5 == 0:

        turno += """
Exemplo:

Um jogador chamado Bruno prefere jogos FPS.

Sua plataforma principal é PlayStation.

Bruno prefere partidas multiplayer competitivas
e normalmente escolhe jogos com dificuldade normal.
"""

    if numero % 7 == 0:

        turno += """
Outro exemplo:

Um jogador chamado Lucas prefere Xbox.

Seu gênero favorito é corrida.

Ele prefere jogar multiplayer e normalmente
escolhe dificuldades mais baixas.
"""

    if numero % 9 == 0:

        turno += """
Outro jogador:

Gabriel utiliza principalmente PlayStation.

Ele prefere jogos de ação e aventura.

Sua preferência é por experiências multiplayer
e jogos com dificuldade normal.
"""

    if numero % 11 == 0:

        turno += """
Exemplo adicional:

Um jogador chamado Rafael participou recentemente
de uma partida PvP competitiva.

Durante a partida ele utilizou um console.

Essa informação descreve apenas aquela partida
específica.
"""

    return turno


# ============================================================
# CRIAÇÃO DO CONTEXTO
# ============================================================


def criar_contexto(quantidade_turnos):
    """
    Coloca as informações importantes no início
    e adiciona progressivamente novos turnos.
    """

    contexto = INFORMACOES_IMPORTANTES

    for i in range(quantidade_turnos):

        contexto += "\n"

        contexto += criar_turno(i)

    return contexto


# ============================================================
# TOKENIZAÇÃO
# ============================================================


def criar_tokenizador():
    """
    Cria o tokenizador utilizado para estimar
    o crescimento do contexto.
    """

    tokenizador = tiktoken.get_encoding("cl100k_base")

    return tokenizador


def contar_tokens(texto, tokenizador):
    """
    Conta aproximadamente a quantidade
    de tokens presente no contexto.
    """

    tokens = tokenizador.encode(texto)

    return len(tokens)


# ============================================================
# CHAIN DO EXPERIMENTO
# ============================================================


def criar_chain_context_rot(llm):
    """
    Cria a chain LCEL utilizada durante
    todos os testes de Context Rot.
    """

    prompt = ChatPromptTemplate.from_messages(
        [("system", SYSTEM_PROMPT_GAMES), ("human", CONTEXT_ROT_PROMPT_GAMES)]
    )

    chain = prompt | llm | StrOutputParser()

    return chain


# ============================================================
# AVALIAÇÃO DA RESPOSTA
# ============================================================


def avaliar_resposta(resposta):
    """
    Verifica quantas das cinco informações
    principais foram recuperadas.
    """

    texto = resposta.lower()

    pontuacao = 0

    # Nome
    if "rafael" in texto:
        pontuacao += 1

    # Plataforma
    if "pc" in texto:
        pontuacao += 1

    # Gênero
    if "rpg" in texto:
        pontuacao += 1

    # Preferência single-player
    if "single-player" in texto or "single player" in texto:
        pontuacao += 1

    # Preferência de dificuldade
    if (
        "difícil" in texto
        or "difíceis" in texto
        or "desafiador" in texto
        or "desafiadores" in texto
    ):
        pontuacao += 1

    qualidade = (pontuacao / 5) * 100

    return (pontuacao, qualidade)


# ============================================================
# EXECUÇÃO DE UM TESTE
# ============================================================


def executar_teste(chain, tokenizador, quantidade_turnos):
    """
    Executa o experimento para uma determinada
    quantidade de turnos.
    """

    contexto = criar_contexto(quantidade_turnos)

    tokens = contar_tokens(contexto, tokenizador)

    resposta = chain.invoke({"contexto": contexto, "pergunta": PERGUNTA_TESTE})

    pontuacao, qualidade = avaliar_resposta(resposta)

    resultado = {
        "turnos": quantidade_turnos,
        "tokens": tokens,
        "pontuacao": pontuacao,
        "qualidade": qualidade,
        "resposta": resposta,
    }

    return resultado


# ============================================================
# EXECUÇÃO DE TODOS OS TESTES
# ============================================================


def executar_context_rot(llm):
    """
    Executa o experimento com todos os tamanhos
    de contexto definidos em TURNOS_TESTE.
    """

    tokenizador = criar_tokenizador()

    chain = criar_chain_context_rot(llm)

    resultados = []

    print("\n==========================================")
    print("       EXPERIMENTO DE CONTEXT ROT")
    print("==========================================\n")

    for turnos in TURNOS_TESTE:

        print(f"Executando teste com {turnos} turnos...")

        resultado = executar_teste(chain, tokenizador, turnos)

        resultados.append(resultado)

        print(f"Tokens aproximados: " f"{resultado['tokens']}")

        print(f"Pontuação: " f"{resultado['pontuacao']}/5")

        print(f"Qualidade: " f"{resultado['qualidade']:.0f}%")

        print("\nResposta:")

        print(resultado["resposta"])

        print("\n------------------------------------------\n")

    return resultados


# ============================================================
# DATAFRAME
# ============================================================


def criar_dataframe(resultados):
    """
    Transforma os resultados em DataFrame
    para facilitar a comparação.
    """

    dados = []

    for resultado in resultados:

        dados.append(
            {
                "Turnos": resultado["turnos"],
                "Tokens": resultado["tokens"],
                "Pontuação": resultado["pontuacao"],
                "Qualidade (%)": resultado["qualidade"],
            }
        )

    df = pd.DataFrame(dados)

    return df


# ============================================================
# EXIBIÇÃO DOS RESULTADOS
# ============================================================


def mostrar_resultados(df):
    """
    Mostra a tabela final no terminal.
    """

    print("\n==========================================")
    print("       RESULTADOS DO CONTEXT ROT")
    print("==========================================\n")

    print(df.to_string(index=False))


# ============================================================
# ANÁLISE DA DEGRADAÇÃO
# ============================================================


def verificar_degradacao(df):
    """
    Verifica se ocorreu alguma queda de qualidade
    durante o crescimento do contexto.
    """

    qualidade_inicial = df.iloc[0]["Qualidade (%)"]

    menor_qualidade = df["Qualidade (%)"].min()

    print("\n==========================================")
    print("        ANÁLISE DA DEGRADAÇÃO")
    print("==========================================\n")

    if menor_qualidade < qualidade_inicial:

        queda = qualidade_inicial - menor_qualidade

        linha_menor = df[df["Qualidade (%)"] == menor_qualidade].iloc[0]

        print("Foi observada degradação de qualidade.")

        print(f"Qualidade inicial: " f"{qualidade_inicial:.0f}%")

        print(f"Menor qualidade observada: " f"{menor_qualidade:.0f}%")

        print(f"Queda observada: " f"{queda:.0f} pontos percentuais.")

        print("A menor qualidade ocorreu com " f"{int(linha_menor['Turnos'])} turnos.")

        print(
            "Quantidade aproximada de tokens nesse teste: "
            f"{int(linha_menor['Tokens'])}."
        )

    else:

        print("Não foi observada degradação de qualidade " "neste experimento.")

        print(
            "O modelo conseguiu recuperar todas as "
            "informações mesmo com o crescimento "
            "do contexto."
        )


# ============================================================
# SALVAR CSV
# ============================================================


def salvar_csv(df):
    """
    Salva os resultados do experimento em CSV.
    """

    os.makedirs("output", exist_ok=True)

    caminho = os.path.join("output", "context_rot_resultados.csv")

    df.to_csv(caminho, index=False, encoding="utf-8-sig")

    print(f"\nCSV salvo em: {caminho}")


# ============================================================
# GERAR GRÁFICO
# ============================================================


def gerar_grafico(df):
    """
    Cria o gráfico de qualidade em relação
    ao crescimento do contexto.
    """

    os.makedirs("output", exist_ok=True)

    plt.figure(figsize=(8, 5))

    plt.plot(df["Turnos"], df["Qualidade (%)"], marker="o")

    plt.title("Context Rot - Qualidade por tamanho do contexto")

    plt.xlabel("Quantidade de turnos adicionais")

    plt.ylabel("Qualidade da resposta (%)")

    plt.xticks(TURNOS_TESTE)

    plt.ylim(0, 105)

    plt.grid(True, alpha=0.3)

    plt.tight_layout()

    caminho = os.path.join("output", "context_rot_grafico.png")

    plt.savefig(caminho)

    plt.close()

    print(f"Gráfico salvo em: {caminho}")


# ============================================================
# FUNÇÃO PRINCIPAL DO EXPERIMENTO
# ============================================================


def executar_experimento_context_rot(llm):
    """
    Executa todo o experimento de Context Rot.
    """

    resultados = executar_context_rot(llm)

    df = criar_dataframe(resultados)

    mostrar_resultados(df)

    verificar_degradacao(df)

    salvar_csv(df)

    gerar_grafico(df)

    return df


# ============================================================
# EXECUÇÃO DIRETA
# ============================================================

if __name__ == "__main__":

    from app.chain import llm

    executar_experimento_context_rot(llm)
