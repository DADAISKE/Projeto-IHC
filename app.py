# Grupo: Rodrigo Daiske Uehara - 10440295 | Felipe Martha - 10437877

import streamlit as st
from datetime import date, timedelta

st.set_page_config(page_title="Direito Certo", page_icon="✅")

# ---------------- DADOS DO PROTÓTIPO ----------------

perguntas = [
    {"texto": "Quantas pessoas moram na sua casa, contando com você?",
     "opcoes": ["1 pessoa", "2 pessoas", "3 pessoas", "4 ou mais"]},
    {"texto": "Somando tudo, quanto a sua família ganha por mês?",
     "opcoes": ["Até R$ 700", "De R$ 701 a R$ 1.500", "De R$ 1.501 a R$ 3.000", "Mais de R$ 3.000"]},
    {"texto": "A conta de luz da sua casa está no seu nome?",
     "opcoes": ["Sim", "Não", "Não sei"]},
    {"texto": "Você já recebe algum destes benefícios?",
     "opcoes": ["Bolsa Família", "BPC (idoso ou pessoa com deficiência)", "Nenhum"]},
]

renda_da_faixa = {"Até R$ 700": 600, "De R$ 701 a R$ 1.500": 1100,
                  "De R$ 1.501 a R$ 3.000": 2250, "Mais de R$ 3.000": 3500}

beneficios = {
    "Tarifa Social de Energia": {
        "resumo": "Desconto na conta de luz.",
        "documentos": ["Documento com foto (RG ou CNH)", "CPF", "Comprovante de residência", "Última conta de luz"],
        "passos": ["Separe os documentos", "Vá ao posto de atendimento (CRAS)",
                   "Atualize seu Cadastro Único", "Aguarde: o desconto aparece na conta de luz"],
    },
    "Bolsa Família": {
        "resumo": "Dinheiro todo mês para famílias de baixa renda.",
        "documentos": ["Documento com foto (RG ou CNH)", "CPF de todos da casa", "Comprovante de residência",
                       "Certidão de nascimento das crianças"],
        "passos": ["Separe os documentos", "Vá ao posto de atendimento (CRAS)",
                   "Faça ou atualize o Cadastro Único", "Acompanhe o pagamento pelo Caixa Tem"],
    },
    "Passe Livre": {
        "resumo": "Viagem de ônibus entre estados sem pagar (pessoas com deficiência).",
        "documentos": ["Documento com foto (RG ou CNH)", "CPF", "Laudo médico", "Comprovante de renda"],
        "passos": ["Separe os documentos", "Vá ao posto de atendimento (CRAS)",
                   "Envie o pedido ao Ministério dos Transportes", "Aguarde a carteirinha pelo correio"],
    },
}

semaforo = {3: "🟢🟢🟢 Grande chance", 2: "🟡🟡⚪ Precisa de atenção", 1: "🔴⚪⚪ Pouca chance"}


# ---------------- MEMÓRIA DO APP (session_state) ----------------

if "tela" not in st.session_state:
    st.session_state.tela = "inicio"
    st.session_state.pergunta = 0
    st.session_state.respostas = {}
    st.session_state.resultado = None
    st.session_state.beneficio = None
    st.session_state.lembretes = []
    st.session_state.docs = {}
    st.session_state.fonte = "Normal"
    st.session_state.contraste = False


def ir_para(tela):
    st.session_state.tela = tela


def botao_voltar():
    st.button("⬅ Voltar ao início", on_click=ir_para, args=["inicio"])


# ---------------- VISUAL (cores e estilo iguais ao protótipo em HTML) ----------------

if st.session_state.contraste:
    cor = {"fundo": "#000000", "cartao": "#000000", "texto": "#ffffff", "suave": "#e8e8e8",
           "borda": "#ffffff", "verde": "#ffd60a", "verde_claro": "#262000", "texto_botao": "#000000"}
else:
    cor = {"fundo": "#eef3f0", "cartao": "#ffffff", "texto": "#15231c", "suave": "#4f6158",
           "borda": "#c9d6cf", "verde": "#17654a", "verde_claro": "#dcefe5", "texto_botao": "#ffffff"}

tamanhos = {"Normal": "16px", "Grande": "20px", "Muito grande": "24px"}
letra = tamanhos[st.session_state.fonte]

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&display=swap');

/* fundo e largura de celular */
.stApp {{ background: {cor["fundo"]}; }}
[data-testid="stHeader"] {{ display: none; }}
[data-testid="stMainBlockContainer"] {{ max-width: 430px; padding: 24px 16px 40px; }}

