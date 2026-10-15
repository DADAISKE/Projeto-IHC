# Grupo:
# Rodrigo Daiske Uehara - 10440295
# Felipe Martha - 10437877

import base64
import html
from datetime import date, timedelta

import streamlit as st

st.set_page_config(page_title="Direito Certo", page_icon="✅")

hoje = date.today()

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
        "descricao": "Desconto na conta de luz para famílias inscritas no Cadastro Único.",
        "documentos": [("Documento com foto", "RG ou CNH"), ("CPF", "Pode ser o número no RG"),
                       ("Comprovante de residência", "Dos últimos 3 meses"),
                       ("Última conta de luz", "Mostra o número da instalação")],
        "passo3": "Atualize seu Cadastro Único",
        "passo4": "O desconto aparece na conta de luz quando for aprovado",
    },
    "Bolsa Família": {
        "resumo": "Dinheiro todo mês para famílias de baixa renda.",
        "descricao": "Dinheiro todo mês para famílias de baixa renda inscritas no Cadastro Único.",
        "documentos": [("Documento com foto", "RG ou CNH"), ("CPF de todos da casa", "Pode ser o número no RG"),
                       ("Comprovante de residência", "Dos últimos 3 meses"),
                       ("Certidão de nascimento das crianças", "Ou o RG das crianças")],
        "passo3": "Faça ou atualize o Cadastro Único",
        "passo4": "O pagamento aparece no Caixa Tem quando for aprovado",
    },
    "Passe Livre": {
        "resumo": "Viagem de ônibus entre estados sem pagar (pessoas com deficiência).",
        "descricao": "Viagem de ônibus entre estados sem pagar, para pessoas com deficiência e baixa renda.",
        "documentos": [("Documento com foto", "RG ou CNH"), ("CPF", "Pode ser o número no RG"),
                       ("Laudo médico", "Feito por um médico"), ("Comprovante de renda", "Da família toda")],
        "passo3": "Envie o pedido ao Ministério dos Transportes",
        "passo4": "A carteirinha chega pelo correio quando for aprovada",
    },
}

chances = {3: "Grande chance", 2: "Precisa de atenção", 1: "Pouca chance"}
antecedencias = {1: "1 dia", 3: "3 dias", 7: "1 semana"}
tamanhos = {"A-": "15px", "A": "17px", "A+": "20px"}

# ícones desenhados em SVG (mesmo traço do protótipo)
traco = 'fill="none" stroke="var(--texto)" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"'
icone = {
    "som": f'<svg viewBox="0 0 24 24" {traco}><path d="M4 9h4l5-4v14l-5-4H4z"/>'
           '<path d="M16.5 9a4 4 0 0 1 0 6M19 6.5a7.5 7.5 0 0 1 0 11"/></svg>',
    "doc": f'<svg viewBox="0 0 24 24" {traco}><path d="M6 2.5h8l4 4v15H6z"/><path d="M9 13h6M9 17h6"/></svg>',
    "sino": f'<svg viewBox="0 0 24 24" {traco}><path d="M6 17v-6a6 6 0 0 1 12 0v6l1.5 1.5h-15z"/>'
            '<path d="M10 21.5h4"/></svg>',
    "nuvem": f'<svg viewBox="0 0 24 24" {traco}><path d="M7 18.5a4 4 0 0 1-.6-8A6 6 0 0 1 18 9.5a4.5 4.5 0 0 1-.5 9z"/>'
             '<path d="M9.5 14l2 2 3.5-3.5"/></svg>',
}

x_vazio = ('<svg viewBox="0 0 100 100" preserveAspectRatio="none">'
           '<line x1="0" y1="0" x2="100" y2="100" stroke="var(--cinza)" stroke-width=".6"/>'
           '<line x1="100" y1="0" x2="0" y2="100" stroke="var(--cinza)" stroke-width=".6"/></svg>')


# ---------------- MEMÓRIA DO APP (session_state) ----------------

padrao = {
    "tela": "inicio",
    "anterior": "inicio",
    "pergunta": 0,
    "respostas": {},
    "resultado": None,
    "beneficio": "Tarifa Social de Energia",
    "docs": {},
    "nome": "Maria",
    "fonte": "A",
    "contraste": False,
    "audio": True,
    "lembretes": [
        {"assunto": "Atualizar Cadastro Único", "data": hoje + timedelta(days=30),
         "antecedencia": 3, "audio": True, "novo": True},
        {"assunto": "Recadastramento do Bolsa Família", "data": hoje + timedelta(days=170),
         "antecedencia": 7, "audio": False, "novo": False},
    ],
    "pre_assunto": "",
    "pre_data": hoje + timedelta(days=30),
    "pre_antecedencia": 3,
    "pre_audio": True,
}
for chave, valor in padrao.items():
    st.session_state.setdefault(chave, valor)


def ir_para(tela):
    st.session_state.anterior = st.session_state.tela
    st.session_state.tela = tela


def voltar():
    st.session_state.tela = st.session_state.anterior


# ---------------- VISUAL (telas do protótipo com as cores do Direito Certo) ----------------

if st.session_state.contraste:
    cores = {"fundo": "#000000", "cartao": "#000000", "texto": "#ffffff", "suave": "#e8e8e8",
             "borda": "#ffffff", "verde": "#ffd60a", "verde-claro": "#262000", "texto-botao": "#000000",
             "linha": "#3a3a3a", "cinza": "#8a8a8a", "cinza-claro": "#262626", "pagina": "#141414"}
