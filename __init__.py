# app/__init__.py

"""
GameGuide — Chatbot Profissional especializado em Games.

Projeto desenvolvido para o CKP01 do 2º semestre.

O pacote app contém os principais módulos do sistema:

- main.py:
  responsável pela execução e interface do chatbot.

- chain.py:
  responsável pela configuração do ChatOllama e
  pela chain LCEL de análise estruturada.

- memory_manager.py:
  responsável pela ConversationChain e pelo
  gerenciamento da memória conversacional.

- schemas.py:
  contém os schemas Pydantic utilizados para
  validar as saídas estruturadas do modelo.

- prompts.py:
  contém os prompts utilizados pelo chatbot.

- context_rot.py:
  responsável pelos testes de Context Rot.
"""