/* fonte e cor do texto */
.stApp h1, .stApp h2, .stApp h3, .stApp p, .stApp label, .stApp li, .stApp button, .stApp input {{
    font-family: "Atkinson Hyperlegible", Arial, sans-serif !important;
    color: {cor["texto"]};
}}
.stApp p, .stApp label, .stApp li, .stApp button, .stApp input {{ font-size: {letra} !important; }}
[data-testid="stCaptionContainer"] p {{ color: {cor["suave"]} !important; }}

/* cartões (containers com key que começa com "cartao") */
[class*="st-key-cartao"] {{
    background: {cor["cartao"]};
    border: 1.5px solid {cor["borda"]};
    border-radius: 14px;
    padding: 16px;
}}
.st-key-cartao_teste {{ border: 2px solid {cor["verde"]}; }}

/* botão principal verde */
button[data-testid="stBaseButton-primary"], button[data-testid="stBaseButton-primaryFormSubmit"] {{
    background: {cor["verde"]} !important;
    border: none !important;
    border-radius: 12px;
    min-height: 52px;
}}
button[data-testid="stBaseButton-primary"] p, button[data-testid="stBaseButton-primaryFormSubmit"] p {{
    color: {cor["texto_botao"]} !important;
    font-weight: 700;
}}

/* botões normais brancos com borda */
button[data-testid="stBaseButton-secondary"] {{
    background: {cor["cartao"]} !important;
    border: 1.5px solid {cor["borda"]} !important;
    border-radius: 12px;
    min-height: 46px;
}}

/* opções das perguntas em caixas, como no HTML */
[data-testid="stRadioOption"], [data-testid="stCheckbox"] label {{
    background: {cor["cartao"]};
    border: 1.5px solid {cor["borda"]};
    border-radius: 12px;
    padding: 12px 14px;
    margin-bottom: 6px;
}}
[data-testid="stRadioOption"][data-selected="true"], [data-testid="stCheckbox"] label:has(input:checked) {{
    border: 2.5px solid {cor["verde"]};
    background: {cor["verde_claro"]};
}}
[data-testid="stRadioOption"][data-selected="true"] p, [data-testid="stCheckbox"] label:has(input:checked) p {{
    font-weight: 700;
}}

/* bolinha do rádio, quadradinho do checkbox e barra de progresso em verde */
[data-testid="stRadioOption"][data-selected="true"] > div > div:first-child {{
    background: {cor["verde"]} !important;
    border-color: {cor["verde"]} !important;
}}
[data-testid="stCheckbox"] label[data-selected="true"] > div:first-of-type {{
    background-color: {cor["verde"]} !important;
    border-color: {cor["verde"]} !important;
}}

/* nas perguntas, cada opção ocupa a largura toda */
[aria-orientation="vertical"] {{ align-items: stretch !important; }}
[data-testid="stRadio"], [data-testid="stRadio"] > div, [aria-orientation="vertical"] [data-testid="stRadioOption"],
[data-testid="stElementContainer"]:has([data-testid="stCheckbox"]), [data-testid="stCheckbox"], [data-testid="stCheckbox"] label {{
    width: 100% !important;
}}

/* botões da tela inicial parecem as linhas do HTML (texto à esquerda) */
[class*="st-key-linha"] button {{ min-height: 60px; justify-content: flex-start; }}
[class*="st-key-linha"] button > div {{ justify-content: flex-start; }}
[data-testid="stProgressBarTrack"] {{ background: {cor["verde_claro"]} !important; }}
[data-testid="stProgressBarTrack"] > div {{ background: {cor["verde"]} !important; }}

