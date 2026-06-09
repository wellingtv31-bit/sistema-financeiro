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
    page_title="Sistema Financeiro Premium",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed"
)

DB_PATH = "sistema_financeiro.db"


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
# CSS PREMIUM PRETO + DOURADO
# =====================================================

st.markdown(
    """
    <style>
    #MainMenu, footer, header {
        visibility: hidden;
    }

    :root {
        --gold: #d4af37;
        --gold-light: #f7df8a;
        --gold-soft: #f3e3ad;
        --gold-dark: #9f7418;
        --dark: #020617;
        --panel: rgba(8, 20, 35, 0.90);
        --panel2: rgba(4, 14, 26, 0.96);
        --border: rgba(212, 175, 55, 0.32);
    }

    .stApp {
        background:
            radial-gradient(circle at top left, rgba(212,175,55,0.14), transparent 34%),
            radial-gradient(circle at bottom right, rgba(212,175,55,0.08), transparent 32%),
            linear-gradient(135deg, #020617 0%, #071526 42%, #020617 100%);
        color: var(--gold-soft);
    }

    .block-container {
        padding-top: 1.4rem;
        padding-bottom: 2rem;
        padding-left: 1.5rem;
        padding-right: 1.5rem;
        max-width: 1360px;
    }

    h1, h2, h3, h4 {
        color: var(--gold) !important;
        font-weight: 950 !important;
        letter-spacing: -0.4px;
        text-shadow: 0 0 18px rgba(212,175,55,0.12);
    }

    p, label, span, div {
        color: var(--gold-soft);
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(2,6,23,0.99), rgba(7,21,38,0.99));
        border-right: 1px solid rgba(212,175,55,0.26);
    }

    section[data-testid="stSidebar"] * {
        color: var(--gold-soft) !important;
    }

    section[data-testid="stSidebar"] img {
        border-radius: 18px;
        border: 1px solid rgba(212,175,55,0.34);
        box-shadow: 0 12px 28px rgba(0,0,0,0.34);
        margin-bottom: 12px;
    }

    .public-topbar {
        width: 100%;
        border-radius: 24px;
        padding: 18px 22px;
        margin-bottom: 22px;
        background:
            linear-gradient(135deg, rgba(8,20,35,0.94), rgba(3,10,20,0.98));
        border: 1px solid rgba(212,175,55,0.30);
        box-shadow: 0 18px 45px rgba(0,0,0,0.30);
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 18px;
        flex-wrap: wrap;
    }

    .public-brand {
        display: flex;
        align-items: center;
        gap: 14px;
    }

    .public-brand-logo {
        width: 56px;
        height: 56px;
        border-radius: 16px;
        border: 1px solid rgba(212,175,55,0.35);
        background: rgba(2,6,23,0.72);
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
    }

    .public-brand-logo img {
        width: 100%;
        height: 100%;
        object-fit: contain;
        padding: 4px;
    }

    .public-brand-title {
        font-size: 22px;
        font-weight: 950;
        color: var(--gold);
        line-height: 1.1;
    }

    .public-brand-subtitle {
        font-size: 13px;
        color: #eadba6;
        margin-top: 3px;
    }

    .public-badge {
        padding: 10px 14px;
        border-radius: 999px;
        background: rgba(212,175,55,0.14);
        border: 1px solid rgba(212,175,55,0.34);
        color: #fff1bd;
        font-size: 13px;
        font-weight: 900;
    }

    .public-hero {
        border-radius: 34px;
        padding: 44px;
        margin-bottom: 26px;
        background:
            radial-gradient(circle at top right, rgba(212,175,55,0.18), transparent 38%),
            radial-gradient(circle at bottom left, rgba(212,175,55,0.08), transparent 36%),
            linear-gradient(135deg, rgba(8,20,35,0.96), rgba(3,10,20,0.98));
        border: 1px solid rgba(212,175,55,0.34);
        box-shadow: 0 30px 80px rgba(0,0,0,0.40), inset 0 0 28px rgba(212,175,55,0.04);
    }

    .public-tag {
        display: inline-block;
        padding: 9px 14px;
        border-radius: 999px;
        background: rgba(212,175,55,0.16);
        border: 1px solid rgba(212,175,55,0.34);
        color: #fff1bd;
        font-weight: 900;
        font-size: 13px;
        margin-bottom: 16px;
    }

    .public-title {
        font-size: 52px;
        font-weight: 950;
        color: var(--gold);
        line-height: 1.04;
        margin-bottom: 18px;
        max-width: 1060px;
    }

    .public-subtitle {
        font-size: 19px;
        color: #f4e8bd;
        max-width: 1000px;
        line-height: 1.65;
        margin-bottom: 28px;
    }

    .public-highlight-row {
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
        margin-top: 18px;
    }

    .public-highlight {
        padding: 12px 16px;
        border-radius: 18px;
        background: rgba(15,23,42,0.82);
        border: 1px solid rgba(212,175,55,0.28);
        color: #fff1bd;
        font-size: 14px;
        font-weight: 850;
    }

    .login-header {
        width: 100%;
        text-align: center;
        margin-bottom: 24px;
        padding: 8px 0 4px 0;
    }

    .login-title {
        font-size: 46px;
        font-weight: 950;
        color: var(--gold);
        margin-bottom: 10px;
        line-height: 1.05;
        text-shadow: 0 0 22px rgba(212,175,55,0.20);
    }

    .login-subtitle {
        font-size: 16px;
        max-width: 900px;
        margin: 0 auto;
        color: #eadba6;
        line-height: 1.6;
    }

    .login-info {
        margin: 18px auto 28px auto;
        max-width: 980px;
        background: linear-gradient(90deg, rgba(212,175,55,0.20), rgba(212,175,55,0.08));
        border: 1px solid rgba(212,175,55,0.38);
        border-radius: 18px;
        padding: 14px 18px;
        text-align: center;
        color: #fff3c4;
        font-size: 15px;
        box-shadow: 0 10px 26px rgba(0,0,0,0.28), inset 0 0 18px rgba(212,175,55,0.04);
    }

    .hero-box {
        min-height: 445px;
        border-radius: 28px;
        border: 1px solid rgba(212,175,55,0.32);
        background:
            linear-gradient(180deg, rgba(2,6,23,0.22), rgba(2,6,23,0.80)),
            linear-gradient(135deg, rgba(212,175,55,0.10), rgba(212,175,55,0.03));
        box-shadow: 0 26px 70px rgba(0,0,0,0.40);
        overflow: hidden;
        position: relative;
        display: flex;
        align-items: stretch;
        justify-content: center;
    }

    .hero-inner {
        width: 100%;
        display: flex;
        align-items: end;
        justify-content: start;
        background-size: contain !important;
        background-repeat: no-repeat !important;
        background-position: center center !important;
        background-color: rgba(2, 6, 23, 0.76);
        position: relative;
    }

    .hero-overlay {
        position: absolute;
        inset: 0;
        background:
            linear-gradient(180deg, rgba(2,6,23,0.02), rgba(2,6,23,0.58)),
            linear-gradient(90deg, rgba(2,6,23,0.36), rgba(2,6,23,0.04));
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
        color: var(--gold) !important;
    }

    .hero-content p {
        margin: 0;
        color: #f4e8bd !important;
        font-size: 15px;
        line-height: 1.65;
    }

    .logo-box {
        min-height: 445px;
        border-radius: 28px;
        border: 1px solid rgba(212,175,55,0.34);
        background:
            radial-gradient(circle at center, rgba(212,175,55,0.08), transparent 56%),
            linear-gradient(180deg, rgba(2,6,23,0.40), rgba(2,6,23,0.82));
        box-shadow: 0 26px 70px rgba(0,0,0,0.40), inset 0 0 30px rgba(212,175,55,0.04);
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
        filter: drop-shadow(0 20px 34px rgba(0,0,0,0.34)) drop-shadow(0 0 18px rgba(212,175,55,0.12));
    }

    .form-box,
    .app-header,
    .menu-panel,
    .page-panel,
    .commercial-panel {
        border-radius: 28px;
        border: 1px solid rgba(212,175,55,0.28);
        background: linear-gradient(180deg, rgba(8,20,35,0.90), rgba(4,14,26,0.94));
        box-shadow: 0 26px 70px rgba(0,0,0,0.34), inset 0 0 20px rgba(212,175,55,0.03);
    }

    .form-box {
        margin-top: 28px;
        padding: 30px;
    }

    .app-header {
        padding: 28px 30px;
        margin-bottom: 20px;
        background:
            linear-gradient(135deg, rgba(8,20,35,0.94), rgba(3,10,20,0.98)),
            radial-gradient(circle at top right, rgba(212,175,55,0.18), transparent 36%);
    }

    .app-header-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 18px;
        flex-wrap: wrap;
    }

    .app-title {
        font-size: 35px;
        font-weight: 950;
        color: var(--gold);
        line-height: 1.1;
        margin-bottom: 6px;
    }

    .app-subtitle {
        font-size: 15px;
        color: #eadba6;
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
        background: rgba(15,23,42,0.82);
        border: 1px solid rgba(212,175,55,0.30);
        color: #f7e7b2;
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
        color: var(--gold);
        margin-bottom: 12px;
    }

    .page-panel {
        padding: 24px;
        margin-bottom: 22px;
    }

    .commercial-panel {
        padding: 32px;
        margin-bottom: 22px;
    }

    .commercial-hero {
        padding: 36px;
        border-radius: 30px;
        border: 1px solid rgba(212,175,55,0.34);
        background:
            radial-gradient(circle at top right, rgba(212,175,55,0.18), transparent 38%),
            linear-gradient(135deg, rgba(8,20,35,0.96), rgba(3,10,20,0.98));
        box-shadow: 0 28px 75px rgba(0,0,0,0.38), inset 0 0 24px rgba(212,175,55,0.04);
        margin-bottom: 24px;
    }

    .commercial-title {
        font-size: 44px;
        font-weight: 950;
        color: var(--gold);
        line-height: 1.08;
        margin-bottom: 12px;
    }

    .commercial-subtitle {
        font-size: 18px;
        color: #f4e8bd;
        max-width: 980px;
        line-height: 1.6;
    }

    .commercial-tag {
        display: inline-block;
        padding: 9px 14px;
        border-radius: 999px;
        background: rgba(212,175,55,0.16);
        border: 1px solid rgba(212,175,55,0.34);
        color: #fff1bd;
        font-weight: 900;
        font-size: 13px;
        margin-bottom: 14px;
    }

    .commercial-card {
        min-height: 165px;
        border-radius: 24px;
        padding: 24px;
        background:
            radial-gradient(circle at top right, rgba(212,175,55,0.10), transparent 42%),
            linear-gradient(145deg, rgba(10,25,45,0.98), rgba(5,15,28,0.98));
        border: 1px solid rgba(212,175,55,0.28);
        box-shadow: 0 16px 38px rgba(0,0,0,0.32), inset 0 0 18px rgba(212,175,55,0.03);
    }

    .commercial-card-title {
        color: var(--gold);
        font-size: 20px;
        font-weight: 950;
        margin-bottom: 10px;
    }

    .commercial-card-text {
        color: #eadba6;
        font-size: 15px;
        line-height: 1.55;
    }

    .price-card {
        min-height: 230px;
        border-radius: 26px;
        padding: 26px;
        background:
            linear-gradient(180deg, rgba(8,20,35,0.96), rgba(4,14,26,0.98));
        border: 1px solid rgba(212,175,55,0.32);
        box-shadow: 0 18px 44px rgba(0,0,0,0.34);
    }

    .price-title {
        font-size: 22px;
        font-weight: 950;
        color: var(--gold);
        margin-bottom: 8px;
    }

    .price-value {
        font-size: 32px;
        font-weight: 950;
        color: #fff1bd;
        margin-bottom: 8px;
    }

    .price-desc {
        font-size: 14px;
        color: #eadba6;
        line-height: 1.5;
    }

    .metric-card {
        background:
            radial-gradient(circle at top right, rgba(212,175,55,0.10), transparent 42%),
            linear-gradient(145deg, rgba(10,25,45,0.98), rgba(5,15,28,0.98));
        border-radius: 24px;
        padding: 24px;
        box-shadow: 0 16px 38px rgba(0,0,0,0.36), inset 0 0 18px rgba(212,175,55,0.03);
        border: 1px solid rgba(212,175,55,0.28);
        border-left: 7px solid var(--gold);
        min-height: 130px;
    }

    .metric-title {
        color: var(--gold);
        font-size: 14px;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .metric-value {
        color: #fff1bd;
        font-size: 30px;
        font-weight: 950;
        margin-top: 6px;
    }

    .metric-sub {
        color: #eadba6;
        font-size: 13px;
        margin-top: 3px;
    }

    .section-title {
        font-size: 27px;
        font-weight: 950;
        color: var(--gold);
        margin-bottom: 8px;
    }

    .section-subtitle {
        color: #eadba6;
        font-size: 15px;
        margin-bottom: 18px;
    }

    .success-box {
        background: rgba(16, 185, 129, 0.13);
        border-left: 6px solid #10b981;
        padding: 14px 18px;
        border-radius: 16px;
        color: #d1fae5;
    }

    .warning-box {
        background: rgba(245, 158, 11, 0.14);
        border-left: 6px solid #f59e0b;
        padding: 14px 18px;
        border-radius: 16px;
        color: #fef3c7;
    }

    .danger-box {
        background: rgba(239, 68, 68, 0.14);
        border-left: 6px solid #ef4444;
        padding: 14px 18px;
        border-radius: 16px;
        color: #fee2e2;
    }

    .stTextInput input,
    .stNumberInput input,
    .stDateInput input,
    .stTextArea textarea {
        border-radius: 15px !important;
        border: 1px solid rgba(212,175,55,0.34) !important;
        background: rgba(15, 23, 42, 0.96) !important;
        color: #fff1bd !important;
        box-shadow: inset 0 0 12px rgba(0,0,0,0.20);
    }

    .stTextArea textarea {
        min-height: 110px !important;
    }

    .stTextInput input::placeholder,
    .stTextArea textarea::placeholder {
        color: #bfa96a !important;
    }

    .stSelectbox div[data-baseweb="select"] > div {
        border-radius: 15px !important;
        background: rgba(15, 23, 42, 0.96) !important;
        border: 1px solid rgba(212,175,55,0.34) !important;
        color: #fff1bd !important;
        min-height: 44px;
    }

    .stSelectbox span,
    div[data-baseweb="select"] * {
        color: #fff1bd !important;
    }

    div[data-testid="stSelectbox"] label,
    div[data-testid="stSelectbox"] label p {
        color: #d4af37 !important;
        font-weight: 900 !important;
    }

    div[data-baseweb="popover"] {
        background: transparent !important;
    }

    div[data-baseweb="menu"],
    ul[role="listbox"],
    div[role="listbox"] {
        background: #030a14 !important;
        border: 1px solid rgba(212,175,55,0.42) !important;
        border-radius: 16px !important;
        box-shadow: 0 18px 45px rgba(0,0,0,0.65) !important;
        padding: 8px !important;
    }

    div[data-baseweb="menu"] *,
    ul[role="listbox"] *,
    div[role="listbox"] * {
        background-color: #030a14 !important;
        color: #f7df8a !important;
        font-weight: 850 !important;
    }

    li[role="option"],
    div[role="option"] {
        background: #030a14 !important;
        background-color: #030a14 !important;
        color: #f7df8a !important;
        font-weight: 850 !important;
        border-radius: 12px !important;
        border: 1px solid transparent !important;
    }

    li[role="option"] *,
    div[role="option"] * {
        background: transparent !important;
        background-color: transparent !important;
        color: #f7df8a !important;
    }

    li[role="option"]:hover,
    div[role="option"]:hover,
    li[role="option"]:focus,
    div[role="option"]:focus {
        background: rgba(212,175,55,0.18) !important;
        background-color: rgba(212,175,55,0.18) !important;
        color: #fff1bd !important;
        border: 1px solid rgba(212,175,55,0.32) !important;
    }

    li[aria-selected="true"],
    div[aria-selected="true"],
    li[role="option"][aria-selected="true"],
    div[role="option"][aria-selected="true"] {
        background: linear-gradient(90deg, rgba(212,175,55,0.28), rgba(212,175,55,0.12)) !important;
        background-color: rgba(212,175,55,0.22) !important;
        color: #fff1bd !important;
        border: 1px solid rgba(212,175,55,0.42) !important;
    }

    li[aria-selected="true"] *,
    div[aria-selected="true"] * {
        color: #fff1bd !important;
        background: transparent !important;
        background-color: transparent !important;
    }

    .stButton > button {
        background: linear-gradient(90deg, #9f7418, #d4af37, #f0d878);
        color: #111827 !important;
        border: none;
        border-radius: 15px;
        padding: 0.74rem 1rem;
        font-weight: 950;
        box-shadow: 0 12px 28px rgba(212,175,55,0.20), inset 0 0 10px rgba(255,255,255,0.10);
        transition: all 0.18s ease-in-out;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        background: linear-gradient(90deg, #d4af37, #f0d878, #fff0a8);
        color: #111827 !important;
        box-shadow: 0 14px 32px rgba(212,175,55,0.28);
    }

    .stDownloadButton > button {
        background: linear-gradient(90deg, #9f7418, #d4af37, #f0d878);
        color: #111827 !important;
        border: none;
        border-radius: 15px;
        padding: 0.74rem 1rem;
        font-weight: 950;
    }

    div[data-testid="stDataFrame"] {
        background: rgba(8, 20, 35, 0.92);
        border-radius: 20px;
        padding: 8px;
        border: 1px solid rgba(212,175,55,0.22);
        box-shadow: 0 14px 34px rgba(0,0,0,0.24);
    }

    div[role="radiogroup"] {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
    }

    div[role="radiogroup"] label {
        background: rgba(15,23,42,0.88) !important;
        border: 1px solid rgba(212,175,55,0.28) !important;
        border-radius: 999px !important;
        padding: 10px 14px !important;
        margin: 0 !important;
        color: #fff1bd !important;
        font-weight: 850 !important;
        box-shadow: inset 0 0 12px rgba(212,175,55,0.03);
    }

    div[role="radiogroup"] label:hover {
        background: rgba(212,175,55,0.16) !important;
        border: 1px solid rgba(212,175,55,0.45) !important;
    }

    div[role="radiogroup"] label * {
        color: #fff1bd !important;
        font-weight: 850 !important;
    }

    button[data-baseweb="tab"] {
        font-size: 15px !important;
        font-weight: 900 !important;
        color: #eadba6 !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: var(--gold) !important;
        border-bottom: 2px solid var(--gold) !important;
    }

    div[data-testid="stAlert"] {
        background: rgba(15, 23, 42, 0.90);
        color: #fff1bd;
        border-radius: 16px;
        border: 1px solid rgba(212,175,55,0.22);
    }

    div[data-testid="stAlert"] * {
        color: #fff1bd !important;
    }

    @media (max-width: 900px) {
        .login-title {
            font-size: 34px;
        }

        .hero-box, .logo-box {
            min-height: 300px;
        }

        .form-box {
            padding: 20px;
        }

        .hero-content h3,
        .commercial-title {
            font-size: 28px;
        }

        .public-title {
            font-size: 34px;
        }

        .public-hero {
            padding: 28px;
        }

        .app-title {
            font-size: 26px;
        }

        .app-badges {
            justify-content: flex-start;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)


# =====================================================
# FUNÇÕES BÁSICAS
# =====================================================

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


def dias_para_vencimento(vencimento):
    try:
        venc = pd.to_datetime(vencimento).date()
        return (venc - date.today()).days
    except Exception:
        return 0


def status_automatico(status, vencimento):
    if status in ["Pago", "Recebido"]:
        return status

    dias = dias_para_vencimento(vencimento)

    if dias < 0:
        return "Vencido"

    if dias == 0:
        return "Vence hoje"

    return "Pendente"


def card(titulo, valor, subtitulo=""):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">{titulo}</div>
            <div class="metric-value">{valor}</div>
            <div class="metric-sub">{subtitulo}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def comercial_card(titulo, texto):
    st.markdown(
        f"""
        <div class="commercial-card">
            <div class="commercial-card-title">{titulo}</div>
            <div class="commercial-card-text">{texto}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def preco_card(titulo, valor, texto):
    st.markdown(
        f"""
        <div class="price-card">
            <div class="price-title">{titulo}</div>
            <div class="price-value">{valor}</div>
            <div class="price-desc">{texto}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def cabecalho_interno(menu_atual):
    usuario = st.session_state.usuario

    st.markdown(
        f"""
        <div class="app-header">
            <div class="app-header-top">
                <div>
                    <div class="app-title">Bem-vindo ao painel financeiro</div>
                    <div class="app-subtitle">
                        Área atual: <b>{menu_atual}</b>. Controle sua empresa com visão clara, segura e profissional.
                    </div>
                </div>
                <div class="app-badges">
                    <div class="app-badge">Empresa: {usuario['empresa_nome']}</div>
                    <div class="app-badge">Usuário: {usuario['nome']}</div>
                    <div class="app-badge">Perfil: {usuario['tipo']}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =====================================================
# BANCO DE DADOS
# =====================================================

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
            criado_em TEXT
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

    con.commit()
    con.close()


def criar_admin_padrao():
    empresas = consultar("SELECT * FROM empresas")

    if empresas.empty:
        executar(
            """
            INSERT INTO empresas (nome, documento, telefone, cidade, criado_em)
            VALUES (?, ?, ?, ?, ?)
            """,
            ("Global Software", "", "", "", datetime.now().isoformat())
        )

    empresa = consultar("SELECT id FROM empresas ORDER BY id ASC LIMIT 1").iloc[0]["id"]

    admin = consultar(
        "SELECT * FROM usuarios WHERE email = ?",
        ("admin@empresa.com",)
    )

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


# =====================================================
# DADOS FIXOS
# =====================================================

TIPOS_USUARIO = [
    "Administrador",
    "Gerente",
    "Financeiro",
    "Vendedor"
]

TIPOS_LANCAMENTO = {
    "Receita": [
        "Venda",
        "Serviço",
        "Comissão",
        "Entrada",
        "Recebimento de parcela",
        "Outras receitas"
    ],
    "Custo": [
        "Produto vendido",
        "Fornecedor",
        "Matéria-prima",
        "Frete de compra",
        "Taxa de cartão",
        "Comissão paga"
    ],
    "Despesa fixa": [
        "Aluguel",
        "Internet",
        "Sistema",
        "Funcionário",
        "Contador",
        "Telefone",
        "MEI / Imposto fixo"
    ],
    "Despesa variável": [
        "Energia",
        "Água",
        "Marketing",
        "Manutenção",
        "Transporte",
        "Alimentação",
        "Outras despesas"
    ],
    "Investimento": [
        "Equipamento",
        "Curso",
        "Ferramenta",
        "Reforma",
        "Estoque",
        "Publicidade estratégica"
    ],
    "Dívida": [
        "Empréstimo",
        "Financiamento",
        "Cartão de crédito",
        "Juros",
        "Parcela de dívida"
    ],
    "Retirada do dono": [
        "Pró-labore",
        "Saque pessoal",
        "Distribuição de lucro"
    ]
}

FORMAS_PAGAMENTO = [
    "Dinheiro",
    "Pix",
    "Cartão de débito",
    "Cartão de crédito",
    "Boleto",
    "Transferência",
    "Promissória",
    "Outro"
]

CONTAS = [
    "Caixa",
    "Banco",
    "Conta digital",
    "Carteira",
    "Cartão",
    "Outro"
]

STATUS_OPCOES = [
    "Pendente",
    "Pago",
    "Recebido"
]


# =====================================================
# TELA PÚBLICA COMERCIAL
# =====================================================

def tela_publica_comercial():
    logo_html = ""

    if logo_base64:
        logo_html = f'<img src="data:image/png;base64,{logo_base64}">'
    else:
        logo_html = '<div style="font-weight:950;color:#d4af37;">GS</div>'

    st.markdown(
        f"""
        <div class="public-topbar">
            <div class="public-brand">
                <div class="public-brand-logo">{logo_html}</div>
                <div>
                    <div class="public-brand-title">Global Software</div>
                    <div class="public-brand-subtitle">Sistema Financeiro Premium para empresas</div>
                </div>
            </div>
            <div class="public-badge">Apresentação comercial pública</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="public-hero">
            <div class="public-tag">GESTÃO FINANCEIRA • CRM • ESTOQUE • RELATÓRIOS</div>
            <div class="public-title">Sua empresa ainda controla dinheiro no caderno, no WhatsApp ou em planilhas bagunçadas?</div>
            <div class="public-subtitle">
                O Sistema Financeiro Premium da Global Software organiza entradas, saídas, parcelas,
                contas a pagar, contas a receber, clientes, estoque, relatórios e usuários em uma plataforma moderna,
                visual e profissional.
            </div>
            <div class="public-highlight-row">
                <div class="public-highlight">✅ Dashboard financeiro</div>
                <div class="public-highlight">✅ Controle de parcelas</div>
                <div class="public-highlight">✅ CRM de clientes</div>
                <div class="public-highlight">✅ Estoque</div>
                <div class="public-highlight">✅ Relatórios PDF</div>
                <div class="public-highlight">✅ Usuários com permissões</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    col_login, col_whats = st.columns([1, 1])

    with col_login:
        if st.button("Acessar área do sistema", use_container_width=True, key="btn_ir_login_publico"):
            st.session_state.tela_login_ativa = True
            st.rerun()

    with col_whats:
        texto_demo = (
            "Olá! Quero uma demonstração do Sistema Financeiro Premium da Global Software. "
            "Tenho interesse em organizar melhor as finanças da minha empresa."
        )
        telefone_global = st.text_input(
            "Seu WhatsApp para demonstração",
            placeholder="62999999999",
            key="telefone_publico"
        )

        if st.button("Solicitar demonstração pelo WhatsApp", use_container_width=True, key="btn_demo_publico"):
            if telefone_global:
                link = f"https://wa.me/55{telefone_global}?text={quote(texto_demo)}"
                st.markdown(f"[Abrir WhatsApp para solicitar demonstração]({link})")
            else:
                st.warning("Digite o telefone com DDD para gerar o link.")

    st.write("")

    c1, c2, c3 = st.columns(3)

    with c1:
        comercial_card(
            "O problema",
            "Muitas empresas vendem, mas não sabem quanto realmente lucram, quais contas estão vencidas e quanto têm a receber."
        )

    with c2:
        comercial_card(
            "A solução",
            "O sistema reúne controle financeiro, clientes, estoque, parcelas e relatórios em uma única plataforma profissional."
        )

    with c3:
        comercial_card(
            "O resultado",
            "Mais clareza, menos perda de dinheiro, melhor tomada de decisão e uma empresa preparada para crescer."
        )

    st.write("")

    st.markdown('<div class="commercial-panel">', unsafe_allow_html=True)
    st.markdown("## 💼 O que o sistema entrega")

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        comercial_card("Dashboard", "Indicadores de receita, despesas, lucro, caixa, contas vencidas, a pagar e a receber.")

    with m2:
        comercial_card("Financeiro completo", "Controle de receitas, custos, despesas fixas, variáveis, dívidas, investimentos e retiradas.")

    with m3:
        comercial_card("Parcelas", "Cadastro de lançamentos parcelados com vencimentos automáticos e acompanhamento.")

    with m4:
        comercial_card("Relatórios", "Geração de relatórios em PDF e CSV para análise e prestação de contas.")

    st.write("")

    m5, m6, m7, m8 = st.columns(4)

    with m5:
        comercial_card("CRM / Clientes", "Cadastro de clientes, fornecedores, telefone, documentos e observações.")

    with m6:
        comercial_card("Estoque", "Controle de produtos, quantidade, custo, preço de venda e fornecedor.")

    with m7:
        comercial_card("Usuários", "Permissões para administrador, gerente, financeiro e vendedor.")

    with m8:
        comercial_card("WhatsApp", "Geração de mensagens e links de cobrança para facilitar o atendimento.")

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="commercial-panel">', unsafe_allow_html=True)
    st.markdown("## 🎯 Para quem é indicado?")

    p1, p2, p3 = st.columns(3)

    with p1:
        comercial_card(
            "Pequenas empresas",
            "Para negócios que precisam sair do improviso e começar a controlar dinheiro com visão profissional."
        )

    with p2:
        comercial_card(
            "Lojas e comércios",
            "Para empresas que vendem, compram, parcelam e precisam acompanhar pagamentos e recebimentos."
        )

    with p3:
        comercial_card(
            "Prestadores de serviço",
            "Para profissionais que precisam controlar faturamento, despesas, clientes e relatórios."
        )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="commercial-panel">', unsafe_allow_html=True)
    st.markdown("## 💰 Planos comerciais sugeridos")

    plano1, plano2, plano3 = st.columns(3)

    with plano1:
        preco_card(
            "Plano Inicial",
            "R$ 97/mês",
            "Ideal para pequenos negócios que precisam controlar entradas, saídas, clientes e relatórios básicos."
        )

    with plano2:
        preco_card(
            "Plano Profissional",
            "R$ 197/mês",
            "Ideal para empresas com parcelas, contas a receber, estoque, usuários e relatórios financeiros."
        )

    with plano3:
        preco_card(
            "Plano Premium",
            "Sob consulta",
            "Sistema personalizado com identidade visual, implantação, treinamento e futuras integrações."
        )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="commercial-panel">', unsafe_allow_html=True)
    st.markdown("## 📲 Mensagem pronta para enviar a um cliente")

    mensagem_padrao = (
        "Olá! Tudo bem? Quero te apresentar o Sistema Financeiro Premium da Global Software. "
        "Ele ajuda sua empresa a controlar entradas, saídas, parcelas, contas a pagar, contas a receber, clientes, estoque e relatórios em um só lugar. "
        "É ideal para empresas que querem parar de perder controle financeiro e começar a tomar decisões com dados reais. "
        "Posso te mostrar uma demonstração rápida?"
    )

    mensagem = st.text_area("Mensagem comercial", value=mensagem_padrao, height=150, key="msg_publica_comercial")
    telefone_cliente = st.text_input("Telefone do cliente com DDD", placeholder="62999999999", key="tel_cliente_publico")

    if st.button("Gerar link para enviar ao cliente", use_container_width=True, key="btn_link_cliente_publico"):
        if telefone_cliente:
            link = f"https://wa.me/55{telefone_cliente}?text={quote(mensagem)}"
            st.markdown(f"[Abrir WhatsApp com mensagem comercial]({link})")
        else:
            st.warning("Digite o telefone do cliente com DDD.")

    st.markdown("</div>", unsafe_allow_html=True)


# =====================================================
# LOGIN
# =====================================================

def tela_login():
    st.markdown(
        """
        <div class="login-header">
            <div class="login-title">💼 Sistema Financeiro Premium</div>
            <div class="login-subtitle">
                Controle completo de finanças, empresas, usuários, parcelas, relatórios, clientes, estoque e permissões.
            </div>
            <div class="login-info">
                <b>Login padrão para teste:</b> admin@empresa.com &nbsp;&nbsp;|&nbsp;&nbsp; <b>Senha:</b> 123456
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

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

        st.markdown(
            f"""
            <div class="hero-box">
                <div class="hero-inner" style="{hero_bg}">
                    <div class="hero-overlay"></div>
                    <div class="hero-content">
                        <h3>Gestão inteligente e profissional</h3>
                        <p>
                            Controle entradas, saídas, parcelas, clientes, usuários e relatórios
                            em uma plataforma moderna, visual e eficiente.
                        </p>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        if logo_base64:
            st.markdown(
                f"""
                <div class="logo-box">
                    <img src="data:image/png;base64,{logo_base64}">
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                """
                <div class="logo-box">
                    <div style="text-align:center;">
                        <h3>GLOBAL SOFTWARE</h3>
                        <p>Sua logo aparecerá aqui quando o arquivo <b>logo.png</b> estiver na pasta do projeto.</p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown('<div class="form-box">', unsafe_allow_html=True)

    aba1, aba2 = st.tabs(["Entrar", "Criar empresa"])

    with aba1:
        st.markdown('<div class="section-title">Acessar sistema</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-subtitle">Entre com seu e-mail e senha para acessar o painel.</div>', unsafe_allow_html=True)

        col_a, col_b = st.columns(2)

        with col_a:
            email = st.text_input("E-mail", key="login_email")

        with col_b:
            senha = st.text_input("Senha", type="password", key="login_senha")

        if st.button("Entrar", use_container_width=True, key="btn_login"):
            usuario = consultar(
                """
                SELECT u.*, e.nome as empresa_nome
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
        st.markdown('<div class="section-title">Cadastrar nova empresa</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-subtitle">Crie sua empresa e o usuário administrador principal.</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            nome_empresa = st.text_input("Nome da empresa", key="cad_nome_empresa")
            documento = st.text_input("CNPJ / CPF", key="cad_documento")
            telefone = st.text_input("Telefone", key="cad_telefone")
            cidade = st.text_input("Cidade", key="cad_cidade")

        with col2:
            nome_usuario = st.text_input("Nome do administrador", key="cad_nome_usuario")
            email_usuario = st.text_input("E-mail do administrador", key="cad_email_usuario")
            senha_usuario = st.text_input("Senha", type="password", key="cad_senha_usuario")

        if st.button("Criar empresa", use_container_width=True, key="btn_criar_empresa"):
            if not nome_empresa or not nome_usuario or not email_usuario or not senha_usuario:
                st.warning("Preencha todos os campos obrigatórios.")
            else:
                try:
                    executar(
                        """
                        INSERT INTO empresas (nome, documento, telefone, cidade, criado_em)
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (nome_empresa, documento, telefone, cidade, datetime.now().isoformat())
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

                    st.success("Empresa criada com sucesso. Agora faça login.")
                except Exception as e:
                    st.error(f"Erro ao criar empresa: {e}")

    st.markdown("</div>", unsafe_allow_html=True)


# =====================================================
# USUÁRIO / PERMISSÕES
# =====================================================

def empresa_id_atual():
    return int(st.session_state.usuario["empresa_id"])


def usuario_id_atual():
    return int(st.session_state.usuario["id"])


def tipo_usuario_atual():
    return st.session_state.usuario["tipo"]


def menus_por_tipo_usuario():
    tipo = tipo_usuario_atual()

    todos_menus = [
        "Dashboard",
        "Apresentação Comercial",
        "Entradas e Saídas",
        "Parcelas",
        "Contas a Pagar/Receber",
        "Contas a Receber",
        "Pix",
        "Relatórios PDF",
        "IA Financeira",
        "CRM / Clientes",
        "Estoque",
        "WhatsApp Manual",
        "Usuários",
        "Configurações"
    ]

    permissoes = {
        "Administrador": todos_menus,

        "Gerente": [
            "Dashboard",
            "Apresentação Comercial",
            "Entradas e Saídas",
            "Parcelas",
            "Contas a Pagar/Receber",
            "Contas a Receber",
            "Pix",
            "Relatórios PDF",
            "IA Financeira",
            "CRM / Clientes",
            "Estoque",
            "WhatsApp Manual",
            "Configurações"
        ],

        "Financeiro": [
            "Dashboard",
            "Entradas e Saídas",
            "Parcelas",
            "Contas a Pagar/Receber",
            "Contas a Receber",
            "Pix",
            "Relatórios PDF",
            "IA Financeira",
            "WhatsApp Manual"
        ],

        "Vendedor": [
            "Dashboard",
            "Apresentação Comercial",
            "Contas a Receber",
            "CRM / Clientes",
            "WhatsApp Manual"
        ]
    }

    return permissoes.get(tipo, ["Dashboard"])


# =====================================================
# CARREGAR DADOS
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
        df["status_real"] = df.apply(
            lambda x: status_automatico(x["status"], x["vencimento"]),
            axis=1
        )

    return df


def carregar_clientes():
    return consultar(
        """
        SELECT *
        FROM clientes
        WHERE empresa_id = ?
        ORDER BY nome ASC
        """,
        (empresa_id_atual(),)
    )


def carregar_estoque():
    return consultar(
        """
        SELECT *
        FROM estoque
        WHERE empresa_id = ?
        ORDER BY produto ASC
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
            "custo": 0,
            "despesa_fixa": 0,
            "despesa_variavel": 0,
            "investimento": 0,
            "divida": 0,
            "retirada": 0,
            "lucro_bruto": 0,
            "lucro_operacional": 0,
            "lucro_liquido": 0,
            "caixa": 0,
            "margem_bruta": 0,
            "margem_liquida": 0,
            "contas_pagar": 0,
            "contas_receber": 0,
            "vencidas": 0,
            "a_vencer": 0,
            "ponto_equilibrio": 0
        }

    receita = df[df["tipo"] == "Receita"]["valor"].sum()
    custo = df[df["tipo"] == "Custo"]["valor"].sum()
    despesa_fixa = df[df["tipo"] == "Despesa fixa"]["valor"].sum()
    despesa_variavel = df[df["tipo"] == "Despesa variável"]["valor"].sum()
    investimento = df[df["tipo"] == "Investimento"]["valor"].sum()
    divida = df[df["tipo"] == "Dívida"]["valor"].sum()
    retirada = df[df["tipo"] == "Retirada do dono"]["valor"].sum()

    lucro_bruto = receita - custo
    lucro_operacional = lucro_bruto - despesa_fixa - despesa_variavel
    lucro_liquido = lucro_operacional - divida
    caixa = receita - custo - despesa_fixa - despesa_variavel - investimento - divida - retirada

    margem_bruta = (lucro_bruto / receita * 100) if receita > 0 else 0
    margem_liquida = (lucro_liquido / receita * 100) if receita > 0 else 0
    ponto_equilibrio = despesa_fixa / (margem_bruta / 100) if margem_bruta > 0 else 0

    pendentes = df[df["status_real"].isin(["Pendente", "Vence hoje", "Vencido"])]

    contas_pagar = pendentes[pendentes["tipo"] != "Receita"]["valor"].sum()
    contas_receber = pendentes[pendentes["tipo"] == "Receita"]["valor"].sum()
    vencidas = pendentes[pendentes["status_real"] == "Vencido"]["valor"].sum()
    a_vencer = pendentes[pendentes["status_real"].isin(["Pendente", "Vence hoje"])]["valor"].sum()

    return {
        "receita": receita,
        "custo": custo,
        "despesa_fixa": despesa_fixa,
        "despesa_variavel": despesa_variavel,
        "investimento": investimento,
        "divida": divida,
        "retirada": retirada,
        "lucro_bruto": lucro_bruto,
        "lucro_operacional": lucro_operacional,
        "lucro_liquido": lucro_liquido,
        "caixa": caixa,
        "margem_bruta": margem_bruta,
        "margem_liquida": margem_liquida,
        "contas_pagar": contas_pagar,
        "contas_receber": contas_receber,
        "vencidas": vencidas,
        "a_vencer": a_vencer,
        "ponto_equilibrio": ponto_equilibrio
    }


# =====================================================
# PDF
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

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(2 * cm, y, "Relatório Financeiro")
    y -= 1 * cm

    pdf.setFont("Helvetica", 10)
    pdf.drawString(2 * cm, y, f"Empresa: {st.session_state.usuario['empresa_nome']}")
    y -= 0.5 * cm
    pdf.drawString(2 * cm, y, f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    y -= 1 * cm

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(2 * cm, y, "Resumo")
    y -= 0.7 * cm

    pdf.setFont("Helvetica", 10)

    linhas = [
        ("Receita", moeda(ind["receita"])),
        ("Custo", moeda(ind["custo"])),
        ("Despesa fixa", moeda(ind["despesa_fixa"])),
        ("Despesa variável", moeda(ind["despesa_variavel"])),
        ("Lucro bruto", moeda(ind["lucro_bruto"])),
        ("Lucro líquido", moeda(ind["lucro_liquido"])),
        ("Caixa", moeda(ind["caixa"])),
        ("Contas a pagar", moeda(ind["contas_pagar"])),
        ("Contas a receber", moeda(ind["contas_receber"])),
        ("Vencidas", moeda(ind["vencidas"])),
    ]

    for nome, valor in linhas:
        pdf.drawString(2 * cm, y, f"{nome}: {valor}")
        y -= 0.45 * cm

    y -= 0.5 * cm
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(2 * cm, y, "Últimos lançamentos")
    y -= 0.7 * cm

    pdf.setFont("Helvetica", 8)

    if not df.empty:
        ultimos = df.sort_values("data", ascending=False).head(15)

        for _, row in ultimos.iterrows():
            linha = f"{data_br(row['data'])} | {row['tipo']} | {row['descricao']} | {moeda(row['valor'])} | {row['status_real']}"
            pdf.drawString(2 * cm, y, linha[:110])
            y -= 0.35 * cm

            if y < 2 * cm:
                pdf.showPage()
                y = altura - 2 * cm
                pdf.setFont("Helvetica", 8)

    pdf.save()
    buffer.seek(0)

    return buffer


# =====================================================
# TELA COMERCIAL INTERNA
# =====================================================

def tela_apresentacao_comercial():
    st.markdown(
        """
        <div class="commercial-hero">
            <div class="commercial-tag">GLOBAL SOFTWARE • Sistema Financeiro Premium</div>
            <div class="commercial-title">Controle financeiro profissional para empresas que querem crescer com organização.</div>
            <div class="commercial-subtitle">
                Uma plataforma moderna para controlar entradas, saídas, parcelas, contas a pagar, contas a receber,
                clientes, estoque, relatórios e usuários em um só lugar.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        comercial_card(
            "O problema",
            "Muitas empresas vendem bem, mas não sabem exatamente quanto lucram, quanto têm a receber, quanto devem pagar e para onde o dinheiro está indo."
        )

    with c2:
        comercial_card(
            "A solução",
            "O Sistema Financeiro Premium organiza os dados financeiros em painéis claros, com relatórios, filtros, parcelas, clientes e visão gerencial."
        )

    with c3:
        comercial_card(
            "O resultado",
            "Mais controle, menos perda de dinheiro, decisões mais rápidas e uma empresa preparada para crescer com gestão profissional."
        )

    st.write("")

    st.markdown('<div class="commercial-panel">', unsafe_allow_html=True)
    st.markdown("## 💼 Principais módulos do sistema")

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        comercial_card("Dashboard", "Indicadores financeiros, lucro, caixa, contas vencidas, a pagar, a receber e ponto de equilíbrio.")

    with m2:
        comercial_card("Lançamentos", "Controle de receitas, custos, despesas, investimentos, dívidas e retiradas do dono.")

    with m3:
        comercial_card("Parcelas", "Cadastro e acompanhamento de vendas ou despesas parceladas com vencimentos automáticos.")

    with m4:
        comercial_card("Relatórios", "Exportação de relatórios em PDF e CSV para análise, prestação de contas e acompanhamento.")

    st.write("")

    m5, m6, m7, m8 = st.columns(4)

    with m5:
        comercial_card("CRM / Clientes", "Cadastro de clientes, fornecedores, contatos, documentos e observações comerciais.")

    with m6:
        comercial_card("Estoque", "Controle de produtos, quantidade, custo, preço de venda e fornecedor.")

    with m7:
        comercial_card("Usuários", "Perfis de acesso por administrador, gerente, financeiro e vendedor.")

    with m8:
        comercial_card("WhatsApp", "Geração de mensagens e links de cobrança para facilitar contato com clientes.")

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="commercial-panel">', unsafe_allow_html=True)
    st.markdown("## 🎯 Para quem é indicado?")

    p1, p2, p3 = st.columns(3)

    with p1:
        comercial_card("Pequenas empresas", "Empresas que precisam sair do caderno, bloco de notas ou planilhas soltas.")

    with p2:
        comercial_card("Lojas e comércios", "Negócios que vendem, compram, parcelam e precisam controlar pagamentos e recebimentos.")

    with p3:
        comercial_card("Prestadores de serviço", "Profissionais e equipes que precisam acompanhar faturamento, despesas e clientes.")

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="commercial-panel">', unsafe_allow_html=True)
    st.markdown("## 💰 Sugestão de planos comerciais")

    plano1, plano2, plano3 = st.columns(3)

    with plano1:
        preco_card(
            "Plano Inicial",
            "R$ 97/mês",
            "Ideal para pequenos negócios que precisam controlar entradas, saídas, clientes e relatórios básicos."
        )

    with plano2:
        preco_card(
            "Plano Profissional",
            "R$ 197/mês",
            "Ideal para empresas com parcelas, contas a receber, estoque, usuários e relatórios financeiros."
        )

    with plano3:
        preco_card(
            "Plano Premium",
            "Sob consulta",
            "Sistema personalizado com identidade visual, implantação, treinamento e futuras integrações."
        )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="commercial-panel">', unsafe_allow_html=True)
    st.markdown("## 📲 Mensagem pronta para enviar ao cliente")

    mensagem_padrao = (
        "Olá! Tudo bem? Quero te apresentar o Sistema Financeiro Premium da Global Software. "
        "Ele ajuda sua empresa a controlar entradas, saídas, parcelas, contas a pagar, contas a receber, clientes, estoque e relatórios em um só lugar. "
        "É ideal para empresas que querem parar de perder controle financeiro e começar a tomar decisões com dados reais. "
        "Posso te mostrar uma demonstração rápida?"
    )

    mensagem = st.text_area("Mensagem comercial", value=mensagem_padrao, height=150, key="msg_comercial")
    telefone = st.text_input("Telefone do cliente com DDD", placeholder="62999999999", key="tel_comercial")

    if st.button("Gerar link de apresentação no WhatsApp", use_container_width=True, key="btn_comercial_whatsapp"):
        if telefone:
            link = f"https://wa.me/55{telefone}?text={quote(mensagem)}"
            st.markdown(f"[Abrir WhatsApp com mensagem comercial]({link})")
        else:
            st.warning("Digite o telefone do cliente com DDD.")

    st.markdown("</div>", unsafe_allow_html=True)


# =====================================================
# APP PRINCIPAL
# =====================================================

def app():
    usuario = st.session_state.usuario

    if Path("logo.png").exists():
        st.sidebar.image("logo.png", use_container_width=True)

    st.sidebar.title("💼 Sistema Financeiro")
    st.sidebar.write(f"**Empresa:** {usuario['empresa_nome']}")
    st.sidebar.write(f"**Usuário:** {usuario['nome']}")
    st.sidebar.write(f"**Tipo:** {usuario['tipo']}")

    df = carregar_lancamentos()
    ind = calcular_indicadores(df)

    menus_liberados = menus_por_tipo_usuario()

    if "menu_atual" not in st.session_state:
        st.session_state.menu_atual = menus_liberados[0]

    if st.session_state.menu_atual not in menus_liberados:
        st.session_state.menu_atual = menus_liberados[0]

    cabecalho_interno(st.session_state.menu_atual)

    st.markdown('<div class="menu-panel">', unsafe_allow_html=True)
    st.markdown('<div class="menu-title">Menu principal do sistema</div>', unsafe_allow_html=True)

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

    st.markdown("</div>", unsafe_allow_html=True)

    menu = st.session_state.menu_atual

    if menu == "Dashboard":
        st.title("📊 Dashboard Financeiro Premium")

        if df.empty:
            st.info("Nenhum lançamento cadastrado ainda. Cadastre entradas e saídas para visualizar o painel.")
        else:
            st.markdown('<div class="page-panel">', unsafe_allow_html=True)
            st.markdown("### 🔎 Filtros do painel")

            col_f1, col_f2, col_f3 = st.columns(3)

            data_min = df["data"].min().date()
            data_max = df["data"].max().date()

            with col_f1:
                data_inicio = st.date_input("Data inicial", value=data_min, key="dash_data_inicio")

            with col_f2:
                data_fim = st.date_input("Data final", value=data_max, key="dash_data_fim")

            with col_f3:
                tipo_filtro = st.selectbox("Tipo", ["Todos"] + list(TIPOS_LANCAMENTO.keys()), key="dash_tipo_filtro")

            df_periodo = df[
                (df["data"].dt.date >= data_inicio) &
                (df["data"].dt.date <= data_fim)
            ].copy()

            if tipo_filtro != "Todos":
                df_periodo = df_periodo[df_periodo["tipo"] == tipo_filtro]

            ind = calcular_indicadores(df_periodo)
            st.markdown("</div>", unsafe_allow_html=True)

            c1, c2, c3, c4 = st.columns(4)

            with c1:
                card("Receita do período", moeda(ind["receita"]), "Entradas filtradas")

            with c2:
                card("Despesas + custos", moeda(ind["custo"] + ind["despesa_fixa"] + ind["despesa_variavel"]), "Saídas operacionais")

            with c3:
                card("Lucro líquido", moeda(ind["lucro_liquido"]), percentual(ind["margem_liquida"]))

            with c4:
                card("Saldo em caixa", moeda(ind["caixa"]), "Resultado final")

            st.write("")

            c5, c6, c7, c8 = st.columns(4)

            with c5:
                card("Contas vencidas", moeda(ind["vencidas"]), "Atenção imediata")

            with c6:
                card("A receber", moeda(ind["contas_receber"]), "Recebimentos pendentes")

            with c7:
                card("A pagar", moeda(ind["contas_pagar"]), "Pagamentos pendentes")

            with c8:
                card("Ponto de equilíbrio", moeda(ind["ponto_equilibrio"]), "Meta mínima de venda")

            st.divider()

            if df_periodo.empty:
                st.warning("Nenhum lançamento encontrado nesse filtro.")
            else:
                col_g1, col_g2 = st.columns(2)

                with col_g1:
                    st.subheader("📈 Receita x Saídas por mês")

                    graf_mensal = df_periodo.copy()
                    graf_mensal["mes"] = graf_mensal["data"].dt.strftime("%Y-%m")

                    resumo_mensal = graf_mensal.groupby(["mes", "tipo"])["valor"].sum().reset_index()
                    tabela_graf = resumo_mensal.pivot(index="mes", columns="tipo", values="valor").fillna(0)

                    st.line_chart(tabela_graf)

                with col_g2:
                    st.subheader("🏷️ Gastos por categoria")

                    gastos = df_periodo[df_periodo["tipo"] != "Receita"]

                    if gastos.empty:
                        st.info("Nenhum gasto no período.")
                    else:
                        categorias = gastos.groupby("categoria")["valor"].sum().sort_values(ascending=False).head(10)
                        st.bar_chart(categorias)

                st.divider()

                col_r1, col_r2 = st.columns(2)

                with col_r1:
                    st.subheader("🧾 Resumo por tipo")

                    resumo_tipo = df_periodo.groupby("tipo")["valor"].sum().reset_index()
                    resumo_tipo["valor_formatado"] = resumo_tipo["valor"].apply(moeda)

                    st.dataframe(
                        resumo_tipo[["tipo", "valor_formatado"]],
                        use_container_width=True,
                        hide_index=True
                    )

                with col_r2:
                    st.subheader("⚠️ Contas críticas")

                    criticas = df_periodo[df_periodo["status_real"].isin(["Vencido", "Vence hoje"])].copy()

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

                st.divider()

                st.subheader("📋 Últimos lançamentos do período")

                tabela = df_periodo.sort_values("data", ascending=False).head(20).copy()
                tabela["data"] = tabela["data"].dt.strftime("%d/%m/%Y")
                tabela["vencimento"] = tabela["vencimento"].dt.strftime("%d/%m/%Y")
                tabela["valor"] = tabela["valor"].apply(moeda)

                st.dataframe(
                    tabela[["data", "vencimento", "tipo", "categoria", "descricao", "cliente_fornecedor", "valor", "status_real"]],
                    use_container_width=True,
                    hide_index=True
                )

    elif menu == "Apresentação Comercial":
        st.title("🚀 Apresentação Comercial")
        tela_apresentacao_comercial()

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
                valor = st.number_input("Valor", min_value=0.0, step=1.0, format="%.2f", key="lanc_valor")
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

            st.dataframe(tabela, use_container_width=True)

            st.subheader("Editar / Excluir")

            id_edit = st.selectbox("Selecione o ID", df["id"].tolist(), key="edit_id")
            item = df[df["id"] == id_edit].iloc[0]

            novo_status = st.selectbox(
                "Novo status",
                STATUS_OPCOES,
                index=STATUS_OPCOES.index(item["status"]) if item["status"] in STATUS_OPCOES else 0,
                key="edit_status"
            )

            novo_valor = st.number_input(
                "Novo valor",
                min_value=0.0,
                value=float(item["valor"]),
                step=1.0,
                key="edit_valor"
            )

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
                executar(
                    """
                    DELETE FROM lancamentos
                    WHERE id = ? AND empresa_id = ?
                    """,
                    (int(id_edit), empresa_id_atual())
                )

                st.warning("Excluído.")
                st.rerun()

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
                st.dataframe(parcelas, use_container_width=True)

    elif menu == "Contas a Pagar/Receber":
        st.title("📌 Contas a Pagar / Receber")

        if df.empty:
            st.info("Nenhuma conta cadastrada.")
        else:
            contas = df[df["status_real"].isin(["Pendente", "Vence hoje", "Vencido"])].copy()

            filtro = st.selectbox(
                "Filtrar",
                ["Todas", "A pagar", "A receber", "Vencidas", "Vence hoje"],
                key="filtro_contas"
            )

            if filtro == "A pagar":
                contas = contas[contas["tipo"] != "Receita"]

            elif filtro == "A receber":
                contas = contas[contas["tipo"] == "Receita"]

            elif filtro == "Vencidas":
                contas = contas[contas["status_real"] == "Vencido"]

            elif filtro == "Vence hoje":
                contas = contas[contas["status_real"] == "Vence hoje"]

            if contas.empty:
                st.info("Nenhuma conta encontrada.")
            else:
                contas["data"] = contas["data"].dt.strftime("%d/%m/%Y")
                contas["vencimento"] = contas["vencimento"].dt.strftime("%d/%m/%Y")
                st.dataframe(contas, use_container_width=True)

    elif menu == "Contas a Receber":
        st.title("💰 Contas a Receber")

        if df.empty:
            st.info("Nenhuma conta a receber.")
        else:
            receber = df[
                (df["tipo"] == "Receita") &
                (df["status_real"].isin(["Pendente", "Vence hoje", "Vencido"]))
            ].copy()

            if receber.empty:
                st.success("Nenhuma conta a receber pendente.")
            else:
                receber["data"] = receber["data"].dt.strftime("%d/%m/%Y")
                receber["vencimento"] = receber["vencimento"].dt.strftime("%d/%m/%Y")
                st.dataframe(receber, use_container_width=True)

    elif menu == "Pix":
        st.title("💳 Pix")

        chave = st.text_input("Chave Pix", key="pix_chave")
        valor_pix = st.number_input("Valor", min_value=0.0, step=1.0, key="pix_valor")
        descricao_pix = st.text_input("Descrição", key="pix_descricao")

        if st.button("Gerar texto de cobrança", key="btn_pix"):
            texto = f"Olá! Segue cobrança via Pix: Chave: {chave} | Valor: {moeda(valor_pix)} | {descricao_pix}"
            st.code(texto)

    elif menu == "Relatórios PDF":
        st.title("📄 Relatórios PDF")

        pdf = gerar_pdf_relatorio(df, ind)

        if pdf is None:
            st.warning("Biblioteca reportlab não instalada. Confira se ela está no requirements.txt.")
        else:
            st.download_button(
                "Baixar relatório PDF",
                data=pdf,
                file_name="relatorio_financeiro.pdf",
                mime="application/pdf",
                key="download_pdf"
            )

        if not df.empty:
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Baixar CSV",
                data=csv,
                file_name="lancamentos.csv",
                mime="text/csv",
                key="download_csv"
            )

    elif menu == "IA Financeira":
        st.title("🤖 IA Financeira")

        if df.empty:
            st.info("Cadastre lançamentos para receber uma análise.")
        else:
            st.subheader("Diagnóstico automático")

            if ind["lucro_liquido"] < 0:
                st.markdown(
                    """
                    <div class="danger-box">
                    Seu negócio está com prejuízo líquido. É necessário reduzir custos,
                    revisar despesas fixas ou aumentar a margem das vendas.
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            elif ind["margem_liquida"] < 10:
                st.markdown(
                    """
                    <div class="warning-box">
                    Sua margem líquida está baixa. O negócio está dando lucro, mas ainda com pouca sobra.
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            else:
                st.markdown(
                    """
                    <div class="success-box">
                    O negócio apresenta resultado saudável no período analisado.
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.write(f"**Margem bruta:** {percentual(ind['margem_bruta'])}")
            st.write(f"**Margem líquida:** {percentual(ind['margem_liquida'])}")
            st.write(f"**Ponto de equilíbrio:** {moeda(ind['ponto_equilibrio'])}")

            pergunta = st.text_area("Faça uma pergunta financeira", key="ia_pergunta")

            if st.button("Responder", key="btn_ia"):
                st.info(
                    "Análise local: acompanhe os vencidos, reduza despesas fixas e priorize receitas recorrentes. "
                    "Para IA real com OpenAI, depois conectamos sua API."
                )

    elif menu == "CRM / Clientes":
        st.title("👥 CRM / Clientes")

        with st.form("form_cliente"):
            col1, col2 = st.columns(2)

            with col1:
                nome = st.text_input("Nome", key="cliente_nome")
                telefone = st.text_input("Telefone / WhatsApp", key="cliente_telefone")
                email = st.text_input("E-mail", key="cliente_email")

            with col2:
                documento = st.text_input("CPF / CNPJ", key="cliente_documento")
                tipo_cliente = st.selectbox("Tipo", ["Cliente", "Fornecedor", "Parceiro"], key="cliente_tipo")
                obs = st.text_area("Observação", key="cliente_obs")

            if st.form_submit_button("Salvar cliente"):
                executar(
                    """
                    INSERT INTO clientes
                    (empresa_id, nome, telefone, email, documento, tipo, observacao, criado_em)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        empresa_id_atual(),
                        nome,
                        telefone,
                        email,
                        documento,
                        tipo_cliente,
                        obs,
                        datetime.now().isoformat()
                    )
                )

                st.success("Cliente salvo.")
                st.rerun()

        clientes = carregar_clientes()

        if clientes.empty:
            st.info("Nenhum cliente cadastrado.")
        else:
            st.dataframe(clientes, use_container_width=True)

    elif menu == "Estoque":
        st.title("📦 Estoque")

        with st.form("form_estoque"):
            col1, col2, col3 = st.columns(3)

            with col1:
                produto = st.text_input("Produto", key="est_produto")
                categoria = st.text_input("Categoria", key="est_categoria")
                fornecedor = st.text_input("Fornecedor", key="est_fornecedor")

            with col2:
                quantidade = st.number_input("Quantidade", min_value=0.0, step=1.0, key="est_quantidade")
                custo_unitario = st.number_input("Custo unitário", min_value=0.0, step=1.0, key="est_custo")

            with col3:
                preco_venda = st.number_input("Preço de venda", min_value=0.0, step=1.0, key="est_preco")
                obs = st.text_area("Observação", key="est_obs")

            if st.form_submit_button("Salvar produto"):
                executar(
                    """
                    INSERT INTO estoque
                    (empresa_id, produto, categoria, quantidade, custo_unitario, preco_venda, fornecedor, observacao, criado_em)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        empresa_id_atual(),
                        produto,
                        categoria,
                        quantidade,
                        custo_unitario,
                        preco_venda,
                        fornecedor,
                        obs,
                        datetime.now().isoformat()
                    )
                )

                st.success("Produto salvo.")
                st.rerun()

        estoque = carregar_estoque()

        if estoque.empty:
            st.info("Nenhum produto cadastrado.")
        else:
            estoque["valor_custo_total"] = estoque["quantidade"] * estoque["custo_unitario"]
            estoque["valor_venda_total"] = estoque["quantidade"] * estoque["preco_venda"]
            st.dataframe(estoque, use_container_width=True)

    elif menu == "WhatsApp Manual":
        st.title("📲 WhatsApp Manual")

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

                st.info(
                    """
                    Permissões:

                    Administrador: acesso total ao sistema.

                    Gerente: financeiro, estoque, CRM, relatórios e configurações.

                    Financeiro: lançamentos, contas, parcelas, Pix, relatórios e IA.

                    Vendedor: clientes, WhatsApp, contas a receber e dashboard.
                    """
                )

                criar = st.form_submit_button("Criar usuário", use_container_width=True)

                if criar:
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
                                (
                                    empresa_id_atual(),
                                    nome,
                                    email,
                                    hash_senha(senha),
                                    tipo_user,
                                    int(ativo),
                                    datetime.now().isoformat()
                                )
                            )

                            st.success("Usuário criado com sucesso.")
                            st.rerun()

                        except Exception as e:
                            st.error(f"Erro ao criar usuário: {e}")

            st.divider()

            st.subheader("Usuários cadastrados")

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
                st.dataframe(usuarios, use_container_width=True)

                st.subheader("Alterar acesso do usuário")

                id_usuario = st.selectbox(
                    "Selecione o usuário",
                    usuarios["id"].tolist(),
                    format_func=lambda x: f"{usuarios[usuarios['id'] == x].iloc[0]['nome']} - {usuarios[usuarios['id'] == x].iloc[0]['tipo']}",
                    key="editar_usuario_id"
                )

                usuario_edit = usuarios[usuarios["id"] == id_usuario].iloc[0]

                colu1, colu2, colu3 = st.columns(3)

                with colu1:
                    novo_tipo = st.selectbox(
                        "Novo tipo de acesso",
                        TIPOS_USUARIO,
                        index=TIPOS_USUARIO.index(usuario_edit["tipo"]) if usuario_edit["tipo"] in TIPOS_USUARIO else 0,
                        key="editar_usuario_tipo"
                    )

                with colu2:
                    novo_ativo = st.selectbox(
                        "Status",
                        ["Ativo", "Bloqueado"],
                        index=0 if usuario_edit["ativo"] == 1 else 1,
                        key="editar_usuario_status"
                    )

                with colu3:
                    nova_senha = st.text_input("Nova senha", type="password", key="editar_usuario_senha")

                col_btn1, col_btn2 = st.columns(2)

                if col_btn1.button("Salvar alterações", key="btn_salvar_usuario"):
                    ativo_int = 1 if novo_ativo == "Ativo" else 0

                    if nova_senha:
                        executar(
                            """
                            UPDATE usuarios
                            SET tipo = ?, ativo = ?, senha_hash = ?
                            WHERE id = ? AND empresa_id = ?
                            """,
                            (novo_tipo, ativo_int, hash_senha(nova_senha), int(id_usuario), empresa_id_atual())
                        )
                    else:
                        executar(
                            """
                            UPDATE usuarios
                            SET tipo = ?, ativo = ?
                            WHERE id = ? AND empresa_id = ?
                            """,
                            (novo_tipo, ativo_int, int(id_usuario), empresa_id_atual())
                        )

                    st.success("Usuário atualizado com sucesso.")
                    st.rerun()

                if col_btn2.button("Excluir usuário", key="btn_excluir_usuario"):
                    if int(id_usuario) == usuario_id_atual():
                        st.error("Você não pode excluir o próprio usuário logado.")
                    else:
                        executar(
                            """
                            DELETE FROM usuarios
                            WHERE id = ? AND empresa_id = ?
                            """,
                            (int(id_usuario), empresa_id_atual())
                        )

                        st.warning("Usuário excluído.")
                        st.rerun()

    elif menu == "Configurações":
        st.title("⚙️ Configurações")

        empresa = consultar("SELECT * FROM empresas WHERE id = ?", (empresa_id_atual(),))

        if empresa.empty:
            st.error("Empresa não encontrada.")
        else:
            emp = empresa.iloc[0]

            nome = st.text_input("Nome da empresa", value=emp["nome"], key="conf_nome")
            documento = st.text_input("Documento", value=emp["documento"] or "", key="conf_doc")
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

        st.subheader("Backup local")

        backup = {
            "empresa": usuario["empresa_nome"],
            "lancamentos": df.to_dict(orient="records") if not df.empty else [],
            "gerado_em": datetime.now().isoformat()
        }

        st.download_button(
            "Baixar backup JSON",
            data=json.dumps(backup, ensure_ascii=False, indent=4, default=str),
            file_name="backup_sistema_financeiro.json",
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