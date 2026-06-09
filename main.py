import streamlit as st
import pandas as pd
import sqlite3
import hashlib
import json
from datetime import date, datetime, timedelta
from io import BytesIO
from urllib.parse import quote


# =====================================================
# CONFIGURAÇÃO INICIAL
# =====================================================

st.set_page_config(
    page_title="Sistema Financeiro Premium",
    page_icon="💼",
    layout="wide"
)

DB_PATH = "sistema_financeiro.db"


# =====================================================
# ESTILO VISUAL
# =====================================================

st.markdown(
    """
    <style>
    .main {
        background-color: #f6f7fb;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #36115c 0%, #171321 100%);
        color: white;
    }

    [data-testid="stSidebar"] * {
        color: white;
    }

    .metric-card {
        background: white;
        border-radius: 18px;
        padding: 22px;
        box-shadow: 0 4px 18px rgba(0,0,0,0.08);
        border-left: 6px solid #7c3aed;
        min-height: 120px;
    }

    .metric-title {
        color: #6b7280;
        font-size: 14px;
        font-weight: 600;
    }

    .metric-value {
        color: #111827;
        font-size: 28px;
        font-weight: 800;
        margin-top: 4px;
    }

    .metric-sub {
        color: #6b7280;
        font-size: 13px;
        margin-top: 2px;
    }

    .success-box {
        background: #ecfdf5;
        border-left: 5px solid #10b981;
        padding: 12px;
        border-radius: 10px;
        color: #064e3b;
    }

    .warning-box {
        background: #fffbeb;
        border-left: 5px solid #f59e0b;
        padding: 12px;
        border-radius: 10px;
        color: #78350f;
    }

    .danger-box {
        background: #fef2f2;
        border-left: 5px solid #ef4444;
        padding: 12px;
        border-radius: 10px;
        color: #7f1d1d;
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


# =====================================================
# BANCO DE DADOS
# =====================================================

def criar_tabelas():
    con = conectar()
    cur = con.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS empresas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            documento TEXT,
            telefone TEXT,
            cidade TEXT,
            criado_em TEXT
        )
        """
    )

    cur.execute(
        """
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
        """
    )

    cur.execute(
        """
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
        """
    )

    cur.execute(
        """
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
        """
    )

    cur.execute(
        """
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
        """
    )

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
            ("Minha Empresa", "", "", "", datetime.now().isoformat())
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
# LOGIN
# =====================================================

def tela_login():
    st.title("💼 Sistema Financeiro Premium")
    st.caption("Controle completo de finanças, empresas, usuários, parcelas, relatórios e clientes.")

    aba1, aba2 = st.tabs(["Entrar", "Criar empresa"])

    with aba1:
        st.subheader("Acessar sistema")

        email = st.text_input("E-mail", key="login_email")
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
                st.rerun()

        st.info("Login padrão para teste: admin@empresa.com | Senha: 123456")

    with aba2:
        st.subheader("Cadastrar nova empresa")

        nome_empresa = st.text_input("Nome da empresa", key="cad_nome_empresa")
        documento = st.text_input("CNPJ / CPF", key="cad_documento")
        telefone = st.text_input("Telefone", key="cad_telefone")
        cidade = st.text_input("Cidade", key="cad_cidade")

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


# =====================================================
# USUÁRIO ATUAL E PERMISSÕES
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
            "Contas a Receber",
            "CRM / Clientes",
            "WhatsApp Manual"
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
# RELATÓRIO PDF
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
# APLICATIVO PRINCIPAL
# =====================================================

