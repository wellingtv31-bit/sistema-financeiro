import streamlit as st
import pandas as pd
import sqlite3
import hashlib
import json
import base64
from pathlib import Path
from datetime import date, datetime, timedelta
from io import BytesIO
from urllib.parse import quote


# =====================================================
# CONFIGURAÇÃO INICIAL
# =====================================================

st.set_page_config(
    page_title="Global Software | Sistema Financeiro Premium",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed"
)

DB_PATH = "sistema_financeiro.db"
WHATSAPP_COMERCIAL = "5564992774409"
TAG_DEMO = "__DEMO_GLOBAL_SOFTWARE__"
SUPER_ADMIN_USUARIO = "Globalfinanças"
SUPER_ADMIN_SENHA = "GLSBENÇAO"
SUPER_ADMIN_NOME = "Super Admin Global Software"


# =====================================================
# IMAGENS
# =====================================================

def imagem_base64(caminho):
    arquivo = Path(caminho)
    if arquivo.exists():
        with open(arquivo, "rb") as img:
            return base64.b64encode(img.read()).decode()
    return ""


logo_base64 = imagem_base64("logo.png")
banner_base64 = imagem_base64("banner_login.png")

if not banner_base64:
    banner_base64 = logo_base64


# =====================================================
# CSS PREMIUM
# =====================================================

st.markdown("""
<style>
#MainMenu, footer, header {
    visibility: hidden;
}

.stApp {
    background:
        radial-gradient(circle at top left, rgba(223,255,107,0.10), transparent 32%),
        linear-gradient(135deg, #001d2b 0%, #002b3d 50%, #001520 100%);
    color: #ffffff;
}

.block-container {
    padding-top: 1rem;
    padding-bottom: 2.5rem;
    max-width: 1380px;
}

h1, h2, h3, h4 {
    font-weight: 950 !important;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(0,29,43,0.99), rgba(0,43,61,0.99));
    border-right: 1px solid rgba(223,255,107,0.18);
}

section[data-testid="stSidebar"] * {
    color: #f7ffe4 !important;
}

section[data-testid="stSidebar"] img {
    border-radius: 18px;
    border: 1px solid rgba(223,255,107,0.28);
    margin-bottom: 12px;
}

.gs-card-dark {
    border-radius: 28px;
    padding: 32px;
    background:
        radial-gradient(circle at top right, rgba(223,255,107,0.10), transparent 42%),
        linear-gradient(145deg, rgba(0,55,77,0.98), rgba(0,29,43,0.98));
    border: 1px solid rgba(223,255,107,0.22);
    box-shadow: 0 18px 44px rgba(0,0,0,0.25);
    color: white;
    margin-bottom: 18px;
}

.gs-card-white {
    border-radius: 28px;
    padding: 32px;
    background: #ffffff;
    border: 1px solid #e5edf2;
    box-shadow: 0 18px 55px rgba(0,43,61,0.08);
    color: #052c3d;
    margin-bottom: 18px;
}

.gs-section-white {
    background: #f7fbfd;
    border-radius: 34px;
    padding: 46px 30px;
    margin: 24px 0;
    color: #052c3d;
}

.gs-section-dark {
    background: #002b3d;
    border-radius: 34px;
    padding: 46px 30px;
    margin: 24px 0;
    color: white;
    border: 1px solid rgba(223,255,107,0.16);
}

.gs-title-big {
    font-size: 56px;
    line-height: 1.04;
    font-weight: 950;
    color: white;
    letter-spacing: -1.5px;
}

.gs-title-big span {
    color: #dfff6b;
}

.gs-subtitle {
    font-size: 20px;
    line-height: 1.62;
    color: rgba(255,255,255,0.72);
}

.gs-kicker {
    color: #dfff6b;
    letter-spacing: 5px;
    font-size: 13px;
    font-weight: 950;
    text-transform: uppercase;
    margin-bottom: 18px;
}

.gs-section-title {
    font-size: 42px;
    line-height: 1.12;
    font-weight: 950;
    color: #052c3d;
    text-align: center;
    letter-spacing: -1px;
}

.gs-section-title-dark {
    font-size: 42px;
    line-height: 1.12;
    font-weight: 950;
    color: white;
    text-align: center;
    letter-spacing: -1px;
}

.gs-muted {
    color: #6c7b86;
    font-size: 17px;
    line-height: 1.55;
}

.gs-muted-light {
    color: rgba(255,255,255,0.65);
    font-size: 17px;
    line-height: 1.55;
}

.gs-btn-fake {
    display: inline-block;
    padding: 18px 32px;
    border-radius: 999px;
    background: linear-gradient(90deg, #dfff6b, #c9ff4f);
    color: #002b3d;
    font-size: 17px;
    font-weight: 950;
    box-shadow: 0 18px 45px rgba(223,255,107,0.20);
    border: 1px solid rgba(223,255,107,0.50);
}

.gs-btn-dark {
    display: inline-block;
    padding: 18px 32px;
    border-radius: 999px;
    background: #002b3d;
    color: #dfff6b;
    font-size: 17px;
    font-weight: 950;
    box-shadow: 0 18px 45px rgba(0,43,61,0.20);
    border: 1px solid rgba(223,255,107,0.30);
}

.gs-floating {
    position: fixed;
    left: 50%;
    transform: translateX(-50%);
    bottom: 22px;
    z-index: 9999;
    background: #002b3d;
    color: #dfff6b !important;
    border: 1px solid rgba(223,255,107,0.38);
    box-shadow: 0 18px 55px rgba(0,43,61,0.36);
    padding: 15px 30px;
    border-radius: 999px;
    font-weight: 950;
    font-size: 16px;
    text-decoration: none !important;
}

.gs-up {
    position: fixed;
    left: 22px;
    bottom: 22px;
    z-index: 9998;
    width: 56px;
    height: 56px;
    border-radius: 999px;
    background: #002b3d;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.12);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 26px;
    text-decoration: none !important;
    box-shadow: 0 18px 45px rgba(0,0,0,0.18);
}

.app-header,
.menu-panel,
.commercial-panel,
.form-box {
    border-radius: 26px;
    border: 1px solid rgba(223,255,107,0.18);
    background: linear-gradient(180deg, rgba(0,43,61,0.92), rgba(0,29,43,0.96));
    box-shadow: 0 22px 60px rgba(0,0,0,0.30);
    color: #f7ffe4;
}

.app-header {
    padding: 28px 30px;
    margin-bottom: 20px;
}

.app-header-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 18px;
    flex-wrap: wrap;
}

.app-title {
    font-size: 34px;
    font-weight: 950;
    color: white;
    line-height: 1.1;
    margin-bottom: 6px;
}

.app-subtitle {
    font-size: 15px;
    color: rgba(255,255,255,0.68);
    line-height: 1.5;
}

.app-badges {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    justify-content: flex-end;
}

.app-badge {
    padding: 10px 14px;
    border-radius: 999px;
    background: rgba(223,255,107,0.08);
    border: 1px solid rgba(223,255,107,0.22);
    color: #dfff6b;
    font-size: 13px;
    font-weight: 850;
    white-space: nowrap;
}

.menu-panel {
    padding: 18px;
    margin-bottom: 22px;
}

.menu-title {
    font-size: 16px;
    font-weight: 950;
    color: #dfff6b;
    margin-bottom: 12px;
}

.commercial-panel,
.form-box {
    padding: 28px;
    margin-bottom: 22px;
}

.commercial-card,
.metric-card,
.price-card {
    border-radius: 24px;
    padding: 24px;
    background:
        radial-gradient(circle at top right, rgba(223,255,107,0.10), transparent 42%),
        linear-gradient(145deg, rgba(0,55,77,0.98), rgba(0,29,43,0.98));
    border: 1px solid rgba(223,255,107,0.20);
    box-shadow: 0 16px 38px rgba(0,0,0,0.22);
    min-height: 155px;
    color: white;
}

.commercial-card-title,
.price-title,
.metric-title {
    color: #dfff6b;
    font-size: 18px;
    font-weight: 950;
    margin-bottom: 9px;
}

.commercial-card-text,
.price-desc,
.metric-sub {
    color: rgba(255,255,255,0.68);
    font-size: 14px;
    line-height: 1.55;
}

.metric-value,
.price-value {
    color: white;
    font-size: 29px;
    font-weight: 950;
    margin-top: 6px;
}

.success-box {
    background: rgba(16,185,129,0.13);
    border-left: 6px solid #10b981;
    padding: 14px 18px;
    border-radius: 16px;
    color: #d1fae5;
}

.warning-box {
    background: rgba(245,158,11,0.14);
    border-left: 6px solid #f59e0b;
    padding: 14px 18px;
    border-radius: 16px;
    color: #fef3c7;
}

.danger-box {
    background: rgba(239,68,68,0.14);
    border-left: 6px solid #ef4444;
    padding: 14px 18px;
    border-radius: 16px;
    color: #fee2e2;
}

.login-header {
    text-align: center;
    margin-bottom: 24px;
    padding: 8px 0 4px 0;
}

.login-title {
    font-size: 46px;
    font-weight: 950;
    color: white;
    margin-bottom: 10px;
    line-height: 1.05;
}

.login-subtitle {
    font-size: 16px;
    max-width: 900px;
    margin: 0 auto;
    color: rgba(255,255,255,0.70);
    line-height: 1.6;
}

.login-info {
    margin: 18px auto 28px auto;
    max-width: 980px;
    background: rgba(223,255,107,0.08);
    border: 1px solid rgba(223,255,107,0.22);
    border-radius: 18px;
    padding: 14px 18px;
    text-align: center;
    color: #dfff6b;
    font-size: 15px;
}

.hero-box {
    min-height: 430px;
    border-radius: 28px;
    border: 1px solid rgba(223,255,107,0.22);
    box-shadow: 0 26px 70px rgba(0,0,0,0.40);
    overflow: hidden;
    position: relative;
    display: flex;
    align-items: stretch;
    justify-content: center;
    background: rgba(0,29,43,0.72);
}

.hero-inner {
    width: 100%;
    display: flex;
    align-items: end;
    justify-content: start;
    background-size: contain !important;
    background-repeat: no-repeat !important;
    background-position: center center !important;
    background-color: rgba(0,29,43,0.76);
    position: relative;
}

.hero-overlay {
    position: absolute;
    inset: 0;
    background:
        linear-gradient(180deg, rgba(0,29,43,0.02), rgba(0,29,43,0.70)),
        linear-gradient(90deg, rgba(0,29,43,0.46), rgba(0,29,43,0.04));
}

.hero-content {
    position: relative;
    z-index: 2;
    padding: 30px;
    max-width: 88%;
}

.hero-content h3 {
    font-size: 31px;
    margin-bottom: 8px;
    color: white !important;
}

.hero-content p {
    margin: 0;
    color: rgba(255,255,255,0.72) !important;
    font-size: 15px;
    line-height: 1.65;
}

.logo-box {
    min-height: 430px;
    border-radius: 28px;
    border: 1px solid rgba(223,255,107,0.22);
    background:
        radial-gradient(circle at center, rgba(223,255,107,0.09), transparent 56%),
        linear-gradient(180deg, rgba(0,43,61,0.55), rgba(0,29,43,0.90));
    box-shadow: 0 26px 70px rgba(0,0,0,0.40);
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 24px;
    overflow: hidden;
}

.logo-box img {
    width: 82%;
    max-width: 380px;
    display: block;
    margin: 0 auto;
    filter: drop-shadow(0 20px 34px rgba(0,0,0,0.34));
}

.stTextInput input,
.stNumberInput input,
.stDateInput input,
.stTextArea textarea {
    border-radius: 16px !important;
    border: 1px solid rgba(0,43,61,0.20) !important;
    background: rgba(255,255,255,0.98) !important;
    color: #052c3d !important;
}

.stSelectbox div[data-baseweb="select"] > div {
    border-radius: 16px !important;
    background: rgba(255,255,255,0.98) !important;
    border: 1px solid rgba(0,43,61,0.20) !important;
    color: #052c3d !important;
    min-height: 44px;
}

.stSelectbox span,
div[data-baseweb="select"] * {
    color: #052c3d !important;
}

div[data-baseweb="menu"],
ul[role="listbox"],
div[role="listbox"] {
    background: white !important;
    border: 1px solid #e5edf2 !important;
    border-radius: 16px !important;
    color: #052c3d !important;
}

div[data-baseweb="menu"] *,
ul[role="listbox"] *,
div[role="listbox"] * {
    background-color: white !important;
    color: #052c3d !important;
    font-weight: 800 !important;
}

.stButton > button {
    background: linear-gradient(90deg, #dfff6b, #c9ff4f);
    color: #002b3d !important;
    border: none;
    border-radius: 999px;
    padding: 0.82rem 1.2rem;
    font-weight: 950;
    box-shadow: 0 12px 28px rgba(223,255,107,0.20);
}

.stButton > button:hover {
    transform: translateY(-1px);
    background: linear-gradient(90deg, #efffa6, #dfff6b);
    color: #002b3d !important;
}

.stDownloadButton > button {
    background: linear-gradient(90deg, #dfff6b, #c9ff4f);
    color: #002b3d !important;
    border: none;
    border-radius: 999px;
    font-weight: 950;
}

div[data-testid="stDataFrame"] {
    background: rgba(255,255,255,0.94);
    border-radius: 20px;
    padding: 8px;
    border: 1px solid rgba(223,255,107,0.18);
}

div[role="radiogroup"] {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}

div[role="radiogroup"] label {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(223,255,107,0.18) !important;
    border-radius: 999px !important;
    padding: 10px 14px !important;
    margin: 0 !important;
    color: white !important;
    font-weight: 850 !important;
}

div[role="radiogroup"] label * {
    color: white !important;
    font-weight: 850 !important;
}

div[data-testid="stAlert"] {
    background: rgba(255,255,255,0.95);
    color: #052c3d;
    border-radius: 16px;
    border: 1px solid #e5edf2;
}

div[data-testid="stAlert"] * {
    color: #052c3d !important;
}

@media (max-width: 980px) {
    .gs-title-big {
        font-size: 38px;
    }

    .gs-section-title,
    .gs-section-title-dark {
        font-size: 30px;
    }

    .gs-floating {
        width: calc(100% - 120px);
        text-align: center;
        padding: 14px 16px;
        font-size: 14px;
    }

    .login-title,
    .app-title {
        font-size: 28px;
    }

    .hero-box,
    .logo-box {
        min-height: 300px;
    }
}
</style>
""", unsafe_allow_html=True)


# =====================================================
# FUNÇÕES BÁSICAS
# =====================================================

def html(codigo):
    st.markdown(codigo.strip(), unsafe_allow_html=True)


def conectar():
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def executar(sql, params=()):
    con = conectar()
    cur = con.cursor()
    cur.execute(sql, params)
    con.commit()
    con.close()


def consultar(sql, params=()):
    con = conectar()
    df = pd.read_sql_query(sql, con, params=params)
    con.close()
    return df


def hash_senha(senha):
    return hashlib.sha256(senha.encode("utf-8")).hexdigest()


def moeda(valor):
    try:
        valor = float(valor)
    except Exception:
        valor = 0
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def percentual(valor):
    try:
        valor = float(valor)
    except Exception:
        valor = 0
    return f"{valor:.1f}%".replace(".", ",")


def data_br(valor):
    try:
        return pd.to_datetime(valor).strftime("%d/%m/%Y")
    except Exception:
        return ""


def mes_atual_str():
    return date.today().strftime("%Y-%m")


def inicio_mes():
    return date.today().replace(day=1)


def status_automatico(status, vencimento):
    if status in ["Pago", "Recebido"]:
        return status

    try:
        venc = pd.to_datetime(vencimento).date()
        dias = (venc - date.today()).days
    except Exception:
        dias = 0

    if dias < 0:
        return "Vencido"
    if dias == 0:
        return "Vence hoje"
    return "Pendente"


def card(titulo, valor, subtitulo=""):
    html(f"""
<div class="metric-card">
    <div class="metric-title">{titulo}</div>
    <div class="metric-value">{valor}</div>
    <div class="metric-sub">{subtitulo}</div>
</div>
""")


def comercial_card(titulo, texto):
    html(f"""
<div class="commercial-card">
    <div class="commercial-card-title">{titulo}</div>
    <div class="commercial-card-text">{texto}</div>
</div>
""")


def preco_card(titulo, valor, texto):
    html(f"""
<div class="price-card">
    <div class="price-title">{titulo}</div>
    <div class="price-value">{valor}</div>
    <div class="price-desc">{texto}</div>
</div>
""")


def cabecalho_interno(menu_atual):
    usuario = st.session_state.usuario
    tipo_pessoa = usuario.get("tipo_pessoa", "PJ")
    texto_tipo_pessoa = "Pessoa Física PF" if tipo_pessoa == "PF" else "Pessoa Jurídica PJ"

    html(f"""
<div class="app-header">
    <div class="app-header-top">
        <div>
            <div class="app-title">Painel Global Software</div>
            <div class="app-subtitle">
                Área atual: <b>{menu_atual}</b>. Gestão completa, clara, segura e profissional.
            </div>
        </div>
        <div class="app-badges">
            <div class="app-badge">Perfil: {texto_tipo_pessoa}</div>
            <div class="app-badge">Conta: {usuario['empresa_nome']}</div>
            <div class="app-badge">Usuário: {usuario['nome']}</div>
            <div class="app-badge">Permissão: {usuario['tipo']}</div>
        </div>
    </div>
</div>
""")


