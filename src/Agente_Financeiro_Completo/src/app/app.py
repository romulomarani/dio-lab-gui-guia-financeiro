"""
Agente Financeiro - Interface Streamlit
Lê dados de arquivos CSV e JSON
"""

import streamlit as st
import plotly.graph_objects as go
from src.agente.agente import (
    carregar_transacoes,
    carregar_perfil_investidor,
    carregar_produtos_financeiros,
    carregar_historico_atendimento,
    analisar_gastos,
    texto_resumo_gastos,
    detalhar_gastos,
    sugestao_reducao_gastos,
    sugerir_investimentos,
    obter_historico_resumido,
    analisar_metas
)

# Configuração da página
st.set_page_config(
    page_title="Gui - Seu Guia Financeiro",
    page_icon="💰",
    layout="wide"
)

# Carregar dados
@st.cache_data
def carregar_dados():
    """Carrega todos os dados necessários"""
    try:
        df_transacoes = carregar_transacoes('data/transacoes.csv')
        perfil = carregar_perfil_investidor('data/perfil_investidor.json')
        produtos = carregar_produtos_financeiros('data/produtos_financeiros.json')
        df_historico = carregar_historico_atendimento('data/historico_atendimento.csv')
        return df_transacoes, perfil, produtos, df_historico, None
    except Exception as e:
        return None, None, None, None, str(e)

# Tentar carregar dados
df_transacoes, perfil_investidor, produtos_financeiros, df_historico, erro = carregar_dados()

# Se houver erro, mostrar mensagem
if erro:
    st.error(f"""
    ⚠️ **Erro ao carregar dados!**
    
    {erro}
    
    **Verifique se:**
    1. A pasta `data/` existe
    2. Os arquivos estão na pasta correta:
       - data/transacoes.csv
       - data/perfil_investidor.json
       - data/produtos_financeiros.json
       - data/historico_atendimento.csv
    """)
    st.stop()

# Inicializar session state
if 'mensagens' not in st.session_state:
    st.session_state.mensagens = []
if 'aguardando_detalhar' not in st.session_state:
    st.session_state.aguardando_detalhar = False
if 'aguardando_grafico' not in st.session_state:
    st.session_state.aguardando_grafico = False
if 'analise_atual' not in st.session_state:
    st.session_state.analise_atual = None

# Título
st.title("💰 Gui - Seu Guia Financeiro")
st.markdown("---")

# Sidebar com informações do perfil
with st.sidebar:
    st.header("👤 Perfil do Cliente")
    st.markdown(f"**Nome:** {perfil_investidor['nome']}")
    st.markdown(f"**Idade:** {perfil_investidor['idade']} anos")
    st.markdown(f"**Profissão:** {perfil_investidor['profissao']}")
    st.markdown(f"**Renda Mensal:** R$ {perfil_investidor['renda_mensal']:.2f}")
    st.markdown(f"**Perfil:** {perfil_investidor['perfil_investidor'].title()}")
    
    st.markdown("---")
    
    st.markdown("**💼 Patrimônio**")
    st.markdown(f"Total: R$ {perfil_investidor['patrimonio_total']:.2f}")
    st.markdown(f"Reserva de Emergência: R$ {perfil_investidor['reserva_emergencia_atual']:.2f}")
    
    st.markdown("---")
    
    if st.button("🗑️ Limpar Conversa"):
        st.session_state.mensagens = []
        st.session_state.aguardando_detalhar = False
        st.session_state.aguardando_grafico = False
        st.session_state.analise_atual = None
        st.rerun()

# Área de chat
chat_container = st.container()

with chat_container:
    # Exibir histórico de mensagens
    for msg in st.session_state.mensagens:
        with st.chat_message(msg['role']):
            st.markdown(msg['content'])
            if 'grafico' in msg and msg['grafico']:
                st.plotly_chart(msg['grafico'], use_container_width=True)

