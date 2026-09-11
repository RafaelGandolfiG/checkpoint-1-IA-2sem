# CKP01 — Chatbot Profissional · GameGuide

**Prompt Engineering & Artificial Intelligence · FIAP · 2º Semestre 2026**

## Integrantes

- Rafael Gandolfi Gonçalves — RM 569036 — 1CCPI
- Rafael Lins — RM 570588 — 1CCPI
- Cauã Paes — RM 569906 — 1CCPI
- Guilherme Miranda — RM 573107 — 1CCPI
- Carlos Eduardo — RM 572949 — 1CCPI
- João Pedro Soler — RM 569725 — 1CCPI

---

# 1. Sobre o projeto

O **GameGuide** é um chatbot profissional especializado no universo de games.

O projeto foi desenvolvido para o CKP01 da disciplina de Prompt Engineering & Artificial Intelligence da FIAP.

O chatbot utiliza um Large Language Model por meio do **Ollama Cloud**, com o modelo `gemma4:cloud`, integrado ao LangChain.

O sistema foi desenvolvido utilizando conceitos de:

- Prompt Engineering;
- Context Engineering;
- LCEL (LangChain Expression Language);
- memória conversacional;
- Pydantic;
- saída estruturada;
- Context Rot;
- XML Tagging;
- gerenciamento de contexto;
- interface com Gradio.

O projeto foi estruturado de forma modular para permitir sua evolução nos próximos checkpoints.

---

# 2. Domínio

O domínio escolhido para o projeto foi **Games**.

O GameGuide é especializado em assuntos relacionados ao universo dos jogos eletrônicos, incluindo:

- jogos;
- consoles;
- PC gaming;
- plataformas;
- gêneros;
- franquias;
- personagens;
- gameplay;
- mecânicas;
- modos de jogo;
- single-player;
- multiplayer;
- PvP;
- PvE;
- estratégias;
- recomendações;
- comparações;
- eSports;
- requisitos de jogos;
- desempenho;
- hardware relacionado a games;
- software relacionado a games;
- cultura gamer.

## 2.1 Justificativa da escolha do domínio

O domínio de games foi escolhido por possuir uma grande variedade de situações em que um chatbot pode auxiliar o usuário.

Jogadores frequentemente precisam comparar jogos, receber recomendações, entender mecânicas, conhecer requisitos, escolher plataformas ou receber auxílio sobre estratégias.

Além disso, o domínio permite demonstrar de maneira clara conceitos estudados durante a disciplina, como memória conversacional, personalização de respostas, saída estruturada e gerenciamento de contexto.

Por exemplo, o chatbot pode lembrar que determinado usuário prefere PC, RPG, jogos single-player e dificuldade elevada e utilizar essas informações posteriormente para produzir recomendações mais adequadas.

---

# 3. Usuários-alvo

O GameGuide foi desenvolvido principalmente para jogadores que procuram informações e auxílio relacionado a games.

O público-alvo inclui:

- jogadores iniciantes;
- jogadores casuais;
- jogadores experientes;
- usuários procurando novos jogos;
- jogadores procurando estratégias;
- usuários comparando jogos ou plataformas;
- pessoas procurando informações sobre mecânicas, gêneros e franquias.

O chatbot adapta o nível de detalhamento da resposta de acordo com a solicitação e o contexto da conversa.

---

# 4. Funcionalidades

O GameGuide permite ao usuário conversar sobre assuntos relacionados ao universo dos games.

Entre suas principais funcionalidades estão:

- responder perguntas sobre games;
- fornecer recomendações;
- comparar jogos e plataformas;
- explicar mecânicas;
- fornecer estratégias;
- identificar o assunto principal da pergunta;
- classificar o tipo da consulta;
- identificar jogos mencionados;
- verificar se a pergunta pertence ao domínio;
- manter informações relevantes da conversa utilizando memória;
- validar respostas estruturadas utilizando Pydantic;
- restringir o comportamento do modelo por meio do System Prompt;
- demonstrar experimentalmente Context Rot.

---

# 5. Arquitetura do projeto

O projeto foi dividido em módulos para separar as responsabilidades do sistema.