# =====================================================
# BANCO DE DADOS
# =====================================================

def coluna_existe(tabela, coluna):
    con = conectar()
    cur = con.cursor()
    cur.execute(f"PRAGMA table_info({tabela})")
    colunas = [linha[1] for linha in cur.fetchall()]
    con.close()
    return coluna in colunas


def adicionar_coluna(tabela, coluna, tipo):
    if not coluna_existe(tabela, coluna):
        executar(f"ALTER TABLE {tabela} ADD COLUMN {coluna} {tipo}")


def criar_tabelas():
    con = conectar()
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS empresas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            documento TEXT,
            telefone TEXT,
            cidade TEXT,
            criado_em TEXT,
            tipo_pessoa TEXT DEFAULT 'PJ'
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            empresa_id INTEGER,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha_hash TEXT NOT NULL,
            tipo TEXT NOT NULL,
            ativo INTEGER DEFAULT 1,
            criado_em TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS lancamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            empresa_id INTEGER,
            usuario_id INTEGER,
            data TEXT,
            vencimento TEXT,
            tipo TEXT,
            categoria TEXT,
            descricao TEXT,
            cliente_fornecedor TEXT,
            valor REAL,
            forma_pagamento TEXT,
            conta TEXT,
            status TEXT,
            parcela_atual INTEGER,
            parcela_total INTEGER,
            observacao TEXT,
            criado_em TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            empresa_id INTEGER,
            nome TEXT,
            telefone TEXT,
            email TEXT,
            documento TEXT,
            tipo TEXT,
            observacao TEXT,
            criado_em TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS estoque (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            empresa_id INTEGER,
            produto TEXT,
            categoria TEXT,
            quantidade REAL,
            custo_unitario REAL,
            preco_venda REAL,
            fornecedor TEXT,
            observacao TEXT,
            criado_em TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS funcionarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            empresa_id INTEGER,
            nome TEXT,
            cargo TEXT,
            telefone TEXT,
            documento TEXT,
            data_admissao TEXT,
            salario_base REAL,
            tipo_contrato TEXT,
            status TEXT,
            observacao TEXT,
            criado_em TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS folha_pagamento (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            empresa_id INTEGER,
            funcionario_id INTEGER,
            mes_referencia TEXT,
            salario_base REAL,
            horas_extras REAL,
            valor_hora_extra REAL,
            comissao REAL,
            bonus REAL,
            premiacao REAL,
            desconto REAL,
            meta_valor REAL,
            meta_batida TEXT,
            total_bruto REAL,
            total_liquido REAL,
            status TEXT,
            data_pagamento TEXT,
            observacao TEXT,
            criado_em TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS metas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            empresa_id INTEGER,
            funcionario_id INTEGER,
            mes_referencia TEXT,
            descricao TEXT,
            meta_valor REAL,
            realizado REAL,
            premio REAL,
            status TEXT,
            criado_em TEXT
        )
    """)


    cur.execute("""
        CREATE TABLE IF NOT EXISTS planejamento_financeiro (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            empresa_id INTEGER,
            usuario_id INTEGER,
            mes_referencia TEXT,
            tipo_planejamento TEXT,
            categoria TEXT,
            descricao TEXT,
            valor_previsto REAL,
            valor_realizado REAL DEFAULT 0,
            status TEXT,
            observacao TEXT,
            criado_em TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS assinaturas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            empresa_id INTEGER UNIQUE,
            plano TEXT,
            status TEXT,
            data_inicio TEXT,
            data_vencimento TEXT,
            valor_mensal REAL DEFAULT 0,
            limite_usuarios INTEGER DEFAULT 1,
            observacao TEXT,
            criado_em TEXT,
            atualizado_em TEXT
        )
    """)

    con.commit()
    con.close()

    adicionar_coluna("estoque", "estoque_minimo", "REAL DEFAULT 0")
    adicionar_coluna("estoque", "codigo", "TEXT")
    adicionar_coluna("clientes", "limite_credito", "REAL DEFAULT 0")
    adicionar_coluna("clientes", "status_cliente", "TEXT DEFAULT 'Ativo'")
    adicionar_coluna("empresas", "tipo_pessoa", "TEXT DEFAULT 'PJ'")


def criar_admin_padrao():
    empresas = consultar("SELECT * FROM empresas")

    if empresas.empty:
        executar(
            """
            INSERT INTO empresas (nome, documento, telefone, cidade, criado_em, tipo_pessoa)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            ("Global Software", "", "", "", datetime.now().isoformat(), "PJ")
        )

    empresa = consultar("SELECT id FROM empresas ORDER BY id ASC LIMIT 1").iloc[0]["id"]

    admin = consultar("SELECT * FROM usuarios WHERE email = ?", ("admin@empresa.com",))

    if admin.empty:
        executar(
            """
            INSERT INTO usuarios
            (empresa_id, nome, email, senha_hash, tipo, ativo, criado_em)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                int(empresa),
                "Administrador",
                "admin@empresa.com",
                hash_senha("123456"),
                "Administrador",
                1,
                datetime.now().isoformat()
            )
        )

    super_admin = consultar("SELECT * FROM usuarios WHERE email = ?", (SUPER_ADMIN_USUARIO,))

    if super_admin.empty:
        executar(
            """
            INSERT INTO usuarios
            (empresa_id, nome, email, senha_hash, tipo, ativo, criado_em)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                int(empresa),
                SUPER_ADMIN_NOME,
                SUPER_ADMIN_USUARIO,
                hash_senha(SUPER_ADMIN_SENHA),
                "Administrador",
                1,
                datetime.now().isoformat()
            )
        )
    else:
        executar(
            """
            UPDATE usuarios
            SET nome = ?, senha_hash = ?, tipo = ?, ativo = 1, empresa_id = ?
            WHERE email = ?
            """,
            (
                SUPER_ADMIN_NOME,
                hash_senha(SUPER_ADMIN_SENHA),
                "Administrador",
                int(empresa),
                SUPER_ADMIN_USUARIO
            )
        )


# =====================================================
# DADOS FIXOS
# =====================================================

TIPOS_USUARIO = ["Administrador", "Gerente", "Financeiro", "Vendedor"]

TIPOS_LANCAMENTO = {
    "Receita": ["Venda", "Serviço", "Comissão", "Entrada", "Recebimento de parcela", "Outras receitas"],
    "Custo": ["Produto vendido", "Fornecedor", "Matéria-prima", "Frete de compra", "Taxa de cartão", "Comissão paga"],
    "Despesa fixa": ["Aluguel", "Internet", "Sistema", "Funcionário", "Contador", "Telefone", "MEI / Imposto fixo", "Folha de pagamento"],
    "Despesa variável": ["Energia", "Água", "Marketing", "Manutenção", "Transporte", "Alimentação", "Outras despesas"],
    "Investimento": ["Equipamento", "Curso", "Ferramenta", "Reforma", "Estoque", "Publicidade estratégica"],
    "Dívida": ["Empréstimo", "Financiamento", "Cartão de crédito", "Juros", "Parcela de dívida"],
    "Retirada do dono": ["Pró-labore", "Saque pessoal", "Distribuição de lucro"]
}

FORMAS_PAGAMENTO = ["Dinheiro", "Pix", "Cartão de débito", "Cartão de crédito", "Boleto", "Transferência", "Promissória", "Outro"]
CONTAS = ["Caixa", "Banco", "Conta digital", "Carteira", "Cartão", "Outro"]
STATUS_OPCOES = ["Pendente", "Pago", "Recebido"]

PLANOS_ASSINATURA = {
    "Gratuito": {"valor": 0.0, "limite": 1, "descricao": "Teste, controle básico e validação inicial."},
    "Básico PF": {"valor": 29.0, "limite": 1, "descricao": "Controle financeiro pessoal, gastos, dívidas, metas e relatórios."},
    "Básico PJ": {"valor": 97.0, "limite": 2, "descricao": "Financeiro, entradas, saídas, clientes e relatórios básicos."},
    "Premium PJ": {"valor": 297.0, "limite": 5, "descricao": "Financeiro completo, CRM, estoque, folha, metas e relatórios."},
    "Premium IA WhatsApp": {"valor": 497.0, "limite": 10, "descricao": "Sistema completo com automações, WhatsApp e IA financeira."},
}

STATUS_ASSINATURA = ["Teste grátis", "Ativo", "Vencido", "Bloqueado", "Cancelado"]


# =====================================================
# FUNÇÕES DE CONTEXTO
# =====================================================

def empresa_id_atual():
    return int(st.session_state.usuario["empresa_id"])


def usuario_id_atual():
    return int(st.session_state.usuario["id"])


def tipo_usuario_atual():
    return st.session_state.usuario["tipo"]


def tipo_pessoa_atual():
    return st.session_state.usuario.get("tipo_pessoa", "PJ")


def is_super_admin_global():
    usuario = st.session_state.get("usuario", {})
    login = str(usuario.get("email", "")).strip()
    tipo = str(usuario.get("tipo", ""))

    return tipo == "Administrador" and login == SUPER_ADMIN_USUARIO


def carregar_clientes_saas():
    empresas = consultar(
        """
        SELECT
            e.id,
            e.nome,
            e.documento,
            e.telefone,
            e.cidade,
            e.tipo_pessoa,
            e.criado_em,
            COALESCE(a.plano, 'Sem plano') as plano,
            COALESCE(a.status, 'Sem assinatura') as status,
            a.data_inicio,
            a.data_vencimento,
            COALESCE(a.valor_mensal, 0) as valor_mensal,
            COALESCE(a.limite_usuarios, 0) as limite_usuarios,
            COALESCE(u.total_usuarios, 0) as total_usuarios
        FROM empresas e
        LEFT JOIN assinaturas a ON a.empresa_id = e.id
        LEFT JOIN (
            SELECT empresa_id, COUNT(*) as total_usuarios
            FROM usuarios
            GROUP BY empresa_id
        ) u ON u.empresa_id = e.id
        ORDER BY e.id DESC
        """
    )

    if not empresas.empty:
        empresas["status_real"] = empresas.apply(
            lambda row: status_assinatura_real(pd.DataFrame([row.to_dict()])),
            axis=1
        )
        empresas["dias_restantes"] = empresas.apply(
            lambda row: dias_restantes_assinatura(pd.DataFrame([row.to_dict()])),
            axis=1
        )

    return empresas


# =====================================================
# ASSINATURAS E PLANOS
# =====================================================

def plano_padrao_por_perfil(tipo_pessoa):
    return "Básico PF" if tipo_pessoa == "PF" else "Básico PJ"