# Input do usuário
user_input = st.chat_input("Digite sua pergunta...")

def criar_grafico_barras(analise):
    """Cria gráfico de barras dos gastos por categoria"""
    categorias = [cat.title() for cat in analise['gastos_por_categoria'].keys()]
    valores = list(analise['gastos_por_categoria'].values())
    
    fig = go.Figure(data=[
        go.Bar(
            x=categorias,
            y=valores,
            marker_color='indianred',
            text=[f'R$ {v:.2f}' for v in valores],
            textposition='auto'
        )
    ])
    
    fig.update_layout(
        title="Gastos por Categoria",
        xaxis_title="Categoria",
        yaxis_title="Valor (R$)",
        height=400
    )
    
    return fig

def criar_grafico_pizza(analise):
    """Cria gráfico de pizza dos gastos por categoria"""
    categorias = [cat.title() for cat in analise['gastos_por_categoria'].keys()]
    valores = list(analise['gastos_por_categoria'].values())
    
    fig = go.Figure(data=[
        go.Pie(
            labels=categorias,
            values=valores,
            hole=0.3,
            textinfo='label+percent',
            textposition='auto'
        )
    ])
    
    fig.update_layout(
        title="Distribuição de Gastos",
        height=400
    )
    
    return fig

def processar_mensagem(mensagem):
    """Processa a mensagem do usuário e gera resposta"""
    mensagem_lower = mensagem.lower()
    
    # Verificar se está aguardando resposta sobre detalhamento
    if st.session_state.aguardando_detalhar:
        st.session_state.aguardando_detalhar = False
        if 'sim' in mensagem_lower or 'quero' in mensagem_lower or 'mostrar' in mensagem_lower:
            detalhamento = detalhar_gastos(st.session_state.analise_atual)
            st.session_state.aguardando_grafico = True
            return detalhamento + "\n\n❓ Gostaria de ver um gráfico visual dos seus gastos?"
        else:
            return "Ok! Se precisar de algo mais, é só perguntar! 😊"
    
    # Verificar se está aguardando resposta sobre gráfico
    if st.session_state.aguardando_grafico:
        st.session_state.aguardando_grafico = False
        if 'sim' in mensagem_lower or 'quero' in mensagem_lower or 'mostrar' in mensagem_lower:
            # Retornar indicação de que deve mostrar gráfico
            sugestao = sugestao_reducao_gastos(st.session_state.analise_atual['categoria_maior_gasto'])
            return {
                'texto': "📊 Aqui estão os gráficos dos seus gastos:\n\n" + sugestao,
                'mostrar_graficos': True
            }
        else:
            sugestao = sugestao_reducao_gastos(st.session_state.analise_atual['categoria_maior_gasto'])
            return sugestao
    
    # Análise de gastos
    if any(palavra in mensagem_lower for palavra in ['gasto', 'despesa', 'gastei', 'análise', 'resumo', 'financeiro']):
        analise = analisar_gastos(df_transacoes)
        st.session_state.analise_atual = analise
        resumo = texto_resumo_gastos(analise)
        st.session_state.aguardando_detalhar = True
        return resumo + "\n\n❓ Gostaria de ver o detalhamento por categoria?"
    
    # Investimentos
    elif any(palavra in mensagem_lower for palavra in ['investimento', 'investir', 'aplicar', 'aplicação', 'renda']):
        analise = analisar_gastos(df_transacoes)
        saldo = analise['saldo']
        
        if saldo > 0:
            sugestao = sugerir_investimentos(perfil_investidor, produtos_financeiros, saldo)
            return sugestao
        else:
            return f"⚠️ Seu saldo atual é negativo (R$ {saldo:.2f}). Recomendo primeiro ajustar seus gastos antes de pensar em investimentos. Posso ajudar com sugestões de redução de gastos!"
    
    # Histórico de atendimentos
    elif any(palavra in mensagem_lower for palavra in ['histórico', 'historico', 'atendimento', 'chamados']):
        historico = obter_historico_resumido(df_historico)
        return historico
    
    # Metas financeiras
    elif any(palavra in mensagem_lower for palavra in ['meta', 'metas', 'objetivo', 'objetivos', 'progresso']):
        analise = analisar_gastos(df_transacoes)
        saldo = analise['saldo']
        metas = analisar_metas(perfil_investidor, saldo)
        return metas
    
    # Saudação
    elif any(palavra in mensagem_lower for palavra in ['oi', 'olá', 'ola', 'bom dia', 'boa tarde', 'boa noite', 'hey', 'ei']):
        return f"""Olá, **{perfil_investidor['nome']}**! 👋

Sou o Gui seu Guia Financeiro pessoal. Posso ajudar você com:

• 📊 Análise de gastos e despesas
• 💡 Sugestões de redução de custos
• 📈 Recomendações de investimentos
• 🎯 Acompanhamento de metas financeiras
• 📜 Histórico de atendimentos

Como posso ajudar hoje?"""
    
    # Ajuda
    elif any(palavra in mensagem_lower for palavra in ['ajuda', 'help', 'o que você faz', 'comandos']):
        return """🤖 **Como posso ajudar você:**

**Análise Financeira:**
• Pergunte sobre seus gastos ou despesas
• Solicite um resumo financeiro
• Peça análise detalhada

**Investimentos:**
• Pergunte sobre investimentos
• Solicite recomendações baseadas no seu perfil

**Metas:**
• Acompanhe o progresso das suas metas
• Veja quanto precisa poupar

**Histórico:**
• Consulte seus atendimentos anteriores

**Exemplos de perguntas:**
• "Como estão meus gastos?"
• "Quero investir, o que você sugere?"
• "Mostre meu progresso nas metas"
• "Qual meu histórico de atendimentos?"

Pode perguntar à vontade! 😊"""
    
    # Mensagem padrão
    else:
        return """Desculpe, não entendi sua pergunta. 😅

Você pode perguntar sobre:
• Seus **gastos** e despesas
• Sugestões de **investimentos**
• Suas **metas** financeiras
• **Histórico** de atendimentos

Ou digite 'ajuda' para ver mais opções!"""