```text
CKP01_Games/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── chain.py
│   ├── memory_manager.py
│   ├── schemas.py
│   ├── context_rot.py
│   └── prompts.py
│
├── output/
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Responsabilidade dos arquivos

### `app/main.py`

É o ponto de entrada da aplicação.

Responsável por:

- inicializar o chatbot;
- conectar os diferentes módulos;
- receber mensagens;
- verificar o domínio da consulta;
- enviar mensagens para o chatbot com memória;
- iniciar a interface Gradio.

### `app/chain.py`

Responsável pela configuração do modelo e pela pipeline LCEL.

Contém:

- `ChatOllama`;
- `ChatPromptTemplate`;
- `PydanticOutputParser`;
- modelo `gemma4:cloud`;
- chain de análise estruturada.

A principal chain segue o formato:

```python
chain_analise = (
    prompt_analise
    | llm_analise
    | parser_analise
)
```

Portanto, o fluxo é:

```text
Prompt
   ↓
ChatOllama
   ↓
PydanticOutputParser
   ↓
AnaliseConsulta
```

### `app/memory_manager.py`

Responsável pela memória conversacional.

Utiliza:

- `ConversationChain`;
- `ConversationTokenBufferMemory`;
- `PromptTemplate`.

### `app/schemas.py`

Contém o modelo Pydantic utilizado para validar a análise estruturada produzida pelo LLM.

### `app/prompts.py`

Centraliza os prompts utilizados pela aplicação.

Contém:

- `SYSTEM_PROMPT_GAMES`;
- `HUMAN_PROMPT_GAMES`;
- `MEMORY_PROMPT_GAMES`;
- `ANALISE_PROMPT_GAMES`;
- `CONTEXT_ROT_PROMPT_GAMES`.

### `app/context_rot.py`

Responsável pelo experimento de Context Rot.

O módulo aumenta progressivamente o contexto e verifica se o modelo continua conseguindo recuperar corretamente informações relevantes.

---

# 6. Fluxo da aplicação

O fluxo principal do GameGuide é:

```text
Usuário
   ↓
Interface Gradio
   ↓
main.py
   ↓
analisar_consulta()
   ↓
LCEL
ChatPromptTemplate
   |
ChatOllama
   |
PydanticOutputParser
   ↓
AnaliseConsulta
   ↓
Consulta pertence ao domínio?
   │
   ├── NÃO
   │     ↓
   │  Resposta informando
   │  o domínio do chatbot
   │
   └── SIM
         ↓
   ConversationChain
         +
   ConversationTokenBufferMemory
         +
   MEMORY_PROMPT_GAMES
         ↓
      GameGuide
         ↓
      Resposta
