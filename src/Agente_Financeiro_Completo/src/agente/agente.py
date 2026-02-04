"""
Agente Financeiro - Módulo de análise e sugestões
Lê dados de arquivos CSV e JSON
"""

import pandas as pd
import json
from datetime import datetime


def carregar_transacoes(caminho='data/transacoes.csv'):
    """
    Carrega as transações do arquivo CSV.
    
    Args:
        caminho: Caminho do arquivo CSV
    
    Returns:
        DataFrame com as transações
    """
    df = pd.read_csv(caminho)
    df['data'] = pd.to_datetime(df['data'])
    return df


def carregar_perfil_investidor(caminho='data/perfil_investidor.json'):
    """
    Carrega o perfil do investidor do arquivo JSON.
    
    Args:
        caminho: Caminho do arquivo JSON
    
    Returns:
        Dicionário com dados do perfil
    """
    with open(caminho, 'r', encoding='utf-8') as f:
        return json.load(f)


def carregar_produtos_financeiros(caminho='data/produtos_financeiros.json'):
    """
    Carrega os produtos financeiros disponíveis do arquivo JSON.
    
    Args:
        caminho: Caminho do arquivo JSON
    
    Returns:
        Lista de dicionários com produtos
    """
    with open(caminho, 'r', encoding='utf-8') as f:
        return json.load(f)


def carregar_historico_atendimento(caminho='data/historico_atendimento.csv'):
    """
    Carrega o histórico de atendimentos do arquivo CSV.
    
    Args:
        caminho: Caminho do arquivo CSV
    
    Returns:
        DataFrame com o histórico
    """
    df = pd.read_csv(caminho)
    df['data'] = pd.to_datetime(df['data'])
    return df


def analisar_gastos(df_transacoes):
    """
    Analisa as transações e retorna estatísticas financeiras.
    
    Args:
        df_transacoes: DataFrame com as transações
    
    Returns:
        dict: Contém receita_total, despesas_totais, saldo, gastos_por_categoria e categoria_maior_gasto
    """
    # Calcular receita total
    receita_total = df_transacoes[df_transacoes['tipo'] == 'entrada']['valor'].sum()
    
    # Calcular despesas totais
    despesas_totais = df_transacoes[df_transacoes['tipo'] == 'saida']['valor'].sum()
    
    # Calcular saldo
    saldo = receita_total - despesas_totais
    
    # Gastos por categoria
    gastos_por_categoria = df_transacoes[df_transacoes['tipo'] == 'saida'].groupby('categoria')['valor'].sum().to_dict()
    
    # Categoria com maior gasto
    if gastos_por_categoria:
        categoria_maior_gasto = max(gastos_por_categoria, key=gastos_por_categoria.get)
        valor_maior_gasto = gastos_por_categoria[categoria_maior_gasto]
    else:
        categoria_maior_gasto = None
        valor_maior_gasto = 0
    
    return {
        'receita_total': receita_total,
        'despesas_totais': despesas_totais,
        'saldo': saldo,
        'gastos_por_categoria': gastos_por_categoria,
        'categoria_maior_gasto': categoria_maior_gasto,
        'valor_maior_gasto': valor_maior_gasto
    }


def texto_resumo_gastos(analise):
    """
    Gera um texto resumido da análise de gastos.
    
    Args:
        analise: Dicionário retornado por analisar_gastos()
    
    Returns:
        str: Texto formatado com o resumo
    """
    texto = f"""📊 **Resumo Financeiro**

💰 **Receita Total:** R$ {analise['receita_total']:.2f}
💸 **Despesas Totais:** R$ {analise['despesas_totais']:.2f}
💵 **Saldo:** R$ {analise['saldo']:.2f}

🎯 **Categoria com Maior Gasto:** {analise['categoria_maior_gasto'].title() if analise['categoria_maior_gasto'] else 'N/A'}
📈 **Valor:** R$ {analise['valor_maior_gasto']:.2f}
"""
    return texto


