def gerar_pdf_relatorio(df, ind):
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
        from reportlab.lib.units import cm
        from reportlab.lib import colors
    except Exception:
        return None

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    largura, altura = A4

    empresa_nome = st.session_state.usuario["empresa_nome"]
    data_emissao = datetime.now().strftime("%d/%m/%Y às %H:%M")

    cor_navy = colors.HexColor("#002B3D")
    cor_navy_escuro = colors.HexColor("#001D2B")
    cor_verde = colors.HexColor("#DFFF6B")
    cor_cinza = colors.HexColor("#6C7B86")
    cor_claro = colors.HexColor("#F4F8FB")
    cor_branco = colors.white
    cor_vermelho = colors.HexColor("#D93025")
    cor_verde_ok = colors.HexColor("#0F9D58")

    def desenhar_capa():
        pdf.setFillColor(cor_navy_escuro)
        pdf.rect(0, 0, largura, altura, fill=1, stroke=0)

        pdf.setFillColor(cor_navy)
        pdf.roundRect(1.2 * cm, 1.2 * cm, largura - 2.4 * cm, altura - 2.4 * cm, 24, fill=1, stroke=0)

        pdf.setFillColor(cor_verde)
        pdf.circle(largura - 3.1 * cm, altura - 3.1 * cm, 1.2 * cm, fill=1, stroke=0)

        if Path("logo.png").exists():
            try:
                pdf.drawImage(
                    "logo.png",
                    2 * cm,
                    altura - 4.6 * cm,
                    width=3.2 * cm,
                    height=3.2 * cm,
                    preserveAspectRatio=True,
                    mask="auto"
                )
            except Exception:
                pdf.setFillColor(cor_verde)
                pdf.setFont("Helvetica-Bold", 22)
                pdf.drawString(2 * cm, altura - 3.1 * cm, "GS")
        else:
            pdf.setFillColor(cor_verde)
            pdf.setFont("Helvetica-Bold", 22)
            pdf.drawString(2 * cm, altura - 3.1 * cm, "GS")

        pdf.setFillColor(cor_branco)
        pdf.setFont("Helvetica-Bold", 24)
        pdf.drawString(2 * cm, altura - 6.4 * cm, "GLOBAL SOFTWARE")

        pdf.setFillColor(cor_verde)
        pdf.setFont("Helvetica-Bold", 28)
        pdf.drawString(2 * cm, altura - 9.2 * cm, "RELATÓRIO FINANCEIRO")
        pdf.drawString(2 * cm, altura - 10.4 * cm, "EXECUTIVO")

        pdf.setFillColor(colors.HexColor("#D7E2E8"))
        pdf.setFont("Helvetica", 12)
        pdf.drawString(2 * cm, altura - 12.1 * cm, f"Empresa: {empresa_nome}")
        pdf.drawString(2 * cm, altura - 12.9 * cm, f"Gerado em: {data_emissao}")

        pdf.setFillColor(cor_verde)
        pdf.roundRect(2 * cm, altura - 15.2 * cm, 7.8 * cm, 1.1 * cm, 14, fill=1, stroke=0)

        pdf.setFillColor(cor_navy_escuro)
        pdf.setFont("Helvetica-Bold", 11)
        pdf.drawCentredString(5.9 * cm, altura - 14.85 * cm, "GESTÃO • CONTROLE • RESULTADOS")

        pdf.setFillColor(colors.HexColor("#D7E2E8"))
        pdf.setFont("Helvetica", 10)
        pdf.drawString(2 * cm, 2.5 * cm, "Documento gerado automaticamente pelo Sistema Financeiro Premium.")
        pdf.drawString(2 * cm, 2.0 * cm, "Global Software — inteligência para gestão empresarial.")

        pdf.showPage()

    def cabecalho_pagina(titulo):
        pdf.setFillColor(cor_navy)
        pdf.rect(0, altura - 2.4 * cm, largura, 2.4 * cm, fill=1, stroke=0)

        pdf.setFillColor(cor_verde)
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(1.5 * cm, altura - 1.35 * cm, "GLOBAL SOFTWARE")

        pdf.setFillColor(cor_branco)
        pdf.setFont("Helvetica-Bold", 15)
        pdf.drawRightString(largura - 1.5 * cm, altura - 1.35 * cm, titulo)

        pdf.setFillColor(cor_cinza)
        pdf.setFont("Helvetica", 8)
        pdf.drawString(1.5 * cm, altura - 2.0 * cm, f"Empresa: {empresa_nome}")
        pdf.drawRightString(largura - 1.5 * cm, altura - 2.0 * cm, f"Emitido em {data_emissao}")

    def rodape():
        pdf.setFillColor(cor_cinza)
        pdf.setFont("Helvetica", 8)
        pdf.drawString(1.5 * cm, 1.0 * cm, "Global Software | Sistema Financeiro Premium")
        pdf.drawRightString(largura - 1.5 * cm, 1.0 * cm, "Relatório gerencial")

    def bloco_resumo(x, y, w, h, titulo, valor, subtitulo, positivo=True):
        pdf.setFillColor(cor_claro)
        pdf.roundRect(x, y, w, h, 12, fill=1, stroke=0)

        pdf.setFillColor(cor_navy)
        pdf.setFont("Helvetica-Bold", 9)
        pdf.drawString(x + 0.35 * cm, y + h - 0.55 * cm, titulo)

        if positivo:
            pdf.setFillColor(cor_verde_ok)
        else:
            pdf.setFillColor(cor_vermelho)

        pdf.setFont("Helvetica-Bold", 15)
        pdf.drawString(x + 0.35 * cm, y + h - 1.25 * cm, valor)

        pdf.setFillColor(cor_cinza)
        pdf.setFont("Helvetica", 7.5)
        pdf.drawString(x + 0.35 * cm, y + 0.35 * cm, subtitulo)

    desenhar_capa()
    cabecalho_pagina("Resumo Executivo")

    y = altura - 3.7 * cm

    pdf.setFillColor(cor_navy)
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(1.5 * cm, y, "Resumo financeiro")
    y -= 0.45 * cm

    pdf.setFillColor(cor_cinza)
    pdf.setFont("Helvetica", 9)
    pdf.drawString(1.5 * cm, y, "Visão geral dos principais indicadores da empresa.")
    y -= 1.1 * cm

    bloco_w = 5.55 * cm
    bloco_h = 2.25 * cm
    espaco = 0.45 * cm

    x1 = 1.5 * cm
    x2 = x1 + bloco_w + espaco
    x3 = x2 + bloco_w + espaco

    bloco_resumo(x1, y, bloco_w, bloco_h, "Receita total", moeda(ind["receita"]), "Entradas registradas", True)
    bloco_resumo(x2, y, bloco_w, bloco_h, "Saídas totais", moeda(ind["saidas"]), "Custos, despesas e dívidas", False)
    bloco_resumo(x3, y, bloco_w, bloco_h, "Lucro / Resultado", moeda(ind["lucro"]), "Receita menos saídas", ind["lucro"] >= 0)

    y -= bloco_h + 0.55 * cm

    bloco_resumo(x1, y, bloco_w, bloco_h, "Caixa estimado", moeda(ind["caixa"]), "Resultado acumulado", ind["caixa"] >= 0)
    bloco_resumo(x2, y, bloco_w, bloco_h, "A receber", moeda(ind["receber"]), "Receitas pendentes", True)
    bloco_resumo(x3, y, bloco_w, bloco_h, "Vencidas", moeda(ind["vencidas"]), "Contas em atraso", False)

    y -= bloco_h + 1.0 * cm

    pdf.setFillColor(cor_navy)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(1.5 * cm, y, "Análise rápida")
    y -= 0.65 * cm

    pdf.setFillColor(cor_cinza)
    pdf.setFont("Helvetica", 10)

    if ind["lucro"] < 0:
        analise = "A empresa apresenta resultado negativo. Recomenda-se revisar despesas, custos, folha e inadimplência."
    elif ind["vencidas"] > 0:
        analise = "A empresa apresenta lucro, porém possui valores vencidos. Recomenda-se priorizar cobrança e renegociação."
    else:
        analise = "A empresa apresenta controle saudável. Recomenda-se manter acompanhamento de caixa, estoque e contas a receber."

    linhas_analise = [
        analise,
        f"Contas pagas ou recebidas no mês: {moeda(ind['pagas_mes'])}.",
        f"Valores a pagar em aberto: {moeda(ind['pagar'])}.",
    ]

    for linha in linhas_analise:
        pdf.drawString(1.5 * cm, y, f"• {linha}")
        y -= 0.55 * cm

    rodape()
    pdf.showPage()

    cabecalho_pagina("Últimos Lançamentos")

    y = altura - 3.6 * cm

    pdf.setFillColor(cor_navy)
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(1.5 * cm, y, "Últimos lançamentos financeiros")
    y -= 0.9 * cm

    if df.empty:
        pdf.setFillColor(cor_cinza)
        pdf.setFont("Helvetica", 10)
        pdf.drawString(1.5 * cm, y, "Nenhum lançamento cadastrado.")
    else:
        tabela = df.sort_values("data", ascending=False).head(28).copy()

        colunas = [
            ("Data", 1.5 * cm, 2.0 * cm),
            ("Tipo", 3.7 * cm, 3.0 * cm),
            ("Descrição", 6.7 * cm, 6.4 * cm),
            ("Valor", 13.1 * cm, 2.7 * cm),
            ("Status", 15.9 * cm, 3.0 * cm),
        ]

        pdf.setFillColor(cor_navy)
        pdf.roundRect(1.3 * cm, y - 0.18 * cm, largura - 2.6 * cm, 0.7 * cm, 8, fill=1, stroke=0)

        pdf.setFillColor(cor_verde)
        pdf.setFont("Helvetica-Bold", 8)

        for nome_col, x, w in colunas:
            pdf.drawString(x, y, nome_col)

        y -= 0.65 * cm

        pdf.setFont("Helvetica", 7.5)

        for i, (_, row) in enumerate(tabela.iterrows()):
            if y < 2 * cm:
                rodape()
                pdf.showPage()
                cabecalho_pagina("Últimos Lançamentos")
                y = altura - 3.5 * cm

            if i % 2 == 0:
                pdf.setFillColor(colors.HexColor("#F7FBFD"))
                pdf.roundRect(1.3 * cm, y - 0.18 * cm, largura - 2.6 * cm, 0.55 * cm, 5, fill=1, stroke=0)

            pdf.setFillColor(colors.HexColor("#052C3D"))

            data_txt = data_br(row["data"])
            tipo_txt = str(row["tipo"])[:18]
            desc_txt = str(row["descricao"])[:42]
            valor_txt = moeda(row["valor"])
            status_txt = str(row.get("status_real", row["status"]))[:16]

            pdf.drawString(1.5 * cm, y, data_txt)
            pdf.drawString(3.7 * cm, y, tipo_txt)
            pdf.drawString(6.7 * cm, y, desc_txt)
            pdf.drawRightString(15.2 * cm, y, valor_txt)

            if status_txt in ["Pago", "Recebido"]:
                pdf.setFillColor(cor_verde_ok)
            elif status_txt in ["Vencido", "Vence hoje"]:
                pdf.setFillColor(cor_vermelho)
            else:
                pdf.setFillColor(colors.HexColor("#F59E0B"))

            pdf.setFont("Helvetica-Bold", 7.5)
            pdf.drawString(15.9 * cm, y, status_txt)
            pdf.setFont("Helvetica", 7.5)

            y -= 0.55 * cm

    rodape()
    pdf.showPage()

    cabecalho_pagina("Conclusão")

    y = altura - 3.8 * cm

    pdf.setFillColor(cor_navy)
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(1.5 * cm, y, "Conclusão gerencial")
    y -= 1.0 * cm

    pdf.setFillColor(cor_cinza)
    pdf.setFont("Helvetica", 10)

    conclusoes = [
        "Este relatório apresenta uma visão executiva da saúde financeira da empresa.",
        "Use os indicadores para acompanhar receita, saídas, lucro, inadimplência e valores pendentes.",
        "Acompanhe este relatório semanalmente para melhorar decisões e reduzir riscos financeiros.",
        "A Global Software ajuda sua empresa a sair do improviso e trabalhar com dados organizados.",
    ]

    for item in conclusoes:
        pdf.drawString(1.8 * cm, y, f"• {item}")
        y -= 0.65 * cm

    y -= 0.6 * cm

    pdf.setFillColor(cor_navy)
    pdf.roundRect(1.5 * cm, y - 2.0 * cm, largura - 3 * cm, 2.0 * cm, 14, fill=1, stroke=0)

    pdf.setFillColor(cor_verde)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawCentredString(largura / 2, y - 0.75 * cm, "GLOBAL SOFTWARE")

    pdf.setFillColor(cor_branco)
    pdf.setFont("Helvetica", 9)
    pdf.drawCentredString(largura / 2, y - 1.25 * cm, "Sistema Financeiro Premium para empresas que querem crescer com controle.")

    rodape()
    pdf.save()
    buffer.seek(0)
    return buffer