def garantir_assinatura_empresa(empresa_id, tipo_pessoa="PJ"):
    assinatura = consultar("SELECT * FROM assinaturas WHERE empresa_id = ?", (int(empresa_id),))
    if not assinatura.empty:
        return

    plano = plano_padrao_por_perfil(tipo_pessoa)
    dados_plano = PLANOS_ASSINATURA.get(plano, PLANOS_ASSINATURA["Gratuito"])
    hoje = date.today()
    vencimento = hoje + timedelta(days=7)
    agora = datetime.now().isoformat()

    executar(
        """
        INSERT INTO assinaturas
        (empresa_id, plano, status, data_inicio, data_vencimento, valor_mensal, limite_usuarios, observacao, criado_em, atualizado_em)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            int(empresa_id),
            plano,
            "Teste grátis",
            str(hoje),
            str(vencimento),
            float(dados_plano["valor"]),
            int(dados_plano["limite"]),
            "Assinatura criada automaticamente no primeiro acesso.",
            agora,
            agora,
        )
    )


def carregar_assinatura():
    garantir_assinatura_empresa(empresa_id_atual(), tipo_pessoa_atual())
    return consultar("SELECT * FROM assinaturas WHERE empresa_id = ?", (empresa_id_atual(),))


def status_assinatura_real(assinatura):
    if assinatura is None or assinatura.empty:
        return "Sem assinatura"

    row = assinatura.iloc[0]
    status = row.get("status", "Teste grátis") or "Teste grátis"

    if status in ["Bloqueado", "Cancelado"]:
        return status

    try:
        vencimento = pd.to_datetime(row.get("data_vencimento")).date()
        if vencimento < date.today():
            return "Vencido"
    except Exception:
        return status

    return status


def dias_restantes_assinatura(assinatura):
    if assinatura is None or assinatura.empty:
        return 0
    try:
        vencimento = pd.to_datetime(assinatura.iloc[0].get("data_vencimento")).date()
        return (vencimento - date.today()).days
    except Exception:
        return 0


def renovar_assinatura_empresa(plano, meses, status="Ativo"):
    dados_plano = PLANOS_ASSINATURA.get(plano, PLANOS_ASSINATURA["Gratuito"])
    assinatura = carregar_assinatura()
    hoje = date.today()

    data_base = hoje
    if not assinatura.empty:
        try:
            venc_atual = pd.to_datetime(assinatura.iloc[0].get("data_vencimento")).date()
            if venc_atual > hoje:
                data_base = venc_atual
        except Exception:
            data_base = hoje

    novo_vencimento = data_base + timedelta(days=30 * int(meses))

    executar(
        """
        UPDATE assinaturas
        SET plano = ?, status = ?, data_vencimento = ?, valor_mensal = ?, limite_usuarios = ?, atualizado_em = ?
        WHERE empresa_id = ?
        """,
        (
            plano,
            status,
            str(novo_vencimento),
            float(dados_plano["valor"]),
            int(dados_plano["limite"]),
            datetime.now().isoformat(),
            empresa_id_atual(),
        )
    )


def link_whatsapp_renovacao(assinatura):
    if assinatura is None or assinatura.empty:
        texto = "Olá! Quero renovar minha assinatura da Global Software."
    else:
        row = assinatura.iloc[0]
        texto = (
            "Olá! Quero renovar minha assinatura da Global Software.\n\n"
            f"Conta: {st.session_state.usuario['empresa_nome']}\n"
            f"Plano atual: {row.get('plano', '')}\n"
            f"Status: {status_assinatura_real(assinatura)}\n"
            f"Vencimento: {data_br(row.get('data_vencimento'))}\n\n"
            "Pode me enviar as opções de renovação?"
        )
    return f"https://wa.me/{WHATSAPP_COMERCIAL}?text={quote(texto)}"


# =====================================================
# DADOS DE EXEMPLO
# =====================================================

def existe_dados_exemplo():
    df = consultar(
        "SELECT COUNT(*) as total FROM lancamentos WHERE empresa_id = ? AND observacao LIKE ?",
        (empresa_id_atual(), f"%{TAG_DEMO}%")
    )
    return int(df.iloc[0]["total"]) > 0


def carregar_dados_exemplo():
    if existe_dados_exemplo():
        return False, "Os dados de exemplo já foram carregados. Para carregar novamente, limpe os dados demo primeiro."

    empresa_id = empresa_id_atual()
    usuario_id = usuario_id_atual()
    hoje = date.today()
    mes_ref = mes_atual_str()
    criado = datetime.now().isoformat()

    clientes_demo = [
        ("Mercado Boa Compra", "64990000001", "financeiro@boacompra.com", "11.111.111/0001-11", "Cliente", 15000, "Ativo"),
        ("Oficina Central", "64990000002", "contato@oficinacentral.com", "22.222.222/0001-22", "Cliente", 8000, "Ativo"),
        ("Auto Peças Goiás", "64990000003", "vendas@autopecasgoias.com", "33.333.333/0001-33", "Fornecedor", 0, "Ativo"),
        ("Clínica Vida", "64990000004", "adm@clinicavida.com", "44.444.444/0001-44", "Cliente", 12000, "Ativo"),
        ("Construtora Sol", "64990000005", "financeiro@construtorasol.com", "55.555.555/0001-55", "Cliente", 30000, "Ativo"),
        ("Loja Estilo", "64990000006", "contato@lojaestilo.com", "66.666.666/0001-66", "Cliente", 6000, "Ativo"),
        ("Restaurante Sabor", "64990000007", "adm@restaurantesabor.com", "77.777.777/0001-77", "Cliente", 9000, "Ativo"),
        ("Transportes Forte", "64990000008", "financeiro@transportesforte.com", "88.888.888/0001-88", "Cliente", 20000, "Ativo"),
    ]

    for nome, telefone, email, documento, tipo, limite, status in clientes_demo:
        executar(
            """
            INSERT INTO clientes
            (empresa_id, nome, telefone, email, documento, tipo, observacao, criado_em, limite_credito, status_cliente)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (empresa_id, nome, telefone, email, documento, tipo, f"Cliente de demonstração {TAG_DEMO}", criado, limite, status)
        )

    estoque_demo = [
        ("Sistema Financeiro Premium", "GS-001", "Software", 18, 250, 1490, "Global Software", 5),
        ("Implantação Sistema", "GS-002", "Serviço", 10, 120, 800, "Equipe Interna", 3),
        ("Treinamento Equipe", "GS-003", "Serviço", 8, 80, 500, "Equipe Interna", 3),
        ("Suporte Premium", "GS-004", "Assinatura", 25, 60, 297, "Global Software", 8),
        ("Automação WhatsApp", "GS-005", "Integração", 4, 300, 1200, "Parceiro API", 5),
        ("Relatório Personalizado", "GS-006", "Serviço", 2, 150, 650, "Global Software", 3),
    ]

    for produto, codigo, categoria, qtd, custo, venda, fornecedor, minimo in estoque_demo:
        executar(
            """
            INSERT INTO estoque
            (empresa_id, produto, categoria, quantidade, custo_unitario, preco_venda, fornecedor, observacao, criado_em, estoque_minimo, codigo)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (empresa_id, produto, categoria, qtd, custo, venda, fornecedor, f"Produto de demonstração {TAG_DEMO}", criado, minimo, codigo)
        )

    funcionarios_demo = [
        ("Ana Paula", "Financeiro", "64991000001", "000.000.001-00", hoje - timedelta(days=420), 3200, "CLT", "Ativo"),
        ("Carlos Mendes", "Vendedor", "64991000002", "000.000.002-00", hoje - timedelta(days=300), 2200, "Comissionado", "Ativo"),
        ("Juliana Rocha", "Gerente", "64991000003", "000.000.003-00", hoje - timedelta(days=520), 4500, "CLT", "Ativo"),
        ("Pedro Lima", "Suporte", "64991000004", "000.000.004-00", hoje - timedelta(days=180), 2500, "PJ", "Ativo"),
    ]

    funcionario_ids = []

    for nome, cargo, telefone, documento, admissao, salario, contrato, status in funcionarios_demo:
        executar(
            """
            INSERT INTO funcionarios
            (empresa_id, nome, cargo, telefone, documento, data_admissao, salario_base, tipo_contrato, status, observacao, criado_em)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (empresa_id, nome, cargo, telefone, documento, str(admissao), salario, contrato, status, f"Funcionário de demonstração {TAG_DEMO}", criado)
        )

        ultimo = consultar(
            "SELECT id FROM funcionarios WHERE empresa_id = ? AND nome = ? ORDER BY id DESC LIMIT 1",
            (empresa_id, nome)
        )
        funcionario_ids.append(int(ultimo.iloc[0]["id"]))

    lancamentos_demo = [
        (hoje - timedelta(days=45), hoje - timedelta(days=45), "Receita", "Venda", "Venda sistema financeiro - Mercado Boa Compra", "Mercado Boa Compra", 8900, "Pix", "Banco", "Recebido", 1, 1),
        (hoje - timedelta(days=38), hoje - timedelta(days=38), "Receita", "Serviço", "Implantação sistema - Clínica Vida", "Clínica Vida", 5200, "Transferência", "Banco", "Recebido", 1, 1),
        (hoje - timedelta(days=32), hoje - timedelta(days=32), "Receita", "Venda", "Licença premium - Construtora Sol", "Construtora Sol", 12400, "Boleto", "Banco", "Recebido", 1, 1),
        (hoje - timedelta(days=25), hoje - timedelta(days=25), "Receita", "Serviço", "Treinamento equipe - Loja Estilo", "Loja Estilo", 2500, "Pix", "Banco", "Recebido", 1, 1),
        (hoje - timedelta(days=20), hoje - timedelta(days=20), "Receita", "Venda", "Automação financeira - Restaurante Sabor", "Restaurante Sabor", 6900, "Boleto", "Banco", "Recebido", 1, 1),
        (hoje - timedelta(days=12), hoje - timedelta(days=12), "Receita", "Comissão", "Comissão implantação - Transportes Forte", "Transportes Forte", 1800, "Pix", "Banco", "Recebido", 1, 1),
        (hoje - timedelta(days=15), hoje - timedelta(days=15), "Despesa fixa", "Aluguel", "Aluguel escritório", "Imobiliária Goiás", 2800, "Boleto", "Banco", "Pago", 1, 1),
        (hoje - timedelta(days=14), hoje - timedelta(days=14), "Despesa fixa", "Internet", "Internet fibra empresarial", "Operadora", 220, "Pix", "Banco", "Pago", 1, 1),
        (hoje - timedelta(days=10), hoje - timedelta(days=10), "Despesa variável", "Marketing", "Campanha tráfego pago", "Meta Ads", 1600, "Cartão de crédito", "Cartão", "Pago", 1, 1),
        (hoje - timedelta(days=8), hoje - timedelta(days=8), "Despesa fixa", "Sistema", "Ferramentas e hospedagem", "Serviços Cloud", 690, "Cartão de crédito", "Cartão", "Pago", 1, 1),
        (hoje - timedelta(days=5), hoje - timedelta(days=5), "Custo", "Fornecedor", "Custos de implantação e API", "Parceiro API", 1350, "Pix", "Banco", "Pago", 1, 1),
        (hoje - timedelta(days=35), hoje - timedelta(days=12), "Receita", "Recebimento de parcela", "Parcela vencida - Oficina Central", "Oficina Central", 2700, "Boleto", "Banco", "Pendente", 1, 3),
        (hoje - timedelta(days=30), hoje - timedelta(days=7), "Receita", "Recebimento de parcela", "Mensalidade vencida - Loja Estilo", "Loja Estilo", 1490, "Boleto", "Banco", "Pendente", 1, 1),
        (hoje - timedelta(days=24), hoje - timedelta(days=3), "Receita", "Serviço", "Suporte premium vencido - Restaurante Sabor", "Restaurante Sabor", 297, "Boleto", "Banco", "Pendente", 1, 1),
        (hoje - timedelta(days=18), hoje - timedelta(days=1), "Receita", "Venda", "Licença pendente - Transportes Forte", "Transportes Forte", 3900, "Boleto", "Banco", "Pendente", 1, 1),
        (hoje, hoje + timedelta(days=3), "Receita", "Venda", "Nova proposta - Clínica Vida", "Clínica Vida", 7800, "Pix", "Banco", "Pendente", 1, 1),
        (hoje, hoje + timedelta(days=7), "Despesa fixa", "Contador", "Honorários contábeis", "Contabilidade Prime", 650, "Boleto", "Banco", "Pendente", 1, 1),
        (hoje, hoje + timedelta(days=10), "Despesa variável", "Manutenção", "Manutenção equipamentos", "Técnico Local", 480, "Pix", "Caixa", "Pendente", 1, 1),
    ]

    for data_lanc, venc, tipo, categoria, descricao, cliente, valor, forma, conta, status, parc_atual, parc_total in lancamentos_demo:
        executar(
            """
            INSERT INTO lancamentos
            (empresa_id, usuario_id, data, vencimento, tipo, categoria, descricao,
            cliente_fornecedor, valor, forma_pagamento, conta, status, parcela_atual,
            parcela_total, observacao, criado_em)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                empresa_id,
                usuario_id,
                str(data_lanc),
                str(venc),
                tipo,
                categoria,
                descricao,
                cliente,
                float(valor),
                forma,
                conta,
                status,
                parc_atual,
                parc_total,
                f"Lançamento de demonstração {TAG_DEMO}",
                criado
            )
        )

    folha_demo = [
        (funcionario_ids[0], 3200, 6, 25, 0, 200, 0, 150, 0, "Não", "Pago"),
        (funcionario_ids[1], 2200, 4, 22, 1800, 300, 500, 100, 15000, "Sim", "Pago"),
        (funcionario_ids[2], 4500, 2, 35, 0, 500, 800, 250, 30000, "Sim", "Pago"),
        (funcionario_ids[3], 2500, 3, 25, 0, 150, 0, 100, 0, "Não", "Pendente"),
    ]

    for func_id, salario, horas, valor_hora, comissao, bonus, premiacao, desconto, meta, meta_batida, status in folha_demo:
        bruto = salario + (horas * valor_hora) + comissao + bonus + premiacao
        liquido = bruto - desconto
        executar(
            """
            INSERT INTO folha_pagamento
            (empresa_id, funcionario_id, mes_referencia, salario_base, horas_extras, valor_hora_extra,
            comissao, bonus, premiacao, desconto, meta_valor, meta_batida, total_bruto, total_liquido,
            status, data_pagamento, observacao, criado_em)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                empresa_id,
                func_id,
                mes_ref,
                salario,
                horas,
                valor_hora,
                comissao,
                bonus,
                premiacao,
                desconto,
                meta,
                meta_batida,
                bruto,
                liquido,
                status,
                str(hoje),
                f"Folha de demonstração {TAG_DEMO}",
                criado
            )
        )

    metas_demo = [
        (funcionario_ids[1], "Meta de vendas de software", 25000, 18400, 800, "Em andamento"),
        (funcionario_ids[2], "Meta de implantação mensal", 30000, 33000, 1200, "Batida"),
        (funcionario_ids[0], "Meta de redução de inadimplência", 10000, 7200, 500, "Em andamento"),
        (funcionario_ids[3], "Meta de tickets de suporte", 100, 88, 300, "Em andamento"),
    ]

    for func_id, desc, meta, realizado, premio, status in metas_demo:
        executar(
            """
            INSERT INTO metas
            (empresa_id, funcionario_id, mes_referencia, descricao, meta_valor, realizado, premio, status, criado_em)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (empresa_id, func_id, mes_ref, f"[DEMO] {desc} {TAG_DEMO}", meta, realizado, premio, status, criado)
        )

    return True, "Dados de exemplo carregados com sucesso."


def limpar_dados_exemplo():
    empresa_id = empresa_id_atual()

    executar("DELETE FROM lancamentos WHERE empresa_id = ? AND observacao LIKE ?", (empresa_id, f"%{TAG_DEMO}%"))
    executar("DELETE FROM clientes WHERE empresa_id = ? AND observacao LIKE ?", (empresa_id, f"%{TAG_DEMO}%"))
    executar("DELETE FROM estoque WHERE empresa_id = ? AND observacao LIKE ?", (empresa_id, f"%{TAG_DEMO}%"))
    executar("DELETE FROM folha_pagamento WHERE empresa_id = ? AND observacao LIKE ?", (empresa_id, f"%{TAG_DEMO}%"))
    executar("DELETE FROM metas WHERE empresa_id = ? AND descricao LIKE ?", (empresa_id, f"%{TAG_DEMO}%"))
    executar("DELETE FROM funcionarios WHERE empresa_id = ? AND observacao LIKE ?", (empresa_id, f"%{TAG_DEMO}%"))

    return True, "Dados de exemplo removidos com sucesso."


# =====================================================
# CARREGAMENTO
# =====================================================

def carregar_lancamentos():
    df = consultar(
        """
        SELECT *
        FROM lancamentos
        WHERE empresa_id = ?
        ORDER BY vencimento ASC, data DESC, id DESC
        """,
        (empresa_id_atual(),)
    )

    if not df.empty:
        df["data"] = pd.to_datetime(df["data"])
        df["vencimento"] = pd.to_datetime(df["vencimento"])
        df["mes"] = df["data"].dt.strftime("%Y-%m")
        df["status_real"] = df.apply(lambda x: status_automatico(x["status"], x["vencimento"]), axis=1)

    return df


def carregar_clientes():
    return consultar("SELECT * FROM clientes WHERE empresa_id = ? ORDER BY nome ASC", (empresa_id_atual(),))


def carregar_estoque():
    return consultar("SELECT * FROM estoque WHERE empresa_id = ? ORDER BY produto ASC", (empresa_id_atual(),))


def carregar_funcionarios():
    return consultar("SELECT * FROM funcionarios WHERE empresa_id = ? ORDER BY nome ASC", (empresa_id_atual(),))


def carregar_folha():
    return consultar(
        """
        SELECT f.*, fun.nome as funcionario_nome, fun.cargo
        FROM folha_pagamento f
        LEFT JOIN funcionarios fun ON fun.id = f.funcionario_id
        WHERE f.empresa_id = ?
        ORDER BY f.mes_referencia DESC, fun.nome ASC
        """,
        (empresa_id_atual(),)
    )


def carregar_metas():
    return consultar(
        """
        SELECT m.*, fun.nome as funcionario_nome
        FROM metas m
        LEFT JOIN funcionarios fun ON fun.id = m.funcionario_id
        WHERE m.empresa_id = ?
        ORDER BY m.mes_referencia DESC
        """,
        (empresa_id_atual(),)
    )


# =====================================================
# CÁLCULOS
# =====================================================



def carregar_planejamento():
    return consultar(
        """
        SELECT *
        FROM planejamento_financeiro
        WHERE empresa_id = ?
        ORDER BY mes_referencia DESC, tipo_planejamento ASC, categoria ASC
        """,
        (empresa_id_atual(),)
    )


# =====================================================
# CÁLCULOS
# =====================================================

def calcular_indicadores(df):
    if df.empty:
        return {
            "receita": 0,
            "saidas": 0,
            "lucro": 0,
            "caixa": 0,
            "pagas_mes": 0,
            "receber": 0,
            "pagar": 0,
            "vencidas": 0
        }

    receita = df[df["tipo"] == "Receita"]["valor"].sum()
    saidas = df[df["tipo"] != "Receita"]["valor"].sum()
    lucro = receita - saidas
    caixa = lucro

    inicio = pd.to_datetime(inicio_mes())
    fim = pd.to_datetime(date.today())

    pagas_mes = df[
        (df["status"].isin(["Pago", "Recebido"])) &
        (df["data"] >= inicio) &
        (df["data"] <= fim)
    ]["valor"].sum()

    pendentes = df[df["status_real"].isin(["Pendente", "Vence hoje", "Vencido"])]
    receber = pendentes[pendentes["tipo"] == "Receita"]["valor"].sum()
    pagar = pendentes[pendentes["tipo"] != "Receita"]["valor"].sum()
    vencidas = pendentes[pendentes["status_real"] == "Vencido"]["valor"].sum()

    return {
        "receita": receita,
        "saidas": saidas,
        "lucro": lucro,
        "caixa": caixa,
        "pagas_mes": pagas_mes,
        "receber": receber,
        "pagar": pagar,
        "vencidas": vencidas
    }


def calcular_folha_total(salario, horas, valor_hora, comissao, bonus, premiacao, desconto):
    bruto = salario + (horas * valor_hora) + comissao + bonus + premiacao
    liquido = bruto - desconto
    return bruto, liquido


# =====================================================
# PDF SEGURO
# =====================================================

def gerar_pdf_relatorio(df, ind):
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
        from reportlab.lib.units import cm
    except Exception:
        return None

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    largura, altura = A4
    y = altura - 2 * cm

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(2 * cm, y, "Relatório Financeiro - Global Software")
    y -= 1 * cm

    pdf.setFont("Helvetica", 10)
    pdf.drawString(2 * cm, y, f"Conta: {st.session_state.usuario['empresa_nome']}")
    y -= 0.5 * cm
    tipo_pessoa = st.session_state.usuario.get("tipo_pessoa", "PJ")
    pdf.drawString(2 * cm, y, f"Perfil: {'Pessoa Física PF' if tipo_pessoa == 'PF' else 'Pessoa Jurídica PJ'}")
    y -= 0.5 * cm
    pdf.drawString(2 * cm, y, f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    y -= 1 * cm

    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(2 * cm, y, "Resumo Financeiro")
    y -= 0.8 * cm

    pdf.setFont("Helvetica", 10)

    linhas = [
        ("Receita total", moeda(ind["receita"])),
        ("Saídas totais", moeda(ind["saidas"])),
        ("Lucro / Resultado", moeda(ind["lucro"])),
        ("Caixa estimado", moeda(ind["caixa"])),
        ("Contas pagas no mês", moeda(ind["pagas_mes"])),
        ("A receber", moeda(ind["receber"])),
        ("A pagar", moeda(ind["pagar"])),
        ("Vencidas", moeda(ind["vencidas"])),
    ]

    for nome, valor in linhas:
        pdf.drawString(2 * cm, y, f"{nome}: {valor}")
        y -= 0.5 * cm

    y -= 0.5 * cm
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(2 * cm, y, "Últimos lançamentos")
    y -= 0.8 * cm

    pdf.setFont("Helvetica", 8)

    if df.empty:
        pdf.drawString(2 * cm, y, "Nenhum lançamento cadastrado.")
    else:
        ultimos = df.sort_values("data", ascending=False).head(25)

        for _, row in ultimos.iterrows():
            if y < 2 * cm:
                pdf.showPage()
                y = altura - 2 * cm
                pdf.setFont("Helvetica", 8)

            linha = (
                f"{data_br(row['data'])} | "
                f"{row['tipo']} | "
                f"{str(row['descricao'])[:45]} | "
                f"{moeda(row['valor'])} | "
                f"{row.get('status_real', row['status'])}"
            )

            pdf.drawString(2 * cm, y, linha[:115])
            y -= 0.4 * cm

    pdf.setFont("Helvetica", 8)
    pdf.drawString(2 * cm, 1 * cm, "Global Software | Sistema Financeiro Premium")

    pdf.save()
    buffer.seek(0)
    return buffer


# =====================================================
# IA AJUDA
# =====================================================

def responder_ajuda(pergunta):
    p = pergunta.lower()

    if "lançamento" in p or "entrada" in p or "saída" in p or "despesa" in p or "receita" in p:
        return "Para cadastrar uma entrada ou saída, vá na aba **Entradas e Saídas**. Escolha data, vencimento, tipo, categoria, descrição, valor, forma de pagamento e status."

    if "cliente" in p and "inadimplente" in p:
        return "Para ver clientes inadimplentes, acesse **Clientes Inadimplentes**. O sistema considera inadimplente todo cliente que possui Receita vencida."

    if "cliente" in p or "crm" in p:
        return "Para cadastrar clientes, vá em **Clientes / CRM**. Preencha nome, telefone, e-mail, documento, limite de crédito, tipo e observação."

    if "estoque" in p or "produto" in p:
        return "Para controlar estoque, acesse **Estoque**. Cadastre produto, código, categoria, quantidade, estoque mínimo, custo, preço de venda e fornecedor."

    if "funcionário" in p or "funcionario" in p:
        return "Para cadastrar funcionários, acesse **Funcionários**. Informe nome, cargo, telefone, documento, data de admissão, salário base, tipo de contrato e status."

    if "folha" in p or "pagamento" in p or "salário" in p or "salario" in p:
        return "Para montar a folha de pagamento, acesse **Folha de Pagamento**. Selecione funcionário, mês, salário, horas extras, comissão, bônus, premiação, descontos e status."

    if "meta" in p or "premiação" in p or "premiacao" in p or "bônus" in p or "bonus" in p:
        return "Para cadastrar metas e premiações, vá em **Metas e Premiações**. Selecione funcionário, informe meta, realizado, prêmio e status."

    if "relatório" in p or "relatorio" in p or "pdf" in p:
        return "Para gerar relatório, acesse **Relatórios**. Você pode baixar PDF financeiro e arquivos CSV."

    if "planejamento" in p or "orçamento" in p or "orcamento" in p or "previsto" in p:
        return "Para planejar o mês, acesse **Planejamento Financeiro**. Cadastre valores previstos, valores realizados, metas, dívidas, investimentos e compare o planejado com o realizado."

    if "super admin" in p or "saas" in p or "clientes do sistema" in p or "clientes global" in p:
        return "O **Super Admin Global** é a área do administrador principal da Global Software. Lá você vê todos os clientes PF/PJ, planos vendidos, status, vencimentos, usuários, receita mensal prevista e pode renovar, bloquear ou liberar contas."

    if "assinatura" in p or "mensalidade" in p or "plano" in p or "renovar" in p or "vencimento" in p:
        return "Para controlar assinatura e mensalidade, acesse **Assinaturas / Planos**. Lá você vê plano atual, status, vencimento, dias restantes, limite de usuários e pode gerar link de renovação pelo WhatsApp."

    if "whatsapp" in p or "cobrança" in p or "cobranca" in p:
        return "Para gerar mensagem de WhatsApp, vá em **Pix e WhatsApp**. Digite telefone, nome, valor, vencimento e gere o link pronto."

    if "dashboard" in p or "painel" in p:
        return "O **Dashboard** mostra receita, saídas, lucro, caixa, contas pagas no mês, clientes inadimplentes, estoque, folha de pagamento, contas a receber e contas vencidas."

    return "Posso te ajudar com lançamentos, clientes, inadimplentes, estoque, funcionários, folha, metas, planejamento, assinatura, relatórios, WhatsApp e dashboard."


# =====================================================
# TELA PÚBLICA
# =====================================================

def tela_publica_comercial():
    html('<a class="gs-up" href="#topo">↑</a>')
    html('<a class="gs-floating" href="#demo">Agendar Demonstração →</a>')

    logo_html = "GS"
    if logo_base64:
        logo_html = f'<img src="data:image/png;base64,{logo_base64}" style="width:100%;height:100%;object-fit:contain;padding:5px;">'

    html(f"""
<div id="topo" class="gs-card-dark">
    <div style="display:flex;align-items:center;justify-content:space-between;gap:18px;flex-wrap:wrap;">
        <div style="display:flex;align-items:center;gap:14px;">
            <div style="width:58px;height:58px;border-radius:18px;background:rgba(255,255,255,0.06);border:1px solid rgba(223,255,107,0.25);display:flex;align-items:center;justify-content:center;overflow:hidden;color:#dfff6b;font-weight:950;font-size:18px;">
                {logo_html}
            </div>
            <div>
                <div style="color:white;font-size:24px;letter-spacing:4px;font-weight:850;">GLOBAL SOFTWARE</div>
                <div style="color:rgba(255,255,255,0.60);font-size:13px;margin-top:2px;">Sistema financeiro completo para empresas e pessoas físicas</div>
            </div>
        </div>
        <div style="color:#dfff6b;border:1px solid rgba(223,255,107,0.32);background:rgba(223,255,107,0.08);padding:10px 16px;border-radius:999px;font-weight:900;font-size:13px;">
            PJ • PF • Financeiro • IA WhatsApp
        </div>
    </div>
</div>
""")

    col_hero, col_mock = st.columns([1.05, 0.95], gap="large")

    with col_hero:
        html("""
<div class="gs-card-dark" style="min-height:520px;display:flex;align-items:center;">
    <div>
        <div class="gs-kicker">PLATAFORMA DE GESTÃO FINANCEIRA</div>
        <div class="gs-title-big">
            Controle financeiro para <span>PJ e PF</span>.
        </div>
        <br>
        <div class="gs-subtitle">
            Pessoa Jurídica controla empresa, clientes, estoque, funcionários, folha, metas e relatórios.
            Pessoa Física controla entradas, gastos pessoais, dívidas, contas e metas.
        </div>
        <br><br>
        <span class="gs-btn-fake">Agendar Demonstração →</span>
        &nbsp;&nbsp;
        <span class="gs-btn-dark">Acessar sistema</span>
    </div>
</div>
""")

    with col_mock:
        st.markdown("### 📊 Demonstração do painel")

        m1, m2 = st.columns(2)

        with m1:
            st.metric("Receita do mês", "R$ 84.750")
            st.metric("Inadimplentes", "12")

        with m2:
            st.metric("Lucro previsto", "R$ 26.400")
            st.metric("Folha do mês", "R$ 18.900")

        dados_demo = pd.DataFrame({
            "Mês": ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun"],
            "Receita": [18000, 25000, 31000, 46000, 62000, 84750],
            "Despesas": [9000, 12000, 18000, 22000, 31000, 38900],
        })

        st.line_chart(dados_demo.set_index("Mês"))
        st.info("Painel demonstrativo com indicadores financeiros para PJ e PF.")

    col_acesso, col_vazio = st.columns([1, 1])

    with col_acesso:
        if st.button("Acessar área do sistema", use_container_width=True, key="btn_login_landing"):
            st.session_state.tela_login_ativa = True
            st.rerun()

    html("""
<div class="gs-section-dark">
    <div style="text-align:center;font-size:42px;line-height:1.18;font-weight:950;color:white;">
        A plataforma para empresas e pessoas que querem sair do <span style="color:#dfff6b;">improviso</span>.
    </div>
</div>
""")

    html("""
<div class="gs-section-white">
    <div style="text-align:center;color:#7a8d98;letter-spacing:7px;font-size:14px;text-transform:uppercase;font-weight:800;margin-bottom:18px;">
        FUNCIONALIDADES
    </div>
    <div class="gs-section-title">
        Tudo o que seu financeiro precisa, em uma única plataforma.
    </div>
</div>
""")

    f1, f2, f3 = st.columns(3)

    with f1:
        html("""
<div class="gs-card-white">
    <div style="font-size:42px;color:#002b3d;">PJ</div>
    <h3 style="color:#052c3d;">Pessoa Jurídica</h3>
    <p class="gs-muted">Empresas controlam contas, clientes, estoque, funcionários, folha de pagamento, metas e relatórios.</p>
</div>
""")

    with f2:
        html("""
<div class="gs-card-white">
    <div style="font-size:42px;color:#002b3d;">PF</div>
    <h3 style="color:#052c3d;">Pessoa Física</h3>
    <p class="gs-muted">Pessoas controlam salário, gastos pessoais, cartão, dívidas, metas e organização financeira.</p>
</div>
""")

    with f3:
        html("""
<div class="gs-card-white">
    <div style="font-size:42px;color:#002b3d;">🤖</div>
    <h3 style="color:#052c3d;">IA WhatsApp</h3>
    <p class="gs-muted">Próxima etapa: registrar receitas e despesas por mensagem no WhatsApp, separado em PF e PJ.</p>
</div>
""")

    html("""
<div id="demo" class="gs-section-dark">
    <div class="gs-section-title-dark">
        Pronto para profissionalizar o financeiro?
    </div>
    <p class="gs-muted-light" style="text-align:center;font-size:20px;">
        Agende uma demonstração gratuita e veja a Global Software na prática.
    </p>
</div>
""")

    html('<div class="gs-card-white">')
    st.markdown("### Agendar demonstração")

    col1, col2 = st.columns(2)

    with col1:
        nome = st.text_input("Seu nome", placeholder="Ex: Fabrício Santos", key="demo_nome")
        empresa = st.text_input("Nome da empresa ou pessoa", placeholder="Ex: Global Software", key="demo_empresa")
        segmento = st.selectbox(
            "Perfil",
            ["Selecionar", "Pessoa Jurídica PJ", "Pessoa Física PF", "Comércio", "Serviços", "Veículos", "Oficina", "Igreja / Instituição", "Indústria", "Outro"],
            key="demo_segmento"
        )

    with col2:
        telefone = st.text_input("Telefone / WhatsApp do cliente", placeholder="Ex: 64999999999", key="demo_telefone")
        email = st.text_input("E-mail", placeholder="contato@empresa.com", key="demo_email")
        necessidade = st.selectbox(
            "Principal necessidade",
            ["Controle financeiro", "PF - gastos pessoais", "PJ - empresa completa", "Estoque", "Clientes inadimplentes", "Folha de pagamento", "Relatórios", "Sistema completo"],
            key="demo_necessidade"
        )

    if st.button("Agendar Demonstração pelo WhatsApp", use_container_width=True, key="btn_agendar_demo_final"):
        texto = (
            f"Olá! Quero agendar uma demonstração da Global Software.\n\n"
            f"Nome: {nome}\n"
            f"Empresa/Pessoa: {empresa}\n"
            f"Perfil: {segmento}\n"
            f"WhatsApp do cliente: {telefone}\n"
            f"E-mail: {email}\n"
            f"Necessidade principal: {necessidade}\n\n"
            f"Quero ver como o sistema pode ajudar."
        )
        link = f"https://wa.me/{WHATSAPP_COMERCIAL}?text={quote(texto)}"
        st.markdown(f"[Abrir WhatsApp para agendar demonstração]({link})")

    html("</div>")


# =====================================================
# LOGIN
# =====================================================

def tela_login():
    html("""
<div class="login-header">
    <div class="login-title">💼 Sistema Financeiro Premium</div>
    <div class="login-subtitle">
        Gestão completa para Pessoa Jurídica PJ e Pessoa Física PF.
    </div>
    <div class="login-info">
        <b>Login cliente PJ:</b> admin@empresa.com &nbsp;&nbsp;|&nbsp;&nbsp; <b>Senha:</b> 123456<br><b>Super Admin Global:</b> Globalfinanças &nbsp;&nbsp;|&nbsp;&nbsp; <b>Senha:</b> GLSBENÇAO
    </div>
</div>
""")

    col_voltar1, col_voltar2, col_voltar3 = st.columns([1, 1, 1])

    with col_voltar2:
        if st.button("Voltar para apresentação pública", use_container_width=True, key="btn_voltar_publica"):
            st.session_state.tela_login_ativa = False
            st.rerun()

    col1, col2 = st.columns([1.15, 0.85], gap="large")

    with col1:
        hero_bg = ""
        if banner_base64:
            hero_bg = f"background-image: url('data:image/png;base64,{banner_base64}');"

        html(f"""
<div class="hero-box">
    <div class="hero-inner" style="{hero_bg}">
        <div class="hero-overlay"></div>
        <div class="hero-content">
            <h3>Gestão inteligente para PJ e PF</h3>
            <p>
                Pessoa Jurídica controla empresa, clientes, estoque, funcionários, folha e metas.
                Pessoa Física controla salário, gastos, contas pessoais, dívidas e metas.
            </p>
        </div>
    </div>
</div>
""")

    with col2:
        if logo_base64:
            html(f"""
<div class="logo-box">
    <img src="data:image/png;base64,{logo_base64}">
</div>
""")
        else:
            html("""
<div class="logo-box">
    <div style="text-align:center;">
        <h3>GLOBAL SOFTWARE</h3>
        <p>Sua logo aparecerá aqui quando o arquivo <b>logo.png</b> estiver na pasta do projeto.</p>
    </div>
</div>
""")

    html('<div class="form-box">')

    aba1, aba2, aba3 = st.tabs(["Entrar", "Criar empresa PJ", "Criar pessoa física PF"])

    with aba1:
        st.markdown("### Acessar sistema")

        col_a, col_b = st.columns(2)

        with col_a:
            email = st.text_input("E-mail ou usuário", key="login_email")

        with col_b:
            senha = st.text_input("Senha", type="password", key="login_senha")

        if st.button("Entrar", use_container_width=True, key="btn_login"):
            usuario = consultar(
                """
                SELECT u.*, e.nome as empresa_nome, e.tipo_pessoa as tipo_pessoa
                FROM usuarios u
                LEFT JOIN empresas e ON e.id = u.empresa_id
                WHERE u.email = ? AND u.senha_hash = ? AND u.ativo = 1
                """,
                (email, hash_senha(senha))
            )

            if usuario.empty:
                st.error("E-mail ou senha inválidos.")
            else:
                st.session_state.usuario = usuario.iloc[0].to_dict()
                st.session_state.tela_login_ativa = False
                st.rerun()

    with aba2:
        st.markdown("### Criar empresa PJ — Pessoa Jurídica")
        st.info("Use esta opção para empresas que vão controlar financeiro empresarial, clientes, estoque, funcionários, folha, metas e relatórios.")

        col1, col2 = st.columns(2)

        with col1:
            nome_empresa = st.text_input("Nome da empresa", key="cad_pj_nome_empresa")
            documento = st.text_input("CNPJ", key="cad_pj_documento")
            telefone = st.text_input("Telefone / WhatsApp da empresa", key="cad_pj_telefone")
            cidade = st.text_input("Cidade", key="cad_pj_cidade")

        with col2:
            nome_usuario = st.text_input("Nome do administrador", key="cad_pj_nome_usuario")
            email_usuario = st.text_input("E-mail do administrador", key="cad_pj_email_usuario")
            senha_usuario = st.text_input("Senha", type="password", key="cad_pj_senha_usuario")

        if st.button("Criar empresa PJ", use_container_width=True, key="btn_criar_empresa_pj"):
            if not nome_empresa or not nome_usuario or not email_usuario or not senha_usuario:
                st.warning("Preencha todos os campos obrigatórios.")
            else:
                try:
                    executar(
                        """
                        INSERT INTO empresas (nome, documento, telefone, cidade, criado_em, tipo_pessoa)
                        VALUES (?, ?, ?, ?, ?, ?)
                        """,
                        (nome_empresa, documento, telefone, cidade, datetime.now().isoformat(), "PJ")
                    )

                    empresa_id = consultar(
                        "SELECT id FROM empresas WHERE nome = ? ORDER BY id DESC LIMIT 1",
                        (nome_empresa,)
                    ).iloc[0]["id"]

                    executar(
                        """
                        INSERT INTO usuarios
                        (empresa_id, nome, email, senha_hash, tipo, ativo, criado_em)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            int(empresa_id),
                            nome_usuario,
                            email_usuario,
                            hash_senha(senha_usuario),
                            "Administrador",
                            1,
                            datetime.now().isoformat()
                        )
                    )

                    st.success("Empresa PJ criada com sucesso. Agora faça login.")
                except Exception as e:
                    st.error(f"Erro ao criar empresa PJ: {e}")

    with aba3:
        st.markdown("### Criar pessoa física PF")
        st.info("Use esta opção para controle financeiro pessoal: salário, gastos, cartão, contas da casa, dívidas, metas pessoais e futuramente IA no WhatsApp PF.")

        col1, col2 = st.columns(2)

        with col1:
            nome_pessoa = st.text_input("Nome completo", key="cad_pf_nome")
            cpf = st.text_input("CPF", key="cad_pf_cpf")
            telefone_pf = st.text_input("Telefone / WhatsApp", key="cad_pf_telefone")
            cidade_pf = st.text_input("Cidade", key="cad_pf_cidade")

        with col2:
            email_pf = st.text_input("E-mail de acesso", key="cad_pf_email")
            senha_pf = st.text_input("Senha", type="password", key="cad_pf_senha")
            confirmar_senha_pf = st.text_input("Confirmar senha", type="password", key="cad_pf_confirmar_senha")

        if st.button("Criar conta PF", use_container_width=True, key="btn_criar_pf"):
            if not nome_pessoa or not email_pf or not senha_pf:
                st.warning("Preencha nome, e-mail e senha.")
            elif senha_pf != confirmar_senha_pf:
                st.error("As senhas não conferem.")
            else:
                try:
                    nome_perfil_pf = f"PF - {nome_pessoa}"

                    executar(
                        """
                        INSERT INTO empresas (nome, documento, telefone, cidade, criado_em, tipo_pessoa)
                        VALUES (?, ?, ?, ?, ?, ?)
                        """,
                        (nome_perfil_pf, cpf, telefone_pf, cidade_pf, datetime.now().isoformat(), "PF")
                    )

                    empresa_id = consultar(
                        "SELECT id FROM empresas WHERE nome = ? ORDER BY id DESC LIMIT 1",
                        (nome_perfil_pf,)
                    ).iloc[0]["id"]

                    executar(
                        """
                        INSERT INTO usuarios
                        (empresa_id, nome, email, senha_hash, tipo, ativo, criado_em)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            int(empresa_id),
                            nome_pessoa,
                            email_pf,
                            hash_senha(senha_pf),
                            "Administrador",
                            1,
                            datetime.now().isoformat()
                        )
                    )

                    st.success("Conta PF criada com sucesso. Agora faça login.")
                except Exception as e:
                    st.error(f"Erro ao criar conta PF: {e}")

    html("</div>")


# =====================================================
# PERMISSÕES
# =====================================================

def menus_por_tipo_usuario():
    tipo = tipo_usuario_atual()

    menus_administrador = [
        "Dashboard",
        "Entradas e Saídas",
        "Contas Pagas no Mês",
        "Clientes / CRM",
        "Clientes Inadimplentes",
        "Estoque",
        "Funcionários",
        "Folha de Pagamento",
        "Metas e Premiações",
        "Parcelas",
        "Planejamento Financeiro",
        "Assinaturas / Planos",
        "Pix e WhatsApp",
        "Relatórios",
        "IA Financeira",
        "Ajuda / Tutorial",
        "Apresentação Comercial",
        "Usuários",
        "Configurações"
    ]

    permissoes = {
        "Administrador": menus_administrador,
        "Gerente": [
            "Dashboard", "Entradas e Saídas", "Contas Pagas no Mês", "Clientes / CRM",
            "Clientes Inadimplentes", "Estoque", "Funcionários", "Folha de Pagamento",
            "Metas e Premiações", "Parcelas", "Planejamento Financeiro", "Assinaturas / Planos", "Pix e WhatsApp", "Relatórios",
            "IA Financeira", "Ajuda / Tutorial", "Configurações"
        ],
        "Financeiro": [
            "Dashboard", "Entradas e Saídas", "Contas Pagas no Mês", "Clientes Inadimplentes",
            "Folha de Pagamento", "Parcelas", "Planejamento Financeiro", "Assinaturas / Planos", "Pix e WhatsApp", "Relatórios",
            "IA Financeira", "Ajuda / Tutorial"
        ],
        "Vendedor": [
            "Dashboard", "Clientes / CRM", "Clientes Inadimplentes", "Pix e WhatsApp", "Ajuda / Tutorial"
        ]
    }

    menus = permissoes.get(tipo, ["Dashboard"])

    if is_super_admin_global() and "Super Admin Global" not in menus:
        menus = ["Super Admin Global"] + menus

    return menus


# =====================================================
# APRESENTAÇÃO COMERCIAL ADMIN
# =====================================================

def tela_apresentacao_comercial():
    if tipo_usuario_atual() != "Administrador":
        st.warning("Esta área é exclusiva para administrador.")
        return

    html("""
<div class="commercial-panel">
    <h1 style="color:white;">🚀 Apresentação Comercial Global Software</h1>
    <p style="font-size:18px;color:rgba(255,255,255,0.70);line-height:1.6;">
    Use esta página como roteiro para vender o sistema. Mostre que a Global Software atende PJ e PF.
    </p>
</div>
""")

    c1, c2, c3 = st.columns(3)

    with c1:
        comercial_card("PJ", "Empresas controlam financeiro, clientes, inadimplência, estoque, funcionários, folha, metas e relatórios.")

    with c2:
        comercial_card("PF", "Pessoas físicas controlam salário, gastos pessoais, contas, dívidas, cartão e metas.")

    with c3:
        comercial_card("WhatsApp IA", "Próxima etapa: registrar lançamentos pelo WhatsApp, separado por PF e PJ.")

    html('<div class="commercial-panel">')
    st.markdown("## Roteiro de venda")

    roteiro = """
Olá, tudo bem? Deixa eu te fazer uma pergunta: você sabe exatamente quanto entra, quanto sai, quanto sobra e onde seu dinheiro está indo?

Para empresas, a Global Software controla financeiro, clientes, inadimplência, estoque, funcionários, folha, metas e relatórios.

Para pessoa física, ajuda a controlar salário, gastos pessoais, cartão, dívidas, contas da casa e metas.

A maioria das pessoas e empresas não quebra por falta de dinheiro. Quebra por falta de controle.

A Global Software transforma bagunça financeira em visão clara para tomar decisão.
"""
    st.text_area("Roteiro de apresentação", value=roteiro, height=260, key="roteiro_venda_completo")
    html("</div>")

    html('<div class="commercial-panel">')
    st.markdown("## Sugestão de planos comerciais")

    p1, p2, p3 = st.columns(3)

    with p1:
        preco_card("Plano PF", "R$ 29/mês", "Controle financeiro pessoal, gastos, entradas, dívidas, metas e relatórios simples.")

    with p2:
        preco_card("Plano PJ Gestão Completa", "R$ 297/mês", "Financeiro, CRM, estoque, funcionários, folha, metas, premiações e relatórios.")

    with p3:
        preco_card("Plano Premium IA WhatsApp", "Sob consulta", "Integração WhatsApp, automações, IA, treinamento, implantação e suporte.")

    html("</div>")


# =====================================================
# APP PRINCIPAL
# =====================================================

def app():
    usuario = st.session_state.usuario

    if Path("logo.png").exists():
        st.sidebar.image("logo.png", use_container_width=True)

    tipo_pessoa = usuario.get("tipo_pessoa", "PJ")
    texto_tipo_pessoa = "Pessoa Física PF" if tipo_pessoa == "PF" else "Pessoa Jurídica PJ"

    st.sidebar.title("💼 Global Software")
    st.sidebar.write(f"**Conta:** {usuario['empresa_nome']}")
    st.sidebar.write(f"**Perfil:** {texto_tipo_pessoa}")
    st.sidebar.write(f"**Usuário:** {usuario['nome']}")
    st.sidebar.write(f"**Permissão:** {usuario['tipo']}")

    garantir_assinatura_empresa(usuario["empresa_id"], usuario.get("tipo_pessoa", "PJ"))
    assinatura_sidebar = consultar("SELECT * FROM assinaturas WHERE empresa_id = ?", (int(usuario["empresa_id"]),))
    status_sidebar = status_assinatura_real(assinatura_sidebar)
    dias_sidebar = dias_restantes_assinatura(assinatura_sidebar)
    st.sidebar.write(f"**Plano:** {assinatura_sidebar.iloc[0]['plano'] if not assinatura_sidebar.empty else 'Sem plano'}")
    st.sidebar.write(f"**Assinatura:** {status_sidebar} ({dias_sidebar} dias)")
    if is_super_admin_global():
        st.sidebar.success("Modo Super Admin Global ativo")

    df = carregar_lancamentos()
    clientes = carregar_clientes()
    estoque = carregar_estoque()
    funcionarios = carregar_funcionarios()
    folha = carregar_folha()
    metas = carregar_metas()
    planejamento = carregar_planejamento()
    assinatura = carregar_assinatura()
    status_assinatura = status_assinatura_real(assinatura)
    dias_assinatura = dias_restantes_assinatura(assinatura)

    ind = calcular_indicadores(df)
    menus_liberados = menus_por_tipo_usuario()

    if "menu_atual" not in st.session_state:
        st.session_state.menu_atual = menus_liberados[0]

    if st.session_state.menu_atual not in menus_liberados:
        st.session_state.menu_atual = menus_liberados[0]

    cabecalho_interno(st.session_state.menu_atual)

    html('<div class="menu-panel">')
    html('<div class="menu-title">Menu principal do sistema</div>')

    menu = st.radio(
        "Menu principal",
        menus_liberados,
        index=menus_liberados.index(st.session_state.menu_atual),
        horizontal=True,
        label_visibility="collapsed",
        key="menu_radio"
    )

    st.session_state.menu_atual = menu
    st.write("")

    col_sair1, col_sair2, col_sair3 = st.columns([6, 1, 1])

    with col_sair3:
        if st.button("Sair", use_container_width=True, key="btn_sair_tela"):
            del st.session_state.usuario
            if "menu_atual" in st.session_state:
                del st.session_state.menu_atual
            st.rerun()

    html("</div>")

    menu = st.session_state.menu_atual

    if menu == "Super Admin Global":
        st.title("👑 Super Admin Global Software")

        if not is_super_admin_global():
            st.error("Acesso exclusivo do administrador principal da Global Software.")
            return

        clientes_saas = carregar_clientes_saas()

        if clientes_saas.empty:
            st.info("Nenhuma conta PF/PJ cadastrada ainda.")
        else:
            total_contas = len(clientes_saas)
            contas_pj = clientes_saas[clientes_saas["tipo_pessoa"] == "PJ"].shape[0]
            contas_pf = clientes_saas[clientes_saas["tipo_pessoa"] == "PF"].shape[0]
            contas_ativas = clientes_saas[clientes_saas["status_real"].isin(["Ativo", "Teste grátis"])].shape[0]
            contas_vencidas = clientes_saas[clientes_saas["status_real"] == "Vencido"].shape[0]
            contas_bloqueadas = clientes_saas[clientes_saas["status_real"].isin(["Bloqueado", "Cancelado"])].shape[0]
            receita_prevista = clientes_saas[clientes_saas["status_real"].isin(["Ativo", "Teste grátis"])] ["valor_mensal"].sum()
            usuarios_total = clientes_saas["total_usuarios"].sum()

            c1, c2, c3, c4 = st.columns(4)
            with c1:
                card("Contas cadastradas", total_contas, f"PJ: {contas_pj} | PF: {contas_pf}")
            with c2:
                card("Ativas / teste", contas_ativas, "Clientes liberados")
            with c3:
                card("Vencidas / bloqueadas", contas_vencidas + contas_bloqueadas, f"Vencidas: {contas_vencidas} | Bloq.: {contas_bloqueadas}")
            with c4:
                card("Receita mensal prevista", moeda(receita_prevista), f"Usuários totais: {int(usuarios_total)}")

            st.divider()

            aba_visao, aba_cliente, aba_planos, aba_exportar = st.tabs([
                "Visão geral",
                "Gerenciar cliente",
                "Planos vendidos",
                "Exportações"
            ])

            with aba_visao:
                st.subheader("Todas as contas PF/PJ")

                filtro_status = st.multiselect(
                    "Filtrar por status",
                    STATUS_ASSINATURA + ["Sem assinatura"],
                    default=[],
                    key="super_filtro_status"
                )
                filtro_tipo = st.multiselect(
                    "Filtrar por perfil",
                    ["PJ", "PF"],
                    default=[],
                    key="super_filtro_tipo"
                )
                busca = st.text_input("Buscar por nome, documento, cidade ou telefone", key="super_busca")

                tabela = clientes_saas.copy()
                if filtro_status:
                    tabela = tabela[tabela["status_real"].isin(filtro_status)]
                if filtro_tipo:
                    tabela = tabela[tabela["tipo_pessoa"].isin(filtro_tipo)]
                if busca:
                    busca_lower = busca.lower()
                    tabela = tabela[
                        tabela.apply(
                            lambda row: busca_lower in " ".join([str(row.get(col, "")) for col in ["nome", "documento", "telefone", "cidade", "plano", "status_real"]]).lower(),
                            axis=1
                        )
                    ]

                colunas_tabela = [
                    "id", "nome", "tipo_pessoa", "plano", "status_real", "data_vencimento",
                    "dias_restantes", "valor_mensal", "limite_usuarios", "total_usuarios", "telefone", "cidade"
                ]
                st.dataframe(tabela[colunas_tabela], use_container_width=True, hide_index=True)

                if not tabela.empty:
                    st.bar_chart(tabela.groupby("status_real")["id"].count())

            with aba_cliente:
                st.subheader("Renovar, bloquear ou liberar cliente")

                opcoes_clientes = clientes_saas.apply(
                    lambda row: f"#{int(row['id'])} - {row['nome']} | {row['tipo_pessoa']} | {row['plano']} | {row['status_real']}",
                    axis=1
                ).tolist()

                cliente_selecionado = st.selectbox("Selecionar conta", opcoes_clientes, key="super_cliente_select")
                cliente_id = int(cliente_selecionado.split(" - ")[0].replace("#", ""))
                cliente_row = clientes_saas[clientes_saas["id"] == cliente_id].iloc[0]

                col_info1, col_info2, col_info3 = st.columns(3)
                with col_info1:
                    st.metric("Cliente", cliente_row["nome"])
                    st.caption(f"Documento: {cliente_row.get('documento', '')}")
                with col_info2:
                    st.metric("Plano", cliente_row["plano"])
                    st.caption(f"Status: {cliente_row['status_real']}")
                with col_info3:
                    st.metric("Mensalidade", moeda(cliente_row["valor_mensal"]))
                    st.caption(f"Vencimento: {data_br(cliente_row.get('data_vencimento'))}")

                with st.form("form_super_admin_cliente"):
                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        novo_plano = st.selectbox(
                            "Plano",
                            list(PLANOS_ASSINATURA.keys()),
                            index=list(PLANOS_ASSINATURA.keys()).index(cliente_row["plano"]) if cliente_row["plano"] in PLANOS_ASSINATURA else 0,
                            key="super_novo_plano"
                        )
                    with col_b:
                        novo_status = st.selectbox(
                            "Status",
                            STATUS_ASSINATURA,
                            index=STATUS_ASSINATURA.index(cliente_row["status_real"]) if cliente_row["status_real"] in STATUS_ASSINATURA else 0,
                            key="super_novo_status"
                        )
                    with col_c:
                        meses = st.number_input("Renovar por quantos meses", min_value=1, max_value=36, value=1, step=1, key="super_meses")

                    observacao_super = st.text_area("Observação interna", value="", key="super_obs")
                    salvar_super = st.form_submit_button("Salvar alteração do cliente", use_container_width=True)

                if salvar_super:
                    dados_plano = PLANOS_ASSINATURA.get(novo_plano, PLANOS_ASSINATURA["Gratuito"])
                    hoje = date.today()
                    data_base = hoje
                    try:
                        venc_atual = pd.to_datetime(cliente_row.get("data_vencimento")).date()
                        if venc_atual > hoje and novo_status not in ["Bloqueado", "Cancelado"]:
                            data_base = venc_atual
                    except Exception:
                        data_base = hoje

                    novo_vencimento = data_base + timedelta(days=30 * int(meses))

                    existe_ass = consultar("SELECT id FROM assinaturas WHERE empresa_id = ?", (cliente_id,))
                    if existe_ass.empty:
                        executar(
                            """
                            INSERT INTO assinaturas
                            (empresa_id, plano, status, data_inicio, data_vencimento, valor_mensal, limite_usuarios, observacao, criado_em, atualizado_em)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                            """,
                            (
                                cliente_id, novo_plano, novo_status, str(hoje), str(novo_vencimento),
                                float(dados_plano["valor"]), int(dados_plano["limite"]),
                                observacao_super, datetime.now().isoformat(), datetime.now().isoformat()
                            )
                        )
                    else:
                        executar(
                            """
                            UPDATE assinaturas
                            SET plano = ?, status = ?, data_vencimento = ?, valor_mensal = ?, limite_usuarios = ?, observacao = ?, atualizado_em = ?
                            WHERE empresa_id = ?
                            """,
                            (
                                novo_plano, novo_status, str(novo_vencimento), float(dados_plano["valor"]),
                                int(dados_plano["limite"]), observacao_super, datetime.now().isoformat(), cliente_id
                            )
                        )

                    st.success("Cliente atualizado com sucesso no Super Admin.")
                    st.rerun()

                st.divider()
                texto_cliente = (
                    "Olá! Aqui é da Global Software.\n\n"
                    f"Sua conta: {cliente_row['nome']}\n"
                    f"Plano atual: {cliente_row['plano']}\n"
                    f"Status: {cliente_row['status_real']}\n"
                    f"Vencimento: {data_br(cliente_row.get('data_vencimento'))}\n\n"
                    "Vamos regularizar/renovar sua assinatura?"
                )
                telefone_cliente = str(cliente_row.get("telefone", "")).replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
                if telefone_cliente:
                    if not telefone_cliente.startswith("55"):
                        telefone_cliente = "55" + telefone_cliente
                    st.markdown(f"[📲 Chamar cliente no WhatsApp](https://wa.me/{telefone_cliente}?text={quote(texto_cliente)})")
                else:
                    st.info("Cliente sem telefone cadastrado. Atualize o telefone em Configurações ou no cadastro da conta.")

            with aba_planos:
                st.subheader("Resumo por plano")
                resumo_planos = clientes_saas.groupby("plano").agg(
                    contas=("id", "count"),
                    receita_prevista=("valor_mensal", "sum"),
                    usuarios=("total_usuarios", "sum")
                ).reset_index()
                st.dataframe(resumo_planos, use_container_width=True, hide_index=True)
                if not resumo_planos.empty:
                    st.bar_chart(resumo_planos.set_index("plano")["receita_prevista"])

                st.subheader("Resumo por status")
                resumo_status = clientes_saas.groupby("status_real").agg(
                    contas=("id", "count"),
                    receita_prevista=("valor_mensal", "sum")
                ).reset_index()
                st.dataframe(resumo_status, use_container_width=True, hide_index=True)

            with aba_exportar:
                st.subheader("Exportar base SaaS")
                st.download_button(
                    "Baixar clientes SaaS CSV",
                    data=clientes_saas.to_csv(index=False).encode("utf-8"),
                    file_name="clientes_saas_global_software.csv",
                    mime="text/csv",
                    key="download_clientes_saas"
                )

                backup_saas = {
                    "gerado_em": datetime.now().isoformat(),
                    "total_contas": int(total_contas),
                    "receita_prevista": float(receita_prevista),
                    "clientes": clientes_saas.to_dict(orient="records"),
                }
                st.download_button(
                    "Baixar backup SaaS JSON",
                    data=json.dumps(backup_saas, ensure_ascii=False, indent=4, default=str),
                    file_name="backup_saas_global_software.json",
                    mime="application/json",
                    key="download_backup_saas"
                )

    elif menu == "Dashboard":
        st.title("📊 Dashboard Executivo Premium")

        if status_assinatura in ["Vencido", "Bloqueado", "Cancelado"]:
            st.error(f"Assinatura {status_assinatura}. Acesse **Assinaturas / Planos** para regularizar e renovar pelo WhatsApp.")
        elif dias_assinatura <= 3:
            st.warning(f"Sua assinatura vence em {dias_assinatura} dia(s). Acesse **Assinaturas / Planos** para renovar.")
        else:
            st.caption(f"Plano ativo: {assinatura.iloc[0]['plano']} • Status: {status_assinatura} • Vencimento: {data_br(assinatura.iloc[0]['data_vencimento'])}")

        inadimplentes_df = pd.DataFrame()
        if not df.empty:
            inadimplentes_df = df[(df["tipo"] == "Receita") & (df["status_real"] == "Vencido")]

        total_estoque_custo = 0
        itens_baixo = 0

        if not estoque.empty:
            estoque["valor_custo_total"] = estoque["quantidade"] * estoque["custo_unitario"]
            estoque["valor_venda_total"] = estoque["quantidade"] * estoque["preco_venda"]
            total_estoque_custo = estoque["valor_custo_total"].sum()
            itens_baixo = estoque[estoque["quantidade"] <= estoque["estoque_minimo"]].shape[0]

        folha_mes = 0
        if not folha.empty:
            folha_mes = folha[folha["mes_referencia"] == mes_atual_str()]["total_liquido"].sum()

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            card("Receita total", moeda(ind["receita"]), "Entradas registradas")

        with c2:
            card("Saídas totais", moeda(ind["saidas"]), "Custos, despesas e dívidas")

        with c3:
            card("Lucro / Resultado", moeda(ind["lucro"]), "Receita menos saídas")

        with c4:
            card("Contas pagas no mês", moeda(ind["pagas_mes"]), "Pagas ou recebidas no mês atual")

        st.write("")

        c5, c6, c7, c8 = st.columns(4)

        with c5:
            card(
                "Clientes inadimplentes",
                str(inadimplentes_df["cliente_fornecedor"].nunique()) if not inadimplentes_df.empty else "0",
                moeda(inadimplentes_df["valor"].sum()) if not inadimplentes_df.empty else moeda(0)
            )

        with c6:
            card("Estoque em custo", moeda(total_estoque_custo), f"{itens_baixo} item(ns) abaixo do mínimo")

        with c7:
            card("Folha do mês", moeda(folha_mes), f"{len(funcionarios)} funcionário(s) cadastrados")

        with c8:
            card("A receber", moeda(ind["receber"]), "Receitas pendentes")

        st.divider()

        if df.empty:
            st.info("Nenhum lançamento cadastrado ainda. Vá em Configurações e clique em Carregar dados de exemplo.")
        else:
            col_g1, col_g2 = st.columns(2)

            with col_g1:
                st.subheader("📈 Movimento por mês")
                graf = df.copy()
                graf["mes"] = graf["data"].dt.strftime("%Y-%m")
                resumo = graf.groupby(["mes", "tipo"])["valor"].sum().reset_index()
                tabela_graf = resumo.pivot(index="mes", columns="tipo", values="valor").fillna(0)
                st.line_chart(tabela_graf)

            with col_g2:
                st.subheader("🏷️ Gastos por categoria")
                gastos = df[df["tipo"] != "Receita"]
                if gastos.empty:
                    st.info("Nenhum gasto registrado.")
                else:
                    st.bar_chart(gastos.groupby("categoria")["valor"].sum().sort_values(ascending=False).head(10))

            st.divider()

            st.subheader("⚠️ Contas críticas")
            criticas = df[df["status_real"].isin(["Vencido", "Vence hoje"])].copy()

            if criticas.empty:
                st.success("Nenhuma conta vencida ou vencendo hoje.")
            else:
                criticas["vencimento"] = criticas["vencimento"].dt.strftime("%d/%m/%Y")
                criticas["valor"] = criticas["valor"].apply(moeda)
                st.dataframe(
                    criticas[["vencimento", "tipo", "descricao", "cliente_fornecedor", "valor", "status_real"]],
                    use_container_width=True,
                    hide_index=True
                )

    elif menu == "Entradas e Saídas":
        st.title("💸 Entradas e Saídas")

        with st.form("form_lancamento"):
            col1, col2, col3 = st.columns(3)

            with col1:
                data_lanc = st.date_input("Data", value=date.today(), key="lanc_data")
                vencimento = st.date_input("Vencimento", value=date.today(), key="lanc_vencimento")
                tipo = st.selectbox("Tipo", list(TIPOS_LANCAMENTO.keys()), key="lanc_tipo")

            with col2:
                categoria = st.selectbox("Categoria", TIPOS_LANCAMENTO[tipo], key="lanc_categoria")
                descricao = st.text_input("Descrição", key="lanc_descricao")
                cliente = st.text_input("Cliente / Fornecedor", key="lanc_cliente")

            with col3:
                valor = st.number_input("Valor total", min_value=0.0, step=1.0, format="%.2f", key="lanc_valor")
                forma = st.selectbox("Forma de pagamento", FORMAS_PAGAMENTO, key="lanc_forma")
                conta = st.selectbox("Conta", CONTAS, key="lanc_conta")

            col4, col5, col6 = st.columns(3)

            with col4:
                status = st.selectbox("Status", STATUS_OPCOES, key="lanc_status")

            with col5:
                parcela_total = st.number_input("Total de parcelas", min_value=1, value=1, step=1, key="lanc_parcelas")

            with col6:
                observacao = st.text_input("Observação", key="lanc_observacao")

            salvar = st.form_submit_button("Salvar lançamento")

            if salvar:
                if valor <= 0:
                    st.error("Digite um valor maior que zero.")
                else:
                    total = int(parcela_total)
                    valor_parcela = valor / total

                    for parcela in range(1, total + 1):
                        data_parcela = data_lanc + timedelta(days=30 * (parcela - 1))
                        venc_parcela = vencimento + timedelta(days=30 * (parcela - 1))

                        executar(
                            """
                            INSERT INTO lancamentos
                            (empresa_id, usuario_id, data, vencimento, tipo, categoria, descricao,
                            cliente_fornecedor, valor, forma_pagamento, conta, status, parcela_atual,
                            parcela_total, observacao, criado_em)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                            """,
                            (
                                empresa_id_atual(),
                                usuario_id_atual(),
                                str(data_parcela),
                                str(venc_parcela),
                                tipo,
                                categoria,
                                descricao,
                                cliente,
                                float(valor_parcela),
                                forma,
                                conta,
                                status,
                                parcela,
                                total,
                                observacao,
                                datetime.now().isoformat()
                            )
                        )

                    st.success("Lançamento salvo com sucesso.")
                    st.rerun()

        st.subheader("Lançamentos cadastrados")

        if df.empty:
            st.info("Nenhum lançamento cadastrado.")
        else:
            tabela = df.copy()
            tabela["data"] = tabela["data"].dt.strftime("%d/%m/%Y")
            tabela["vencimento"] = tabela["vencimento"].dt.strftime("%d/%m/%Y")
            tabela["valor_formatado"] = tabela["valor"].apply(moeda)

            st.dataframe(
                tabela[["id", "data", "vencimento", "tipo", "categoria", "descricao", "cliente_fornecedor", "valor_formatado", "status_real"]],
                use_container_width=True,
                hide_index=True
            )

            st.subheader("Editar / Excluir")

            id_edit = st.selectbox("Selecione o ID", df["id"].tolist(), key="edit_id")
            item = df[df["id"] == id_edit].iloc[0]

            col_e1, col_e2, col_e3 = st.columns(3)

            with col_e1:
                novo_status = st.selectbox(
                    "Novo status",
                    STATUS_OPCOES,
                    index=STATUS_OPCOES.index(item["status"]) if item["status"] in STATUS_OPCOES else 0,
                    key="edit_status"
                )

            with col_e2:
                novo_valor = st.number_input("Novo valor", min_value=0.0, value=float(item["valor"]), step=1.0, key="edit_valor")

            with col_e3:
                nova_desc = st.text_input("Nova descrição", value=item["descricao"], key="edit_desc")

            col_a, col_b = st.columns(2)

            if col_a.button("Atualizar lançamento", key="btn_atualizar_lancamento"):
                executar(
                    """
                    UPDATE lancamentos
                    SET status = ?, valor = ?, descricao = ?
                    WHERE id = ? AND empresa_id = ?
                    """,
                    (novo_status, novo_valor, nova_desc, int(id_edit), empresa_id_atual())
                )
                st.success("Atualizado.")
                st.rerun()

            if col_b.button("Excluir lançamento", key="btn_excluir_lancamento"):
                executar("DELETE FROM lancamentos WHERE id = ? AND empresa_id = ?", (int(id_edit), empresa_id_atual()))
                st.warning("Excluído.")
                st.rerun()

    elif menu == "Contas Pagas no Mês":
        st.title("✅ Contas Pagas no Mês")

        if df.empty:
            st.info("Nenhuma conta cadastrada.")
        else:
            mes_ref = st.text_input("Mês de referência", value=mes_atual_str(), key="mes_contas_pagas")

            pagas = df[
                (df["status"].isin(["Pago", "Recebido"])) &
                (df["data"].dt.strftime("%Y-%m") == mes_ref)
            ].copy()

            if pagas.empty:
                st.info("Nenhuma conta paga/recebida nesse mês.")
            else:
                total_pago = pagas["valor"].sum()
                card("Total pago/recebido no mês", moeda(total_pago), f"Mês {mes_ref}")

                pagas["data"] = pagas["data"].dt.strftime("%d/%m/%Y")
                pagas["vencimento"] = pagas["vencimento"].dt.strftime("%d/%m/%Y")
                pagas["valor_formatado"] = pagas["valor"].apply(moeda)

                st.dataframe(
                    pagas[["data", "vencimento", "tipo", "categoria", "descricao", "cliente_fornecedor", "valor_formatado", "status"]],
                    use_container_width=True,
                    hide_index=True
                )

    elif menu == "Clientes / CRM":
        st.title("👥 Clientes / CRM")

        if tipo_pessoa_atual() == "PF":
            st.info("No perfil PF, esta aba pode ser usada para contatos pessoais, pessoas que devem, pessoas que você paga ou fornecedores pessoais.")

        with st.form("form_cliente"):
            col1, col2 = st.columns(2)

            with col1:
                nome = st.text_input("Nome", key="cliente_nome")
                telefone = st.text_input("Telefone / WhatsApp", key="cliente_telefone")
                email = st.text_input("E-mail", key="cliente_email")
                documento = st.text_input("CPF / CNPJ", key="cliente_documento")

            with col2:
                tipo_cliente = st.selectbox("Tipo", ["Cliente", "Fornecedor", "Parceiro", "Contato pessoal", "Pessoa que devo", "Pessoa que me deve"], key="cliente_tipo")
                limite_credito = st.number_input("Limite de crédito", min_value=0.0, step=100.0, key="cliente_limite")
                status_cliente = st.selectbox("Status do cliente", ["Ativo", "Inativo", "Bloqueado"], key="cliente_status")
                obs = st.text_area("Observação", key="cliente_obs")

            if st.form_submit_button("Salvar cliente"):
                executar(
                    """
                    INSERT INTO clientes
                    (empresa_id, nome, telefone, email, documento, tipo, observacao, criado_em, limite_credito, status_cliente)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (empresa_id_atual(), nome, telefone, email, documento, tipo_cliente, obs, datetime.now().isoformat(), limite_credito, status_cliente)
                )
                st.success("Cliente salvo.")
                st.rerun()

        if clientes.empty:
            st.info("Nenhum cliente cadastrado.")
        else:
            st.dataframe(clientes, use_container_width=True, hide_index=True)

    elif menu == "Clientes Inadimplentes":
        st.title("🚨 Clientes Inadimplentes")

        if tipo_pessoa_atual() == "PF":
            st.info("No perfil PF, esta aba mostra pessoas ou recebimentos pessoais vencidos.")

        if df.empty:
            st.info("Nenhum lançamento cadastrado.")
        else:
            inad = df[(df["tipo"] == "Receita") & (df["status_real"] == "Vencido")].copy()

            if inad.empty:
                st.success("Nenhum inadimplente encontrado.")
            else:
                total_inad = inad["valor"].sum()
                qtd_clientes = inad["cliente_fornecedor"].nunique()

                c1, c2 = st.columns(2)

                with c1:
                    card("Inadimplentes", str(qtd_clientes), "Receitas vencidas")

                with c2:
                    card("Valor inadimplente", moeda(total_inad), "Total vencido")

                resumo = inad.groupby("cliente_fornecedor")["valor"].sum().reset_index()
                resumo["valor_formatado"] = resumo["valor"].apply(moeda)

                st.subheader("Resumo")
                st.dataframe(resumo[["cliente_fornecedor", "valor_formatado"]], use_container_width=True, hide_index=True)

                st.subheader("Detalhamento")
                inad["vencimento"] = inad["vencimento"].dt.strftime("%d/%m/%Y")
                inad["valor_formatado"] = inad["valor"].apply(moeda)

                st.dataframe(
                    inad[["vencimento", "cliente_fornecedor", "descricao", "valor_formatado", "forma_pagamento", "observacao"]],
                    use_container_width=True,
                    hide_index=True
                )

    elif menu == "Estoque":
        st.title("📦 Controle de Estoque Completo")

        if tipo_pessoa_atual() == "PF":
            st.info("Perfil PF: esta aba pode ser usada para controle de bens pessoais, itens de casa, equipamentos ou objetos de valor.")

        with st.form("form_estoque"):
            col1, col2, col3 = st.columns(3)

            with col1:
                produto = st.text_input("Produto / Item", key="est_produto")
                codigo = st.text_input("Código / Referência", key="est_codigo")
                categoria = st.text_input("Categoria", key="est_categoria")

            with col2:
                quantidade = st.number_input("Quantidade", min_value=0.0, step=1.0, key="est_quantidade")
                estoque_minimo = st.number_input("Estoque mínimo", min_value=0.0, step=1.0, key="est_minimo")
                fornecedor = st.text_input("Fornecedor", key="est_fornecedor")

            with col3:
                custo_unitario = st.number_input("Custo unitário", min_value=0.0, step=1.0, key="est_custo")
                preco_venda = st.number_input("Preço de venda", min_value=0.0, step=1.0, key="est_preco")
                obs = st.text_area("Observação", key="est_obs")

            if st.form_submit_button("Salvar produto"):
                executar(
                    """
                    INSERT INTO estoque
                    (empresa_id, produto, categoria, quantidade, custo_unitario, preco_venda, fornecedor, observacao, criado_em, estoque_minimo, codigo)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (empresa_id_atual(), produto, categoria, quantidade, custo_unitario, preco_venda, fornecedor, obs, datetime.now().isoformat(), estoque_minimo, codigo)
                )
                st.success("Produto salvo.")
                st.rerun()

        if estoque.empty:
            st.info("Nenhum produto cadastrado.")
        else:
            estoque["valor_custo_total"] = estoque["quantidade"] * estoque["custo_unitario"]
            estoque["valor_venda_total"] = estoque["quantidade"] * estoque["preco_venda"]
            estoque["lucro_previsto"] = estoque["valor_venda_total"] - estoque["valor_custo_total"]
            estoque["alerta"] = estoque.apply(lambda x: "Baixo estoque" if x["quantidade"] <= x["estoque_minimo"] else "OK", axis=1)

            c1, c2, c3 = st.columns(3)

            with c1:
                card("Valor em custo", moeda(estoque["valor_custo_total"].sum()), "Valor investido")

            with c2:
                card("Valor em venda", moeda(estoque["valor_venda_total"].sum()), "Potencial de venda")

            with c3:
                card("Lucro previsto", moeda(estoque["lucro_previsto"].sum()), "Venda menos custo")

            st.dataframe(estoque, use_container_width=True, hide_index=True)

    elif menu == "Funcionários":
        st.title("👨‍💼 Cadastro de Funcionários")

        if tipo_pessoa_atual() == "PF":
            st.info("No perfil PF, esta aba não é essencial. Ela continua disponível para uso avançado ou controle de equipe doméstica/prestadores.")

        with st.form("form_funcionario"):
            col1, col2, col3 = st.columns(3)

            with col1:
                nome = st.text_input("Nome do funcionário", key="fun_nome")
                cargo = st.text_input("Cargo", key="fun_cargo")
                telefone = st.text_input("Telefone", key="fun_telefone")

            with col2:
                documento = st.text_input("CPF / Documento", key="fun_doc")
                data_admissao = st.date_input("Data de admissão", value=date.today(), key="fun_admissao")
                salario_base = st.number_input("Salário base", min_value=0.0, step=100.0, key="fun_salario")

            with col3:
                tipo_contrato = st.selectbox("Tipo de contrato", ["CLT", "PJ", "Comissionado", "Freelancer", "Outro"], key="fun_contrato")
                status_fun = st.selectbox("Status", ["Ativo", "Inativo", "Afastado"], key="fun_status")
                obs = st.text_area("Observação", key="fun_obs")

            if st.form_submit_button("Salvar funcionário"):
                executar(
                    """
                    INSERT INTO funcionarios
                    (empresa_id, nome, cargo, telefone, documento, data_admissao, salario_base, tipo_contrato, status, observacao, criado_em)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (empresa_id_atual(), nome, cargo, telefone, documento, str(data_admissao), salario_base, tipo_contrato, status_fun, obs, datetime.now().isoformat())
                )
                st.success("Funcionário salvo.")
                st.rerun()

        if funcionarios.empty:
            st.info("Nenhum funcionário cadastrado.")
        else:
            funcionarios["salario_formatado"] = funcionarios["salario_base"].apply(moeda)
            st.dataframe(funcionarios, use_container_width=True, hide_index=True)

    elif menu == "Folha de Pagamento":
        st.title("🧾 Folha de Pagamento Completa")

        if tipo_pessoa_atual() == "PF":
            st.info("No perfil PF, esta aba pode ser ignorada ou usada para controle de prestadores/serviços mensais.")

        if funcionarios.empty:
            st.warning("Cadastre funcionários antes de lançar folha de pagamento.")
        else:
            func_dict = {f"{row['nome']} - {row['cargo']}": int(row["id"]) for _, row in funcionarios.iterrows()}

            with st.form("form_folha"):
                col1, col2, col3 = st.columns(3)

                with col1:
                    funcionario_label = st.selectbox("Funcionário", list(func_dict.keys()), key="folha_func")
                    funcionario_id = func_dict[funcionario_label]
                    mes_ref = st.text_input("Mês referência", value=mes_atual_str(), key="folha_mes")
                    funcionario_row = funcionarios[funcionarios["id"] == funcionario_id].iloc[0]
                    salario = st.number_input("Salário base", min_value=0.0, value=float(funcionario_row["salario_base"] or 0), step=100.0, key="folha_salario")

                with col2:
                    horas_extras = st.number_input("Horas extras", min_value=0.0, step=1.0, key="folha_horas")
                    valor_hora_extra = st.number_input("Valor da hora extra", min_value=0.0, step=10.0, key="folha_valor_hora")
                    comissao = st.number_input("Comissão", min_value=0.0, step=50.0, key="folha_comissao")

                with col3:
                    bonus = st.number_input("Bônus", min_value=0.0, step=50.0, key="folha_bonus")
                    premiacao = st.number_input("Premiação", min_value=0.0, step=50.0, key="folha_premiacao")
                    desconto = st.number_input("Descontos", min_value=0.0, step=50.0, key="folha_desconto")

                col4, col5, col6 = st.columns(3)

                with col4:
                    meta_valor = st.number_input("Meta do mês", min_value=0.0, step=100.0, key="folha_meta")
                    meta_batida = st.selectbox("Meta batida?", ["Não", "Sim"], key="folha_meta_batida")

                with col5:
                    status_folha = st.selectbox("Status da folha", ["Pendente", "Pago"], key="folha_status")
                    data_pagamento = st.date_input("Data de pagamento", value=date.today(), key="folha_pagamento")

                with col6:
                    observacao = st.text_area("Observação", key="folha_obs")

                bruto, liquido = calcular_folha_total(salario, horas_extras, valor_hora_extra, comissao, bonus, premiacao, desconto)

                st.info(f"Total bruto: {moeda(bruto)} | Total líquido: {moeda(liquido)}")

                salvar = st.form_submit_button("Salvar folha")

                if salvar:
                    executar(
                        """
                        INSERT INTO folha_pagamento
                        (empresa_id, funcionario_id, mes_referencia, salario_base, horas_extras, valor_hora_extra,
                        comissao, bonus, premiacao, desconto, meta_valor, meta_batida, total_bruto, total_liquido,
                        status, data_pagamento, observacao, criado_em)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            empresa_id_atual(),
                            funcionario_id,
                            mes_ref,
                            salario,
                            horas_extras,
                            valor_hora_extra,
                            comissao,
                            bonus,
                            premiacao,
                            desconto,
                            meta_valor,
                            meta_batida,
                            bruto,
                            liquido,
                            status_folha,
                            str(data_pagamento),
                            observacao,
                            datetime.now().isoformat()
                        )
                    )

                    if status_folha == "Pago":
                        executar(
                            """
                            INSERT INTO lancamentos
                            (empresa_id, usuario_id, data, vencimento, tipo, categoria, descricao,
                            cliente_fornecedor, valor, forma_pagamento, conta, status, parcela_atual,
                            parcela_total, observacao, criado_em)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                            """,
                            (
                                empresa_id_atual(),
                                usuario_id_atual(),
                                str(data_pagamento),
                                str(data_pagamento),
                                "Despesa fixa",
                                "Folha de pagamento",
                                f"Folha de pagamento - {funcionario_label}",
                                funcionario_label,
                                float(liquido),
                                "Transferência",
                                "Banco",
                                "Pago",
                                1,
                                1,
                                "Lançamento automático gerado pela folha de pagamento",
                                datetime.now().isoformat()
                            )
                        )

                    st.success("Folha salva com sucesso.")
                    st.rerun()

        if folha.empty:
            st.info("Nenhuma folha cadastrada.")
        else:
            folha["salario_formatado"] = folha["salario_base"].apply(moeda)
            folha["bruto_formatado"] = folha["total_bruto"].apply(moeda)
            folha["liquido_formatado"] = folha["total_liquido"].apply(moeda)

            total_mes = folha[folha["mes_referencia"] == mes_atual_str()]["total_liquido"].sum()
            card("Total folha do mês", moeda(total_mes), mes_atual_str())

            st.dataframe(folha, use_container_width=True, hide_index=True)

    elif menu == "Metas e Premiações":
        st.title("🎯 Metas e Premiações")

        if tipo_pessoa_atual() == "PF":
            st.info("Perfil PF: use esta aba para metas pessoais, reserva de emergência, quitar dívidas, juntar entrada ou controlar objetivos financeiros.")

        if funcionarios.empty and tipo_pessoa_atual() == "PJ":
            st.warning("Cadastre funcionários antes de criar metas.")
        else:
            if funcionarios.empty:
                st.info("Para PF, você pode cadastrar uma meta pela aba Entradas e Saídas usando categoria Investimento ou Dívida. Em breve criaremos metas PF próprias.")
            else:
                func_dict = {f"{row['nome']} - {row['cargo']}": int(row["id"]) for _, row in funcionarios.iterrows()}

                with st.form("form_meta"):
                    col1, col2, col3 = st.columns(3)

                    with col1:
                        funcionario_label = st.selectbox("Funcionário", list(func_dict.keys()), key="meta_func")
                        funcionario_id = func_dict[funcionario_label]
                        mes_ref = st.text_input("Mês referência", value=mes_atual_str(), key="meta_mes")
                        descricao = st.text_input("Descrição da meta", key="meta_desc")

                    with col2:
                        meta_valor = st.number_input("Valor da meta", min_value=0.0, step=100.0, key="meta_valor")
                        realizado = st.number_input("Realizado", min_value=0.0, step=100.0, key="meta_realizado")
                        premio = st.number_input("Prêmio / bônus", min_value=0.0, step=50.0, key="meta_premio")

                    with col3:
                        status_meta = st.selectbox("Status", ["Em andamento", "Batida", "Não batida", "Paga"], key="meta_status")

                    if st.form_submit_button("Salvar meta"):
                        executar(
                            """
                            INSERT INTO metas
                            (empresa_id, funcionario_id, mes_referencia, descricao, meta_valor, realizado, premio, status, criado_em)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                            """,
                            (empresa_id_atual(), funcionario_id, mes_ref, descricao, meta_valor, realizado, premio, status_meta, datetime.now().isoformat())
                        )
                        st.success("Meta salva.")
                        st.rerun()

        if metas.empty:
            st.info("Nenhuma meta cadastrada.")
        else:
            metas["meta_formatada"] = metas["meta_valor"].apply(moeda)
            metas["realizado_formatado"] = metas["realizado"].apply(moeda)
            metas["premio_formatado"] = metas["premio"].apply(moeda)
            metas["percentual"] = metas.apply(lambda x: percentual((x["realizado"] / x["meta_valor"] * 100) if x["meta_valor"] else 0), axis=1)
            st.dataframe(metas, use_container_width=True, hide_index=True)

    elif menu == "Parcelas":
        st.title("📆 Controle de Parcelas")

        if df.empty:
            st.info("Nenhuma parcela cadastrada.")
        else:
            parcelas = df[df["parcela_total"] > 1].copy()

            if parcelas.empty:
                st.info("Nenhum lançamento parcelado.")
            else:
                parcelas["data"] = parcelas["data"].dt.strftime("%d/%m/%Y")
                parcelas["vencimento"] = parcelas["vencimento"].dt.strftime("%d/%m/%Y")
                parcelas["valor_formatado"] = parcelas["valor"].apply(moeda)

                st.dataframe(
                    parcelas[["id", "data", "vencimento", "descricao", "cliente_fornecedor", "valor_formatado", "parcela_atual", "parcela_total", "status_real"]],
                    use_container_width=True,
                    hide_index=True
                )


    elif menu == "Planejamento Financeiro":
        st.title("🧭 Planejamento Financeiro")

        st.info(
            "Use esta área para planejar receitas, despesas, investimentos, dívidas, metas pessoais ou metas da empresa. "
            "Depois compare o previsto com o realizado."
        )

        mes_ref_padrao = mes_atual_str()

        with st.form("form_planejamento_financeiro"):
            col1, col2, col3 = st.columns(3)

            with col1:
                mes_ref = st.text_input("Mês referência", value=mes_ref_padrao, key="plan_mes")
                tipo_plan = st.selectbox(
                    "Tipo",
                    ["Receita prevista", "Despesa prevista", "Investimento", "Dívida", "Meta de economia", "Reserva de emergência", "Outro"],
                    key="plan_tipo"
                )
                categoria_plan = st.text_input("Categoria", placeholder="Ex: Vendas, aluguel, cartão, combustível", key="plan_categoria")

            with col2:
                descricao_plan = st.text_input("Descrição", placeholder="Ex: Meta de vendas do mês", key="plan_descricao")
                valor_previsto = st.number_input("Valor previsto", min_value=0.0, step=100.0, key="plan_previsto")
                valor_realizado = st.number_input("Valor realizado", min_value=0.0, step=100.0, key="plan_realizado")

            with col3:
                status_plan = st.selectbox(
                    "Status",
                    ["Planejado", "Em andamento", "Concluído", "Atrasado", "Cancelado"],
                    key="plan_status"
                )
                observacao_plan = st.text_area("Observação", key="plan_obs")

            if st.form_submit_button("Salvar planejamento", use_container_width=True):
                if not mes_ref or not tipo_plan or not categoria_plan:
                    st.warning("Preencha mês, tipo e categoria.")
                else:
                    executar(
                        """
                        INSERT INTO planejamento_financeiro
                        (empresa_id, usuario_id, mes_referencia, tipo_planejamento, categoria, descricao,
                        valor_previsto, valor_realizado, status, observacao, criado_em)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            empresa_id_atual(),
                            usuario_id_atual(),
                            mes_ref,
                            tipo_plan,
                            categoria_plan,
                            descricao_plan,
                            float(valor_previsto),
                            float(valor_realizado),
                            status_plan,
                            observacao_plan,
                            datetime.now().isoformat()
                        )
                    )
                    st.success("Planejamento salvo com sucesso.")
                    st.rerun()

        planejamento = carregar_planejamento()

        if planejamento.empty:
            st.info("Nenhum planejamento cadastrado ainda.")
        else:
            planejamento["valor_previsto"] = pd.to_numeric(planejamento["valor_previsto"], errors="coerce").fillna(0)
            planejamento["valor_realizado"] = pd.to_numeric(planejamento["valor_realizado"], errors="coerce").fillna(0)
            planejamento["diferenca"] = planejamento["valor_realizado"] - planejamento["valor_previsto"]

            total_previsto = planejamento["valor_previsto"].sum()
            total_realizado = planejamento["valor_realizado"].sum()
            diferenca_total = total_realizado - total_previsto

            c1, c2, c3 = st.columns(3)
            with c1:
                card("Total previsto", moeda(total_previsto), "Somatório dos planejamentos")
            with c2:
                card("Total realizado", moeda(total_realizado), "Valor já realizado")
            with c3:
                card("Diferença", moeda(diferenca_total), "Realizado menos previsto")

            filtro_mes = st.selectbox(
                "Filtrar por mês",
                ["Todos"] + sorted(planejamento["mes_referencia"].dropna().unique().tolist(), reverse=True),
                key="plan_filtro_mes"
            )

            planejamento_filtrado = planejamento.copy()
            if filtro_mes != "Todos":
                planejamento_filtrado = planejamento_filtrado[planejamento_filtrado["mes_referencia"] == filtro_mes]

            if not planejamento_filtrado.empty:
                resumo = planejamento_filtrado.groupby("tipo_planejamento")[["valor_previsto", "valor_realizado"]].sum().reset_index()
                resumo["diferença"] = resumo["valor_realizado"] - resumo["valor_previsto"]
                st.subheader("Resumo por tipo")
                st.dataframe(resumo, use_container_width=True, hide_index=True)

                chart_df = resumo.set_index("tipo_planejamento")[["valor_previsto", "valor_realizado"]]
                st.bar_chart(chart_df)

                planejamento_filtrado["valor_previsto_formatado"] = planejamento_filtrado["valor_previsto"].apply(moeda)
                planejamento_filtrado["valor_realizado_formatado"] = planejamento_filtrado["valor_realizado"].apply(moeda)
                planejamento_filtrado["diferenca_formatada"] = planejamento_filtrado["diferenca"].apply(moeda)

                st.subheader("Planejamentos cadastrados")
                st.dataframe(planejamento_filtrado, use_container_width=True, hide_index=True)

                csv_plan = planejamento_filtrado.to_csv(index=False).encode("utf-8-sig")
                st.download_button(
                    "Baixar planejamento em CSV",
                    data=csv_plan,
                    file_name="planejamento_financeiro_global_software.csv",
                    mime="text/csv",
                    use_container_width=True,
                    key="download_planejamento_csv"
                )

                st.subheader("Excluir planejamento")
                ids_plan = planejamento_filtrado["id"].astype(int).tolist()
                id_excluir = st.selectbox("Selecione o ID para excluir", ids_plan, key="plan_excluir_id")
                if st.button("Excluir planejamento selecionado", use_container_width=True, key="btn_excluir_planejamento"):
                    executar(
                        "DELETE FROM planejamento_financeiro WHERE id = ? AND empresa_id = ?",
                        (int(id_excluir), empresa_id_atual())
                    )
                    st.success("Planejamento excluído com sucesso.")
                    st.rerun()


    elif menu == "Assinaturas / Planos":
        st.title("💳 Assinaturas e Planos")

        if assinatura.empty:
            st.warning("Nenhuma assinatura encontrada para esta conta.")
        else:
            ass = assinatura.iloc[0]
            plano_atual = ass.get("plano", "Gratuito")
            status_real = status_assinatura_real(assinatura)
            dias_restantes = dias_restantes_assinatura(assinatura)
            valor_mensal = float(ass.get("valor_mensal") or 0)
            limite_usuarios = int(ass.get("limite_usuarios") or 1)
            vencimento = ass.get("data_vencimento")

            c1, c2, c3, c4 = st.columns(4)
            with c1:
                card("Plano atual", plano_atual, PLANOS_ASSINATURA.get(plano_atual, {}).get("descricao", "Plano cadastrado"))
            with c2:
                card("Status", status_real, "Situação atual da mensalidade")
            with c3:
                card("Vencimento", data_br(vencimento), f"Faltam {dias_restantes} dia(s)")
            with c4:
                card("Mensalidade", moeda(valor_mensal), f"Limite de {limite_usuarios} usuário(s)")

            if status_real == "Vencido":
                st.error("Assinatura vencida. Gere o link de renovação pelo WhatsApp ou renove manualmente como administrador.")
            elif status_real == "Bloqueado":
                st.error("Conta bloqueada. Entre em contato com o suporte Global Software.")
            elif status_real == "Cancelado":
                st.warning("Assinatura cancelada. Regularize para continuar usando como cliente ativo.")
            elif dias_restantes <= 3:
                st.warning(f"Atenção: sua assinatura vence em {dias_restantes} dia(s).")
            else:
                st.success("Assinatura em dia.")

            st.markdown(f"[📲 Renovar pelo WhatsApp]({link_whatsapp_renovacao(assinatura)})")

        st.divider()
        st.subheader("Planos comerciais da Global Software")

        p1, p2, p3, p4, p5 = st.columns(5)
        planos_cols = [p1, p2, p3, p4, p5]
        for coluna, (nome_plano, dados) in zip(planos_cols, PLANOS_ASSINATURA.items()):
            with coluna:
                preco_card(nome_plano, moeda(dados["valor"]), f"{dados['descricao']} Limite: {dados['limite']} usuário(s).")

        if tipo_usuario_atual() == "Administrador":
            st.divider()
            st.subheader("Controle administrativo da assinatura")
            st.info("Use esta área para liberar teste, renovar mensalidade, bloquear cliente ou alterar plano.")

            with st.form("form_assinatura_admin"):
                col1, col2 = st.columns(2)
                with col1:
                    novo_plano = st.selectbox("Plano", list(PLANOS_ASSINATURA.keys()), index=list(PLANOS_ASSINATURA.keys()).index(plano_atual) if not assinatura.empty and plano_atual in PLANOS_ASSINATURA else 0, key="ass_novo_plano")
                    novo_status = st.selectbox("Status", STATUS_ASSINATURA, index=STATUS_ASSINATURA.index(status_real) if status_real in STATUS_ASSINATURA else 0, key="ass_status")
                with col2:
                    meses = st.number_input("Adicionar quantos meses?", min_value=1, max_value=36, value=1, step=1, key="ass_meses")
                    observacao = st.text_area("Observação interna", value=ass.get("observacao", "") if not assinatura.empty else "", key="ass_obs")

                if st.form_submit_button("Salvar / Renovar assinatura", use_container_width=True):
                    renovar_assinatura_empresa(novo_plano, int(meses), novo_status)
                    executar(
                        "UPDATE assinaturas SET observacao = ?, atualizado_em = ? WHERE empresa_id = ?",
                        (observacao, datetime.now().isoformat(), empresa_id_atual())
                    )
                    st.success("Assinatura atualizada com sucesso.")
                    st.rerun()

            st.divider()
            st.subheader("Usuários x limite do plano")
            usuarios_conta = consultar(
                "SELECT id, nome, email, tipo, ativo, criado_em FROM usuarios WHERE empresa_id = ? ORDER BY nome ASC",
                (empresa_id_atual(),)
            )
            total_usuarios = len(usuarios_conta)
            st.info(f"Usuários cadastrados: {total_usuarios} de {limite_usuarios} permitidos no plano atual.")
            if total_usuarios > limite_usuarios:
                st.warning("Esta conta possui mais usuários do que o limite contratado. Considere migrar para um plano superior.")
            if not usuarios_conta.empty:
                st.dataframe(usuarios_conta, use_container_width=True, hide_index=True)


    elif menu == "Pix e WhatsApp":
        st.title("📲 Pix e WhatsApp")

        aba1, aba2, aba3 = st.tabs(["Cobrança WhatsApp", "Texto Pix", "IA WhatsApp PF/PJ"])

        with aba1:
            telefone = st.text_input("Telefone com DDD", placeholder="62999999999", key="zap_telefone")
            nome = st.text_input("Nome do cliente", key="zap_nome")
            valor_msg = st.number_input("Valor", min_value=0.0, step=1.0, key="zap_valor")
            venc_msg = st.date_input("Vencimento", value=date.today(), key="zap_vencimento")

            mensagem = st.text_area(
                "Mensagem",
                value="Olá {nome}, tudo bem? Passando para lembrar sobre o pagamento no valor de {valor}, com vencimento em {vencimento}.",
                key="zap_mensagem"
            )

            if st.button("Gerar link WhatsApp", key="btn_zap"):
                texto = mensagem.replace("{nome}", nome)
                texto = texto.replace("{valor}", moeda(valor_msg))
                texto = texto.replace("{vencimento}", venc_msg.strftime("%d/%m/%Y"))

                link = f"https://wa.me/55{telefone}?text={quote(texto)}"
                st.markdown(f"[Abrir WhatsApp]({link})")

        with aba2:
            chave = st.text_input("Chave Pix", key="pix_chave")
            valor_pix = st.number_input("Valor Pix", min_value=0.0, step=1.0, key="pix_valor")
            descricao_pix = st.text_input("Descrição", key="pix_descricao")

            if st.button("Gerar texto Pix", key="btn_pix"):
                texto = f"Olá! Segue cobrança via Pix: Chave: {chave} | Valor: {moeda(valor_pix)} | {descricao_pix}"
                st.code(texto)

        with aba3:
            st.subheader("🤖 IA WhatsApp PF/PJ")
            st.info("Estrutura preparada. Na próxima etapa vamos integrar com n8n e WhatsApp Business Cloud.")

            perfil_ia = st.radio("Perfil da IA", ["Pessoa Física PF", "Pessoa Jurídica PJ"], horizontal=True, key="perfil_ia_whatsapp")

            exemplo = st.text_area(
                "Simule uma mensagem recebida no WhatsApp",
                value="Gastei 85 reais no mercado hoje" if perfil_ia == "Pessoa Física PF" else "Recebi 1500 do cliente João pelo pix",
                key="simulador_ia_whatsapp"
            )

            if st.button("Simular interpretação da IA", key="btn_simular_ia"):
                texto = exemplo.lower()
                valor_detectado = "não identificado"

                import re
                numeros = re.findall(r"\\d+[\\.,]?\\d*", texto)
                if numeros:
                    valor_detectado = numeros[0].replace(".", "").replace(",", ".")

                if perfil_ia == "Pessoa Física PF":
                    if any(palavra in texto for palavra in ["gastei", "paguei", "comprei", "mercado", "lanche", "gasolina"]):
                        tipo_sim = "Despesa"
                    else:
                        tipo_sim = "Receita"

                    st.success(f"PF interpretado: {tipo_sim} pessoal no valor aproximado de R$ {valor_detectado}.")
                else:
                    if any(palavra in texto for palavra in ["recebi", "venda", "cliente", "entrada"]):
                        tipo_sim = "Receita"
                    else:
                        tipo_sim = "Despesa"

                    st.success(f"PJ interpretado: {tipo_sim} empresarial no valor aproximado de R$ {valor_detectado}.")

    elif menu == "Relatórios":
        st.title("📄 Relatórios e Exportações")

        pdf = gerar_pdf_relatorio(df, ind)

        if pdf is None:
            st.warning("Biblioteca reportlab não instalada. Confira o requirements.txt.")
        else:
            st.download_button("Baixar relatório PDF", data=pdf, file_name="relatorio_financeiro.pdf", mime="application/pdf", key="download_pdf")

        if not df.empty:
            st.download_button("Baixar lançamentos CSV", data=df.to_csv(index=False).encode("utf-8"), file_name="lancamentos.csv", mime="text/csv", key="download_csv_lancamentos")

        if not clientes.empty:
            st.download_button("Baixar clientes CSV", data=clientes.to_csv(index=False).encode("utf-8"), file_name="clientes.csv", mime="text/csv", key="download_csv_clientes")

        if not estoque.empty:
            st.download_button("Baixar estoque CSV", data=estoque.to_csv(index=False).encode("utf-8"), file_name="estoque.csv", mime="text/csv", key="download_csv_estoque")

        if not funcionarios.empty:
            st.download_button("Baixar funcionários CSV", data=funcionarios.to_csv(index=False).encode("utf-8"), file_name="funcionarios.csv", mime="text/csv", key="download_csv_funcionarios")

        if not folha.empty:
            st.download_button("Baixar folha CSV", data=folha.to_csv(index=False).encode("utf-8"), file_name="folha_pagamento.csv", mime="text/csv", key="download_csv_folha")

    elif menu == "IA Financeira":
        st.title("🤖 IA Financeira")

        if df.empty:
            st.info("Cadastre lançamentos para receber uma análise.")
        else:
            if ind["lucro"] < 0:
                html('<div class="danger-box">A conta está com resultado negativo. Revise despesas, custos, folha de pagamento e inadimplência.</div>')
            elif ind["vencidas"] > 0:
                html('<div class="warning-box">Existem contas vencidas ou recebimentos atrasados. Priorize cobrança e renegociação.</div>')
            else:
                html('<div class="success-box">O controle está saudável. Continue acompanhando caixa, estoque, folha e metas.</div>')

            st.write(f"**Receita:** {moeda(ind['receita'])}")
            st.write(f"**Saídas:** {moeda(ind['saidas'])}")
            st.write(f"**Lucro:** {moeda(ind['lucro'])}")
            st.write(f"**Contas pagas no mês:** {moeda(ind['pagas_mes'])}")
            st.write(f"**A receber:** {moeda(ind['receber'])}")
            st.write(f"**Vencidas:** {moeda(ind['vencidas'])}")

            pergunta = st.text_area("Pergunte algo sobre a situação financeira", key="ia_financeira_pergunta")

            if st.button("Analisar", key="btn_ia_financeira"):
                resposta = responder_ajuda(pergunta)
                st.info(resposta)

    elif menu == "Ajuda / Tutorial":
        st.title("🆘 Ajuda / Tutorial do Sistema")

        st.markdown("""
### Como usar o sistema

**1. Dashboard**  
Mostra os principais indicadores da conta.

**2. Entradas e Saídas**  
Cadastre receitas, despesas, custos, dívidas, investimentos e retiradas.

**3. Contas Pagas no Mês**  
Veja tudo que foi pago ou recebido no mês selecionado.

**4. Clientes / CRM**  
No PJ, use para clientes e fornecedores. No PF, use para contatos financeiros pessoais.

**5. Clientes Inadimplentes**  
Mostra receitas vencidas.

**6. Estoque**  
No PJ, controle produtos. No PF, pode usar para bens pessoais.

**7. Funcionários / Folha**  
Mais indicado para PJ.

**8. Metas e Premiações**  
No PJ, metas de equipe. No PF, futuramente metas pessoais.

**9. Pix e WhatsApp**  
Gere mensagens e simule IA WhatsApp PF/PJ.

**10. Planejamento Financeiro**  
Cadastre previsto x realizado, metas, dívidas, investimentos e reserva.

**11. Assinaturas / Planos**  
Controle plano, status, vencimento, mensalidade, limite de usuários e renovação pelo WhatsApp.

**12. Relatórios**  
Baixe PDF e planilhas CSV.

**13. Dados de exemplo**  
Vá em **Configurações** e clique em **Carregar dados de exemplo** para apresentar o sistema bonito para clientes.
""")

        st.divider()
        st.subheader("🤖 IA de Ajuda do Sistema")

        pergunta = st.text_area(
            "Digite sua dúvida",
            placeholder="Exemplo: como cadastrar lançamento? como ver inadimplentes? como lançar folha de pagamento?",
            key="pergunta_ajuda_sistema"
        )

        if st.button("Perguntar para IA de ajuda", use_container_width=True, key="btn_ia_ajuda"):
            if pergunta.strip():
                st.success(responder_ajuda(pergunta))
            else:
                st.warning("Digite sua dúvida para a IA responder.")

    elif menu == "Apresentação Comercial":
        st.title("🚀 Apresentação Comercial")
        tela_apresentacao_comercial()

    elif menu == "Usuários":
        st.title("👤 Usuários e Permissões")

        if tipo_usuario_atual() != "Administrador":
            st.warning("Somente administrador pode acessar esta área.")
        else:
            st.subheader("Criar novo usuário")

            with st.form("form_usuario"):
                col1, col2 = st.columns(2)

                with col1:
                    nome = st.text_input("Nome do usuário", key="user_nome")
                    email = st.text_input("E-mail", key="user_email")
                    senha = st.text_input("Senha", type="password", key="user_senha")

                with col2:
                    tipo_user = st.selectbox("Tipo de usuário", TIPOS_USUARIO, key="user_tipo")
                    ativo = st.checkbox("Usuário ativo", value=True, key="user_ativo")

                if st.form_submit_button("Criar usuário", use_container_width=True):
                    if not nome or not email or not senha:
                        st.warning("Preencha nome, e-mail e senha.")
                    else:
                        try:
                            executar(
                                """
                                INSERT INTO usuarios
                                (empresa_id, nome, email, senha_hash, tipo, ativo, criado_em)
                                VALUES (?, ?, ?, ?, ?, ?, ?)
                                """,
                                (empresa_id_atual(), nome, email, hash_senha(senha), tipo_user, int(ativo), datetime.now().isoformat())
                            )
                            st.success("Usuário criado com sucesso.")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Erro ao criar usuário: {e}")

            usuarios = consultar(
                """
                SELECT id, nome, email, tipo, ativo, criado_em
                FROM usuarios
                WHERE empresa_id = ?
                ORDER BY id DESC
                """,
                (empresa_id_atual(),)
            )

            if usuarios.empty:
                st.info("Nenhum usuário cadastrado.")
            else:
                st.dataframe(usuarios, use_container_width=True, hide_index=True)

    elif menu == "Configurações":
        st.title("⚙️ Configurações")

        empresa = consultar("SELECT * FROM empresas WHERE id = ?", (empresa_id_atual(),))

        if empresa.empty:
            st.error("Conta não encontrada.")
        else:
            emp = empresa.iloc[0]
            tipo_conta = emp["tipo_pessoa"] if "tipo_pessoa" in emp.index and emp["tipo_pessoa"] else "PJ"

            st.info(f"Tipo da conta: {'Pessoa Física PF' if tipo_conta == 'PF' else 'Pessoa Jurídica PJ'}")

            nome = st.text_input("Nome da conta", value=emp["nome"], key="conf_nome")
            documento_label = "CPF" if tipo_conta == "PF" else "CNPJ / CPF"
            documento = st.text_input(documento_label, value=emp["documento"] or "", key="conf_doc")
            telefone = st.text_input("Telefone", value=emp["telefone"] or "", key="conf_tel")
            cidade = st.text_input("Cidade", value=emp["cidade"] or "", key="conf_cidade")

            if st.button("Salvar configurações", key="btn_conf"):
                executar(
                    """
                    UPDATE empresas
                    SET nome = ?, documento = ?, telefone = ?, cidade = ?
                    WHERE id = ?
                    """,
                    (nome, documento, telefone, cidade, empresa_id_atual())
                )
                st.success("Configurações atualizadas.")
                st.rerun()

        st.divider()
        st.subheader("📥 Dados de exemplo para demonstração")

        if existe_dados_exemplo():
            st.info("Os dados de exemplo já estão carregados. Agora o Dashboard, gráficos, clientes, estoque, folha e metas já aparecem preenchidos.")
        else:
            st.warning("Nenhum dado de exemplo carregado. Clique no botão abaixo para preencher o sistema automaticamente.")

        col_demo1, col_demo2 = st.columns(2)

        with col_demo1:
            if st.button("📥 Carregar dados de exemplo", use_container_width=True, key="btn_carregar_demo"):
                ok, msg = carregar_dados_exemplo()
                if ok:
                    st.success(msg)
                else:
                    st.warning(msg)
                st.rerun()

        with col_demo2:
            if st.button("🧹 Limpar dados de exemplo", use_container_width=True, key="btn_limpar_demo"):
                ok, msg = limpar_dados_exemplo()
                if ok:
                    st.success(msg)
                else:
                    st.warning(msg)
                st.rerun()

        st.caption("A limpeza remove somente os dados marcados como demonstração. Dados reais cadastrados sem a marca demo não serão apagados.")

        st.divider()
        st.subheader("Backup local")

        backup = {
            "conta": usuario["empresa_nome"],
            "tipo_pessoa": usuario.get("tipo_pessoa", "PJ"),
            "lancamentos": df.to_dict(orient="records") if not df.empty else [],
            "clientes": clientes.to_dict(orient="records") if not clientes.empty else [],
            "estoque": estoque.to_dict(orient="records") if not estoque.empty else [],
            "funcionarios": funcionarios.to_dict(orient="records") if not funcionarios.empty else [],
            "folha": folha.to_dict(orient="records") if not folha.empty else [],
            "metas": metas.to_dict(orient="records") if not metas.empty else [],
            "planejamento": planejamento.to_dict(orient="records") if not planejamento.empty else [],
            "assinatura": assinatura.to_dict(orient="records") if not assinatura.empty else [],
            "gerado_em": datetime.now().isoformat()
        }

        st.download_button(
            "Baixar backup JSON",
            data=json.dumps(backup, ensure_ascii=False, indent=4, default=str),
            file_name="backup_sistema_financeiro_completo.json",
            mime="application/json",
            key="download_backup_json"
        )


# =====================================================
# INICIAR SISTEMA
# =====================================================

criar_tabelas()
criar_admin_padrao()

if "usuario" in st.session_state:
    app()
else:
    if "tela_login_ativa" not in st.session_state:
        st.session_state.tela_login_ativa = False

    if st.session_state.tela_login_ativa:
        tela_login()
    else:
        tela_publica_comercial()
