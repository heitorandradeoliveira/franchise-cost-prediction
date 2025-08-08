import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import os
import plotly.graph_objs as go

# =======================================
# Configuração inicial
# =======================================
st.set_page_config(
    page_title="Previsão de Custo de Franquia",
    page_icon="💰",
    layout="wide"
)

st.markdown(
    """
    <div style="display:flex; justify-content: flex-end; align-items: center; margin-bottom: 10px;">
        <a href="https://github.com/heitorandradeoliveira" target="_blank" style="text-decoration:none; font-weight:bold; font-size:16px;">
            🚀 github.com/heitorandradeoliveira
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

st.title("💰 Previsão Inicial de Custo para Franquia")
st.write("Este aplicativo usa Regressão Linear para prever o custo inicial de uma franquia a partir do valor anual.")

# =======================================
# Função para carregar dados
# =======================================


@st.cache_data
def carregar_dados(caminho_csv):
    if not os.path.exists(caminho_csv):
        st.error(f"Arquivo `{caminho_csv}` não encontrado.")
        return None
    try:
        return pd.read_csv(caminho_csv, sep=";")
    except Exception as e:
        st.error(f"Erro ao ler o arquivo: {e}")
        return None


# =======================================
# Carregamento e pré-processamento
# =======================================
dados = carregar_dados("./app/slr12.csv")
# print(dados.head())
# dados.FrqAnual = pd.to_numeric(dados.FrqAnual)
# dados.Cuslnic = pd.to_numeric(dados.Cuslnic)
if dados is not None:
    X = dados[['FrqAnual']]
    y = dados['CusInic']

    # =======================================
    # Treinamento do modelo
    # =======================================
    modelo = LinearRegression()
    modelo.fit(X, y)

    # =======================================
    # Layout de duas colunas
    # =======================================
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📄 Dados de Entrada")
        st.dataframe(dados.head(10).style.format({
            # zero casas decimais, sem separador de milhar
            'FrqAnual': '{:.0f}',
            'CusInic': '{:.0f}'
        }))

    # with col2:
    #     st.subheader("📊 Gráfico de Dispersão")
    #     fig, ax = plt.subplots()
    #     ax.scatter(X, y, color='blue', label="Dados reais")
    #     ax.plot(X, modelo.predict(X), color='red', label="Linha de Regressão")
    #     ax.set_xlabel("Valor Anual da Franquia (R$)")
    #     ax.set_ylabel("Custo Inicial (R$)")
    #     ax.legend()
    #     st.pyplot(fig)
    with col2:
        st.subheader("📊 Gráfico de Dispersão Interativo")
        fig = go.Figure()
        # Pontos reais
        fig.add_trace(go.Scatter(
            x=X['FrqAnual'],
            y=y,
            mode='markers',
            name='Dados reais',
            marker=dict(color='blue')
        ))
        # Linha da regressão
        fig.add_trace(go.Scatter(
            x=X['FrqAnual'],
            y=modelo.predict(X),
            mode='lines',
            name='Linha de Regressão',
            line=dict(color='red')
        ))
        fig.update_layout(
            xaxis_title='Valor Anual da Franquia (R$)',
            yaxis_title='Custo Inicial (R$)',
            legend=dict(x=0, y=1),
            margin=dict(l=40, r=40, t=40, b=40),
            height=400,
            hovermode='closest'
        )
        st.plotly_chart(fig, use_container_width=True)

    # =======================================
    # Previsão de novo valor
    # =======================================
    st.subheader("🔮 Previsão para Novo Valor Anual")
    novo_valor = st.number_input(
        "Insira Novo Valor Anual (R$)",
        min_value=1.0,
        max_value=999999.0,
        value=1500.0,
        step=0.01
    )

    if st.button("Calcular Previsão"):
        dados_novo_valor = pd.DataFrame([[novo_valor]], columns=['FrqAnual'])
        previsao = modelo.predict(dados_novo_valor)
        st.success(f"💡 Previsão de Custo Inicial: R$ {previsao[0]:.2f}")
