import streamlit as st
import pandas as pd
import sqlite3
from datetime import date, datetime, timedelta
import os
import urllib.parse
import io

# =========================================================
# CONFIGURAÇÃO DO APP
# =========================================================
st.set_page_config(
    page_title="Sistema Financeiro Profissional",
    page_icon="💰",
    layout="wide"
)

DB_NAME = "financeiro.db"

# =========================================================
# BANCO DE DADOS
# =========================================================
def conectar():
    return sqlite3.connect(DB_NAME, check_same_thread=False)


def executar_sql(query, params=()):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()


def carregar_df(query, params=()):
    conn = conectar()
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df


def garantir_coluna(tabela, coluna, tipo):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({tabela})")
    colunas = [c[1] for c in cursor.fetchall()]

    if coluna not in colunas:
        try:
            cursor.execute(f"ALTER TABLE {tabela} ADD COLUMN {coluna} {tipo}")
            conn.commit()
        except Exception:
            pass
    conn.close()


def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS empresas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            cnpj TEXT,
            telefone TEXT,
            endereco TEXT,
            pix_chave TEXT,
            pix_nome TEXT,
            pix_cidade TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE,
            senha TEXT,
            nome TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lancamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT,
            tipo TEXT,
            categoria TEXT,
            descricao TEXT,
            valor REAL,
            forma_pagamento TEXT,
            status TEXT,
            observacao TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            telefone TEXT,
            cpf TEXT,
            endereco TEXT,
            observacao TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS parcelas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente TEXT,
            descricao TEXT,
            valor REAL,
            vencimento TEXT,
            status TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT,
            tipo TEXT,
            valor REAL,
            vencimento TEXT,
            status TEXT,
            observacao TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS estoque (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto TEXT,
            categoria TEXT,
            quantidade INTEGER,
            valor_custo REAL,
            valor_venda REAL,
            observacao TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS configuracoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            empresa_id INTEGER,
            chave TEXT,
            valor TEXT
        )
    """)

    conn.commit()
    conn.close()

    # Atualização automática do banco antigo
    garantir_coluna("usuarios", "tipo", "TEXT")
    garantir_coluna("usuarios", "empresa_id", "INTEGER")
    garantir_coluna("lancamentos", "empresa_id", "INTEGER")
    garantir_coluna("clientes", "empresa_id", "INTEGER")
    garantir_coluna("parcelas", "empresa_id", "INTEGER")
    garantir_coluna("contas", "empresa_id", "INTEGER")
    garantir_coluna("estoque", "empresa_id", "INTEGER")
    garantir_coluna("empresas", "pix_chave", "TEXT")
    garantir_coluna("empresas", "pix_nome", "TEXT")
    garantir_coluna("empresas", "pix_cidade", "TEXT")

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO empresas 
        (id, nome, cnpj, telefone, endereco, pix_chave, pix_nome, pix_cidade)
        VALUES 
        (1, 'Minha Empresa', '', '', '', '', 'MINHA EMPRESA', 'GOIANIA')
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO usuarios 
        (usuario, senha, nome, tipo, empresa_id)
        VALUES 
        ('admin', '123', 'Administrador', 'Administrador', 1)
    """)

    cursor.execute("UPDATE usuarios SET tipo = 'Administrador' WHERE usuario = 'admin' AND (tipo IS NULL OR tipo = '')")
    cursor.execute("UPDATE usuarios SET empresa_id = 1 WHERE empresa_id IS NULL")

    conn.commit()
    conn.close()


criar_tabelas()

# =========================================================
# FUNÇÕES GERAIS
# =========================================================
def empresa_atual():
    return st.session_state.get("empresa_id", 1)


def formatar_moeda(valor):
    try:
        return f"R$ {float(valor):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        return "R$ 0,00"


def mostrar_tabela(df):
    # Não usa st.dataframe para evitar erro de pyarrow
    if df is None or df.empty:
        st.info("Nenhum registro encontrado.")
        return

    html = df.astype(str).to_html(index=False, escape=False)
    st.markdown("""
        <style>
        table { width: 100%; border-collapse: collapse; font-size: 14px; }
        th { background-color: #111827; color: white; padding: 8px; border: 1px solid #374151; text-align: left; }
        td { padding: 8px; border: 1px solid #374151; }
        tr:nth-child(even) { background-color: rgba(255,255,255,0.04); }
        </style>
    """, unsafe_allow_html=True)
    st.markdown(html, unsafe_allow_html=True)


def carregar_lancamentos():
    return carregar_df(
        "SELECT * FROM lancamentos WHERE IFNULL(empresa_id, 1) = ? ORDER BY data DESC, id DESC",
        (empresa_atual(),)
    )


def carregar_clientes():
    return carregar_df(
        "SELECT * FROM clientes WHERE IFNULL(empresa_id, 1) = ? ORDER BY nome ASC",
        (empresa_atual(),)
    )


def carregar_parcelas():
    return carregar_df(
        "SELECT * FROM parcelas WHERE IFNULL(empresa_id, 1) = ? ORDER BY vencimento ASC",
        (empresa_atual(),)
    )