def detalhar_gastos(analise):
    """
    Gera um detalhamento completo dos gastos por categoria.
    
    Args:
        analise: Dicionário retornado por analisar_gastos()
    
    Returns:
        str: Texto formatado com detalhamento
    """
    texto = "📋 **Detalhamento por Categoria**\n\n"
    
    gastos_ordenados = sorted(
        analise['gastos_por_categoria'].items(), 
        key=lambda x: x[1], 
        reverse=True
    )
    
    for categoria, valor in gastos_ordenados:
        percentual = (valor / analise['despesas_totais']) * 100 if analise['despesas_totais'] > 0 else 0
        texto += f"• **{categoria.title()}:** R$ {valor:.2f} ({percentual:.1f}%)\n"
    
    return texto


def sugestao_reducao_gastos(categoria):
    """
    Retorna sugestão personalizada de redução de gastos por categoria.
    
    Args:
        categoria: Nome da categoria com maior gasto
    
    Returns:
        str: Sugestão específica para a categoria
    """
    # Normalizar categoria para lowercase
    categoria = categoria.lower() if categoria else ""
    
    sugestoes = {
        'alimentacao': "🍽️ **Sugestão para Alimentação:**\nPlaneje suas compras semanalmente e use aplicativos de desconto como Rappi, iFood ou programas de cashback. Prefira mercados com promoções e compre em atacado itens não perecíveis. Você pode cortar até 15% dos gastos com alimentação!",
        
        'lazer': "🎮 **Sugestão para Lazer:**\nRevise suas assinaturas de streaming (Netflix, Spotify, etc.) e mantenha apenas as essenciais. Limite saídas semanais e busque atividades gratuitas como parques e eventos culturais. Potencial de economia: até R$ 150/mês!",
        
        'moradia': "🏠 **Sugestão para Moradia:**\nRenegocie o valor do aluguel com o proprietário ou considere mudança para área mais acessível. Revise contas fixas (internet, energia, água) e busque planos mais econômicos. Você pode liberar até R$ 200/mês com essas ações!",
        
        'transporte': "🚗 **Sugestão para Transporte:**\nUse aplicativos de carona compartilhada como Uber/99 em pool, ou opte pelo transporte público quando possível. Avalie a viabilidade de home office alguns dias da semana. Economia significativa nos deslocamentos diários!",
        
        'saude': "💊 **Sugestão para Saúde:**\nAvalie planos de saúde familiares que podem ser mais econômicos. Opte por medicamentos genéricos nas farmácias e use programas de descontos como Farmácia Popular. Compare preços antes de realizar exames e consultas particulares."
    }
    
    if categoria in sugestoes:
        return sugestoes[categoria]
    else:
        return f"💡 **Sugestão Geral:**\nRevise seus gastos em {categoria.title()} e identifique oportunidades de redução. Compare preços, busque alternativas mais econômicas e estabeleça um orçamento mensal para esta categoria."