else:
    cores = {"fundo": "#eef3f0", "cartao": "#ffffff", "texto": "#15231c", "suave": "#4f6158",
             "borda": "#c9d6cf", "verde": "#17654a", "verde-claro": "#dcefe5", "texto-botao": "#ffffff",
             "linha": "#dbe4df", "cinza": "#9aa8a0", "cinza-claro": "#e4ebe7", "pagina": "#d6e0da"}

variaveis = "".join(f"--{nome}: {valor};" for nome, valor in cores.items())
variaveis += f"--fs: {tamanhos[st.session_state.fonte]};"

estilo = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&display=swap');
:root { VARIAVEIS }

/* página e moldura do celular */
html, body, .stApp { background: var(--pagina) !important; }
.stApp *:not([data-testid="stIconMaterial"]) { font-family: "Atkinson Hyperlegible", Arial, sans-serif; }
.stApp, .stApp p, .stApp label, .stApp span, .stApp div { color: var(--texto); }
[data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"] { display: none !important; }
[data-testid="stMain"] { padding: 0 !important; }
[data-testid="stMainBlockContainer"] {
    max-width: 398px; padding: 0 !important; margin: 28px auto;
    background: var(--fundo); border: 4px solid var(--texto); border-radius: 48px; overflow: clip;
}
[data-testid="stMainBlockContainer"] > [data-testid="stVerticalBlock"] { gap: 0; min-height: 836px; }
@media (max-width: 500px) {
    /* no celular quem rola é a própria página (o Safari do iPhone trava a rolagem de caixas internas) */
    html { height: auto !important; overflow-y: auto !important; }
    body, #root, [data-testid="stScreencast"], .stApp, [data-testid="stAppViewContainer"],
    [data-testid="stAppViewContainer"] > div, [data-testid="stMain"] {
        position: relative !important; inset: auto !important; height: auto !important;
        min-height: 100dvh; overflow: visible !important;
    }
    [data-testid="stMainBlockContainer"] { margin: 0; max-width: 100%; border: none; border-radius: 0; overflow: visible; }
    [data-testid="stMainBlockContainer"] > [data-testid="stVerticalBlock"] { min-height: 100dvh; }
    /* deixa livre o canto de baixo, onde o Streamlit Cloud põe os selos dele no celular */
    .st-key-rodape, .st-key-nav { padding-bottom: calc(46px + env(safe-area-inset-bottom)) !important; }
    .st-key-nav { padding-top: 4px !important; }
    .st-key-nav button { min-height: 50px !important; }
    .st-key-rodape { padding-top: 12px !important; gap: 0 !important; }
    .st-key-rodape [data-testid="stBaseButton-primary"] { min-height: 50px; }
    .st-key-topo { padding-top: 12px !important; min-height: 64px; }
    .st-key-corpo { padding-top: 18px !important; }
    .imagem { height: 90px !important; margin-bottom: 14px !important; }
}

/* cabeçalho, corpo e rodapé */
.st-key-topo { padding: 22px 18px 14px; background: var(--cartao); border-bottom: 2px solid var(--borda);
               min-height: 74px; flex-wrap: nowrap; }
.st-key-topo > div:has(.titulo-topo) { flex: 1 1 auto !important; min-width: 0; }
.titulo-topo { font-weight: 700; font-size: calc(var(--fs) * 1.2); line-height: 1.2; }
.st-key-voltar button { border: none !important; background: transparent !important; padding: 0 2px; min-height: 44px; }
.st-key-voltar p, .st-key-voltar span[role="img"] { font-size: 34px !important; line-height: 1; color: var(--texto); }
.st-key-corpo { padding: 22px 20px 28px; gap: 16px; }
.st-key-rodape, .st-key-nav { background: var(--cartao); border-top: 2px solid var(--borda); }
[data-testid="stLayoutWrapper"]:has(> .st-key-rodape), [data-testid="stLayoutWrapper"]:has(> .st-key-nav),
[data-testid="stMainBlockContainer"] > [data-testid="stVerticalBlock"] > .st-key-rodape {
    margin-top: auto; position: sticky; bottom: 0; z-index: 5;
}
.st-key-rodape { padding: 20px 20px 14px; gap: 6px; }
.st-key-nav { padding: 8px 4px 12px; flex-wrap: nowrap; gap: 0; }
.st-key-nav button { padding: 4px 0; min-height: 60px; }
.st-key-nav button > div > span { display: flex; flex-direction: column; align-items: center; gap: 2px; }
.st-key-nav [data-testid="stIconMaterial"] { font-size: 30px; color: var(--suave); }
.st-key-nav p { font-size: 15px !important; text-decoration: none !important; color: var(--suave) !important; }

/* botões quadrados do cabeçalho (A+ e ouvir) */
.st-key-a_mais button, .quadrado {
    width: 52px; height: 52px; min-height: 52px; padding: 0; cursor: pointer;
    display: flex; align-items: center; justify-content: center;
    border: 2px solid var(--borda) !important; border-radius: 12px; background: var(--cartao) !important;
}
[data-testid="stElementContainer"]:has(.quadrado) { flex: none !important; width: auto !important; }
.st-key-a_mais p { font-weight: 700; font-size: 20px !important; }
.quadrado img { width: 28px; height: 28px; }

/* botões */
[data-testid="stBaseButton-primary"] {
    background: var(--verde) !important; border: none !important; border-radius: 12px; min-height: 56px;
}
[data-testid="stBaseButton-primary"] p {
    color: var(--texto-botao) !important; font-weight: 700; font-size: calc(var(--fs) * 1.2) !important;
}
[data-testid="stBaseButton-primary"]:disabled { opacity: .4; }
[data-testid="stBaseButton-secondary"] {
    background: var(--cartao) !important; border: 2px solid var(--borda) !important; border-radius: 12px;
}
[data-testid="stBaseButton-secondary"] p { font-weight: 700; font-size: calc(var(--fs) * 1.1) !important; }
[data-testid="stBaseButton-tertiary"] p {
    text-decoration: underline; color: var(--verde) !important; font-size: calc(var(--fs) * 1.1) !important;
}
[class*="st-key-mini_"] button { min-height: 42px; padding: 4px 20px; border-radius: 10px;
                                 border-color: var(--verde) !important; }
[class*="st-key-mini_"] p { font-size: var(--fs) !important; color: var(--verde) !important; }
.st-key-novo_lembrete button { min-height: 62px; border-radius: 14px; }
[class*="st-key-pill_"] button { border-radius: 999px; min-height: 48px; padding: 4px 16px; }
[class*="st-key-tam_"] button { min-height: 56px; }

/* cartões e áreas clicáveis inteiras (botão invisível por cima do cartão) */
[class*="st-key-toque_"] { position: relative; }
[class*="st-key-tq_"] { position: absolute !important; inset: 0; z-index: 3; margin: 0 !important; width: 100% !important; }
[class*="st-key-tq_"] button {
    width: 100%; height: 100%; opacity: 0; cursor: pointer; border: none !important; background: transparent !important;
}
.stApp button { touch-action: manipulation; }
[class*="st-key-tq_"] button:focus-visible { opacity: 1; outline: 3px solid var(--verde); outline-offset: 3px; }
[class*="st-key-tq_"] button:focus-visible p { color: transparent !important; }

.cartao { border: 2px solid var(--borda); border-radius: 14px; padding: 18px 18px; background: var(--cartao); }
.tracejado { border-style: dashed; border-color: var(--suave); }
.st-key-cartao_teste { background: var(--cartao); border: 2px solid var(--verde); border-radius: 16px;
                       padding: 24px 24px; gap: 12px; }
[class*="st-key-lemb_"] { background: var(--cartao); border: 2px solid var(--borda); border-radius: 14px; padding: 16px 18px; }
.imagem { position: relative; height: 130px; border: 2px solid var(--borda); border-radius: 10px;
          background: var(--cinza-claro); overflow: hidden; margin-bottom: 18px; }
.imagem img { position: absolute; inset: 0; width: 100%; height: 100%; }

/* textos */
.saudacao { font-size: calc(var(--fs) * 1.8); font-weight: 700; line-height: 1.2; }
.titulo { font-size: calc(var(--fs) * 1.6); font-weight: 700; line-height: 1.25; }
.titulo-cartao { font-size: calc(var(--fs) * 1.3); font-weight: 700; line-height: 1.25; margin-bottom: 6px; }
.texto { font-size: calc(var(--fs) * 1.15); line-height: 1.45; }
.rotulo { font-weight: 700; font-size: var(--fs); margin-bottom: 10px; }
.etiqueta { font-weight: 700; font-size: calc(var(--fs) * .9); color: var(--suave) !important; margin-bottom: 4px; }

/* linhas da tela inicial */
.linha { display: flex; align-items: center; gap: 18px; background: var(--cartao); border: 2px solid var(--borda);
         border-radius: 14px; padding: 16px 20px; }
.linha .ic img { width: 28px; height: 28px; display: block; }
.linha .tx { flex: 1; display: flex; flex-direction: column; }
.linha b { font-size: calc(var(--fs) * 1.25); }
.linha small { color: var(--suave) !important; font-size: var(--fs); }
.seta { font-size: 30px; font-weight: 700; line-height: 1; color: var(--suave) !important; }

/* opções das perguntas */
.opcao { display: flex; align-items: center; gap: 18px; background: var(--cartao); border: 2px solid var(--borda);
         border-radius: 12px; padding: 18px 20px; font-size: calc(var(--fs) * 1.2); line-height: 1.35; }
.opcao.sel { border: 2.5px solid var(--verde); background: var(--verde-claro); font-weight: 700; padding: 17.5px 19.5px; }
.radio { flex: none; width: 32px; height: 32px; border: 2px solid var(--suave); border-radius: 50%; box-sizing: border-box; }
.sel .radio { border-color: var(--verde); background: radial-gradient(circle, var(--verde) 0 40%, transparent 44%); }
.caixa { flex: none; width: 30px; height: 30px; border: 2px solid var(--suave); border-radius: 7px; box-sizing: border-box;
         display: flex; align-items: center; justify-content: center; font-size: 18px; font-weight: 700; }
.sel .caixa { background: var(--verde); border-color: var(--verde); }
.sel .caixa::after { content: "✔"; color: var(--texto-botao); }
.progresso { height: 14px; background: var(--verde-claro); border-radius: 8px; overflow: hidden; margin-bottom: 18px; }
.progresso div { height: 100%; background: var(--verde); border-radius: 8px; }
.pergunta { font-size: calc(var(--fs) * 1.6); font-weight: 700; line-height: 1.3; }

/* resultado (semáforo de chances) */
.ponto { display: inline-block; width: 15px; height: 15px; border: 2.5px solid var(--verde); border-radius: 50%;
         margin-right: 3px; vertical-align: -2px; box-sizing: border-box; }
.ponto.cheio { background: var(--verde); }
.legenda { display: flex; flex-wrap: wrap; gap: 8px 18px; font-size: calc(var(--fs) * .85); }
.legenda .ponto { width: 13px; height: 13px; }
.rodape-cartao { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;
                 gap: 6px; margin-top: 12px; font-weight: 700; font-size: calc(var(--fs) * .92); }
.link { color: var(--verde) !important; }

/* botão de ouvir largo */
.ouvir-largo { display: flex; align-items: center; gap: 14px; width: 100%; padding: 13px 24px; cursor: pointer;
               border: 2px solid var(--borda); border-radius: 12px; background: var(--cartao);
               color: var(--texto); font-weight: 700; font-size: calc(var(--fs) * 1.1); }
.ouvir-largo img { width: 26px; height: 26px; }

/* guia passo a passo */
.pilula { display: inline-flex; align-items: center; gap: 8px; border: 2px solid var(--verde); border-radius: 999px;
          background: var(--verde-claro); color: var(--verde) !important; padding: 6px 16px; font-weight: 700;
          font-size: calc(var(--fs) * .9); margin-bottom: 14px; }
.pilula img { width: 20px; height: 20px; }
.st-key-passos { counter-reset: passo; gap: 0; }
[class*="st-key-passo_"] { position: relative; padding: 0 0 24px 62px; gap: 6px; counter-increment: passo; }
[class*="st-key-passo_"]::before {
    content: counter(passo); position: absolute; left: 0; top: -4px; z-index: 1;
    width: 42px; height: 42px; border: 2.5px solid var(--verde); border-radius: 50%; background: var(--cartao);
    color: var(--verde); display: flex; align-items: center; justify-content: center;
    font-weight: 700; font-size: 20px; box-sizing: border-box;
}
[data-testid="stLayoutWrapper"]:not(:last-child) > [class*="st-key-passo_"]::after {
    content: ""; position: absolute; left: 19.5px; top: 38px; bottom: -4px; border-left: 3px dashed var(--borda);
}
.passo-titulo { font-weight: 700; font-size: calc(var(--fs) * 1.18); line-height: 1.25; }

/* checklist de documentos */
.item-doc { display: flex; gap: 18px; align-items: flex-start; padding: 16px 0; border-bottom: 2px solid var(--linha); }
.item-doc .caixa { margin-top: 2px; }
.item-doc b { font-size: calc(var(--fs) * 1.2); }
.item-doc small { display: block; color: var(--suave) !important; font-size: var(--fs); margin-top: 4px; }
.item-doc.sel b { text-decoration: line-through; color: var(--suave) !important; }

/* posto mais próximo */
.posto p { margin: 4px 0 0; font-size: calc(var(--fs) * 1.05); line-height: 1.4; }
.posto ul { margin: 4px 0 8px; padding-left: 22px; }
.posto li { font-size: calc(var(--fs) * 1.05); line-height: 1.5; }

/* lembretes */
.lembrete { display: flex; gap: 16px; align-items: flex-start; }
.sino { flex: none; width: 52px; height: 52px; border: 2px solid var(--verde); background: var(--verde-claro);
        border-radius: 50%; display: flex; align-items: center; justify-content: center; }
.sino img { width: 26px; height: 26px; }
.lembrete b { font-size: calc(var(--fs) * 1.15); line-height: 1.3; }
.lembrete p { margin: 4px 0 0; font-size: var(--fs); }
.selo { display: inline-block; border: 2px solid var(--verde); background: var(--verde-claro); color: var(--verde) !important;
        border-radius: 8px; padding: 0 8px; font-size: calc(var(--fs) * .8); margin-left: 6px; vertical-align: 2px; }

/* chaves liga/desliga */
.linha-toggle { display: flex; justify-content: space-between; align-items: center; gap: 16px;
                padding: 14px 0 18px; border-bottom: 2px solid var(--linha); font-size: calc(var(--fs) * 1.15); }
.linha-toggle b { display: block; font-size: calc(var(--fs) * 1.2); }
.linha-toggle small { font-size: var(--fs); color: var(--suave) !important; }
.switch { flex: none; position: relative; width: 62px; height: 36px; border: 2px solid var(--borda);
          background: var(--cartao); border-radius: 999px; box-sizing: border-box; }
.switch::after { content: ""; position: absolute; top: 5px; left: 5px; width: 22px; height: 22px;
                 border-radius: 50%; background: var(--cinza); }
.switch.on { background: var(--verde); border-color: var(--verde); }
.switch.on::after { left: auto; right: 5px; background: var(--texto-botao); }
.previa { border: 2px dashed var(--borda); background: var(--cartao); border-radius: 12px;
          padding: 18px 22px; font-size: calc(var(--fs) * 1.15); }

/* campos de texto e data */
[data-testid="stWidgetLabel"] p { font-weight: 700; font-size: var(--fs) !important; }
[data-testid="stTextInputRootElement"], [data-testid="stDateInputField"] {
    border: 2px solid var(--borda) !important; border-radius: 12px !important; background: var(--cartao) !important;
    min-height: 56px; padding: 0 16px; display: flex; align-items: center;
}
[data-testid="stTextInputRootElement"]:focus-within, [data-testid="stDateInputField"]:focus-within {
    border-color: var(--verde) !important;
}
[data-testid="stTextInputRootElement"] input { background: transparent !important; border: none !important; padding: 0; }
.stApp input, [data-testid="stDateInputField"] [role="spinbutton"], [data-testid="stDateInputField"] [data-type="literal"] {
    font-size: calc(var(--fs) * 1.2) !important; color: var(--texto) !important;
}
[data-testid="stDateInputField"] svg { color: var(--suave); }
</style>
""".replace("VARIAVEIS", variaveis)

st.html(estilo)

# lê em voz alta (voz do navegador) o texto de qualquer botão com data-texto
st.html("""<script>
if (!window.vozDireitoCerto) {
    window.vozDireitoCerto = true;
    document.addEventListener("click", function (e) {
        var botao = e.target.closest("[data-texto]");
        if (!botao) return;
        speechSynthesis.cancel();
        var fala = new SpeechSynthesisUtterance(botao.dataset.texto);
        fala.lang = "pt-BR";
        fala.rate = 0.95;
        speechSynthesis.speak(fala);
    });
}
</script>""", unsafe_allow_javascript=True)


# ---------------- PEDAÇOS DE TELA REUTILIZADOS ----------------

def desenho(svg, classe=""):
    """O st.html não aceita <svg>, então o desenho vira uma imagem com as cores do tema atual."""
    for nome, valor in cores.items():
        svg = svg.replace(f"var(--{nome})", valor)
    svg = svg.replace("<svg", '<svg xmlns="http://www.w3.org/2000/svg"', 1)
    dados = base64.b64encode(svg.encode()).decode()
    return f'<img class="{classe}" alt="" src="data:image/svg+xml;base64,{dados}">'


def imagem_vazia():
    return f'<div class="imagem">{desenho(x_vazio)}</div>'


def esc(texto):
    return html.escape(str(texto))


def rotulo_botao(texto):
    # o "$" faria o Streamlit tentar desenhar fórmula matemática
    return str(texto).replace("$", "\\$")


def botao_ouvir(texto, rotulo=""):
    """Botão que lê o texto em voz alta usando a voz do próprio navegador."""
    if not st.session_state.audio:
        return
    classe = "ouvir-largo" if rotulo else "quadrado"
    titulo = rotulo or "Ouvir esta tela"
    st.html(f'<button class="{classe}" aria-label="{esc(titulo)}" data-texto="{esc(texto)}">'
            f'{desenho(icone["som"])}{esc(rotulo)}</button>')


def aumentar_letra():
    ordem = list(tamanhos)
    st.session_state.fonte = ordem[(ordem.index(st.session_state.fonte) + 1) % len(ordem)]


def topo(titulo, ao_voltar=None, ouvir=None, a_mais=False):
    with st.container(key="topo", horizontal=True, vertical_alignment="center", gap="small"):
        if ao_voltar:
            st.button(":material/chevron_left:", key="voltar", help="Voltar", on_click=ao_voltar)
        st.html(f'<div class="titulo-topo">{esc(titulo)}</div>', width="stretch")
        if a_mais:
            st.button("A+", key="a_mais", help="Aumentar o texto", on_click=aumentar_letra)
        if ouvir:
            botao_ouvir(ouvir)


def corpo():
    return st.container(key="corpo")


def rodape():
    return st.container(key="rodape")


def navegacao(ativa):
    st.html(f"<style>.st-key-nav_{ativa} p {{ font-weight: 700; text-decoration: underline !important; "
            f"color: var(--verde) !important; }} .st-key-nav_{ativa} [data-testid='stIconMaterial'] "
            "{ color: var(--verde) !important; }</style>")
    with st.container(key="nav", horizontal=True):
        for nome, simbolo, destino in [("Início", "home", "inicio"), ("Guias", "description", "guia"),
                                       ("Lembretes", "notifications", "lembretes"),
                                       ("Perfil", "person", "acessibilidade")]:
            st.button(nome, icon=f":material/{simbolo}:", key=f"nav_{destino}", type="tertiary",
                      width="stretch", on_click=ir_para, args=[destino])


def cartao_toque(chave, conteudo, ao_tocar, args=(), rotulo="Abrir"):
    """Cartão desenhado em HTML com um botão invisível por cima: o cartão inteiro é clicável."""
    with st.container(key=f"toque_{chave}"):
        st.html(conteudo)
        st.button(rotulo_botao(rotulo), key=f"tq_{chave}", on_click=ao_tocar, args=args)


def linha(simbolo, titulo, subtitulo):
    return (f'<div class="linha"><span class="ic">{desenho(icone[simbolo])}</span>'
            f'<span class="tx"><b>{esc(titulo)}</b><small>{esc(subtitulo)}</small></span>'
            '<span class="seta">›</span></div>')


def barra_progresso(fracao):
    return f'<div class="progresso"><div style="width:{fracao * 100:.0f}%"></div></div>'


def pontos(nivel):
    return "".join(f'<span class="ponto{" cheio" if i < nivel else ""}"></span>' for i in range(3))


def chave_toggle(chave, titulo, subtitulo=""):
    ligado = " on" if st.session_state[chave] else ""
    if subtitulo:
        texto = f"<span><b>{esc(titulo)}</b><small>{esc(subtitulo)}</small></span>"
    else:
        texto = f"<span>{esc(titulo)}</span>"
    cartao_toque(f"sw_{chave}", f'<div class="linha-toggle">{texto}<span class="switch{ligado}"></span></div>',
                 alternar, (chave,), rotulo=titulo)


def alternar(chave):
    st.session_state[chave] = not st.session_state[chave]


def contar_docs(nome):
    docs = beneficios[nome]["documentos"]
    separados = sum(1 for doc, _ in docs if st.session_state.docs.get(f"{nome}|{doc}"))
    return separados, len(docs)


def prazo_cadastro():
    return hoje + timedelta(days=30)


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
        resultado["Bolsa Família"] = (2, "Seu Cadastro Único precisa ser atualizado.")
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


# ---------------- AÇÕES DOS BOTÕES ----------------

def escolher_opcao(n, opcao):
    respostas = st.session_state.respostas
    if n < 3:
        respostas[n] = opcao
        return
    marcadas = list(respostas.get(n) or [])
    if opcao in marcadas:
        marcadas.remove(opcao)
    else:
        marcadas.append(opcao)
    respostas[n] = marcadas


def proxima_pergunta():
    if st.session_state.pergunta < 3:
        st.session_state.pergunta += 1
    else:
        calcular_resultado()
        st.session_state.pergunta = 0
        ir_para("resultado")


def voltar_pergunta():
    if st.session_state.pergunta > 0:
        st.session_state.pergunta -= 1
    else:
        ir_para("inicio")


def refazer_teste():
    st.session_state.respostas = {}
    st.session_state.pergunta = 0
    ir_para("teste")


def abrir_guia(nome):
    st.session_state.beneficio = nome
    ir_para("guia")


def voltar_do_guia():
    st.session_state.tela = "resultado" if st.session_state.resultado else "inicio"


def alternar_doc(nome, doc):
    chave = f"{nome}|{doc}"
    st.session_state.docs[chave] = not st.session_state.docs.get(chave, False)


def lembrete_do_guia(passo, prazo):
    st.session_state.pre_assunto = "Atualizar Cadastro Único" if "Cadastro Único" in passo else passo
    st.session_state.pre_data = prazo
    st.session_state.pre_antecedencia = 3
    st.session_state.pre_audio = True
    ir_para("novolembrete")


def lembrete_em_branco():
    st.session_state.pre_assunto = ""
    st.session_state.pre_data = hoje + timedelta(days=30)
    st.session_state.pre_antecedencia = 3
    st.session_state.pre_audio = True
    ir_para("novolembrete")


def escolher(chave, valor):
    st.session_state[chave] = valor


# ---------------- TELAS ----------------

def tela_inicio():
    nome = st.session_state.nome
    topo("Direito Certo", a_mais=True,
         ouvir=f"Olá, {nome}! Descubra os benefícios que são seus por direito. "
               "Toque em Começar teste para responder poucas perguntas, em cerca de 3 minutos.")

    with corpo():
        st.html(f'<div class="saudacao">Olá, {esc(nome)}!</div>'
                '<div class="texto">Descubra os benefícios que são seus por direito.</div>')

        with st.container(key="cartao_teste"):
            st.html(f'{imagem_vazia()}<div class="titulo-cartao">Teste Rápido</div>'
                    '<div class="texto">Poucas perguntas, cerca de 3 minutos.</div>')
            st.button("Começar teste", type="primary", width="stretch", key="comecar", on_click=ir_para, args=["teste"])

        cartao_toque("guias", linha("doc", "Meus guias salvos", "Funcionam sem internet"),
                     ir_para, ["guia"], "Meus guias salvos")
        cartao_toque("lembretes", linha("sino", "Lembretes", "Prazos e renovações"),
                     ir_para, ["lembretes"], "Lembretes")

    navegacao("inicio")


def tela_teste():
    n = st.session_state.pergunta
    p = perguntas[n]
    multipla = n == 3
    resposta = st.session_state.respostas.get(n)

    topo("Teste Rápido", ao_voltar=voltar_pergunta,
         ouvir=f"Pergunta {n + 1} de 4. {p['texto']} As opções são: {', '.join(p['opcoes'])}.")

    with corpo():
        extra = '<div class="texto" style="margin-top:10px">Pode marcar mais de um.</div>' if multipla else ""
        st.html(f'<div class="rotulo">Pergunta {n + 1} de 4</div>{barra_progresso((n + 1) / 4)}'
                f'{imagem_vazia()}<div class="pergunta">{esc(p["texto"])}</div>{extra}')

        for i, opcao in enumerate(p["opcoes"]):
            if multipla:
                marcada, marcador = bool(resposta) and opcao in resposta, "caixa"
            else:
                marcada, marcador = resposta == opcao, "radio"
            classe = "opcao sel" if marcada else "opcao"
            cartao_toque(f"op{n}_{i}", f'<div class="{classe}"><span class="{marcador}"></span>'
                                       f'<span>{esc(opcao)}</span></div>',
                         escolher_opcao, (n, opcao), rotulo=opcao)

    with rodape():
        st.button("Ver resultado" if multipla else "Próxima", type="primary", width="stretch",
                  key="avancar", disabled=not resposta, on_click=proxima_pergunta)
        st.button("Pausar e continuar depois", type="tertiary", width="stretch", key="pausar",
                  on_click=ir_para, args=["inicio"])


def tela_resultado():
    resultado = st.session_state.resultado
    encontrados = sum(1 for nivel, _ in resultado.values() if nivel >= 2)
    titulo = f"Encontramos {encontrados} benefício{'s' if encontrados != 1 else ''} para você"
    resumo = titulo + ". " + " ".join(f"{nome}: {chances[nivel]}. {motivo}"
                                      for nome, (nivel, motivo) in resultado.items())

    topo("Resultado", ao_voltar=lambda: ir_para("inicio"), ouvir=resumo)

    with corpo():
        st.html(f'<div class="titulo">{titulo}</div>')
        botao_ouvir(resumo, "Ouvir resumo")
        st.html('<div class="legenda">'
                f'<span>{pontos(3)} Grande chance</span><span>{pontos(2)} Precisa de atenção</span>'
                f'<span>{pontos(1)} Pouca chance</span></div>')

        for nome, (nivel, motivo) in resultado.items():
            texto = beneficios[nome]["resumo"] if nivel == 3 else motivo
            link = '<span class="link">Ver passo a passo ›</span>' if nivel >= 2 else ""
            conteudo = (f'<div class="titulo-cartao">{esc(nome)}</div><div class="texto">{esc(texto)}</div>'
                        f'<div class="rodape-cartao"><span>{pontos(nivel)} {chances[nivel]}</span>{link}</div>')
            if nivel >= 2:
                cartao_toque(f"res_{nome}", f'<div class="cartao">{conteudo}</div>', abrir_guia, (nome,),
                             rotulo=f"Ver passo a passo de {nome}")
            else:
                st.html(f'<div class="cartao tracejado">{conteudo}</div>')

        st.button("Refazer o teste", type="tertiary", width="stretch", key="refazer", on_click=refazer_teste)


def tela_guia():
    nome = st.session_state.beneficio
    b = beneficios[nome]
    prazo = prazo_cadastro()
    separados, total = contar_docs(nome)
    passos = [
        ("Separe os documentos", f"{separados} de {total} separados", "Ver lista", ir_para, ["documentos"]),
        ("Vá ao posto de atendimento", "CRAS Centro, a 1,2 km", "Ver endereço e horário", ir_para, ["posto"]),
        (b["passo3"], f"Prazo: até {prazo:%d/%m/%Y}", "Criar lembrete", lembrete_do_guia, [b["passo3"], prazo]),
        ("Aguarde a análise", b["passo4"], None, None, None),
    ]
    explicacao = b["descricao"] + " " + " ".join(f"Passo {i}: {t}. {s}." for i, (t, s, *_) in enumerate(passos, 1))

    topo(nome, ao_voltar=voltar_do_guia, ouvir=explicacao)

    with corpo():
        st.html(f'<div class="pilula">{desenho(icone["nuvem"])}Salvo para usar sem internet</div>'
                f'<div class="texto">{esc(b["descricao"])}</div>')
        botao_ouvir(explicacao, "Ouvir explicação")

        with st.container(key="passos"):
            for i, (titulo, sub, botao, acao, args) in enumerate(passos):
                with st.container(key=f"passo_{i}"):
                    st.html(f'<div class="passo-titulo">{esc(titulo)}</div><div class="texto">{esc(sub)}</div>')
                    if botao:
                        st.button(botao, key=f"mini_{i}", on_click=acao, args=args)


def tela_documentos():
    nome = st.session_state.beneficio
    docs = beneficios[nome]["documentos"]
    separados, total = contar_docs(nome)

    topo("Documentos", ao_voltar=lambda: ir_para("guia"),
         ouvir=f"Documentos para {nome}. " + ". ".join(f"{d}, {det}" for d, det in docs) +
               ". Leve os originais. Não precisa de cópia.")

    with corpo():
        st.html('<div class="titulo">Marque o que você já separou</div>'
                f'<div class="rotulo" style="margin-top:10px">{separados} de {total} separados</div>'
                f'{barra_progresso(separados / total)}')
        for i, (doc, detalhe) in enumerate(docs):
            marcado = st.session_state.docs.get(f"{nome}|{doc}", False)
            classe = "item-doc sel" if marcado else "item-doc"
            cartao_toque(f"doc_{i}", f'<div class="{classe}"><span class="caixa"></span>'
                                     f'<span><b>{esc(doc)}</b><small>{esc(detalhe)}</small></span></div>',
                         alternar_doc, (nome, doc), rotulo=doc)
        st.html('<div class="texto">Leve os originais. Não precisa de cópia.</div>')

    with rodape():
        st.button("Pronto, voltar ao guia", type="primary", width="stretch", key="pronto",
                  on_click=ir_para, args=["guia"])


def tela_posto():
    docs = beneficios[st.session_state.beneficio]["documentos"]
    itens = "".join(f"<li>{esc(doc)}{' (' + esc(det) + ')' if doc == 'Documento com foto' else ''}</li>"
                    for doc, det in docs)

    topo("Posto mais próximo", ao_voltar=voltar)

    with corpo():
        st.html('<div class="texto">Este é o posto de atendimento mais perto de você.</div>')
        st.html('<div class="cartao posto"><div class="etiqueta">Endereço</div>'
                '<div class="titulo-cartao" style="margin:0">CRAS Centro</div>'
                '<p>Rua das Flores, 120 – Centro</p><p>A 1,2 km de você</p></div>')
        st.html('<div class="cartao posto"><div class="etiqueta">Horário de funcionamento</div>'
                '<p><b>Segunda a sexta, das 8h às 17h</b></p>'
                '<p>Sábados, domingos e feriados: fechado</p></div>')
        st.html(f'<div class="cartao posto"><div class="etiqueta">Documentos para levar</div><ul>{itens}</ul>'
                '<p>Leve os originais. Não precisa de cópia.</p></div>')


def tela_lembretes():
    topo("Lembretes")

    with corpo():
        for i, lembrete in enumerate(st.session_state.lembretes):
            selo = '<span class="selo">novo</span>' if lembrete.get("novo") else ""
            aviso = f"Aviso {antecedencias[lembrete['antecedencia']]} antes"
            if lembrete.get("audio"):
                aviso += ", com áudio"
            with st.container(key=f"lemb_{i}"):
                st.html(f'<div class="lembrete"><span class="sino">{desenho(icone["sino"])}</span><div>'
                        f'<b>{esc(lembrete["assunto"])}</b>{selo}'
                        f'<p>Até {lembrete["data"]:%d/%m/%Y}</p><p>{aviso}</p></div></div>')

        nome = st.session_state.beneficio
        separados, total = contar_docs(nome)
        if separados < total:
            faltam = total - separados
            cartao_toque("pendentes",
                         f'<div class="cartao tracejado lembrete"><span class="sino">{desenho(icone["doc"])}</span><div>'
                         f'<b>Documentos pendentes</b><p>{faltam} documento(s) ainda não separado(s)</p></div></div>',
                         ir_para, ["documentos"], "Documentos pendentes")

        st.button("\\+ Novo lembrete", width="stretch", key="novo_lembrete", on_click=lembrete_em_branco)

    navegacao("lembretes")


def tela_novolembrete():
    topo("Novo lembrete", ao_voltar=voltar)

    with corpo():
        assunto = st.text_input("Sobre o quê?", value=st.session_state.pre_assunto,
                                placeholder="Ex.: Atualizar Cadastro Único")
        data = st.date_input("Data limite", value=st.session_state.pre_data, min_value=hoje, format="DD/MM/YYYY")

        st.html('<div class="rotulo" style="margin:4px 0 -6px">Avisar com antecedência</div>')
        with st.container(horizontal=True, gap="small", wrap=False):
            for dias, texto in antecedencias.items():
                tipo = "primary" if st.session_state.pre_antecedencia == dias else "secondary"
                st.button(texto, key=f"pill_{dias}", type=tipo, on_click=escolher, args=["pre_antecedencia", dias])

        chave_toggle("pre_audio", "Receber o aviso também em áudio")

    with rodape():
        if st.button("Salvar lembrete", type="primary", width="stretch", key="salvar"):
            if assunto.strip() == "":
                st.error("Escreva sobre o que é o lembrete.")
            else:
                for lembrete in st.session_state.lembretes:
                    lembrete["novo"] = False
                st.session_state.lembretes.insert(0, {
                    "assunto": assunto.strip(), "data": data, "novo": True,
                    "antecedencia": st.session_state.pre_antecedencia, "audio": st.session_state.pre_audio,
                })
                st.session_state.tela = "lembretes"
                st.rerun()


def tela_acessibilidade():
    topo("Acessibilidade", ao_voltar=lambda: ir_para("inicio"))

    with corpo():
        st.html('<div class="rotulo" style="font-size:calc(var(--fs)*1.2);margin:0">Tamanho do texto</div>')
        with st.container(horizontal=True, gap="small"):
            for i, tamanho in enumerate(tamanhos):
                tipo = "primary" if st.session_state.fonte == tamanho else "secondary"
                st.button(tamanho, key=f"tam_{i}", type=tipo, width="stretch",
                          on_click=escolher, args=["fonte", tamanho])
        st.html('<div class="previa">Assim fica o texto no aplicativo.</div>')

        chave_toggle("contraste", "Alto contraste", "Fundo escuro com letras claras")
        chave_toggle("audio", "Explicações em áudio", "Mostra o botão de ouvir nas telas")

    navegacao("acessibilidade")


# ---------------- MOSTRA A TELA ATUAL ----------------

telas = {
    "inicio": tela_inicio,
    "teste": tela_teste,
    "resultado": tela_resultado,
    "guia": tela_guia,
    "documentos": tela_documentos,
    "posto": tela_posto,
    "lembretes": tela_lembretes,
    "novolembrete": tela_novolembrete,
    "acessibilidade": tela_acessibilidade,
}
telas[st.session_state.tela]()

# ao trocar de tela, volta para o topo (no celular quem rola é a página inteira)
st.html(f"""<script>
if (window.telaAtual !== "{st.session_state.tela}") {{
    window.telaAtual = "{st.session_state.tela}";
    window.scrollTo(0, 0);
    var principal = document.querySelector('[data-testid="stMain"]');
    if (principal) principal.scrollTo(0, 0);
}}
</script>""", unsafe_allow_javascript=True)