def carregar_contas():
    return carregar_df(
        "SELECT * FROM contas WHERE IFNULL(empresa_id, 1) = ? ORDER BY vencimento ASC",
        (empresa_atual(),)
    )


def carregar_estoque():
    return carregar_df(
        "SELECT * FROM estoque WHERE IFNULL(empresa_id, 1) = ? ORDER BY produto ASC",
        (empresa_atual(),)
    )


def carregar_empresas():
    return carregar_df("SELECT * FROM empresas ORDER BY nome ASC")


def dados_empresa():
    df = carregar_df("SELECT * FROM empresas WHERE id = ?", (empresa_atual(),))
    if df.empty:
        return None
    return df.iloc[0]

# =========================================================
# PIX
# =========================================================
def crc16(payload):
    crc = 0xFFFF
    polynomial = 0x1021
    for char in payload:
        crc ^= ord(char) << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ polynomial
            else:
                crc <<= 1
            crc &= 0xFFFF
    return f"{crc:04X}"


def campo(id_campo, valor):
    valor = str(valor)
    return f"{id_campo}{len(valor):02d}{valor}"


def gerar_pix_copia_cola(chave, nome, cidade, valor, descricao):
    chave = str(chave).strip()
    nome = str(nome).strip()[:25].upper()
    cidade = str(cidade).strip()[:15].upper()
    descricao = str(descricao).strip()[:25]
    gui = campo("00", "BR.GOV.BCB.PIX")
    chave_pix = campo("01", chave)
    desc = campo("02", descricao) if descricao else ""
    merchant_account = campo("26", gui + chave_pix + desc)
    payload = ""
    payload += campo("00", "01")
    payload += merchant_account
    payload += campo("52", "0000")
    payload += campo("53", "986")
    if valor and float(valor) > 0:
        payload += campo("54", f"{float(valor):.2f}")
    payload += campo("58", "BR")
    payload += campo("59", nome if nome else "EMPRESA")
    payload += campo("60", cidade if cidade else "GOIANIA")
    payload += campo("62", campo("05", "***"))
    payload_sem_crc = payload + "6304"
    return payload_sem_crc + crc16(payload_sem_crc)