def sugerir_investimentos(perfil_investidor, produtos_financeiros, saldo_disponivel):
    """
    Sugere investimentos de acordo com o perfil do cliente e produtos disponíveis.
    
    Args:
        perfil_investidor: Dicionário com dados do perfil
        produtos_financeiros: Lista de produtos disponíveis
        saldo_disponivel: Valor disponível para investimento
    
    Returns:
        str: Sugestão personalizada de investimentos
    """
    perfil = perfil_investidor['perfil_investidor'].lower()
    nome = perfil_investidor['nome']
    objetivo = perfil_investidor['objetivo_principal']
    
    # Filtrar produtos por perfil de risco
    if perfil == 'conservador':
        produtos_recomendados = [p for p in produtos_financeiros if p['risco'] == 'baixo']
        emoji = "🛡️"
        titulo = "Conservador"
    elif perfil == 'moderado':
        produtos_recomendados = [p for p in produtos_financeiros if p['risco'] in ['baixo', 'medio']]
        emoji = "⚖️"
        titulo = "Moderado"
    elif perfil == 'arrojado':
        produtos_recomendados = produtos_financeiros
        emoji = "🚀"
        titulo = "Arrojado"
    else:
        produtos_recomendados = produtos_financeiros
        emoji = "💼"
        titulo = perfil.title()
    
    # Montar texto com produtos
    texto_produtos = ""
    for produto in produtos_recomendados:
        texto_produtos += f"• **{produto['nome']}** - {produto['rentabilidade']}\n"
        texto_produtos += f"  └─ Risco: {produto['risco'].title()} | Aporte mínimo: R$ {produto['aporte_minimo']:.2f}\n"
        texto_produtos += f"  └─ {produto['indicado_para']}\n\n"
    
    # Recomendação personalizada baseada no objetivo
    if 'emergência' in objetivo.lower():
        recomendacao = f"""**Recomendação Personalizada:**

Com R$ {saldo_disponivel:.2f} disponíveis e objetivo de {objetivo.lower()}, sugiro:

• **100% em Tesouro Selic ou CDB Liquidez Diária**
  └─ Priorize liquidez total para emergências
  └─ Mantenha o dinheiro acessível a qualquer momento

**Meta:** Completar 6 meses de despesas em reserva de emergência antes de investir em outros produtos."""
    else:
        recomendacao = f"""**Recomendação Personalizada:**

Com R$ {saldo_disponivel:.2f} disponíveis, sugiro diversificar:

• 60% em produtos de **baixo risco** (segurança)
• 30% em produtos de **risco moderado** (rentabilidade)
• 10% para **novos aportes** ou oportunidades

Seu objetivo "{objetivo}" será alcançado com disciplina e aportes mensais consistentes."""
    
    texto_final = f"""{emoji} **Recomendação para Perfil {titulo}**

**Olá, {nome}!**

**Produtos Financeiros Disponíveis:**

{texto_produtos}

{recomendacao}
"""
    
    return texto_final


def obter_historico_resumido(df_historico, limite=5):
    """
    Retorna um resumo do histórico de atendimentos.
    
    Args:
        df_historico: DataFrame com histórico
        limite: Número máximo de registros a retornar
    
    Returns:
        str: Texto formatado com histórico
    """
    texto = "📜 **Histórico de Atendimentos Recentes**\n\n"
    
    # Ordenar por data decrescente e pegar os últimos registros
    df_recente = df_historico.sort_values('data', ascending=False).head(limite)
    
    for _, row in df_recente.iterrows():
        data_formatada = row['data'].strftime('%d/%m/%Y')
        status = "✅" if row['resolvido'].lower() == 'sim' else "⏳"
        texto += f"{status} **{data_formatada}** - {row['tema']}\n"
        texto += f"   └─ {row['resumo']}\n\n"
    
    return texto


def analisar_metas(perfil_investidor, saldo_disponivel):
    """
    Analisa o progresso das metas financeiras.
    
    Args:
        perfil_investidor: Dicionário com dados do perfil
        saldo_disponivel: Saldo disponível atual
    
    Returns:
        str: Texto formatado com análise das metas
    """
    metas = perfil_investidor.get('metas', [])
    
    if not metas:
        return "Você ainda não tem metas cadastradas. Que tal definir alguns objetivos financeiros?"
    
    texto = "🎯 **Análise de Metas Financeiras**\n\n"
    
    for i, meta in enumerate(metas, 1):
        nome_meta = meta['meta']
        valor_necessario = meta['valor_necessario']
        prazo = meta['prazo']
        
        # Calcular progresso (baseado no saldo disponível)
        progresso_percentual = min((saldo_disponivel / valor_necessario) * 100, 100)
        
        # Calcular meses até o prazo
        prazo_date = datetime.strptime(prazo, '%Y-%m')
        hoje = datetime.now()
        meses_restantes = (prazo_date.year - hoje.year) * 12 + (prazo_date.month - hoje.month)
        
        texto += f"**Meta {i}: {nome_meta}**\n"
        texto += f"• Valor necessário: R$ {valor_necessario:.2f}\n"
        texto += f"• Prazo: {prazo_date.strftime('%m/%Y')}\n"
        texto += f"• Progresso: {progresso_percentual:.1f}%\n"
        texto += f"• Meses restantes: {meses_restantes} meses\n"
        
        if meses_restantes > 0:
            aporte_mensal = (valor_necessario - saldo_disponivel) / meses_restantes
            texto += f"• Aporte mensal necessário: R$ {aporte_mensal:.2f}\n"
        
        texto += "\n"
    
    return texto