```

Dessa forma, a aplicação utiliza duas partes principais: uma chain estruturada para analisar a mensagem e uma ConversationChain responsável pela conversa com memória.

---

# 7. Pipeline LCEL

O projeto utiliza **LCEL (LangChain Expression Language)** para construir a pipeline de análise estruturada.

A composição utiliza o operador pipe (`|`):

```python
chain_analise = (
    prompt_analise
    | llm_analise
    | parser_analise
)
```

A mensagem passa por três etapas:

1. `ChatPromptTemplate` estrutura a entrada;
2. `ChatOllama` envia a solicitação para o modelo;
3. `PydanticOutputParser` transforma e valida a saída.

Essa separação torna a chain modular e permite substituir ou modificar componentes individualmente.

---

# 8. Modelo de IA

O projeto utiliza exclusivamente:

```text
gemma4:cloud
```

por meio do **Ollama Cloud**.

A configuração é carregada através de variáveis de ambiente.

O arquivo `.env` contém as configurações reais:

```env
OLLAMA_HOST=https://ollama.com
OLLAMA_API_KEY=SUA_CHAVE_REAL
OLLAMA_MODEL=gemma4:cloud
```

A chave nunca é escrita diretamente no código.

O arquivo `.env` também não deve ser versionado nem incluído na entrega.

Para demonstrar quais variáveis são necessárias, o projeto contém:

```text
.env.example
```

com:

```env
OLLAMA_HOST=https://ollama.com
OLLAMA_API_KEY=sua_chave_aqui
OLLAMA_MODEL=gemma4:cloud
```

---

# 9. Memória conversacional

O projeto utiliza:

```text
ConversationTokenBufferMemory
```

com limite de:

```text
1000 tokens
```

A memória é integrada a uma:

```text
ConversationChain
```

## 9.1 Justificativa da escolha da memória

Foi escolhida a `ConversationTokenBufferMemory` porque informações recentes da conversa são importantes para o domínio de games.

Durante uma conversa, o usuário pode informar preferências como:

- plataforma principal;
- gênero favorito;
- preferência por single-player ou multiplayer;
- dificuldade desejada;
- estilo de jogo.

Essas informações podem ser utilizadas posteriormente para personalizar respostas e recomendações.

Por exemplo, se o usuário informar anteriormente que joga no PC, prefere RPG, single-player e jogos difíceis, o chatbot pode utilizar essas informações posteriormente sem precisar perguntar tudo novamente.

## 9.2 Por que TokenBuffer?

A `ConversationTokenBufferMemory` mantém o histórico recente da conversa e controla seu tamanho por meio de um limite de tokens.

Foi utilizado o limite de **1000 tokens**.

Esse valor está dentro da faixa de 800 a 1500 tokens definida para o projeto e permite manter contexto suficiente sem permitir crescimento ilimitado do histórico.

## 9.3 Comparação com outras estratégias

A `ConversationBufferMemory` poderia armazenar todo o histórico da conversa, porém o contexto continuaria crescendo conforme novas mensagens fossem adicionadas.

Isso aumentaria o número de tokens enviados ao modelo.

A `ConversationSummaryMemory` poderia resumir mensagens anteriores, reduzindo o tamanho do histórico. Entretanto, o processo de resumo pode acrescentar custo de processamento e remover pequenos detalhes que podem ser importantes para personalizar recomendações.

Por esse motivo, para o GameGuide foi escolhida a `ConversationTokenBufferMemory`.

Ela oferece um equilíbrio entre:

- preservação das mensagens recentes;
- controle da quantidade de tokens;
- manutenção de preferências relevantes;
- prevenção do crescimento ilimitado do contexto.

---

# 10. Demonstração da memória

O projeto possui uma demonstração com mais de cinco turnos de conversa.

Exemplo:

```text
Turno 1
Usuário: Meu nome é Rafael.

Turno 2
Usuário: Eu jogo principalmente no PC.

Turno 3
Usuário: Meu gênero favorito é RPG.

Turno 4
Usuário: Eu prefiro jogos single-player.

Turno 5
Usuário: Eu gosto de jogos difíceis e desafiadores.

Turno 6
Usuário:
Com base no que eu falei anteriormente,
qual é minha plataforma principal,
meu gênero favorito e qual estilo de jogo eu prefiro?
```

A finalidade desse teste é verificar se o chatbot consegue recuperar informações fornecidas em turnos anteriores.

---

# 11. Pydantic v2 e saída estruturada

O projeto utiliza **Pydantic v2** para validar uma das saídas produzidas pelo modelo.

O schema principal é:

```python
class AnaliseConsulta(BaseModel):
    dentro_dominio: bool
    assunto: str

    tipo_consulta: Literal[
        "informacao",
        "recomendacao",
        "comparacao",
        "estrategia",
        "outro"
    ]

    jogo_mencionado: str | None
    precisa_contexto_adicional: bool
    resumo: str
```

O schema possui **6 campos tipados**.

A validação é realizada através de:

```python
PydanticOutputParser
```

O parser é integrado diretamente à pipeline LCEL:

```python
chain_analise = (
    prompt_analise
    | llm_analise
    | parser_analise
)
```

Além dos tipos definidos, foram adicionados `Field` e `field_validator` para aumentar a consistência das informações retornadas.

---

# 12. Análise estruturada

Antes de produzir a resposta conversacional, o sistema analisa a mensagem recebida.

A análise gera os seguintes campos:

```text
dentro_dominio
assunto
tipo_consulta
jogo_mencionado
precisa_contexto_adicional
resumo
```

O campo `tipo_consulta` aceita somente:

```text
informacao
recomendacao
comparacao
estrategia
outro
```

Isso reduz respostas inconsistentes e permite que o sistema trabalhe com categorias previamente definidas.

---

# 13. System Prompt

O GameGuide possui um System Prompt específico para o domínio de games.

O prompt define:

- identidade;
- objetivo;
- domínio;
- interpretação;
- gerenciamento de contexto;
- hierarquia de instruções;
- regras;
- confiabilidade;
- recomendações;
- comparações;
- estratégias;
- tratamento de spoilers;
- comportamento fora do domínio;
- proteção contra prompt injection;
- proteção contra jailbreak;
- proteção contra indirect prompt injection;
- proteção contra prompt leaking;
- privacidade;
- formato das respostas;
- critérios de qualidade;
- prioridades.

O prompt utiliza **XML Tagging** para separar claramente suas diferentes seções.

Exemplo:

```xml
<identidade>
...
</identidade>

