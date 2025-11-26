import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc

# ============================================================
# CARGA DE DATOS
# ============================================================
df = pd.read_csv("df_limpio.csv")

numericas = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
numericas = [c for c in numericas if c != "diabetes"]
categ = df.select_dtypes(include=["object"]).columns.tolist()
objetivo = "diabetes"

# ============================================================
# ESTILOS
# ============================================================
FONTS = {"fontFamily": "'Poppins', sans-serif"}

TITLE = {
    "fontSize": "48px",
    "fontWeight": "900",
    "color": "#4F46E5",
    "textAlign": "center",
    "marginBottom": "10px",
    **FONTS
}

SUBTITLE = {
    "fontSize": "32px",
    "fontWeight": "700",
    "color": "#E2EEFF",
    **FONTS
}

CARD = {
    "padding": "25px",
    "backgroundColor": "nightblue",
    "borderRadius": "15px",
    "boxShadow": "0px 0px 12px rgba(0,0,0,0.12)",
    "marginBottom": "30px",
    "color": "black",
    **FONTS
}

KPI_CARD = {
    "padding": "25px",
    "backgroundColor": "white",
    "borderRadius": "15px",
    "boxShadow": "0px 0px 12px rgba(0,0,0,0.18)",
    "marginBottom": "20px",
    "textAlign": "center",
    "color": "black",
    **FONTS
}

CONTENT = {
    "padding": "2rem",
    "backgroundColor": "#1D1C74",
    "height": "80vh",
    "overflowY": "auto"
}

TAB = {
    "padding": "12px",
    "fontSize": "17px",
    "fontWeight": "600",
    "background": "#002087",
    "borderRadius": "8px",
    "marginRight": "6px",
    **FONTS
}

TAB_SELECTED = {
    "padding": "12px",
    "fontSize": "17px",
    "fontWeight": "700",
    "background": "#4F46E5",
    "color": "white",
    "borderRadius": "8px",
    **FONTS
}

# ============================================================
# APP
# ============================================================
app = Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.COSMO,
        "https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800;900&display=swap"
    ],
    suppress_callback_exceptions=True
)

server = app.server   # ← NECESARIO PARA RENDER

# ============================================================
# LAYOUT
# ============================================================
app.layout = html.Div([
    html.Br(),
    html.H1("ANALISIS EXPLORATORIO - DIABETES ", style=TITLE),
    html.Hr(),

    dcc.Tabs(
        id="tabs",
        value="tab-kpi",
        children=[
            dcc.Tab("📌 KPIs Globales", value="tab-kpi", style=TAB, selected_style=TAB_SELECTED),
            dcc.Tab("📊 Univariado Numérico", value="tab-uni", style=TAB, selected_style=TAB_SELECTED),
            dcc.Tab("📈 Univariado Categórico", value="tab-cat", style=TAB, selected_style=TAB_SELECTED),
            dcc.Tab("📦 Desbalance", value="tab-desb", style=TAB, selected_style=TAB_SELECTED),
            dcc.Tab("🧩 Correlación", value="tab-corr", style=TAB, selected_style=TAB_SELECTED),
            dcc.Tab("📊 EDA Bivariado", value="tab-biv", style=TAB, selected_style=TAB_SELECTED),
        ]
    ),

    html.Div(id="content", style=CONTENT)
])