/* campos de texto e data */
.stApp input {{ background: {cor["cartao"]} !important; }}
</style>
""", unsafe_allow_html=True)


# ---------------- REGRAS DO RESULTADO ----------------

def calcular_resultado():
    r = st.session_state.respostas
    pessoas = perguntas[0]["opcoes"].index(r[0]) + 1
    renda_por_pessoa = renda_da_faixa[r[1]] / pessoas
    recebe = r[3]
    renda_baixa = renda_por_pessoa <= 810 

    resultado = {}

    if renda_baixa and r[2] == "Sim":
        resultado["Tarifa Social de Energia"] = (3, "Sua renda e a conta de luz no seu nome combinam com as regras.")
    elif renda_baixa:
        resultado["Tarifa Social de Energia"] = (2, "A conta de luz precisa estar no nome de alguém da família.")
    else:
        resultado["Tarifa Social de Energia"] = (1, "Pela renda informada, a família passa do limite.")


    if "Bolsa Família" in recebe:
        resultado["Bolsa Família"] = (2, "Você já recebe. Mantenha o Cadastro Único atualizado para não perder.")
    elif renda_por_pessoa <= 218:
        resultado["Bolsa Família"] = (3, "A renda por pessoa está dentro do limite do programa.")
    elif renda_baixa:
        resultado["Bolsa Família"] = (2, "A renda está perto do limite. Vale conferir no CRAS.")
    else:
        resultado["Bolsa Família"] = (1, "Pela renda informada, a família passa do limite.")


    if "BPC (idoso ou pessoa com deficiência)" in recebe:
        resultado["Passe Livre"] = (2, "É para pessoas com deficiência. Se for o seu caso, você pode pedir.")
    else:
        resultado["Passe Livre"] = (1, "Pelas suas respostas, você não se encaixa agora.")


    st.session_state.resultado = dict(sorted(resultado.items(), key=lambda item: item[1][0], reverse=True))


# ---------------- TELAS ----------------

def tela_inicio():
    st.title("Direito Certo")
    st.write("Olá! Descubra os benefícios que são seus por direito.")


    for lembrete in st.session_state.lembretes:
        dias = (lembrete["data"] - date.today()).days
        if 0 <= dias <= lembrete["antecedencia"]:
            st.warning(f"🔔 **{lembrete['assunto']}** vence em {dias} dia(s) ({lembrete['data']:%d/%m/%Y})")

    with st.container(key="cartao_teste"):
        st.subheader("Teste Rápido")
        if st.session_state.pergunta > 0:
            st.write(f"Você parou na pergunta {st.session_state.pergunta + 1} de 4.")
            st.button("Continuar teste", type="primary", on_click=ir_para, args=["teste"], use_container_width=True)
        else:
            st.write("4 perguntas, cerca de 3 minutos.")
            st.button("Começar teste", type="primary", on_click=ir_para, args=["teste"], use_container_width=True)

    if st.session_state.resultado:
        st.button("📋  Ver meu último resultado", on_click=ir_para, args=["resultado"],
                  use_container_width=True, key="linha_resultado")
    st.button("🔔  Lembretes", on_click=ir_para, args=["lembretes"], use_container_width=True, key="linha_lembretes")
    st.button("🔠  Acessibilidade", on_click=ir_para, args=["acessibilidade"],
              use_container_width=True, key="linha_acessibilidade")


def tela_teste():
    n = st.session_state.pergunta
    p = perguntas[n]

    st.header("Teste Rápido")
    st.write(f"**Pergunta {n + 1} de 4**")
    st.progress((n + 1) / 4)

    resposta_antiga = st.session_state.respostas.get(n)

    if n < 3:
        posicao = p["opcoes"].index(resposta_antiga) if resposta_antiga else None

        resposta = st.radio(f"**{p['texto']}**", p["opcoes"], index=posicao, key=f"pergunta{n}",
                            format_func=lambda x: x.replace("$", "\\$"))
    else:
        st.write(f"**{p['texto']}**")
        st.caption("Pode marcar mais de um.")
        resposta = []
        for opcao in p["opcoes"]:
            marcado = resposta_antiga is not None and opcao in resposta_antiga
            if st.checkbox(opcao, value=marcado, key=f"op_{opcao}"):
                resposta.append(opcao)

    respondeu = bool(resposta)
    texto_botao = "Ver resultado" if n == 3 else "Próxima"

    if st.button(texto_botao, type="primary", disabled=not respondeu, use_container_width=True):
        st.session_state.respostas[n] = resposta
        if n < 3:
            st.session_state.pergunta += 1
        else:
            calcular_resultado()
            st.session_state.pergunta = 0
            st.session_state.tela = "resultado"
        st.rerun()

    col1, col2 = st.columns(2)
    if n > 0 and col1.button("⬅ Pergunta anterior"):
        st.session_state.pergunta -= 1
        st.rerun()
    if col2.button("Pausar e continuar depois"):
        if respondeu:
            st.session_state.respostas[n] = resposta
        ir_para("inicio")
        st.rerun()


def tela_resultado():
    botao_voltar()
    encontrados = sum(1 for nivel, motivo in st.session_state.resultado.values() if nivel >= 2)
    st.header(f"Encontramos {encontrados} benefício(s) para você")
    st.caption("🟢 Grande chance · 🟡 Precisa de atenção · 🔴 Pouca chance")

    for i, (nome, (nivel, motivo)) in enumerate(st.session_state.resultado.items()):
        with st.container(key=f"cartao_resultado_{i}"):
            st.subheader(nome)
            st.write(beneficios[nome]["resumo"])
            st.caption(motivo)
            st.write(f"**{semaforo[nivel]}**")
            if st.button("Ver passo a passo", key=f"ver_{nome}"):
                st.session_state.beneficio = nome
                ir_para("guia")
                st.rerun()

    st.info("Este resultado é uma estimativa. Quem decide é o órgão responsável.")
    if st.button("Refazer o teste"):
        st.session_state.respostas = {}
        st.session_state.pergunta = 0
        ir_para("teste")
        st.rerun()


def tela_guia():
    nome = st.session_state.beneficio
    b = beneficios[nome]
    prazo = date.today() + timedelta(days=30)  

    st.button("⬅ Voltar ao resultado", on_click=ir_para, args=["resultado"])
    st.header(nome)
    st.write(b["resumo"])

    st.subheader("Passo a passo")
    for i, passo in enumerate(b["passos"], start=1):
        st.write(f"**{i}.** {passo}")
    st.write(f"📅 Prazo para atualizar o cadastro: **{prazo:%d/%m/%Y}**")

    st.subheader("Documentos: marque o que já separou")
    separados = 0
    for doc in b["documentos"]:
        chave = nome + doc
        marcado = st.checkbox(doc, value=st.session_state.docs.get(chave, False))
        st.session_state.docs[chave] = marcado 
        if marcado:
            separados += 1
    st.progress(separados / len(b["documentos"]), text=f"{separados} de {len(b['documentos'])} separados")
    st.caption("Leve os originais. Não precisa de cópia.")

    st.subheader("Posto de atendimento mais próximo")
    st.info("**CRAS Centro**  \nRua das Flores, 120 – Centro (a 1,2 km)  \n"
            "Segunda a sexta, das 8h às 17h  \nSábados, domingos e feriados: fechado")

    if st.button("🔔 Criar lembrete do prazo", type="primary", use_container_width=True):
        st.session_state.lembretes.append({"assunto": f"Atualizar Cadastro Único ({nome})",
                                           "data": prazo, "antecedencia": 3})
        ir_para("lembretes")
        st.rerun()


def tela_lembretes():
    botao_voltar()
    st.header("Lembretes")

    if not st.session_state.lembretes:
        st.write("Você ainda não tem lembretes.")

    for i, lembrete in enumerate(st.session_state.lembretes):
        with st.container(key=f"cartao_lembrete_{i}"):
            st.write(f"🔔 **{lembrete['assunto']}**")
            st.caption(f"Até {lembrete['data']:%d/%m/%Y} · aviso {lembrete['antecedencia']} dia(s) antes")
            if st.button("Excluir", key=f"excluir_{i}"):
                st.session_state.lembretes.pop(i)
                st.rerun()

    st.subheader("Novo lembrete")
    with st.form("novo_lembrete", clear_on_submit=True):
        assunto = st.text_input("Sobre o quê?", placeholder="Ex.: Atualizar Cadastro Único")
        data = st.date_input("Data limite", min_value=date.today(), format="DD/MM/YYYY")
        aviso = st.radio("Avisar com antecedência", ["1 dia", "3 dias", "7 dias"], index=1, horizontal=True)
        salvar = st.form_submit_button("Salvar lembrete", type="primary", use_container_width=True)

    if salvar:
        if assunto.strip() == "":
            st.error("Escreva sobre o que é o lembrete.")
        else:
            dias = int(aviso.split()[0])
            st.session_state.lembretes.append({"assunto": assunto, "data": data, "antecedencia": dias})
            st.toast("Lembrete salvo!")
            st.rerun()


def tela_acessibilidade():
    botao_voltar()
    st.header("Acessibilidade")
    opcoes = ["Normal", "Grande", "Muito grande"]
    fonte = st.radio("Tamanho do texto", opcoes, index=opcoes.index(st.session_state.fonte), horizontal=True)
    contraste = st.toggle("Alto contraste (fundo escuro com letras claras)", value=st.session_state.contraste)
    st.write("Assim fica o texto no aplicativo.")

    if fonte != st.session_state.fonte or contraste != st.session_state.contraste:
        st.session_state.fonte = fonte
        st.session_state.contraste = contraste
        st.rerun()


# ---------------- MOSTRA A TELA ATUAL ----------------

telas = {
    "inicio": tela_inicio,
    "teste": tela_teste,
    "resultado": tela_resultado,
    "guia": tela_guia,
    "lembretes": tela_lembretes,
    "acessibilidade": tela_acessibilidade,
}
telas[st.session_state.tela]()