<dominio>
...
</dominio>

<regras>
...
</regras>

<confiabilidade>
...
</confiabilidade>

<guardrail_prompt_injection>
...
</guardrail_prompt_injection>

<formato_resposta>
...
</formato_resposta>
```

Essa organização facilita a interpretação das diferentes responsabilidades presentes no contexto enviado ao modelo.

---

# 14. Restrições e guardrails

As principais regras de segurança e comportamento estão definidas dentro do próprio System Prompt.

O GameGuide deve manter sua identidade e permanecer dentro do domínio de games.

O prompt também contém regras relacionadas a:

- prompt injection;
- jailbreak;
- indirect prompt injection;
- prompt leaking;
- privacidade;
- hierarquia de instruções.

Por exemplo, solicitações que tentem fazer o modelo ignorar suas instruções não devem substituir o comportamento definido pelo System Prompt.

As mensagens do usuário são tratadas como entradas, enquanto as instruções do sistema permanecem como regras principais de comportamento.

---

# 15. Context Engineering

O projeto utiliza princípios de **Context Engineering** para controlar quais informações são fornecidas ao modelo.

O objetivo é utilizar informações relevantes no contexto sem aumentar desnecessariamente a quantidade de tokens.

O System Prompt orienta o modelo a:

- utilizar informações relevantes do histórico;
- ignorar informações irrelevantes;
- evitar repetições;
- priorizar informações mais recentes quando houver conflito;
- não inventar informações ausentes.

A memória também possui um limite de tokens justamente para evitar crescimento ilimitado do contexto.

---

# 16. Context Rot

O projeto implementa um experimento de **Context Rot**.

Context Rot representa a possibilidade de degradação da capacidade do modelo de localizar, interpretar ou utilizar corretamente informações relevantes conforme a quantidade de contexto aumenta.

O objetivo do experimento é observar se o crescimento da janela de contexto afeta a capacidade do modelo de recuperar informações importantes.

---

# 17. Metodologia do experimento de Context Rot

O experimento mantém constantes:

- o modelo;
- o System Prompt;
- a pergunta final;
- as informações importantes;
- os critérios de avaliação.

A variável modificada é a quantidade de contexto adicionada antes da pergunta.

São utilizados os seguintes tamanhos:

```text
0 turnos
5 turnos
10 turnos
15 turnos
20 turnos
```

As informações importantes são apresentadas no início do contexto.

Depois são adicionados progressivamente turnos relacionados ao universo de games.

Ao final, o modelo precisa recuperar cinco informações:

1. nome do usuário;
2. plataforma principal;
3. gênero favorito;
4. preferência entre single-player e multiplayer;
5. preferência de dificuldade.

---

# 18. Métrica de qualidade do Context Rot

Cada informação corretamente recuperada vale **1 ponto**.

A pontuação máxima é:

```text
5 pontos
```

A qualidade é calculada por:

```text
qualidade = (pontuacao / 5) * 100
```

Exemplo:

```text
5 informações corretas
5 / 5 = 100%

4 informações corretas
4 / 5 = 80%

