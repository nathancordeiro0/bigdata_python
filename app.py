from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_mantine_components as dmc

# Manipulação de dados
arquivo_excel = "Controle.xlsx"
df = pd.read_excel(arquivo_excel)

df["Preço de Venda Atacado"] = df["Preço de Venda Atacado"].apply(lambda x: float(str(x).replace("R$", "").replace(" ", "").replace(",",".")))
df["Preço de Venda"] = df["Preço de Venda"].apply(lambda x: float(str(x).replace("R$", "").replace(" ", "").replace(",",".")))


def vendas():
    df["Vendas"].sort_values(ascending=False)
    novo_arquivo_excel = "Vendas.xlsx"
    dados_ordenados = df.sort_values(by="Vendas", ascending=False)
    dados_ordenados.to_excel(novo_arquivo_excel, index=False)

def desconto_xlsx():

 df["Desconto"] = (df["Preço de Venda"] - df["Preço de Venda Atacado"])
 novo_arquivo_excel = "Desconto.xlsx"
 dados_ordenados = df.sort_values(by="Desconto", ascending=False)
 dados_ordenados.to_excel(novo_arquivo_excel, index=False)



desconto_xlsx()
vendas()

a = "Desconto.xlsx"
b = "Vendas.xlsx"

top_10_produtos = pd.read_excel(a).head(30)
top_10_vendas = pd.read_excel(b).head(30)

# Frontend
external_stylesheets = [dmc.theme.DEFAULT_COLORS]
app = Dash(__name__, external_stylesheets=external_stylesheets)

style = {
    'height': '100',
    'background': '#f6f8fc'
}

app.layout = dmc.Container([
    dmc.Title('GRÁFICOS DE CONTROLE', size='h4', style={'textAlign': 'center'}),
    html.Hr(),

    dmc.Grid([
        dmc.Col([
            dmc.Card(
                children=[
                    dmc.Group(
                        [
                            dmc.Text("TOP 10 DESCONTOS", weight=500),
                            dmc.Badge("GRÁFICO EM BARRAS", color="blue", variant="light"),
                        ],
                        position="apart",
                        mt="md",
                        mb="xs",
                    ),
                    dmc.CardSection(
                        dcc.Graph(figure=px.bar(top_10_produtos, x='Produtos', y='Desconto'))
                    ),
                ],
                withBorder=True,
                shadow="sm",
                radius="md"
            )
        ], span=12),

        dmc.Col([
            dmc.Card(
                children=[
                    dmc.Group(
                        [
                            dmc.Text("TOP 10 VENDAS", weight=500),
                            dmc.Badge("GRÁFICO EM TORTA", color="blue", variant="light"),
                        ],
                        position="apart",
                        mt="md",
                        mb="xs",
                    ),
                    dmc.CardSection(
                        dcc.Graph(figure=px.pie(top_10_vendas,  values='Vendas', names='Produtos'))
                    )
                ],
                withBorder=True,
                shadow="sm",
                radius="md"
            )
        ], span=12)
    ])
], fluid=True, style=style )

if __name__ == '__main__':
    app.run(debug=True)