# ============================================================
# CALLBACK — MOSTRAR CONTENIDO
# ============================================================
@app.callback(
    Output("content", "children"),
    Input("tabs", "value")
)
def mostrar_contenido(tab):

    if tab == "tab-kpi":
        total = len(df)
        diabetes_rate = df["diabetes"].mean() * 100
        fisica = df["dias_salud_fisica"].mean()
        mental = df["dias_salud_mental"].mean()
        sueño = df["horas_sueño"].mean()
        bmi = df["bmi"].mean()

        return html.Div([
            html.H2("Indicadores Globales", style=SUBTITLE),

            dbc.Row([
                dbc.Col(html.Div([
                    html.H3("📊 Población Total"),
                    html.H1(f"{total:,}"),
                    html.P("Total de personas encuestadas en el estudio.", style={"fontSize": "14px"})
                ], style=KPI_CARD), md=4),

                dbc.Col(html.Div([
                    html.H3("🩸 % Diabetes"),
                    html.H1(f"{diabetes_rate:.2f}%"),
                    html.P("Proporción de participantes diagnosticados.", style={"fontSize": "14px"})
                ], style=KPI_CARD), md=4),

                dbc.Col(html.Div([
                    html.H3("⚖️ BMI Promedio"),
                    html.H1(f"{bmi:.2f}"),
                    html.P("Promedio del índice de masa corporal.", style={"fontSize": "14px"})
                ], style=KPI_CARD), md=4),
            ]),

            dbc.Row([
                dbc.Col(html.Div([
                    html.H3("💪 Salud Física"),
                    html.H1(f"{fisica:.1f}"),
                    html.P("Promedio de días con mala salud física.", style={"fontSize": "14px"})
                ], style=KPI_CARD), md=4),

                dbc.Col(html.Div([
                    html.H3("🧠 Salud Mental"),
                    html.H1(f"{mental:.1f}"),
                    html.P("Promedio de días con mala salud mental.", style={"fontSize": "14px"})
                ], style=KPI_CARD), md=4),

                dbc.Col(html.Div([
                    html.H3("😴 Horas de Sueño"),
                    html.H1(f"{sueño:.1f}"),
                    html.P("Promedio de horas de sueño por noche.", style={"fontSize": "14px"})
                ], style=KPI_CARD), md=4),
            ])
        ])

    if tab == "tab-uni":
        return html.Div([
            html.Div([
                html.H2("Distribución Numérica", style=SUBTITLE),
                dcc.Dropdown(id="uni-num", options=[{"label": n, "value": n} for n in numericas],
                             value=numericas[0], style={"marginBottom": "15px"}),
                dcc.Graph(id="g-uni-num")
            ], style=CARD)
        ])

    if tab == "tab-cat":
        return html.Div([
            html.Div([
                html.H2("Distribución Categórica", style=SUBTITLE),
                dcc.Dropdown(id="uni-cat", options=[{"label": c, "value": c} for c in categ],
                             value=categ[0], style={"marginBottom": "15px"}),
                dcc.Graph(id="g-uni-cat")
            ], style=CARD)
        ])

    if tab == "tab-desb":
        return html.Div([
            html.Div([
                html.H2("Desbalance de Clases", style=SUBTITLE),
                dcc.Graph(id="g-desb")
            ], style=CARD)
        ])

    if tab == "tab-corr":
        return html.Div([
            html.Div([
                html.H2("Matriz de Correlación", style=SUBTITLE),
                dcc.Graph(id="g-corr")
            ], style=CARD)
        ])

    if tab == "tab-biv":
        return html.Div([
            html.Div([
                html.H2("EDA Bivariado", style=SUBTITLE),
                html.H4("Variable Numérica"),
                dcc.Dropdown(id="biv-num", options=[{"label": n, "value": n} for n in numericas],
                             value=numericas[0], style={"marginBottom": "15px"}),
                html.H4("Variable Categórica"),
                dcc.Dropdown(id="biv-cat", options=[{"label": c, "value": c} for c in categ],
                             value=categ[0], style={"marginBottom": "15px"}),
                dcc.Graph(id="g-biv")
            ], style=CARD)
        ])

# ============================================================
# CALLBACKS GRAFICOS
# ============================================================
@app.callback(Output("g-uni-num", "figure"), Input("uni-num", "value"))
def g_uninum(v):
    fig = px.histogram(df, x=v, nbins=30, color_discrete_sequence=["#4F46E5"])
    fig.update_layout(template="plotly_white")
    return fig

@app.callback(Output("g-uni-cat", "figure"), Input("uni-cat", "value"))
def g_unicat(v):
    t = df[v].value_counts().reset_index()
    t.columns = ["categoria", "frecuencia"]
    fig = px.bar(t, x="categoria", y="frecuencia", color="categoria")
    fig.update_layout(template="plotly_white")
    return fig

@app.callback(Output("g-desb", "figure"), Input("tabs", "value"))
def g_desb(_):
    t = df["diabetes"].value_counts().reset_index()
    t.columns = ["clase", "frecuencia"]
    fig = px.bar(t, x="clase", y="frecuencia", text="frecuencia",
                 color="clase", color_discrete_sequence=["#4F46E5", "#0EA5E9"])
    fig.update_layout(template="plotly_white")
    return fig

@app.callback(Output("g-corr", "figure"), Input("tabs", "value"))
def g_corr(_):
    fig = px.imshow(df[numericas].corr(), color_continuous_scale="Viridis")
    return fig

@app.callback(Output("g-biv", "figure"), Input("biv-num", "value"), Input("biv-cat", "value"))
def g_biv(num, cat):
    fig = px.box(df, x=cat, y=num, color=cat)
    fig.update_layout(template="plotly_white")
    return fig

# ============================================================
# RUN
# ============================================================
if __name__ == "__main__":
    app.run(debug=True)