# =========================================================
# LOGIN
# =========================================================
def tela_login():
    st.title("💰 Sistema Financeiro Profissional")
    st.subheader("Login de acesso")

    with st.form("form_login"):
        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")
        entrar = st.form_submit_button("Entrar")

    if entrar:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, usuario, senha, nome, IFNULL(tipo, 'Usuário'), IFNULL(empresa_id, 1)
            FROM usuarios 
            WHERE usuario = ? AND senha = ?
        """, (usuario, senha))
        user = cursor.fetchone()
        conn.close()

        if user:
            st.session_state["logado"] = True
            st.session_state["usuario"] = user[1]
            st.session_state["nome"] = user[3]
            st.session_state["tipo"] = user[4]
            st.session_state["empresa_id"] = user[5]
            st.success("Login realizado com sucesso!")
            st.rerun()
        else:
            st.error("Usuário ou senha incorretos.")

# =========================================================
# DASHBOARD
# =========================================================
def pagina_dashboard():
    st.title("📊 Dashboard estilo Nubank")
    df = carregar_lancamentos()

    if df.empty:
        st.info("Nenhum lançamento cadastrado ainda.")
        return

    df["valor"] = pd.to_numeric(df["valor"], errors="coerce").fillna(0)
    df["data"] = pd.to_datetime(df["data"], errors="coerce")

    entradas = df[df["tipo"] == "Entrada"]["valor"].sum()
    saidas = df[df["tipo"] == "Saída"]["valor"].sum()
    saldo = entradas - saidas

    st.markdown("""
        <style>
        .card-nubank { background: linear-gradient(135deg, #6D28D9, #9333EA); padding: 28px; border-radius: 22px; color: white; box-shadow: 0px 8px 25px rgba(0,0,0,0.25); margin-bottom: 18px; }
        .card-nubank h2 { font-size: 20px; margin-bottom: 5px; }
        .card-nubank h1 { font-size: 42px; margin-top: 0px; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="card-nubank">
            <h2>Saldo atual</h2>
            <h1>{formatar_moeda(saldo)}</h1>
            <p>Entradas: {formatar_moeda(entradas)} | Saídas: {formatar_moeda(saidas)}</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("Entradas", formatar_moeda(entradas))
    col2.metric("Saídas", formatar_moeda(saidas))
    col3.metric("Resultado", formatar_moeda(saldo))

    st.divider()
    st.subheader("📈 Evolução financeira")

    df_grafico = df.dropna(subset=["data"]).copy()

    if not df_grafico.empty:
        resumo_diario = df_grafico.groupby(
            [df_grafico["data"].dt.strftime("%d/%m/%Y"), "tipo"]
        )["valor"].sum().reset_index()

        resumo_diario.columns = ["Data", "Tipo", "Valor"]

        resumo_diario["Valor"] = resumo_diario["Valor"].apply(formatar_moeda)

        mostrar_tabela(resumo_diario)
    else:
        st.info("Nenhuma data válida para gerar evolução financeira.")

    st.divider()
    st.subheader("📋 Últimos lançamentos")
    mostrar_tabela(df.head(10))

# =========================================================
# ENTRADAS E SAÍDAS
# =========================================================
def pagina_lancamentos():
    st.title("💵 Entradas e Saídas")

    with st.form("form_lancamento"):
        col1, col2 = st.columns(2)
        with col1:
            data_lancamento = st.date_input("Data", value=date.today())
            tipo = st.selectbox("Tipo", ["Entrada", "Saída"])
            categoria = st.selectbox("Categoria", ["Venda", "Compra", "Despesa", "Salário", "Aluguel", "Combustível", "Manutenção", "Parcela", "Pix", "Promissória", "Outros"])
        with col2:
            valor = st.number_input("Valor", min_value=0.0, step=10.0)
            forma_pagamento = st.selectbox("Forma de pagamento", ["Dinheiro", "Pix", "Cartão", "Boleto", "Promissória", "Transferência"])
            status = st.selectbox("Status", ["Pago", "Pendente", "Atrasado"])
        descricao = st.text_input("Descrição")
        observacao = st.text_area("Observação")
        salvar = st.form_submit_button("Salvar lançamento")

    if salvar:
        executar_sql("""
            INSERT INTO lancamentos 
            (empresa_id, data, tipo, categoria, descricao, valor, forma_pagamento, status, observacao)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (empresa_atual(), str(data_lancamento), tipo, categoria, descricao, valor, forma_pagamento, status, observacao))
        st.success("Lançamento salvo com sucesso!")
        st.rerun()

    st.divider()
    st.subheader("Lançamentos cadastrados")
    df = carregar_lancamentos()
    if not df.empty:
        mostrar_tabela(df)
        id_excluir = st.number_input("ID para excluir lançamento", min_value=1, step=1)
        if st.button("Excluir lançamento"):
            executar_sql("DELETE FROM lancamentos WHERE id = ? AND IFNULL(empresa_id, 1) = ?", (id_excluir, empresa_atual()))
            st.success("Lançamento excluído.")
            st.rerun()
    else:
        st.info("Nenhum lançamento cadastrado.")

# =========================================================
# CONTAS A PAGAR / RECEBER
# =========================================================
def pagina_contas():
    st.title("📅 Contas a Pagar e Receber")

    with st.form("form_contas"):
        descricao = st.text_input("Descrição")
        tipo = st.selectbox("Tipo", ["A pagar", "A receber"])
        valor = st.number_input("Valor", min_value=0.0, step=10.0)
        vencimento = st.date_input("Vencimento")
        status = st.selectbox("Status", ["Pendente", "Pago", "Recebido", "Atrasado"])
        observacao = st.text_area("Observação")
        salvar = st.form_submit_button("Salvar conta")

    if salvar:
        executar_sql("""
            INSERT INTO contas (empresa_id, descricao, tipo, valor, vencimento, status, observacao)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (empresa_atual(), descricao, tipo, valor, str(vencimento), status, observacao))
        st.success("Conta salva com sucesso!")
        st.rerun()

    df = carregar_contas()
    if not df.empty:
        df["valor"] = pd.to_numeric(df["valor"], errors="coerce").fillna(0)
        col1, col2 = st.columns(2)
        col1.metric("Total a pagar", formatar_moeda(df[df["tipo"] == "A pagar"]["valor"].sum()))
        col2.metric("Total a receber", formatar_moeda(df[df["tipo"] == "A receber"]["valor"].sum()))
        mostrar_tabela(df)
    else:
        st.info("Nenhuma conta cadastrada.")


def pagina_contas_receber():
    st.title("💰 Contas a Receber")
    st.subheader("Cadastrar conta a receber")
    clientes = carregar_clientes()
    nomes_clientes = clientes["nome"].tolist() if not clientes.empty else []

    with st.form("form_contas_receber"):
        cliente = st.selectbox("Cliente", nomes_clientes) if nomes_clientes else st.text_input("Cliente")
        descricao = st.text_input("Descrição")
        valor = st.number_input("Valor a receber", min_value=0.0, step=10.0)
        vencimento = st.date_input("Data de vencimento")
        status = st.selectbox("Status", ["Pendente", "Recebido", "Atrasado"])
        forma_pagamento = st.selectbox("Forma de pagamento", ["Dinheiro", "Pix", "Cartão", "Boleto", "Promissória", "Transferência"])
        observacao = st.text_area("Observação")
        salvar = st.form_submit_button("Salvar conta a receber")

    if salvar:
        executar_sql("""
            INSERT INTO contas (empresa_id, descricao, tipo, valor, vencimento, status, observacao)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (empresa_atual(), f"{cliente} - {descricao}", "A receber", valor, str(vencimento), status, f"Forma de pagamento: {forma_pagamento} | {observacao}"))
        st.success("Conta a receber salva com sucesso!")
        st.rerun()

    df = carregar_contas()
    if df.empty:
        st.info("Nenhuma conta a receber cadastrada.")
        return

    df = df[df["tipo"] == "A receber"]
    if df.empty:
        st.info("Nenhuma conta a receber cadastrada.")
        return

    df["valor"] = pd.to_numeric(df["valor"], errors="coerce").fillna(0)
    df["vencimento_data"] = pd.to_datetime(df["vencimento"], errors="coerce").dt.date
    hoje = date.today()
    df.loc[(df["status"] != "Recebido") & (df["status"] != "Pago") & (df["vencimento_data"] < hoje), "status"] = "Atrasado"

    col1, col2, col3 = st.columns(3)
    col1.metric("Total a receber", formatar_moeda(df[df["status"] != "Recebido"]["valor"].sum()))
    col2.metric("Total recebido", formatar_moeda(df[df["status"].isin(["Recebido", "Pago"])]["valor"].sum()))
    col3.metric("Total atrasado", formatar_moeda(df[df["status"] == "Atrasado"]["valor"].sum()))

    filtro = st.selectbox("Filtrar por status", ["Todos", "Pendente", "Recebido", "Atrasado"])
    df_mostrar = df if filtro == "Todos" else df[df["status"] == filtro]
    mostrar_tabela(df_mostrar.drop(columns=["vencimento_data"], errors="ignore"))

    st.divider()
    id_receber = st.number_input("ID da conta recebida", min_value=1, step=1)
    if st.button("Marcar como recebido"):
        executar_sql("UPDATE contas SET status = ? WHERE id = ? AND tipo = ? AND IFNULL(empresa_id, 1) = ?", ("Recebido", id_receber, "A receber", empresa_atual()))
        st.success("Conta marcada como recebida!")
        st.rerun()

    id_excluir = st.number_input("ID para excluir conta a receber", min_value=1, step=1, key="excluir_receber")
    if st.button("Excluir conta a receber"):
        executar_sql("DELETE FROM contas WHERE id = ? AND tipo = ? AND IFNULL(empresa_id, 1) = ?", (id_excluir, "A receber", empresa_atual()))
        st.success("Conta a receber excluída!")
        st.rerun()

# =========================================================
# PARCELAS / CRM / ESTOQUE
# =========================================================
def pagina_parcelas():
    st.title("🧾 Controle de Parcelas")
    clientes = carregar_clientes()
    nomes_clientes = clientes["nome"].tolist() if not clientes.empty else []
    with st.form("form_parcelas"):
        cliente = st.selectbox("Cliente", nomes_clientes) if nomes_clientes else st.text_input("Cliente")
        descricao = st.text_input("Descrição")
        valor = st.number_input("Valor da parcela", min_value=0.0, step=10.0)
        vencimento = st.date_input("Vencimento")
        status = st.selectbox("Status", ["Pendente", "Pago", "Atrasado"])
        salvar = st.form_submit_button("Salvar parcela")
    if salvar:
        executar_sql("INSERT INTO parcelas (empresa_id, cliente, descricao, valor, vencimento, status) VALUES (?, ?, ?, ?, ?, ?)", (empresa_atual(), cliente, descricao, valor, str(vencimento), status))
        st.success("Parcela salva com sucesso!")
        st.rerun()
    df = carregar_parcelas()
    if not df.empty:
        df["valor"] = pd.to_numeric(df["valor"], errors="coerce").fillna(0)
        col1, col2, col3 = st.columns(3)
        col1.metric("Pendente", formatar_moeda(df[df["status"] == "Pendente"]["valor"].sum()))
        col2.metric("Pago", formatar_moeda(df[df["status"] == "Pago"]["valor"].sum()))
        col3.metric("Atrasado", formatar_moeda(df[df["status"] == "Atrasado"]["valor"].sum()))
        mostrar_tabela(df)
    else:
        st.info("Nenhuma parcela cadastrada.")


def pagina_clientes():
    st.title("👥 CRM Financeiro / Clientes")
    with st.form("form_clientes"):
        nome = st.text_input("Nome")
        telefone = st.text_input("Telefone")
        cpf = st.text_input("CPF")
        endereco = st.text_input("Endereço")
        observacao = st.text_area("Observação")
        salvar = st.form_submit_button("Salvar cliente")
    if salvar:
        executar_sql("INSERT INTO clientes (empresa_id, nome, telefone, cpf, endereco, observacao) VALUES (?, ?, ?, ?, ?, ?)", (empresa_atual(), nome, telefone, cpf, endereco, observacao))
        st.success("Cliente salvo com sucesso!")
        st.rerun()
    df = carregar_clientes()
    if not df.empty:
        pesquisa = st.text_input("Pesquisar cliente")
        if pesquisa:
            df = df[df["nome"].str.contains(pesquisa, case=False, na=False) | df["telefone"].str.contains(pesquisa, case=False, na=False) | df["cpf"].str.contains(pesquisa, case=False, na=False)]
        mostrar_tabela(df)
    else:
        st.info("Nenhum cliente cadastrado.")


def pagina_estoque():
    st.title("📦 Controle de Estoque")
    with st.form("form_estoque"):
        produto = st.text_input("Produto")
        categoria = st.text_input("Categoria")
        quantidade = st.number_input("Quantidade", min_value=0, step=1)
        valor_custo = st.number_input("Valor de custo", min_value=0.0, step=10.0)
        valor_venda = st.number_input("Valor de venda", min_value=0.0, step=10.0)
        observacao = st.text_area("Observação")
        salvar = st.form_submit_button("Salvar produto")
    if salvar:
        executar_sql("INSERT INTO estoque (empresa_id, produto, categoria, quantidade, valor_custo, valor_venda, observacao) VALUES (?, ?, ?, ?, ?, ?, ?)", (empresa_atual(), produto, categoria, quantidade, valor_custo, valor_venda, observacao))
        st.success("Produto salvo com sucesso!")
        st.rerun()
    df = carregar_estoque()
    if not df.empty:
        df["quantidade"] = pd.to_numeric(df["quantidade"], errors="coerce").fillna(0)
        df["valor_custo"] = pd.to_numeric(df["valor_custo"], errors="coerce").fillna(0)
        df["valor_venda"] = pd.to_numeric(df["valor_venda"], errors="coerce").fillna(0)
        total_custo = (df["quantidade"] * df["valor_custo"]).sum()
        total_venda = (df["quantidade"] * df["valor_venda"]).sum()
        lucro = total_venda - total_custo
        col1, col2, col3 = st.columns(3)
        col1.metric("Total em custo", formatar_moeda(total_custo))
        col2.metric("Total em venda", formatar_moeda(total_venda))
        col3.metric("Lucro previsto", formatar_moeda(lucro))
        mostrar_tabela(df)
    else:
        st.info("Nenhum produto cadastrado.")

# =========================================================
# PIX / RELATÓRIOS / IA / WHATSAPP
# =========================================================
def pagina_pix():
    st.title("⚡ Integração Pix")
    empresa = dados_empresa()
    if empresa is None:
        st.warning("Cadastre uma empresa primeiro.")
        return
    with st.form("form_pix_config"):
        chave = st.text_input("Chave Pix", value=str(empresa["pix_chave"]) if pd.notna(empresa["pix_chave"]) else "")
        nome = st.text_input("Nome recebedor", value=str(empresa["pix_nome"]) if pd.notna(empresa["pix_nome"]) else "")
        cidade = st.text_input("Cidade", value=str(empresa["pix_cidade"]) if pd.notna(empresa["pix_cidade"]) else "GOIANIA")
        salvar_config = st.form_submit_button("Salvar configuração Pix")
    if salvar_config:
        executar_sql("UPDATE empresas SET pix_chave = ?, pix_nome = ?, pix_cidade = ? WHERE id = ?", (chave, nome, cidade, empresa_atual()))
        st.success("Configuração Pix salva!")
        st.rerun()
    valor = st.number_input("Valor do Pix", min_value=0.0, step=10.0)
    descricao = st.text_input("Descrição do pagamento", value="Pagamento")
    if st.button("Gerar Pix"):
        empresa = dados_empresa()
        if not empresa["pix_chave"]:
            st.error("Cadastre a chave Pix primeiro.")
        else:
            pix = gerar_pix_copia_cola(empresa["pix_chave"], empresa["pix_nome"], empresa["pix_cidade"], valor, descricao)
            st.success("Pix gerado com sucesso!")
            st.text_area("Pix copia e cola", pix, height=180)


def gerar_relatorio_texto(df, titulo):
    linhas = [titulo, "=" * 60, f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ""]
    for _, row in df.iterrows():
        linhas.append(f"{row.get('data', '')} | {row.get('tipo', '')} | {row.get('categoria', '')} | {row.get('descricao', '')} | {formatar_moeda(row.get('valor', 0))} | {row.get('status', '')}")
    return "\n".join(linhas)


def gerar_pdf_simples(df, titulo):
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
        buffer = io.BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=A4)
        largura, altura = A4
        y = altura - 50
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(40, y, titulo)
        y -= 25
        pdf.setFont("Helvetica", 9)
        pdf.drawString(40, y, f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        y -= 30
        for _, row in df.iterrows():
            texto = f"{row.get('data', '')} | {row.get('tipo', '')} | {row.get('categoria', '')} | {row.get('descricao', '')} | {formatar_moeda(row.get('valor', 0))}"
            pdf.drawString(40, y, texto[:110])
            y -= 18
            if y < 50:
                pdf.showPage()
                pdf.setFont("Helvetica", 9)
                y = altura - 50
        pdf.save()
        buffer.seek(0)
        return buffer.getvalue()
    except Exception:
        return None


def pagina_relatorios():
    st.title("📑 Relatórios PDF / CSV")
    df = carregar_lancamentos()
    if df.empty:
        st.info("Nenhum dado para gerar relatório.")
        return
    df["data"] = pd.to_datetime(df["data"], errors="coerce")
    df["valor"] = pd.to_numeric(df["valor"], errors="coerce").fillna(0)
    col1, col2 = st.columns(2)
    with col1:
        data_inicio = st.date_input("Data inicial", value=date.today().replace(day=1))
    with col2:
        data_fim = st.date_input("Data final", value=date.today())
    df_filtrado = df[(df["data"] >= pd.to_datetime(data_inicio)) & (df["data"] <= pd.to_datetime(data_fim))]
    if df_filtrado.empty:
        st.warning("Nenhum lançamento encontrado nesse período.")
        return
    entradas = df_filtrado[df_filtrado["tipo"] == "Entrada"]["valor"].sum()
    saidas = df_filtrado[df_filtrado["tipo"] == "Saída"]["valor"].sum()
    saldo = entradas - saidas
    col1, col2, col3 = st.columns(3)
    col1.metric("Entradas", formatar_moeda(entradas))
    col2.metric("Saídas", formatar_moeda(saidas))
    col3.metric("Saldo", formatar_moeda(saldo))
    mostrar_tabela(df_filtrado)
    csv = df_filtrado.to_csv(index=False).encode("utf-8")
    st.download_button("Baixar CSV", csv, "relatorio_financeiro.csv", "text/csv")
    pdf = gerar_pdf_simples(df_filtrado, "Relatório Financeiro")
    if pdf:
        st.download_button("Baixar PDF", pdf, "relatorio_financeiro.pdf", "application/pdf")
    else:
        txt = gerar_relatorio_texto(df_filtrado, "Relatório Financeiro")
        st.warning("Para gerar PDF real, instale o reportlab.")
        st.code(r'.\venv\Scripts\python.exe -m pip install reportlab')
        st.download_button("Baixar relatório em TXT", txt.encode("utf-8"), "relatorio_financeiro.txt", "text/plain")


def pagina_ia():
    st.title("🤖 IA para Análise Financeira")
    df = carregar_lancamentos()
    if df.empty:
        st.info("Cadastre lançamentos para gerar análise.")
        return
    df["valor"] = pd.to_numeric(df["valor"], errors="coerce").fillna(0)
    entradas = df[df["tipo"] == "Entrada"]["valor"].sum()
    saidas = df[df["tipo"] == "Saída"]["valor"].sum()
    saldo = entradas - saidas
    st.write(f"Total de entradas: **{formatar_moeda(entradas)}**")
    st.write(f"Total de saídas: **{formatar_moeda(saidas)}**")
    st.write(f"Saldo atual: **{formatar_moeda(saldo)}**")
    if saldo > 0:
        st.success("Sua empresa está com saldo positivo. Continue controlando as despesas e mantenha uma reserva.")
    elif saldo == 0:
        st.warning("Seu saldo está zerado. O ideal é criar margem de lucro e controlar melhor as saídas.")
    else:
        st.error("Seu saldo está negativo. É necessário reduzir despesas, cobrar pendências ou aumentar entradas.")
    categorias = df.groupby("categoria")["valor"].sum().sort_values(ascending=False).reset_index()
    if not categorias.empty:
        st.subheader("Categorias com maior movimentação")
        mostrar_tabela(categorias)


def pagina_whatsapp():
    st.title("📲 Integração WhatsApp Manual")
    st.info("Gere mensagens prontas e link para abrir no WhatsApp.")
    clientes = carregar_clientes()
    nomes_clientes = clientes["nome"].tolist() if not clientes.empty else []
    if nomes_clientes:
        cliente_nome = st.selectbox("Cliente", nomes_clientes)
        cliente_row = clientes[clientes["nome"] == cliente_nome].iloc[0]
        telefone = str(cliente_row["telefone"])
    else:
        cliente_nome = st.text_input("Nome do cliente")
        telefone = st.text_input("Telefone com DDD")
    valor = st.number_input("Valor", min_value=0.0, step=10.0)
    vencimento = st.date_input("Vencimento")
    tipo_msg = st.selectbox("Tipo de mensagem", ["Cobrança amigável", "Lembrete de vencimento", "Agradecimento", "Oferta"])
    if st.button("Gerar mensagem"):
        if tipo_msg == "Cobrança amigável":
            mensagem = f"Olá, {cliente_nome}! Tudo bem?\n\nPassando para lembrar sobre o valor de {formatar_moeda(valor)}, com vencimento em {vencimento.strftime('%d/%m/%Y')}.\n\nQualquer dúvida, estou à disposição."
        elif tipo_msg == "Lembrete de vencimento":
            mensagem = f"Olá, {cliente_nome}! Tudo certo?\n\nSua parcela no valor de {formatar_moeda(valor)} vence em {vencimento.strftime('%d/%m/%Y')}.\n\nObrigado pela atenção."
        elif tipo_msg == "Oferta":
            mensagem = f"Olá, {cliente_nome}! Temos uma condição especial disponível para você.\n\nMe chama aqui para eu te passar os detalhes."
        else:
            mensagem = f"Olá, {cliente_nome}!\n\nObrigado pela confiança. Conte sempre conosco."
        st.text_area("Mensagem pronta", mensagem, height=180)
        telefone_limpo = "".join(filter(str.isdigit, telefone))
        if telefone_limpo:
            link = f"https://wa.me/55{telefone_limpo}?text={urllib.parse.quote(mensagem)}"
            st.markdown(f"[Abrir no WhatsApp]({link})")


def pagina_whatsapp_automatico():
    st.title("🤖 WhatsApp Automático → Sistema")
    st.success("Esta aba mostra como ligar o WhatsApp ao sistema usando o arquivo whatsapp_api.py.")
    st.write("Mensagens aceitas pelo robô:")
    st.code("""
entrada venda prisma 45900 pix pago
saida compra peça 350 dinheiro pago
compra pneu 1200 pix pago
venda moto cg 9999 promissória pendente
recebi parcela João 800 pix pago
paguei aluguel 1500 pix pago
""")
    st.subheader("1. Instalar biblioteca da API")
    st.code(r".\venv\Scripts\python.exe -m pip install fastapi uvicorn")
    st.subheader("2. Rodar a API do WhatsApp em outro terminal")
    st.code(r".\venv\Scripts\python.exe -m uvicorn whatsapp_api:app --host 0.0.0.0 --port 8000")
    st.subheader("3. Teste local sem WhatsApp")
    st.code(r'''Invoke-RestMethod -Uri "http://localhost:8000/whatsapp" -Method POST -ContentType "application/json" -Body '{"texto":"entrada venda prisma 45900 pix pago"}' ''')
    st.info("Depois disso, basta ligar esse webhook no n8n, Z-API, Evolution API ou WhatsApp Cloud API.")

# =========================================================
# NOTIFICAÇÕES / BACKUP / MULTIEMPRESA / ADMIN / MYSQL / ANDROID
# =========================================================
def pagina_notificacoes():
    st.title("🔔 Notificações Automáticas")
    hoje = date.today()
    limite = hoje + timedelta(days=3)
    contas = carregar_contas()
    parcelas = carregar_parcelas()
    st.subheader("Contas vencidas ou próximas do vencimento")
    if not contas.empty:
        contas["vencimento_data"] = pd.to_datetime(contas["vencimento"], errors="coerce").dt.date
        alertas = contas[(contas["status"] != "Pago") & (contas["status"] != "Recebido") & (contas["vencimento_data"] <= limite)]
        mostrar_tabela(alertas.drop(columns=["vencimento_data"], errors="ignore")) if not alertas.empty else st.success("Nenhuma conta vencida ou próxima do vencimento.")
    else:
        st.info("Nenhuma conta cadastrada.")
    st.divider()
    st.subheader("Parcelas vencidas ou próximas do vencimento")
    if not parcelas.empty:
        parcelas["vencimento_data"] = pd.to_datetime(parcelas["vencimento"], errors="coerce").dt.date
        alertas = parcelas[(parcelas["status"] != "Pago") & (parcelas["vencimento_data"] <= limite)]
        mostrar_tabela(alertas.drop(columns=["vencimento_data"], errors="ignore")) if not alertas.empty else st.success("Nenhuma parcela vencida ou próxima do vencimento.")
    else:
        st.info("Nenhuma parcela cadastrada.")


def pagina_backup():
    st.title("☁️ Backup em Nuvem / Local")
    if os.path.exists(DB_NAME):
        with open(DB_NAME, "rb") as file:
            st.download_button("Baixar backup local", file, f"backup_financeiro_{datetime.now().strftime('%Y%m%d_%H%M')}.db", "application/octet-stream")
    else:
        st.warning("Banco de dados ainda não encontrado.")
    st.info("Backup em nuvem pode ser integrado futuramente com Google Drive, Dropbox, OneDrive ou MySQL online.")


def pagina_multiempresas():
    st.title("🏢 Multiempresas")
    with st.form("form_empresa"):
        nome = st.text_input("Nome da empresa")
        cnpj = st.text_input("CNPJ")
        telefone = st.text_input("Telefone")
        endereco = st.text_input("Endereço")
        pix_chave = st.text_input("Chave Pix")
        pix_nome = st.text_input("Nome para Pix")
        pix_cidade = st.text_input("Cidade Pix", value="GOIANIA")
        salvar = st.form_submit_button("Salvar empresa")
    if salvar:
        executar_sql("INSERT INTO empresas (nome, cnpj, telefone, endereco, pix_chave, pix_nome, pix_cidade) VALUES (?, ?, ?, ?, ?, ?, ?)", (nome, cnpj, telefone, endereco, pix_chave, pix_nome, pix_cidade))
        st.success("Empresa cadastrada com sucesso!")
        st.rerun()
    empresas = carregar_empresas()
    if not empresas.empty:
        mostrar_tabela(empresas)
        opcoes = {f"{row['id']} - {row['nome']}": row["id"] for _, row in empresas.iterrows()}
        escolha = st.selectbox("Selecionar empresa atual", list(opcoes.keys()))
        if st.button("Usar esta empresa"):
            st.session_state["empresa_id"] = opcoes[escolha]
            st.success("Empresa selecionada com sucesso!")
            st.rerun()


def pagina_admin():
    st.title("⚙️ Painel Administrativo")
    empresas = carregar_empresas()
    empresas_opcoes = {f"{row['id']} - {row['nome']}": row["id"] for _, row in empresas.iterrows()}
    with st.form("form_usuario"):
        nome = st.text_input("Nome")
        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")
        tipo = st.selectbox("Tipo", ["Administrador", "Usuário"])
        empresa_escolhida = st.selectbox("Empresa", list(empresas_opcoes.keys())) if empresas_opcoes else None
        salvar = st.form_submit_button("Criar usuário")
    if salvar:
        try:
            empresa_id = empresas_opcoes[empresa_escolhida] if empresa_escolhida else 1
            executar_sql("INSERT INTO usuarios (usuario, senha, nome, tipo, empresa_id) VALUES (?, ?, ?, ?, ?)", (usuario, senha, nome, tipo, empresa_id))
            st.success("Usuário criado com sucesso!")
            st.rerun()
        except Exception:
            st.error("Esse usuário já existe ou ocorreu algum erro.")
    usuarios = carregar_df("""
        SELECT usuarios.id, usuarios.usuario, usuarios.nome, usuarios.tipo, empresas.nome AS empresa
        FROM usuarios
        LEFT JOIN empresas ON empresas.id = usuarios.empresa_id
        ORDER BY usuarios.id DESC
    """)
    mostrar_tabela(usuarios)


def pagina_mysql():
    st.title("🗄️ Banco de Dados SQLite / MySQL")
    st.success("Este sistema está rodando com SQLite local.")
    st.write(f"Arquivo do banco atual: `{DB_NAME}`")
    st.info("Para versão online com MySQL, instale mysql-connector-python e troque a função conectar().")
    st.code(r".\venv\Scripts\python.exe -m pip install mysql-connector-python")


def pagina_android():
    st.title("📱 App Android APK")
    st.info("Este sistema pode virar app Android usando WebView ou PWA.")
    st.write("1. Hospedar o sistema. 2. Criar app WebView. 3. Gerar APK pelo Android Studio.")
    st.code(r".\venv\Scripts\python.exe -m streamlit run main.py")

# =========================================================
# APP PRINCIPAL
# =========================================================
def app():
    empresa = dados_empresa()
    nome_empresa = empresa["nome"] if empresa is not None else "Empresa"
    st.sidebar.title("💰 Sistema Financeiro")
    st.sidebar.write(f"Empresa: {nome_empresa}")
    st.sidebar.write(f"Usuário: {st.session_state.get('nome', '')}")
    st.sidebar.write(f"Tipo: {st.session_state.get('tipo', '')}")

    menu = st.sidebar.radio("Menu", [
        "Dashboard Nubank",
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
        "WhatsApp Automático",
        "Notificações",
        "Backup",
        "Multiempresas",
        "Painel Administrativo",
        "SQLite / MySQL",
        "App Android APK"
    ])

    if st.sidebar.button("Sair"):
        st.session_state["logado"] = False
        st.session_state["usuario"] = ""
        st.session_state["nome"] = ""
        st.session_state["tipo"] = ""
        st.session_state["empresa_id"] = 1
        st.rerun()

    if menu == "Dashboard Nubank": pagina_dashboard()
    elif menu == "Entradas e Saídas": pagina_lancamentos()
    elif menu == "Parcelas": pagina_parcelas()
    elif menu == "Contas a Pagar/Receber": pagina_contas()
    elif menu == "Contas a Receber": pagina_contas_receber()
    elif menu == "Pix": pagina_pix()
    elif menu == "Relatórios PDF": pagina_relatorios()
    elif menu == "IA Financeira": pagina_ia()
    elif menu == "CRM / Clientes": pagina_clientes()
    elif menu == "Estoque": pagina_estoque()
    elif menu == "WhatsApp Manual": pagina_whatsapp()
    elif menu == "WhatsApp Automático": pagina_whatsapp_automatico()
    elif menu == "Notificações": pagina_notificacoes()
    elif menu == "Backup": pagina_backup()
    elif menu == "Multiempresas": pagina_multiempresas()
    elif menu == "Painel Administrativo": pagina_admin()
    elif menu == "SQLite / MySQL": pagina_mysql()
    elif menu == "App Android APK": pagina_android()

# =========================================================
# INICIALIZAÇÃO
# =========================================================
if "logado" not in st.session_state: st.session_state["logado"] = False
if "usuario" not in st.session_state: st.session_state["usuario"] = ""
if "nome" not in st.session_state: st.session_state["nome"] = ""
if "tipo" not in st.session_state: st.session_state["tipo"] = ""
if "empresa_id" not in st.session_state: st.session_state["empresa_id"] = 1

if st.session_state["logado"]:
    app()
else:
    tela_login()