3 informações corretas
3 / 5 = 60%
```

Dessa forma, é possível comparar quantitativamente a capacidade do modelo de recuperar informações conforme o contexto cresce.

---

# 19. Contagem de tokens

O experimento utiliza a biblioteca:

```text
tiktoken
```

para obter uma estimativa comparativa da quantidade de tokens presente em cada contexto.

É utilizada a codificação:

```python
tiktoken.get_encoding(
    "cl100k_base"
)
```

Essa contagem é utilizada como **métrica aproximada e comparativa**.

Ela não representa necessariamente a tokenização exata utilizada internamente pelo modelo `gemma4:cloud`.

O objetivo é medir de maneira consistente o crescimento relativo do contexto entre os testes.

---

# 20. Resultados do Context Rot

Após executar o experimento, o sistema gera uma tabela com:

- quantidade de turnos;
- quantidade aproximada de tokens;
- pontuação;
- qualidade percentual.

Os resultados também são exportados para:

```text
output/context_rot_resultados.csv
```

e o gráfico para:

```text
output/context_rot_grafico.png
```

## Resultado obtido

> Esta seção deve ser preenchida após executar o experimento real.

| Turnos | Tokens | Pontuação | Qualidade |
|---:|---:|---:|---:|
| 0 | [PREENCHER] | [PREENCHER]/5 | [PREENCHER]% |
| 5 | [PREENCHER] | [PREENCHER]/5 | [PREENCHER]% |
| 10 | [PREENCHER] | [PREENCHER]/5 | [PREENCHER]% |
| 15 | [PREENCHER] | [PREENCHER]/5 | [PREENCHER]% |
| 20 | [PREENCHER] | [PREENCHER]/5 | [PREENCHER]% |

## Análise dos resultados

Após executar o experimento, esta seção deve descrever o comportamento realmente observado.

Caso exista queda de qualidade, informar:

- em qual tamanho de contexto ela apareceu;
- qual era a qualidade anterior;
- qual foi a nova qualidade;
- quais informações o modelo deixou de recuperar corretamente.

Caso não exista degradação durante a execução, isso também deve ser informado.

**Não deve ser afirmado que houve Context Rot caso os resultados reais não apresentem degradação.**

---

# 21. Requisitos atendidos

| Requisito | Status | Implementação |
|---|---|---|
| Pipeline LCEL | ✅ | `chain.py` — `prompt \| llm \| parser` |
| ChatOllama | ✅ | `gemma4:cloud` via Ollama Cloud |
| ChatPromptTemplate | ✅ | Utilizado na chain estruturada |
| PydanticOutputParser | ✅ | Integrado à pipeline LCEL |
| Pydantic v2 | ✅ | `AnaliseConsulta` com 6 campos tipados |
| Memória gerenciada | ✅ | `ConversationTokenBufferMemory` |
| ConversationChain | ✅ | Implementada em `memory_manager.py` |
| Limite da memória | ✅ | 1000 tokens |
| Memória 5+ turnos | ✅ | Teste com 6 turnos |
| System Prompt | ✅ | Persona e domínio definidos |
| XML Tagging | ✅ | Seções estruturadas em `prompts.py` |
| Context Engineering | ✅ | Controle e seleção de contexto |
| Context Rot | ✅ | Testes 0/5/10/15/20 turnos |
| Métrica de tokens | ✅ | `tiktoken` |
| Métrica de qualidade | ✅ | Pontuação de 0 a 5 e percentual |
| Gráfico comparativo | ✅ | `matplotlib` |
| Tabela de resultados | ✅ | `pandas` + CSV |
| Interface | ✅ | Gradio |
| Variáveis de ambiente | ✅ | `.env` + `python-dotenv` |
| `.env.example` | ✅ | Template sem chave real |
| Projeto modular | ✅ | Pacote `app/` |
| Execução local | ✅ | `python -m app.main` |

---

# 22. Tecnologias utilizadas

- Python
- LangChain
- LangChain Core
- LangChain Classic
- LangChain Ollama
- Ollama Cloud
- gemma4:cloud
- Pydantic v2
- Gradio
- python-dotenv
- pandas
- matplotlib
- tiktoken

---

# 23. Dependências

O arquivo `requirements.txt` contém:

```text
langchain
langchain-core
langchain-classic
langchain-ollama
pydantic
python-dotenv
gradio
pandas
matplotlib
tiktoken
```

Para instalar:

```bash
pip install -r requirements.txt
```

---

# 24. Configuração das variáveis de ambiente

O projeto utiliza um arquivo `.env` para armazenar as configurações da Ollama Cloud.

Primeiro, copie o arquivo de exemplo:

```bash
cp .env.example .env
```

Depois, edite o `.env`:

```env
OLLAMA_HOST=https://ollama.com
OLLAMA_API_KEY=SUA_CHAVE_REAL
OLLAMA_MODEL=gemma4:cloud
```

A chave real deve ser obtida na conta utilizada para acessar a Ollama Cloud.

**Nunca coloque a chave real no `.env.example`.**

**Nunca envie o `.env` na entrega.**

---

# 25. Como executar

## 1. Instale as dependências

Na raiz do projeto:

```bash
pip install -r requirements.txt
```

## 2. Configure o `.env`

Crie o arquivo `.env` baseado no `.env.example` e coloque sua `OLLAMA_API_KEY`.

## 3. Execute o projeto

```bash
python -m app.main
```

## 4. Abra a interface

Após iniciar o programa, o Gradio disponibilizará a interface local da aplicação.

Normalmente:

```text
http://localhost:7860
```

---

# 26. Executando somente a análise estruturada

Para testar a chain LCEL + Pydantic separadamente:

```bash
python -m app.chain
```

O teste envia uma consulta de exemplo e exibe os campos produzidos pela `AnaliseConsulta`.

---

# 27. Executando o experimento de Context Rot

Para executar separadamente o experimento:

```bash
python -m app.context_rot
```

O programa executará os testes com:

```text
0
5
10
15
20
```

turnos adicionais de contexto.

Ao final, serão produzidos os resultados comparativos e os arquivos de saída do experimento.

---

# 28. Interface Gradio

A interface foi desenvolvida utilizando `gr.ChatInterface`.

O Gradio recebe a mensagem do usuário e chama a função principal:

```python
responder()
```

Essa função conecta:

```text
Gradio
   ↓
