import os
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import base64


# Carregar dados do Excel
dados = pd.read_csv("vinculo_externo.csv", delimiter=';')
dados

pasta_pdf = 'match'

# Inicializar o aplicativo Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])


# Layout do aplicativo
app.layout = html.Div(children=[

       dbc.Row([
        dbc.Col([
            dbc.Card([
                html.H2("Gente & Gestão", style={"font-family": "Voltaire", "font-size": "25px"}),
                html.Hr(),
                dcc.Dropdown(
                    id='dropdown-funcionario',
                    options=[{'label': nome, 'value': nome} for nome in dados['Nome']],
                    value=dados['Nome'].iloc[0],  # Valor padrão
                    style={'width': '100%'}
                )
            ], style={"width": "80%", "height": "30vh", "margin": "20px", "padding": "20px"}
            ),
        ], sm=4),

        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Salário Pago"),
                        dbc.CardBody(
                            html.H5(id='Salario', className="card-title")
                        )
                    ], style={"height": "30vh", "margin": "20px", "padding": "20px"}),
                ], sm=4),

                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Nome"),
                        dbc.CardBody(
                            html.H5(id='Nome', className="card-title")
                        )
                    ], style={"height": "30vh", "margin": "20px", "padding": "20px"}),
                ], sm=4),

                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Cargo"),
                        dbc.CardBody(
                            html.H5(id='Cargo', className="card-title")
                        )
                    ], style={"height": "30vh", "margin": "20px", "padding": "20px"}),
                ], sm=4),
            ]),
        ], sm=8),
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Avaliação Sólides"),
                dbc.CardBody([
                    html.H3("Visualização do PDF"),
                    html.Iframe(id='iframe-pdf', width='100%', height='500')
                ], className='mb-3')
            ], style={"height": "100vh", "margin": "20px", "padding": "20px"}),
        ], sm=12),
    ]),
])
        
# Callback para atualizar informações e visualização do PDF
@app.callback(
    Output('Salario', 'children'),
    [Input('dropdown-funcionario', 'value')]
)
def uptade_salario(selected_funcionario):
    # Informações de salário
    salario = dados.loc[dados["Nome"] == selected_funcionario, 'Salario'].iloc[0]
    return f"Salario:{salario}"

@app.callback(
    Output('Nome', 'children'),
    Output('Cargo', 'children'),
    [Input('dropdown-funcionario', 'value')]
)

def update_nome_cargo(selected_funcionario):
    nome = dados.loc[dados["Nome"] == selected_funcionario, 'Nome'].iloc[0]
    cargo = dados.loc[dados["Nome"] == selected_funcionario, 'Cargo'].iloc[0]
    return f"Nome: {nome}", f"Cargo: {cargo}"

@app.callback(
    Output('iframe-pdf', 'src'),
    [Input('dropdown-funcionario', 'value')]
)
def update_pdf(selected_funcionario):  
    # Caminho completo para o arquivo PDF
    pdf_path = os.path.join(pasta_pdf, f"{selected_funcionario}.pdf")
    pdf_base64 = base64.b64encode(open(pdf_path, "rb").read()).decode('ascii')
    
    return f"data:application/pdf;base64,{pdf_base64}"

# Executar o aplicativo
if __name__ == '__main__':
    app.run_server(port = 5000,debug=True)