def app():
    usuario = st.session_state.usuario

    st.sidebar.title("💼 Sistema Financeiro")
    st.sidebar.write(f"**Empresa:** {usuario['empresa_nome']}")
    st.sidebar.write(f"**Usuário:** {usuario['nome']}")
    st.sidebar.write(f"**Tipo:** {usuario['tipo']}")

    menus_liberados = menus_por_tipo_usuario()

    menu = st.sidebar.radio(
        "Menu",
        menus_liberados,
        key="menu_principal"
    )

    if st.sidebar.button("Sair", key="btn_sair"):
        del st.session_state.usuario
        st.rerun()

    df = carregar_lancamentos()
    ind = calcular_indicadores(df)

    # =================================================
    # DASHBOARD
    # =================================================
    if menu == "Dashboard":
        st.title("📊 Dashboard estilo Nubank")

        if df.empty:
            st.info("Nenhum lançamento cadastrado ainda.")

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            card("Receita total", moeda(ind["receita"]), "Total de entradas")

        with c2:
            card("Lucro líquido", moeda(ind["lucro_liquido"]), percentual(ind["margem_liquida"]))

        with c3:
            card("Saldo em caixa", moeda(ind["caixa"]), "Entradas - saídas")

        with c4:
            card("Vencidas", moeda(ind["vencidas"]), "Atenção")

        st.write("")

        c5, c6, c7, c8 = st.columns(4)

        with c5:
            card("Custos", moeda(ind["custo"]))

        with c6:
            card("Despesas", moeda(ind["despesa_fixa"] + ind["despesa_variavel"]))

        with c7:
            card("A receber", moeda(ind["contas_receber"]))

        with c8:
            card("A pagar", moeda(ind["contas_pagar"]))

        st.divider()

        if not df.empty:
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Evolução mensal")
                mensal = df.groupby(["mes", "tipo"])["valor"].sum().reset_index()
                graf = mensal.pivot(index="mes", columns="tipo", values="valor").fillna(0)
                st.line_chart(graf)

            with col2:
                st.subheader("Categorias")
                cat = df.groupby("categoria")["valor"].sum().sort_values(ascending=False).head(10)
                st.bar_chart(cat)

            st.subheader("Últimos lançamentos")
            tabela = df.sort_values("data", ascending=False).head(10).copy()
            tabela["data"] = tabela["data"].dt.strftime("%d/%m/%Y")
            tabela["vencimento"] = tabela["vencimento"].dt.strftime("%d/%m/%Y")
            st.dataframe(tabela, use_container_width=True)

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
                st.dataframe(parcelas, use_container_width=True)

    # =================================================
    # CONTAS A PAGAR / RECEBER
    # =================================================
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

    # =================================================
    # CONTAS A RECEBER
    # =================================================
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

    # =================================================
    # PIX
    # =================================================
    elif menu == "Pix":
        st.title("💳 Pix")

        chave = st.text_input("Chave Pix", key="pix_chave")
        valor_pix = st.number_input("Valor", min_value=0.0, step=1.0, key="pix_valor")
        descricao_pix = st.text_input("Descrição", key="pix_descricao")

        if st.button("Gerar texto de cobrança", key="btn_pix"):
            texto = f"Olá! Segue cobrança via Pix: Chave: {chave} | Valor: {moeda(valor_pix)} | {descricao_pix}"
            st.code(texto)

    # =================================================
    # PDF
    # =================================================
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

    # =================================================
    # IA FINANCEIRA
    # =================================================
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

    # =================================================
    # CRM
    # =================================================
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

    # =================================================
    # ESTOQUE
    # =================================================
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

    # =================================================
    # WHATSAPP MANUAL
    # =================================================
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

    # =================================================
    # USUÁRIOS E PERMISSÕES
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
                    tipo_user = st.selectbox(
                        "Tipo de usuário",
                        TIPOS_USUARIO,
                        key="user_tipo"
                    )

                    ativo = st.checkbox(
                        "Usuário ativo",
                        value=True,
                        key="user_ativo"
                    )

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
                    nova_senha = st.text_input(
                        "Nova senha",
                        type="password",
                        key="editar_usuario_senha"
                    )

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
                            (
                                novo_tipo,
                                ativo_int,
                                hash_senha(nova_senha),
                                int(id_usuario),
                                empresa_id_atual()
                            )
                        )
                    else:
                        executar(
                            """
                            UPDATE usuarios
                            SET tipo = ?, ativo = ?
                            WHERE id = ? AND empresa_id = ?
                            """,
                            (
                                novo_tipo,
                                ativo_int,
                                int(id_usuario),
                                empresa_id_atual()
                            )
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
                            (
                                int(id_usuario),
                                empresa_id_atual()
                            )
                        )

                        st.warning("Usuário excluído.")
                        st.rerun()

    # =================================================
    # CONFIGURAÇÕES
    # =================================================
    elif menu == "Configurações":
        st.title("⚙️ Configurações")

        empresa = consultar(
            "SELECT * FROM empresas WHERE id = ?",
            (empresa_id_atual(),)
        )

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

if "usuario" not in st.session_state:
    tela_login()
else:
    app()