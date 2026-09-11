# app/main.py

import gradio as gr

from app.chain import llm_chat, analisar_consulta

from app.memory_manager import criar_chat_com_memoria, enviar_mensagem, limpar_memoria

from app.prompts import SYSTEM_PROMPT_GAMES

# ============================================================
# CRIAÇÃO DO CHAT COM MEMÓRIA
# ============================================================

chat, memoria = criar_chat_com_memoria(llm=llm_chat, system_prompt=SYSTEM_PROMPT_GAMES)


# ============================================================
# MENSAGEM PARA ASSUNTOS FORA DO DOMÍNIO
# ============================================================

MENSAGEM_FORA_DOMINIO = (
    "Minha especialidade é games. "
    "Posso ajudar com jogos, consoles, plataformas, "
    "mecânicas, estratégias, recomendações, comparações "
    "e assuntos relacionados."
)


# ============================================================
# FUNÇÃO PRINCIPAL DO CHATBOT
# ============================================================


def responder(mensagem, historico):
    """
    Recebe a mensagem do usuário, analisa a consulta
    e gera a resposta do GameGuide.
    """

    # Verifica se a mensagem está vazia
    if not mensagem:
        return "Digite uma mensagem para conversar " "com o GameGuide."

    mensagem = mensagem.strip()

    # Verifica novamente depois de remover espaços
    if not mensagem:
        return "Digite uma mensagem para conversar " "com o GameGuide."

    # ========================================================
    # ANÁLISE ESTRUTURADA
    # ========================================================

    try:

        analise = analisar_consulta(mensagem)

    except Exception as erro:

        print("\nErro durante a análise estruturada:")

        print(erro)

        return (
            "Não consegui analisar sua mensagem corretamente. "
            "Tente reformular a pergunta."
        )

    # ========================================================
    # VERIFICAÇÃO DO DOMÍNIO
    # ========================================================

    if not analise.dentro_dominio:

        return MENSAGEM_FORA_DOMINIO

    # ========================================================
    # RESPOSTA COM MEMÓRIA
    # ========================================================

    try:

        resposta = enviar_mensagem(chat, mensagem)

    except Exception as erro:

        print("\nErro durante a geração da resposta:")

        print(erro)

        return "Ocorreu um problema ao gerar a resposta. " "Tente novamente."

    return resposta


# ============================================================
# FUNÇÃO PARA LIMPAR A MEMÓRIA
# ============================================================


def limpar_conversa():
    """
    Limpa o histórico armazenado pela memória
    do chatbot.
    """

    limpar_memoria(memoria)

    return "Memória da conversa limpa."


# ============================================================
# INTERFACE GRADIO
# ============================================================

demo = gr.ChatInterface(
    fn=responder,
    title="GameGuide",
    description=(
        "Chatbot profissional especializado no universo de games. "
        "Pergunte sobre jogos, consoles, plataformas, mecânicas, "
        "estratégias, recomendações e comparações."
    ),
)


# ============================================================
# FUNÇÃO PRINCIPAL
# ============================================================


def main():
    """
    Inicia a interface Gradio do GameGuide.
    """

    print("\n==========================================")

    print("             GAMEGUIDE")

    print("==========================================")

    print("\nChatbot iniciado com sucesso.")

    print("Modelo: gemma4:cloud")

    print("Memória: ConversationTokenBufferMemory")

    print("Pipeline estruturada: LCEL + Pydantic")

    print("\nAbrindo interface Gradio...\n")

    demo.launch()


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()