análise estruturada
   ↓
validação Pydantic
   ↓
verificação do domínio
   ↓
ConversationChain
   ↓
memória
   ↓
resposta
```

Isso permite utilizar o GameGuide através de uma interface de chatbot em vez de interagir diretamente com o terminal.

---

# 29. Segurança das credenciais

A `OLLAMA_API_KEY` nunca é armazenada diretamente no código-fonte.

O `chain.py` utiliza:

```python
load_dotenv()
```

e:

```python
os.getenv(
    "OLLAMA_API_KEY"
)
```

para recuperar a chave.

O `.gitignore` contém:

```text
.env
```

evitando o versionamento acidental da credencial.

---

# 30. Limitações conhecidas

O projeto possui algumas limitações importantes:

- depende de conexão com a Ollama Cloud;
- depende de uma `OLLAMA_API_KEY` válida;
- as respostas ainda dependem do conhecimento disponível ao modelo;
- o chatbot não utiliza RAG nesta versão;
- informações muito recentes podem não estar disponíveis;
- a memória possui limite de 1000 tokens;
- informações antigas podem deixar a memória quando o limite for atingido;
- a análise estruturada depende da geração correta do modelo;
- a métrica de tokens do experimento de Context Rot é aproximada;
- a ocorrência de Context Rot pode variar entre execuções.

Essas limitações fazem parte do escopo atual do CKP01.

---

# 31. Evolução futura

O projeto foi estruturado de maneira modular para permitir evolução nos próximos checkpoints.

No futuro, o GameGuide poderá receber:

- RAG;
- base de conhecimento sobre games;
- recuperação de documentos;
- embeddings;
- busca semântica;
- agentes;
- ferramentas externas;
- novas chains;
- novos schemas Pydantic;
- memória mais avançada;
- fontes externas de informações sobre jogos.

Dessa forma, o GameGuide desenvolvido no CKP01 pode servir como base para versões mais completas do sistema.

---

# 32. Conclusão

O GameGuide demonstra a construção de um chatbot profissional especializado no domínio de games utilizando técnicas estudadas durante a disciplina de Prompt Engineering & Artificial Intelligence.

O projeto combina:

- prompt engineering;
- system prompt estruturado;
- XML tagging;
- LCEL;
- ChatOllama;
- Pydantic;
- memória conversacional;
- context engineering;
- Context Rot;
- interface Gradio.

A arquitetura modular permite separar as diferentes responsabilidades da aplicação e prepara o projeto para futuras evoluções.