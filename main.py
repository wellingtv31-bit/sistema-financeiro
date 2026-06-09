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
# CSS PREMIUM GLOBAL SOFTWARE
# =====================================================

st.markdown(
    """
    <style>
    #MainMenu, footer, header {
        visibility: hidden;
    }

    :root {
        --navy: #002b3d;
        --navy2: #001d2b;
        --navy3: #00384d;
        --lime: #dfff6b;
        --lime2: #c9ff4f;
        --gold: #d4af37;
        --gold-soft: #f3e3ad;
        --white: #ffffff;
        --soft: #f4f8fb;
        --text-dark: #052c3d;
        --text-gray: #6c7b86;
        --border: #e5edf2;
    }

    .stApp {
        background: linear-gradient(135deg, #001d2b 0%, #002b3d 50%, #001520 100%);
        color: var(--gold-soft);
    }

    .block-container {
        padding-top: 0.8rem;
        padding-bottom: 2rem;
        padding-left: 1.2rem;
        padding-right: 1.2rem;
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

    /* =========================
       LANDING PAGE PÚBLICA
    ========================= */

    .lp-wrap {
        margin: -12px -6px 0 -6px;
        font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }

    .lp-topbar {
        background: var(--navy2);
        border-radius: 0 0 28px 28px;
        padding: 26px 28px 10px 28px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 18px;
        flex-wrap: wrap;
    }

    .lp-brand {
        display: flex;
        align-items: center;
        gap: 14px;
    }

    .lp-logo {
        width: 58px;
        height: 58px;
        border-radius: 18px;
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(223,255,107,0.25);
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
        color: var(--lime);
        font-weight: 950;
        font-size: 18px;
    }

    .lp-logo img {
        width: 100%;
        height: 100%;
        object-fit: contain;
        padding: 5px;
    }

    .lp-brand-title {
        color: white;
        font-size: 24px;
        letter-spacing: 4px;
        font-weight: 850;
    }

    .lp-brand-sub {
        color: rgba(255,255,255,0.60);
        font-size: 13px;
        margin-top: 2px;
    }

    .lp-top-actions {
        display: flex;
        gap: 10px;
        align-items: center;
        flex-wrap: wrap;
    }

    .lp-pill {
        color: var(--lime);
        border: 1px solid rgba(223,255,107,0.32);
        background: rgba(223,255,107,0.08);
        padding: 10px 16px;
        border-radius: 999px;
        font-weight: 900;
        font-size: 13px;
    }

    .lp-hero {
        background:
            radial-gradient(circle at 80% 25%, rgba(223,255,107,0.15), transparent 32%),
            radial-gradient(circle at 20% 70%, rgba(212,175,55,0.12), transparent 34%),
            linear-gradient(180deg, var(--navy2), var(--navy));
        padding: 52px 28px 78px 28px;
        border-radius: 0 0 42px 42px;
        position: relative;
        overflow: hidden;
    }

    .lp-hero-grid {
        display: grid;
        grid-template-columns: 1.05fr 0.95fr;
        gap: 34px;
        align-items: center;
        max-width: 1220px;
        margin: 0 auto;
    }

    .lp-kicker {
        color: var(--lime);
        letter-spacing: 5px;
        font-size: 13px;
        font-weight: 950;
        margin-bottom: 22px;
        text-transform: uppercase;
    }

    .lp-title {
        color: white;
        font-size: 62px;
        line-height: 1.02;
        font-weight: 950;
        margin-bottom: 26px;
        letter-spacing: -1.8px;
    }

    .lp-title span {
        color: var(--lime);
    }

    .lp-subtitle {
        color: rgba(255,255,255,0.72);
        font-size: 22px;
        line-height: 1.65;
        max-width: 720px;
        margin-bottom: 34px;
    }

    .lp-cta-row {
        display: flex;
        gap: 14px;
        flex-wrap: wrap;
        align-items: center;
    }

    .lp-fake-btn-primary {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 16px;
        padding: 19px 34px;
        border-radius: 999px;
        background: linear-gradient(90deg, rgba(223,255,107,0.95), rgba(201,255,79,0.95));
        color: #002b3d;
        font-weight: 950;
        font-size: 17px;
        box-shadow: 0 18px 45px rgba(223,255,107,0.22);
        border: 1px solid rgba(223,255,107,0.55);
    }

    .lp-fake-btn-secondary {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 18px 28px;
        border-radius: 999px;
        color: white;
        border: 1px solid rgba(255,255,255,0.22);
        background: rgba(255,255,255,0.05);
        font-weight: 900;
        font-size: 16px;
    }

    .lp-dashboard-mock {
        min-height: 440px;
        border-radius: 34px;
        background:
            linear-gradient(135deg, rgba(255,255,255,0.12), rgba(255,255,255,0.04)),
            radial-gradient(circle at top right, rgba(223,255,107,0.18), transparent 42%);
        border: 1px solid rgba(255,255,255,0.18);
        box-shadow: 0 30px 100px rgba(0,0,0,0.35);
        padding: 28px;
        position: relative;
        overflow: hidden;
    }

    .lp-mock-screen {
        height: 100%;
        border-radius: 26px;
        background: rgba(255,255,255,0.92);
        padding: 22px;
        color: var(--text-dark);
        transform: rotate(-3deg);
        box-shadow: 0 28px 70px rgba(0,0,0,0.30);
    }

    .lp-mock-bar {
        height: 12px;
        width: 44%;
        background: #dfe9ef;
        border-radius: 20px;
        margin-bottom: 20px;
    }

    .lp-mock-card-row {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 14px;
        margin-bottom: 14px;
    }

    .lp-mock-card {
        background: #f2f7fa;
        border: 1px solid #e5edf2;
        border-radius: 18px;
        padding: 18px;
        min-height: 94px;
    }

    .lp-mock-label {
        color: #78909c;
        font-size: 13px;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .lp-mock-value {
        color: #002b3d;
        font-size: 24px;
        font-weight: 950;
    }

    .lp-mock-chart {
        height: 130px;
        border-radius: 20px;
        background:
            linear-gradient(90deg, rgba(223,255,107,0.35), rgba(0,43,61,0.18)),
            repeating-linear-gradient(90deg, transparent 0 38px, rgba(0,43,61,0.05) 38px 40px);
        border: 1px solid #e3edf2;
    }

    .lp-trust {
        background: var(--navy2);
        padding: 58px 28px;
        text-align: center;
    }

    .lp-trust-title {
        color: white;
        font-size: 44px;
        line-height: 1.12;
        font-weight: 950;
    }

    .lp-trust-title span {
        color: var(--lime);
    }

    .lp-section-white {
        background: #f7fbfd;
        color: var(--text-dark);
        padding: 74px 28px;
        border-radius: 0;
    }

    .lp-section-dark {
        background: var(--navy);
        color: white;
        padding: 74px 28px;
        border-radius: 0;
    }

    .lp-container {
        max-width: 1220px;
        margin: 0 auto;
    }

    .lp-section-kicker {
        text-align: center;
        color: #7a8d98;
        letter-spacing: 7px;
        font-size: 14px;
        text-transform: uppercase;
        font-weight: 800;
        margin-bottom: 18px;
    }

    .lp-section-kicker.dark {
        color: rgba(255,255,255,0.42);
    }

    .lp-section-title {
        text-align: center;
        color: var(--text-dark);
        font-size: 50px;
        line-height: 1.14;
        letter-spacing: -1.3px;
        font-weight: 950;
        max-width: 930px;
        margin: 0 auto 44px auto;
    }

    .lp-section-title.dark {
        color: white;
    }

    .lp-section-title span {
        color: var(--lime2);
    }

    .lp-feature-tabs {
        display: flex;
        gap: 14px;
        flex-wrap: wrap;
        justify-content: center;
        margin-bottom: 34px;
    }

    .lp-tab-active,
    .lp-tab {
        padding: 18px 24px;
        border-radius: 18px;
        font-weight: 900;
        display: inline-flex;
        gap: 10px;
        align-items: center;
        box-shadow: 0 14px 30px rgba(0,0,0,0.06);
    }

    .lp-tab-active {
        background: var(--navy);
        color: white;
        border: 1px solid var(--navy);
    }

    .lp-tab {
        background: white;
        color: #607682;
        border: 1px solid var(--border);
    }

    .lp-feature-card-dark {
        background:
            radial-gradient(circle at top right, rgba(223,255,107,0.08), transparent 36%),
            linear-gradient(180deg, #002b3d, #001d2b);
        border: 1px solid rgba(223,255,107,0.16);
        border-radius: 32px;
        padding: 46px;
        color: white;
        box-shadow: 0 24px 70px rgba(0,0,0,0.24);
    }

    .lp-chip {
        display: inline-flex;
        gap: 10px;
        align-items: center;
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.13);
        border-radius: 999px;
        padding: 13px 20px;
        color: rgba(255,255,255,0.70);
        letter-spacing: 4px;
        font-weight: 850;
        font-size: 13px;
        text-transform: uppercase;
        margin-bottom: 28px;
    }

    .lp-feature-title {
        color: white;
        font-size: 43px;
        line-height: 1.15;
        font-weight: 950;
        max-width: 690px;
        margin-bottom: 34px;
    }

    .lp-check-list {
        display: grid;
        grid-template-columns: 1fr;
        gap: 28px;
        max-width: 820px;
    }

    .lp-check-item {
        display: grid;
        grid-template-columns: 52px 1fr;
        gap: 18px;
        align-items: flex-start;
    }

    .lp-check-icon {
        width: 42px;
        height: 42px;
        border-radius: 999px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: rgba(223,255,107,0.13);
        border: 1px solid rgba(223,255,107,0.30);
        color: var(--lime);
        font-weight: 950;
    }

    .lp-check-title {
        color: white;
        font-size: 23px;
        font-weight: 950;
        margin-bottom: 8px;
    }

    .lp-check-text {
        color: rgba(255,255,255,0.60);
        font-size: 19px;
        line-height: 1.55;
    }

    .lp-profile-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 22px;
    }

    .lp-profile-card {
        background: white;
        border: 1px solid var(--border);
        border-radius: 28px;
        padding: 38px 32px;
        box-shadow: 0 18px 55px rgba(0,43,61,0.06);
        color: var(--text-dark);
        min-height: 460px;
    }

    .lp-icon-box {
        width: 72px;
        height: 72px;
        border-radius: 18px;
        background: var(--navy);
        color: var(--lime);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 34px;
        margin-bottom: 32px;
    }

    .lp-profile-title {
        font-size: 31px;
        color: var(--text-dark);
        font-weight: 950;
        margin-bottom: 8px;
    }

    .lp-profile-sub {
        color: #7b8c96;
        font-size: 18px;
        margin-bottom: 26px;
    }

    .lp-profile-feature {
        margin-bottom: 18px;
    }

    .lp-profile-feature b {
        display: block;
        color: var(--text-dark);
        font-size: 18px;
        margin-bottom: 4px;
    }

    .lp-profile-feature span {
        color: #6e7f8a;
        font-size: 16px;
        line-height: 1.45;
    }

    .lp-steps {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 22px;
        margin-top: 38px;
    }

    .lp-step {
        background: white;
        border-radius: 26px;
        border: 1px solid var(--border);
        padding: 30px 24px;
        text-align: center;
        color: var(--text-dark);
        min-height: 270px;
        box-shadow: 0 18px 45px rgba(0,43,61,0.05);
    }

    .lp-step-icon {
        width: 72px;
        height: 72px;
        border-radius: 20px;
        background: var(--navy);
        color: var(--lime);
        font-size: 32px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 20px auto;
    }

    .lp-step-small {
        color: #92a1aa;
        letter-spacing: 2px;
        font-weight: 850;
        font-size: 13px;
        text-transform: uppercase;
        margin-bottom: 10px;
    }

    .lp-step-title {
        color: var(--text-dark);
        font-weight: 950;
        font-size: 21px;
        margin-bottom: 12px;
    }

    .lp-step-text {
        color: #6d7f89;
        font-size: 15px;
        line-height: 1.55;
    }

    .lp-compare {
        background: white;
        border: 1px solid var(--border);
        border-radius: 30px;
        overflow: hidden;
        box-shadow: 0 18px 55px rgba(0,43,61,0.06);
    }

    .lp-compare-row {
        display: grid;
        grid-template-columns: 1.1fr 1fr 1fr;
        border-bottom: 1px solid var(--border);
        color: var(--text-dark);
    }

    .lp-compare-row:last-child {
        border-bottom: none;
    }

    .lp-compare-cell {
        padding: 24px;
        font-size: 16px;
        color: #667985;
    }

    .lp-compare-cell strong {
        color: var(--text-dark);
        font-size: 21px;
        display: block;
        margin-bottom: 8px;
    }

    .lp-good {
        color: var(--navy);
        font-weight: 850;
    }

    .lp-bad {
        color: #9aa9b1;
    }

    .lp-testimonial-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 22px;
    }

    .lp-testimonial {
        background: white;
        color: var(--text-dark);
        border-radius: 28px;
        padding: 34px;
        min-height: 300px;
        border: 1px solid rgba(255,255,255,0.16);
        box-shadow: 0 22px 60px rgba(0,0,0,0.16);
    }

    .lp-quote {
        color: var(--lime);
        font-size: 52px;
        line-height: 0.7;
        margin-bottom: 22px;
        font-weight: 950;
    }

    .lp-testimonial-text {
        color: #314b58;
        font-size: 17px;
        line-height: 1.65;
        margin-bottom: 26px;
    }

    .lp-person {
        border-top: 1px solid var(--border);
        padding-top: 18px;
        color: var(--text-dark);
    }

    .lp-person b {
        font-size: 18px;
    }

    .lp-person span {
        display: block;
        color: #74858e;
        font-size: 14px;
        margin-top: 4px;
    }

    .lp-faq {
        display: grid;
        gap: 14px;
        max-width: 920px;
        margin: 0 auto;
    }

    .lp-faq-item {
        background: white;
        border: 1px solid var(--border);
        color: var(--text-dark);
        border-radius: 20px;
        padding: 24px 26px;
        font-size: 19px;
        font-weight: 900;
        display: flex;
        justify-content: space-between;
        gap: 14px;
        align-items: center;
    }

    .lp-demo-box {
        background: white;
        border-radius: 34px;
        padding: 38px;
        max-width: 780px;
        margin: 36px auto 0 auto;
        color: var(--text-dark);
        box-shadow: 0 24px 70px rgba(0,0,0,0.18);
    }

    .lp-final-title {
        text-align: center;
        color: white;
        font-size: 48px;
        line-height: 1.15;
        font-weight: 950;
        max-width: 900px;
        margin: 0 auto 20px auto;
    }

    .lp-final-sub {
        text-align: center;
        color: rgba(255,255,255,0.60);
        font-size: 20px;
        line-height: 1.55;
    }

    .lp-floating {
        position: fixed;
        left: 50%;
        transform: translateX(-50%);
        bottom: 22px;
        z-index: 9999;
        background: var(--navy);
        color: var(--lime) !important;
        border: 1px solid rgba(223,255,107,0.38);
        box-shadow: 0 18px 55px rgba(0,43,61,0.36);
        padding: 17px 34px;
        border-radius: 999px;
        font-weight: 950;
        font-size: 17px;
        text-decoration: none !important;
    }

    .lp-up {
        position: fixed;
        left: 22px;
        bottom: 22px;
        z-index: 9998;
        width: 58px;
        height: 58px;
        border-radius: 999px;
        background: var(--navy);
        color: white !important;
        border: 1px solid rgba(255,255,255,0.12);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 28px;
        text-decoration: none !important;
        box-shadow: 0 18px 45px rgba(0,0,0,0.18);
    }

    /* =========================
       SISTEMA INTERNO
    ========================= */

    .app-header,
    .menu-panel,
    .page-panel,
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
        color: var(--lime);
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
        color: var(--lime);
        margin-bottom: 12px;
    }

    .page-panel,
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
        color: var(--lime);
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
        color: var(--lime);
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
        box-shadow: inset 0 0 12px rgba(0,0,0,0.04);
    }

    .stTextArea textarea {
        min-height: 110px !important;
    }

    .stTextInput input::placeholder,
    .stTextArea textarea::placeholder {
        color: #9aa9b1 !important;
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
        box-shadow: 0 18px 45px rgba(0,0,0,0.15) !important;
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
        transition: all 0.18s ease-in-out;
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

    div[role="radiogroup"] label:hover {
        background: rgba(223,255,107,0.14) !important;
        border: 1px solid rgba(223,255,107,0.38) !important;
    }

    div[role="radiogroup"] label * {
        color: white !important;
        font-weight: 850 !important;
    }

    button[data-baseweb="tab"] {
        font-size: 15px !important;
        font-weight: 900 !important;
        color: rgba(255,255,255,0.70) !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: var(--lime) !important;
        border-bottom: 2px solid var(--lime) !important;
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
        .lp-hero-grid,
        .lp-profile-grid,
        .lp-steps,
        .lp-testimonial-grid {
            grid-template-columns: 1fr;
        }

        .lp-title {
            font-size: 42px;
        }

        .lp-subtitle {
            font-size: 18px;
        }

        .lp-section-title,
        .lp-final-title,
        .lp-trust-title {
            font-size: 34px;
        }

        .lp-dashboard-mock {
            min-height: 360px;
        }

        .lp-compare-row {
            grid-template-columns: 1fr;
        }

        .lp-floating {
            width: calc(100% - 120px);
            text-align: center;
            padding: 15px 18px;
            font-size: 15px;
        }

        .lp-up {
            width: 54px;
            height: 54px;
            left: 14px;
            bottom: 22px;
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
                    <div class="app-title">Painel Global Software</div>
                    <div class="app-subtitle">
                        Área atual: <b>{menu_atual}</b>. Gestão completa, clara, segura e profissional.
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
# BANCO DE DADOS E MIGRAÇÃO
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

    con.commit()
    con.close()

    adicionar_coluna("estoque", "estoque_minimo", "REAL DEFAULT 0")
    adicionar_coluna("estoque", "codigo", "TEXT")
    adicionar_coluna("clientes", "limite_credito", "REAL DEFAULT 0")
    adicionar_coluna("clientes", "status_cliente", "TEXT DEFAULT 'Ativo'")


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


# =====================================================
# DADOS FIXOS
# =====================================================

TIPOS_USUARIO = ["Administrador", "Gerente", "Financeiro", "Vendedor"]

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
        "MEI / Imposto fixo",
        "Folha de pagamento"
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

CONTAS = ["Caixa", "Banco", "Conta digital", "Carteira", "Cartão", "Outro"]
STATUS_OPCOES = ["Pendente", "Pago", "Recebido"]


# =====================================================
# TELA PÚBLICA LANDING PAGE PREMIUM
# =====================================================

def logo_html_publica():
    if logo_base64:
        return f'<img src="data:image/png;base64,{logo_base64}">'
    return "GS"


def tela_publica_comercial():
    st.markdown(
        f"""
        <div class="lp-wrap" id="topo">
            <a class="lp-up" href="#topo">↑</a>
            <a class="lp-floating" href="#demo">Agendar Demonstração →</a>

            <div class="lp-topbar">
                <div class="lp-brand">
                    <div class="lp-logo">{logo_html_publica()}</div>
                    <div>
                        <div class="lp-brand-title">GLOBAL SOFTWARE</div>
                        <div class="lp-brand-sub">Sistema financeiro completo para empresas</div>
                    </div>
                </div>
                <div class="lp-top-actions">
                    <div class="lp-pill">Gestão • Financeiro • Estoque • Folha</div>
                </div>
            </div>

            <section class="lp-hero">
                <div class="lp-hero-grid">
                    <div>
                        <div class="lp-kicker">PLATAFORMA DE GESTÃO FINANCEIRA</div>
                        <div class="lp-title">
                            Software financeiro completo que sua empresa <span>precisa</span>.
                        </div>
                        <div class="lp-subtitle">
                            Controle contas a pagar, receber, clientes inadimplentes, estoque, funcionários,
                            folha de pagamento, metas, comissões, bônus e relatórios em uma única plataforma.
                        </div>
                        <div class="lp-cta-row">
                            <div class="lp-fake-btn-primary">Agendar Demonstração →</div>
                            <div class="lp-fake-btn-secondary">Acessar sistema</div>
                        </div>
                    </div>

                    <div class="lp-dashboard-mock">
                        <div class="lp-mock-screen">
                            <div class="lp-mock-bar"></div>
                            <div class="lp-mock-card-row">
                                <div class="lp-mock-card">
                                    <div class="lp-mock-label">Receita do mês</div>
                                    <div class="lp-mock-value">R$ 84.750</div>
                                </div>
                                <div class="lp-mock-card">
                                    <div class="lp-mock-label">Lucro previsto</div>
                                    <div class="lp-mock-value">R$ 26.400</div>
                                </div>
                            </div>
                            <div class="lp-mock-card-row">
                                <div class="lp-mock-card">
                                    <div class="lp-mock-label">Inadimplentes</div>
                                    <div class="lp-mock-value">12</div>
                                </div>
                                <div class="lp-mock-card">
                                    <div class="lp-mock-label">Folha do mês</div>
                                    <div class="lp-mock-value">R$ 18.900</div>
                                </div>
                            </div>
                            <div class="lp-mock-chart"></div>
                        </div>
                    </div>
                </div>
            </section>

            <section class="lp-trust">
                <div class="lp-container">
                    <div class="lp-trust-title">
                        A plataforma para empresas que querem sair do <span>improviso</span>.
                    </div>
                </div>
            </section>
        </div>
        """,
        unsafe_allow_html=True
    )

    col_acesso, col_demo = st.columns([1, 1])

    with col_acesso:
        if st.button("Acessar área do sistema", use_container_width=True, key="btn_login_landing"):
            st.session_state.tela_login_ativa = True
            st.rerun()

    with col_demo:
        st.write("")

    st.markdown(
        """
        <div class="lp-wrap">
            <section class="lp-section-white">
                <div class="lp-container">
                    <div class="lp-section-kicker">FUNCIONALIDADES</div>
                    <div class="lp-section-title">
                        Tudo o que seu financeiro precisa, em uma única plataforma.
                    </div>

                    <div class="lp-feature-tabs">
                        <div class="lp-tab-active">▣ Contas a Pagar</div>
                        <div class="lp-tab">▤ Contas a Receber</div>
                        <div class="lp-tab">↻ Inadimplentes</div>
                        <div class="lp-tab">▥ Estoque</div>
                        <div class="lp-tab">◉ Folha</div>
                        <div class="lp-tab">▧ Relatórios</div>
                    </div>

                    <div class="lp-feature-card-dark">
                        <div class="lp-chip">▣ Gestão Financeira</div>
                        <div class="lp-feature-title">
                            Controle ponta a ponta da operação financeira.
                        </div>

                        <div class="lp-check-list">
                            <div class="lp-check-item">
                                <div class="lp-check-icon">✓</div>
                                <div>
                                    <div class="lp-check-title">Contas a pagar e receber</div>
                                    <div class="lp-check-text">Visualize vencimentos, status, formas de pagamento e valores pendentes com clareza.</div>
                                </div>
                            </div>

                            <div class="lp-check-item">
                                <div class="lp-check-icon">✓</div>
                                <div>
                                    <div class="lp-check-title">Clientes inadimplentes</div>
                                    <div class="lp-check-text">Identifique quem deve, quanto deve e gere cobranças pelo WhatsApp com poucos cliques.</div>
                                </div>
                            </div>

                            <div class="lp-check-item">
                                <div class="lp-check-icon">✓</div>
                                <div>
                                    <div class="lp-check-title">Contas pagas no mês</div>
                                    <div class="lp-check-text">Acompanhe tudo que foi pago ou recebido no mês e veja o impacto no caixa.</div>
                                </div>
                            </div>

                            <div class="lp-check-item">
                                <div class="lp-check-icon">✓</div>
                                <div>
                                    <div class="lp-check-title">Relatórios e DRE gerencial</div>
                                    <div class="lp-check-text">Exporte PDF, CSV e acompanhe receita, despesas, lucro e resultado da empresa.</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <section class="lp-section-white">
                <div class="lp-container">
                    <div class="lp-section-kicker">PARA CADA PERFIL</div>
                    <div class="lp-section-title">
                        Valor real para cada nível da organização.
                    </div>

                    <div class="lp-profile-grid">
                        <div class="lp-profile-card">
                            <div class="lp-icon-box">▥</div>
                            <div class="lp-profile-title">Estratégico</div>
                            <div class="lp-profile-sub">Do achismo à previsibilidade.</div>

                            <div class="lp-profile-feature">
                                <b>DRE e fluxo de caixa</b>
                                <span>Visão clara de receita, saídas, lucro, contas pagas e valores a receber.</span>
                            </div>

                            <div class="lp-profile-feature">
                                <b>Decisão com dados</b>
                                <span>O empresário sabe onde está ganhando, onde está perdendo e onde precisa agir.</span>
                            </div>

                            <div class="lp-profile-feature">
                                <b>Crescimento organizado</b>
                                <span>Menos improviso, mais gestão e mais previsibilidade para crescer.</span>
                            </div>
                        </div>

                        <div class="lp-profile-card">
                            <div class="lp-icon-box">👥</div>
                            <div class="lp-profile-title">Gerencial</div>
                            <div class="lp-profile-sub">O fim do caos operacional.</div>

                            <div class="lp-profile-feature">
                                <b>Clientes e inadimplência</b>
                                <span>Cadastro completo, limite de crédito, status e acompanhamento de pendências.</span>
                            </div>

                            <div class="lp-profile-feature">
                                <b>Controle de permissões</b>
                                <span>Administrador, gerente, financeiro e vendedor com acessos separados.</span>
                            </div>

                            <div class="lp-profile-feature">
                                <b>Estoque e operação</b>
                                <span>Produtos, custo, preço de venda, estoque mínimo e lucro previsto.</span>
                            </div>
                        </div>

                        <div class="lp-profile-card">
                            <div class="lp-icon-box">⚙</div>
                            <div class="lp-profile-title">Operacional</div>
                            <div class="lp-profile-sub">Adeus ao trabalho manual.</div>

                            <div class="lp-profile-feature">
                                <b>Folha completa</b>
                                <span>Salário, horas extras, comissão, bônus, premiação, descontos e metas.</span>
                            </div>

                            <div class="lp-profile-feature">
                                <b>WhatsApp de cobrança</b>
                                <span>Gere mensagens e links prontos para cobrar ou atender clientes.</span>
                            </div>

                            <div class="lp-profile-feature">
                                <b>IA de ajuda</b>
                                <span>O usuário pergunta como usar o sistema e recebe orientação dentro da plataforma.</span>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <section class="lp-section-dark">
                <div class="lp-container">
                    <div class="lp-section-kicker dark">DEMONSTRAÇÃO</div>
                    <div class="lp-section-title dark">
                        Veja como a Global Software funciona na prática.
                    </div>

                    <div class="lp-feature-card-dark">
                        <div style="text-align:center;">
                            <div style="width:96px;height:96px;border-radius:28px;background:rgba(223,255,107,0.18);display:flex;align-items:center;justify-content:center;margin:0 auto 24px auto;color:#dfff6b;font-size:44px;">▶</div>
                            <div style="font-size:32px;font-weight:950;color:white;margin-bottom:14px;">Explore a plataforma</div>
                            <div style="font-size:20px;line-height:1.55;color:rgba(255,255,255,0.62);max-width:760px;margin:0 auto 30px auto;">
                                Navegue pela demonstração e veja como controlar financeiro, estoque, clientes,
                                funcionários, folha de pagamento e relatórios em um único lugar.
                            </div>
                            <div class="lp-fake-btn-primary">Demonstração Interativa →</div>
                        </div>
                    </div>
                </div>
            </section>

            <section class="lp-section-white">
                <div class="lp-container">
                    <div class="lp-section-kicker">IMPLANTAÇÃO</div>
                    <div class="lp-section-title">
                        Um processo ágil, consultivo e feito junto com você.
                    </div>

                    <div class="lp-steps">
                        <div class="lp-step">
                            <div class="lp-step-icon">🚀</div>
                            <div class="lp-step-small">ETAPA 1</div>
                            <div class="lp-step-title">Configuração inicial</div>
                            <div class="lp-step-text">Parametrizamos empresa, usuários, categorias, permissões e estrutura do sistema.</div>
                        </div>

                        <div class="lp-step">
                            <div class="lp-step-icon">🎓</div>
                            <div class="lp-step-small">ETAPA 2</div>
                            <div class="lp-step-title">Treinamento mão na massa</div>
                            <div class="lp-step-text">Ensinamos como cadastrar lançamentos, clientes, estoque, funcionários e folha.</div>
                        </div>

                        <div class="lp-step">
                            <div class="lp-step-icon">▶</div>
                            <div class="lp-step-small">ETAPA 3</div>
                            <div class="lp-step-title">Go-live</div>
                            <div class="lp-step-text">A empresa começa a usar o sistema com acompanhamento nos primeiros passos.</div>
                        </div>

                        <div class="lp-step">
                            <div class="lp-step-icon">🎧</div>
                            <div class="lp-step-small">ETAPA 4</div>
                            <div class="lp-step-title">Suporte rápido</div>
                            <div class="lp-step-text">Atendimento humano por WhatsApp, treinamento e melhoria contínua.</div>
                        </div>
                    </div>
                </div>
            </section>

            <section class="lp-section-dark">
                <div class="lp-container">
                    <div class="lp-section-title dark" style="text-align:left;margin-left:0;">
                        Veja o que nossos clientes dizem sobre a <span>transformação</span> financeira.
                    </div>

                    <div class="lp-testimonial-grid">
                        <div class="lp-testimonial">
                            <div class="lp-quote">“</div>
                            <div class="lp-testimonial-text">
                                Antes era tudo no caderno e no WhatsApp. Agora consigo ver contas, clientes,
                                pagamentos e estoque em poucos minutos.
                            </div>
                            <div class="lp-person">
                                <b>Cliente varejo</b>
                                <span>Pequena empresa</span>
                            </div>
                        </div>

                        <div class="lp-testimonial">
                            <div class="lp-quote">“</div>
                            <div class="lp-testimonial-text">
                                A folha de pagamento ficou muito mais organizada. Comissão, bônus e metas ficaram claros para todos.
                            </div>
                            <div class="lp-person">
                                <b>Gestor comercial</b>
                                <span>Equipe de vendas</span>
                            </div>
                        </div>

                        <div class="lp-testimonial">
                            <div class="lp-quote">“</div>
                            <div class="lp-testimonial-text">
                                O dashboard mostrou onde a empresa estava perdendo dinheiro. Foi uma virada na nossa gestão.
                            </div>
                            <div class="lp-person">
                                <b>Empresário</b>
                                <span>Prestação de serviços</span>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <section class="lp-section-white">
                <div class="lp-container">
                    <div class="lp-section-title">
                        Por que a Global Software?
                    </div>

                    <div class="lp-compare">
                        <div class="lp-compare-row">
                            <div class="lp-compare-cell"><strong>Controle financeiro</strong></div>
                            <div class="lp-compare-cell lp-good">✓ Global Software<br>Financeiro, clientes, estoque e folha no mesmo lugar.</div>
                            <div class="lp-compare-cell lp-bad">× Planilhas<br>Dados espalhados e difíceis de acompanhar.</div>
                        </div>

                        <div class="lp-compare-row">
                            <div class="lp-compare-cell"><strong>Implantação</strong></div>
                            <div class="lp-compare-cell lp-good">✓ Rápida e guiada<br>Configuração e treinamento com orientação.</div>
                            <div class="lp-compare-cell lp-bad">× Sistemas comuns<br>Cliente recebe acesso e precisa se virar sozinho.</div>
                        </div>

                        <div class="lp-compare-row">
                            <div class="lp-compare-cell"><strong>Usuários e permissões</strong></div>
                            <div class="lp-compare-cell lp-good">✓ Controle por função<br>Administrador, gerente, financeiro e vendedor.</div>
                            <div class="lp-compare-cell lp-bad">× Sem controle<br>Todo mundo vê tudo ou ninguém sabe usar.</div>
                        </div>

                        <div class="lp-compare-row">
                            <div class="lp-compare-cell"><strong>Suporte</strong></div>
                            <div class="lp-compare-cell lp-good">✓ Humano e direto<br>Ajuda por WhatsApp e IA de tutorial interno.</div>
                            <div class="lp-compare-cell lp-bad">× Demorado<br>Sem orientação prática para o dia a dia.</div>
                        </div>
                    </div>
                </div>
            </section>

            <section class="lp-section-white">
                <div class="lp-container">
                    <div class="lp-section-title">
                        Perguntas Frequentes
                    </div>

                    <div class="lp-faq">
                        <div class="lp-faq-item">Quanto tempo leva para começar a usar? <span>⌄</span></div>
                        <div class="lp-faq-item">Consigo cadastrar vários usuários? <span>⌄</span></div>
                        <div class="lp-faq-item">O sistema controla clientes inadimplentes? <span>⌄</span></div>
                        <div class="lp-faq-item">Tem controle de estoque e folha de pagamento? <span>⌄</span></div>
                        <div class="lp-faq-item">Consigo gerar relatórios? <span>⌄</span></div>
                        <div class="lp-faq-item">Tem treinamento para minha equipe? <span>⌄</span></div>
                    </div>
                </div>
            </section>

            <section class="lp-section-dark" id="demo">
                <div class="lp-container">
                    <div class="lp-final-title">
                        Pronto para profissionalizar o financeiro da sua empresa?
                    </div>
                    <div class="lp-final-sub">
                        Agende uma demonstração gratuita e veja a Global Software na prática.
                    </div>
                </div>
            </section>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="lp-wrap"><div class="lp-section-dark" style="padding-top:0;"><div class="lp-demo-box">', unsafe_allow_html=True)

    st.markdown("### Agendar demonstração")

    col1, col2 = st.columns(2)

    with col1:
        nome = st.text_input("Seu nome", placeholder="Ex: Fabrício Santos", key="demo_nome")
        empresa = st.text_input("Nome da empresa", placeholder="Ex: Global Software", key="demo_empresa")
        segmento = st.selectbox(
            "Segmento da empresa",
            ["Selecionar", "Comércio", "Serviços", "Veículos", "Oficina", "Igreja / Instituição", "Indústria", "Outro"],
            key="demo_segmento"
        )

    with col2:
        telefone = st.text_input("Telefone / WhatsApp", placeholder="62999999999", key="demo_telefone")
        email = st.text_input("E-mail profissional", placeholder="contato@empresa.com", key="demo_email")
        necessidade = st.selectbox(
            "Principal necessidade",
            ["Controle financeiro", "Estoque", "Clientes inadimplentes", "Folha de pagamento", "Relatórios", "Sistema completo"],
            key="demo_necessidade"
        )

    if st.button("Agendar Demonstração pelo WhatsApp", use_container_width=True, key="btn_agendar_demo_final"):
        if telefone:
            texto = (
                f"Olá! Quero agendar uma demonstração da Global Software.%0A%0A"
                f"Nome: {nome}%0A"
                f"Empresa: {empresa}%0A"
                f"Segmento: {segmento}%0A"
                f"E-mail: {email}%0A"
                f"Necessidade principal: {necessidade}%0A%0A"
                f"Quero ver como o sistema pode ajudar minha empresa."
            )
            link = f"https://wa.me/55{telefone}?text={texto}"
            st.markdown(f"[Abrir WhatsApp para agendar demonstração]({link})")
        else:
            st.warning("Digite o telefone com DDD para gerar o link.")

    st.markdown("</div></div></div>", unsafe_allow_html=True)


# =====================================================
# LOGIN
# =====================================================

def tela_login():
    st.markdown(
        """
        <div class="login-header">
            <div class="login-title">💼 Sistema Financeiro Premium</div>
            <div class="login-subtitle">
                Gestão completa de financeiro, clientes, estoque, funcionários, folha de pagamento, metas e relatórios.
            </div>
            <div class="login-info">
                <b>Login padrão:</b> admin@empresa.com &nbsp;&nbsp;|&nbsp;&nbsp; <b>Senha:</b> 123456
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
                            Controle financeiro completo, clientes, estoque, funcionários, folha de pagamento,
                            metas, relatórios e IA de ajuda.
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
        st.markdown("### Acessar sistema")

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
        st.markdown("### Cadastrar nova empresa")

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
            "Pix e WhatsApp",
            "Relatórios",
            "IA Financeira",
            "Ajuda / Tutorial",
            "Configurações"
        ],

        "Financeiro": [
            "Dashboard",
            "Entradas e Saídas",
            "Contas Pagas no Mês",
            "Clientes Inadimplentes",
            "Folha de Pagamento",
            "Parcelas",
            "Pix e WhatsApp",
            "Relatórios",
            "IA Financeira",
            "Ajuda / Tutorial"
        ],

        "Vendedor": [
            "Dashboard",
            "Clientes / CRM",
            "Clientes Inadimplentes",
            "Pix e WhatsApp",
            "Ajuda / Tutorial"
        ]
    }

    return permissoes.get(tipo, ["Dashboard"])


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


def carregar_funcionarios():
    return consultar(
        """
        SELECT *
        FROM funcionarios
        WHERE empresa_id = ?
        ORDER BY nome ASC
        """,
        (empresa_id_atual(),)
    )


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

    linhas = [
        ("Receita", moeda(ind["receita"])),
        ("Saídas", moeda(ind["saidas"])),
        ("Lucro", moeda(ind["lucro"])),
        ("Caixa", moeda(ind["caixa"])),
        ("Contas pagas no mês", moeda(ind["pagas_mes"])),
        ("A receber", moeda(ind["receber"])),
        ("A pagar", moeda(ind["pagar"])),
        ("Vencidas", moeda(ind["vencidas"])),
    ]

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(2 * cm, y, "Resumo")
    y -= 0.7 * cm
    pdf.setFont("Helvetica", 10)

    for nome, valor in linhas:
        pdf.drawString(2 * cm, y, f"{nome}: {valor}")
        y -= 0.45 * cm

    y -= 0.5 * cm
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(2 * cm, y, "Últimos lançamentos")
    y -= 0.7 * cm
    pdf.setFont("Helvetica", 8)

    if not df.empty:
        ultimos = df.sort_values("data", ascending=False).head(18)

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
# IA DE AJUDA LOCAL
# =====================================================

def responder_ajuda(pergunta):
    p = pergunta.lower()

    if "lançamento" in p or "entrada" in p or "saída" in p or "despesa" in p or "receita" in p:
        return (
            "Para cadastrar uma entrada ou saída, vá na aba **Entradas e Saídas**. "
            "Escolha data, vencimento, tipo, categoria, descrição, valor, forma de pagamento e status. "
            "Se for parcelado, informe o total de parcelas."
        )

    if "cliente" in p and "inadimplente" in p:
        return (
            "Para ver clientes inadimplentes, acesse **Clientes Inadimplentes**. "
            "O sistema considera inadimplente todo cliente que possui Receita vencida."
        )

    if "cliente" in p or "crm" in p:
        return (
            "Para cadastrar clientes, vá em **Clientes / CRM**. "
            "Preencha nome, telefone, e-mail, documento, limite de crédito, tipo e observação."
        )

    if "estoque" in p or "produto" in p:
        return (
            "Para controlar estoque, acesse **Estoque**. "
            "Cadastre produto, código, categoria, quantidade, estoque mínimo, custo, preço de venda e fornecedor."
        )

    if "funcionário" in p or "funcionario" in p:
        return (
            "Para cadastrar funcionários, acesse **Funcionários**. "
            "Informe nome, cargo, telefone, documento, data de admissão, salário base, tipo de contrato e status."
        )

    if "folha" in p or "pagamento" in p or "salário" in p or "salario" in p:
        return (
            "Para montar a folha de pagamento, acesse **Folha de Pagamento**. "
            "Selecione funcionário, mês, salário, horas extras, comissão, bônus, premiação, descontos e status."
        )

    if "meta" in p or "premiação" in p or "premiacao" in p or "bônus" in p or "bonus" in p:
        return (
            "Para cadastrar metas e premiações, vá em **Metas e Premiações**. "
            "Selecione funcionário, informe meta, realizado, prêmio e status."
        )

    if "relatório" in p or "relatorio" in p or "pdf" in p:
        return (
            "Para gerar relatório, acesse **Relatórios**. "
            "Você pode baixar PDF financeiro e arquivos CSV."
        )

    if "whatsapp" in p or "cobrança" in p or "cobranca" in p:
        return (
            "Para gerar mensagem de WhatsApp, vá em **Pix e WhatsApp**. "
            "Digite telefone, nome, valor, vencimento e gere o link pronto."
        )

    if "dashboard" in p or "painel" in p:
        return (
            "O **Dashboard** mostra receita, saídas, lucro, caixa, contas pagas no mês, "
            "clientes inadimplentes, estoque, folha de pagamento, contas a receber e contas vencidas."
        )

    return (
        "Posso te ajudar com lançamentos, clientes, inadimplentes, estoque, funcionários, folha, metas, "
        "relatórios, WhatsApp e dashboard. Exemplo: **como cadastrar funcionário?**"
    )


# =====================================================
# APRESENTAÇÃO COMERCIAL ADMIN
# =====================================================

def tela_apresentacao_comercial():
    if tipo_usuario_atual() != "Administrador":
        st.warning("Esta área é exclusiva para administrador.")
        return

    st.markdown(
        """
        <div class="commercial-panel">
            <h1 style="color:white;">🚀 Apresentação Comercial Global Software</h1>
            <p style="font-size:18px;color:rgba(255,255,255,0.70);line-height:1.6;">
            Use esta página como roteiro para vender o sistema. Mostre que a Global Software não é apenas
            um financeiro, mas uma central de controle para a empresa.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        comercial_card(
            "Dor principal",
            "A empresa vende, mas não sabe exatamente quanto lucra, quem deve, o que venceu e para onde o dinheiro vai."
        )

    with c2:
        comercial_card(
            "Solução",
            "Financeiro, clientes, inadimplência, estoque, funcionários, folha, metas e relatórios em uma plataforma."
        )

    with c3:
        comercial_card(
            "Resultado",
            "Mais clareza, menos prejuízo, decisões com dados e uma empresa preparada para crescer."
        )

    st.markdown('<div class="commercial-panel">', unsafe_allow_html=True)
    st.markdown("## Roteiro de venda")

    roteiro = """
Olá, tudo bem? Deixa eu te fazer uma pergunta: sua empresa sabe exatamente quanto lucra, quanto tem para receber, quanto pagou no mês, quais clientes estão inadimplentes e quanto custa sua equipe?

A maioria das empresas não quebra por falta de venda. Quebra por falta de controle.

A Global Software resolve isso em um só lugar:
controle financeiro, clientes, inadimplentes, estoque, funcionários, folha de pagamento, bônus, comissão, horas extras, metas, premiações, relatórios e IA de ajuda.

Na prática, o empresário passa a enxergar a empresa de verdade:
o que entrou, o que saiu, quem deve, o que está vencido, o que está parado no estoque e quanto custa a operação.

Não é apenas um sistema. É uma central de controle para a empresa crescer com organização.
"""
    st.text_area("Roteiro de apresentação", value=roteiro, height=260, key="roteiro_venda_completo")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="commercial-panel">', unsafe_allow_html=True)
    st.markdown("## Sugestão de planos comerciais")

    p1, p2, p3 = st.columns(3)

    with p1:
        preco_card(
            "Plano Gestão Inicial",
            "R$ 147/mês",
            "Financeiro, clientes, contas a pagar, contas a receber, inadimplentes e relatórios básicos."
        )

    with p2:
        preco_card(
            "Plano Gestão Completa",
            "R$ 297/mês",
            "Inclui financeiro, CRM, estoque, funcionários, folha, metas, premiações e relatórios."
        )

    with p3:
        preco_card(
            "Plano Premium Personalizado",
            "Sob consulta",
            "Identidade visual, treinamento, implantação, suporte, IA avançada e integrações futuras."
        )

    st.markdown("</div>", unsafe_allow_html=True)


# =====================================================
# APP PRINCIPAL
# =====================================================

def app():
    usuario = st.session_state.usuario

    if Path("logo.png").exists():
        st.sidebar.image("logo.png", use_container_width=True)

    st.sidebar.title("💼 Global Software")
    st.sidebar.write(f"**Empresa:** {usuario['empresa_nome']}")
    st.sidebar.write(f"**Usuário:** {usuario['nome']}")
    st.sidebar.write(f"**Tipo:** {usuario['tipo']}")

    df = carregar_lancamentos()
    clientes = carregar_clientes()
    estoque = carregar_estoque()
    funcionarios = carregar_funcionarios()
    folha = carregar_folha()
    metas = carregar_metas()

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

    # =================================================
    # DASHBOARD
    # =================================================

    if menu == "Dashboard":
        st.title("📊 Dashboard Executivo Premium")

        inadimplentes_df = pd.DataFrame()
        if not df.empty:
            inadimplentes_df = df[
                (df["tipo"] == "Receita") &
                (df["status_real"] == "Vencido")
            ]

        total_estoque_custo = 0
        total_estoque_venda = 0
        itens_baixo = 0

        if not estoque.empty:
            estoque["valor_custo_total"] = estoque["quantidade"] * estoque["custo_unitario"]
            estoque["valor_venda_total"] = estoque["quantidade"] * estoque["preco_venda"]
            total_estoque_custo = estoque["valor_custo_total"].sum()
            total_estoque_venda = estoque["valor_venda_total"].sum()
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
            st.info("Nenhum lançamento cadastrado ainda.")
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

    # =================================================
    # ENTRADAS E SAÍDAS
    # =================================================

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
                novo_valor = st.number_input(
                    "Novo valor",
                    min_value=0.0,
                    value=float(item["valor"]),
                    step=1.0,
                    key="edit_valor"
                )

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
                executar(
                    "DELETE FROM lancamentos WHERE id = ? AND empresa_id = ?",
                    (int(id_edit), empresa_id_atual())
                )
                st.warning("Excluído.")
                st.rerun()

    # =================================================
    # CONTAS PAGAS
    # =================================================

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

    # =================================================
    # CLIENTES
    # =================================================

    elif menu == "Clientes / CRM":
        st.title("👥 Clientes / CRM")

        with st.form("form_cliente"):
            col1, col2 = st.columns(2)

            with col1:
                nome = st.text_input("Nome", key="cliente_nome")
                telefone = st.text_input("Telefone / WhatsApp", key="cliente_telefone")
                email = st.text_input("E-mail", key="cliente_email")
                documento = st.text_input("CPF / CNPJ", key="cliente_documento")

            with col2:
                tipo_cliente = st.selectbox("Tipo", ["Cliente", "Fornecedor", "Parceiro"], key="cliente_tipo")
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
                    (
                        empresa_id_atual(),
                        nome,
                        telefone,
                        email,
                        documento,
                        tipo_cliente,
                        obs,
                        datetime.now().isoformat(),
                        limite_credito,
                        status_cliente
                    )
                )
                st.success("Cliente salvo.")
                st.rerun()

        if clientes.empty:
            st.info("Nenhum cliente cadastrado.")
        else:
            st.dataframe(clientes, use_container_width=True, hide_index=True)

    # =================================================
    # INADIMPLENTES
    # =================================================

    elif menu == "Clientes Inadimplentes":
        st.title("🚨 Clientes Inadimplentes")

        if df.empty:
            st.info("Nenhum lançamento cadastrado.")
        else:
            inad = df[
                (df["tipo"] == "Receita") &
                (df["status_real"] == "Vencido")
            ].copy()

            if inad.empty:
                st.success("Nenhum cliente inadimplente encontrado.")
            else:
                total_inad = inad["valor"].sum()
                qtd_clientes = inad["cliente_fornecedor"].nunique()

                c1, c2 = st.columns(2)
                with c1:
                    card("Clientes inadimplentes", str(qtd_clientes), "Clientes com receita vencida")
                with c2:
                    card("Valor inadimplente", moeda(total_inad), "Total vencido")

                resumo = inad.groupby("cliente_fornecedor")["valor"].sum().reset_index()
                resumo["valor_formatado"] = resumo["valor"].apply(moeda)

                st.subheader("Resumo por cliente")
                st.dataframe(
                    resumo[["cliente_fornecedor", "valor_formatado"]],
                    use_container_width=True,
                    hide_index=True
                )

                st.subheader("Detalhamento")
                inad["vencimento"] = inad["vencimento"].dt.strftime("%d/%m/%Y")
                inad["valor_formatado"] = inad["valor"].apply(moeda)

                st.dataframe(
                    inad[["vencimento", "cliente_fornecedor", "descricao", "valor_formatado", "forma_pagamento", "observacao"]],
                    use_container_width=True,
                    hide_index=True
                )

    # =================================================
    # ESTOQUE
    # =================================================

    elif menu == "Estoque":
        st.title("📦 Controle de Estoque Completo")

        with st.form("form_estoque"):
            col1, col2, col3 = st.columns(3)

            with col1:
                produto = st.text_input("Produto", key="est_produto")
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
                    (
                        empresa_id_atual(),
                        produto,
                        categoria,
                        quantidade,
                        custo_unitario,
                        preco_venda,
                        fornecedor,
                        obs,
                        datetime.now().isoformat(),
                        estoque_minimo,
                        codigo
                    )
                )
                st.success("Produto salvo.")
                st.rerun()

        if estoque.empty:
            st.info("Nenhum produto cadastrado.")
        else:
            estoque["valor_custo_total"] = estoque["quantidade"] * estoque["custo_unitario"]
            estoque["valor_venda_total"] = estoque["quantidade"] * estoque["preco_venda"]
            estoque["lucro_previsto"] = estoque["valor_venda_total"] - estoque["valor_custo_total"]
            estoque["alerta"] = estoque.apply(
                lambda x: "Baixo estoque" if x["quantidade"] <= x["estoque_minimo"] else "OK",
                axis=1
            )

            c1, c2, c3 = st.columns(3)
            with c1:
                card("Valor em custo", moeda(estoque["valor_custo_total"].sum()), "Valor investido no estoque")
            with c2:
                card("Valor em venda", moeda(estoque["valor_venda_total"].sum()), "Potencial de venda")
            with c3:
                card("Lucro previsto", moeda(estoque["lucro_previsto"].sum()), "Venda menos custo")

            st.dataframe(estoque, use_container_width=True, hide_index=True)

    # =================================================
    # FUNCIONÁRIOS
    # =================================================

    elif menu == "Funcionários":
        st.title("👨‍💼 Cadastro de Funcionários")

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
                    (
                        empresa_id_atual(),
                        nome,
                        cargo,
                        telefone,
                        documento,
                        str(data_admissao),
                        salario_base,
                        tipo_contrato,
                        status_fun,
                        obs,
                        datetime.now().isoformat()
                    )
                )
                st.success("Funcionário salvo.")
                st.rerun()

        if funcionarios.empty:
            st.info("Nenhum funcionário cadastrado.")
        else:
            funcionarios["salario_formatado"] = funcionarios["salario_base"].apply(moeda)
            st.dataframe(funcionarios, use_container_width=True, hide_index=True)

    # =================================================
    # FOLHA
    # =================================================

    elif menu == "Folha de Pagamento":
        st.title("🧾 Folha de Pagamento Completa")

        if funcionarios.empty:
            st.warning("Cadastre funcionários antes de lançar folha de pagamento.")
        else:
            func_dict = {
                f"{row['nome']} - {row['cargo']}": int(row["id"])
                for _, row in funcionarios.iterrows()
            }

            with st.form("form_folha"):
                col1, col2, col3 = st.columns(3)

                with col1:
                    funcionario_label = st.selectbox("Funcionário", list(func_dict.keys()), key="folha_func")
                    funcionario_id = func_dict[funcionario_label]
                    mes_ref = st.text_input("Mês referência", value=mes_atual_str(), key="folha_mes")
                    funcionario_row = funcionarios[funcionarios["id"] == funcionario_id].iloc[0]
                    salario = st.number_input(
                        "Salário base",
                        min_value=0.0,
                        value=float(funcionario_row["salario_base"] or 0),
                        step=100.0,
                        key="folha_salario"
                    )

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

                bruto, liquido = calcular_folha_total(
                    salario,
                    horas_extras,
                    valor_hora_extra,
                    comissao,
                    bonus,
                    premiacao,
                    desconto
                )

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

    # =================================================
    # METAS
    # =================================================

    elif menu == "Metas e Premiações":
        st.title("🎯 Metas e Premiações")

        if funcionarios.empty:
            st.warning("Cadastre funcionários antes de criar metas.")
        else:
            func_dict = {
                f"{row['nome']} - {row['cargo']}": int(row["id"])
                for _, row in funcionarios.iterrows()
            }

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
                        (
                            empresa_id_atual(),
                            funcionario_id,
                            mes_ref,
                            descricao,
                            meta_valor,
                            realizado,
                            premio,
                            status_meta,
                            datetime.now().isoformat()
                        )
                    )
                    st.success("Meta salva.")
                    st.rerun()

        if metas.empty:
            st.info("Nenhuma meta cadastrada.")
        else:
            metas["meta_formatada"] = metas["meta_valor"].apply(moeda)
            metas["realizado_formatado"] = metas["realizado"].apply(moeda)
            metas["premio_formatado"] = metas["premio"].apply(moeda)
            metas["percentual"] = metas.apply(
                lambda x: percentual((x["realizado"] / x["meta_valor"] * 100) if x["meta_valor"] else 0),
                axis=1
            )

            st.dataframe(metas, use_container_width=True, hide_index=True)

    # =================================================
    # PARCELAS
    # =================================================

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

    # =================================================
    # PIX E WHATSAPP
    # =================================================

    elif menu == "Pix e WhatsApp":
        st.title("📲 Pix e WhatsApp")

        aba1, aba2 = st.tabs(["Cobrança WhatsApp", "Texto Pix"])

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

    # =================================================
    # RELATÓRIOS
    # =================================================

    elif menu == "Relatórios":
        st.title("📄 Relatórios e Exportações")

        pdf = gerar_pdf_relatorio(df, ind)

        if pdf is None:
            st.warning("Biblioteca reportlab não instalada. Confira o requirements.txt.")
        else:
            st.download_button(
                "Baixar relatório PDF",
                data=pdf,
                file_name="relatorio_financeiro.pdf",
                mime="application/pdf",
                key="download_pdf"
            )

        if not df.empty:
            st.download_button(
                "Baixar lançamentos CSV",
                data=df.to_csv(index=False).encode("utf-8"),
                file_name="lancamentos.csv",
                mime="text/csv",
                key="download_csv_lancamentos"
            )

        if not clientes.empty:
            st.download_button(
                "Baixar clientes CSV",
                data=clientes.to_csv(index=False).encode("utf-8"),
                file_name="clientes.csv",
                mime="text/csv",
                key="download_csv_clientes"
            )

        if not estoque.empty:
            st.download_button(
                "Baixar estoque CSV",
                data=estoque.to_csv(index=False).encode("utf-8"),
                file_name="estoque.csv",
                mime="text/csv",
                key="download_csv_estoque"
            )

        if not funcionarios.empty:
            st.download_button(
                "Baixar funcionários CSV",
                data=funcionarios.to_csv(index=False).encode("utf-8"),
                file_name="funcionarios.csv",
                mime="text/csv",
                key="download_csv_funcionarios"
            )

        if not folha.empty:
            st.download_button(
                "Baixar folha CSV",
                data=folha.to_csv(index=False).encode("utf-8"),
                file_name="folha_pagamento.csv",
                mime="text/csv",
                key="download_csv_folha"
            )

    # =================================================
    # IA FINANCEIRA
    # =================================================

    elif menu == "IA Financeira":
        st.title("🤖 IA Financeira")

        if df.empty:
            st.info("Cadastre lançamentos para receber uma análise.")
        else:
            if ind["lucro"] < 0:
                st.markdown(
                    """
                    <div class="danger-box">
                    A empresa está com resultado negativo. Revise despesas, custos, folha de pagamento e inadimplência.
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            elif ind["vencidas"] > 0:
                st.markdown(
                    """
                    <div class="warning-box">
                    Existem contas vencidas ou clientes inadimplentes. Priorize cobrança e renegociação.
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    """
                    <div class="success-box">
                    O controle está saudável. Continue acompanhando caixa, estoque, folha e metas.
                    </div>
                    """,
                    unsafe_allow_html=True
                )

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

    # =================================================
    # AJUDA
    # =================================================

    elif menu == "Ajuda / Tutorial":
        st.title("🆘 Ajuda / Tutorial do Sistema")

        st.markdown(
            """
            ### Como usar o sistema

            **1. Dashboard**  
            Mostra os principais indicadores da empresa.

            **2. Entradas e Saídas**  
            Cadastre receitas, despesas, custos, dívidas, investimentos e retiradas.

            **3. Contas Pagas no Mês**  
            Veja tudo que foi pago ou recebido no mês selecionado.

            **4. Clientes / CRM**  
            Cadastre clientes, fornecedores, contatos e limite de crédito.

            **5. Clientes Inadimplentes**  
            Mostra clientes com receitas vencidas.

            **6. Estoque**  
            Controle produtos, quantidade, estoque mínimo, custo e preço de venda.

            **7. Funcionários**  
            Cadastre a equipe da empresa.

            **8. Folha de Pagamento**  
            Calcule salário, horas extras, comissão, bônus, premiação, descontos e total líquido.

            **9. Metas e Premiações**  
            Controle metas da equipe, realizado, prêmio e status.

            **10. Relatórios**  
            Baixe PDF e planilhas CSV.
            """
        )

        st.divider()

        st.subheader("🤖 IA de Ajuda do Sistema")

        pergunta = st.text_area(
            "Digite sua dúvida",
            placeholder="Exemplo: como cadastrar funcionário? como ver clientes inadimplentes? como lançar folha de pagamento?",
            key="pergunta_ajuda_sistema"
        )

        if st.button("Perguntar para IA de ajuda", use_container_width=True, key="btn_ia_ajuda"):
            if pergunta.strip():
                st.success(responder_ajuda(pergunta))
            else:
                st.warning("Digite sua dúvida para a IA responder.")

    # =================================================
    # APRESENTAÇÃO
    # =================================================

    elif menu == "Apresentação Comercial":
        st.title("🚀 Apresentação Comercial")
        tela_apresentacao_comercial()

    # =================================================
    # USUÁRIOS
    # =================================================

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

    # =================================================
    # CONFIGURAÇÕES
    # =================================================

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
            "clientes": clientes.to_dict(orient="records") if not clientes.empty else [],
            "estoque": estoque.to_dict(orient="records") if not estoque.empty else [],
            "funcionarios": funcionarios.to_dict(orient="records") if not funcionarios.empty else [],
            "folha": folha.to_dict(orient="records") if not folha.empty else [],
            "metas": metas.to_dict(orient="records") if not metas.empty else [],
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