# Processar input do usuário
if user_input:
    # Adicionar mensagem do usuário
    st.session_state.mensagens.append({'role': 'user', 'content': user_input})
    
    # Gerar resposta
    resposta = processar_mensagem(user_input)
    
    # Verificar se precisa mostrar gráficos
    if isinstance(resposta, dict) and resposta.get('mostrar_graficos'):
        # Criar gráficos
        grafico_barras = criar_grafico_barras(st.session_state.analise_atual)
        grafico_pizza = criar_grafico_pizza(st.session_state.analise_atual)
        
        # Adicionar mensagem com gráficos
        st.session_state.mensagens.append({
            'role': 'assistant',
            'content': resposta['texto'],
            'grafico': grafico_barras
        })
        st.session_state.mensagens.append({
            'role': 'assistant',
            'content': "",
            'grafico': grafico_pizza
        })
    else:
        # Adicionar resposta normal
        st.session_state.mensagens.append({
            'role': 'assistant',
            'content': resposta,
            'grafico': None
        })
    
    # Recarregar para mostrar novas mensagens
    st.rerun()

# Mensagem inicial se não houver histórico
if len(st.session_state.mensagens) == 0:
    with st.chat_message("assistant"):
        st.markdown(f"""👋 Olá, **{perfil_investidor['nome']}**! 

Sou seu Agente Financeiro Inteligente. Estou aqui para ajudar você a:

• 📊 Analisar seus gastos e despesas
• 💡 Sugerir formas de economizar
• 📈 Recomendar investimentos baseados no seu perfil **{perfil_investidor['perfil_investidor'].title()}**
• 🎯 Acompanhar suas metas financeiras

**Como posso ajudar hoje?**""")
