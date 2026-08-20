# app.py
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

# Cargar el dataset optimizado generado en la fase ETL
df = pd.read_parquet("data/taxi_final_dataset.parquet")

# Inicializar la aplicación de Dash
app = Dash(__name__)

# Estructura visual del Dashboard (Layout)
app.layout = html.Div(style={'backgroundColor': '#f4f6f9', 'padding': '30px', 'fontFamily': 'Arial, sans-serif'}, children=[
    
    html.H1("Dashboard Analítico: Taxis de Nueva York 🚖", style={'textAlign': 'center', 'color': '#2c3e50'}),
    html.P("Pipeline completo de Big Data con Python, ETL y Plotly Dash en Ubuntu", style={'textAlign': 'center', 'color': '#7f8c8d'}),
    
    # Filtro interactivo (Dropdown de días de la semana)
    html.Div([
        html.Label("Selecciona el Día de la Semana:", style={'fontWeight': 'bold', 'display': 'block', 'marginBottom': '5px'}),
        dcc.Dropdown(
            id='dropdown-day',
            options=[{'label': day, 'value': day} for day in sorted(df['day_of_week'].unique())],
            value='Monday',
            clearable=False,
            style={'width': '100%'}
        )
    ], style={'width': '40%', 'margin': '0 auto 30px auto', 'background': 'white', 'padding': '15px', 'borderRadius': '8px', 'boxShadow': '0px 2px 5px rgba(0,0,0,0.05)'}),
    
    # Contenedor de KPIs (Tarjetas de resumen)
    html.Div(id='kpi-output', style={'display': 'flex', 'justifyContent': 'space-around', 'marginBottom': '30px'}),
    
    # Contenedor de Gráficos Interactivos
    html.Div([
        html.Div([dcc.Graph(id='graph-hours')], style={'width': '48%', 'display': 'inline-block', 'background': 'white', 'padding': '10px', 'borderRadius': '8px', 'boxShadow': '0px 2px 5px rgba(0,0,0,0.05)'}),
        html.Div([dcc.Graph(id='graph-distance')], style={'width': '48%', 'display': 'inline-block', 'background': 'white', 'padding': '10px', 'borderRadius': '8px', 'boxShadow': '0px 2px 5px rgba(0,0,0,0.05)', 'float': 'right'})
    ])
])

# Interactividad mediante Callbacks de Dash
@callback(
    [Output('kpi-output', 'children'),
     Output('graph-hours', 'figure'),
     Output('graph-distance', 'figure')],
    [Input('dropdown-day', 'value')]
)
def update_dashboard(selected_day):
    # Filtrar datos según el día seleccionado en el dropdown
    dff = df[df['day_of_week'] == selected_day]
    
    # Calcular métricas clave
    total_trips = len(dff)
    avg_fare = dff['total_amount'].mean()
    avg_distance = dff['trip_distance'].mean()
    
    # Estilo visual de las tarjetas KPI
    card_style = {
        'background': 'white', 
        'padding': '20px', 
        'borderRadius': '8px', 
        'boxShadow': '0px 2px 5px rgba(0,0,0,0.05)', 
        'textAlign': 'center', 
        'width': '28%'
    }
    
    kpis = [
        html.Div([html.H4("Total Viajes", style={'color': '#7f8c8d', 'margin': '0 0 10px 0'}), html.P(f"{total_trips:,}", style={'fontSize': '24px', 'fontWeight': 'bold', 'color': '#2c3e50', 'margin': '0'})], style=card_style),
        html.Div([html.H4("Tarifa Promedio", style={'color': '#7f8c8d', 'margin': '0 0 10px 0'}), html.P(f"${avg_fare:.2f}", style={'fontSize': '24px', 'fontWeight': 'bold', 'color': '#2c3e50', 'margin': '0'})], style=card_style),
        html.Div([html.H4("Distancia Promedio", style={'color': '#7f8c8d', 'margin': '0 0 10px 0'}), html.P(f"{avg_distance:.2f} mi", style={'fontSize': '24px', 'fontWeight': 'bold', 'color': '#2c3e50', 'margin': '0'})], style=card_style)
    ]
    
    # Gráfico 1: Demanda de viajes por hora
    df_hours = dff.groupby('hour').size().reset_index(name='count')
    fig_hours = px.bar(df_hours, x='hour', y='count', title=f"Demanda de Viajes por Hora ({selected_day})",
                       labels={'hour': 'Hora del Día', 'count': 'Cantidad de Viajes'})
    fig_hours.update_layout(margin=dict(t=40, b=20, l=20, r=20))
    
    # Gráfico 2: Histograma de distribución de distancias
    fig_distance = px.histogram(dff, x='trip_distance', nbins=30, title=f"Distribución de Distancias de Viaje ({selected_day})",
                                labels={'trip_distance': 'Distancia (Millas)'})
    fig_distance.update_layout(margin=dict(t=40, b=20, l=20, r=20))
    
    return kpis, fig_hours, fig_distance

# Ejecutar el servidor web local
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)
