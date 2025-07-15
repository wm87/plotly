import json
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import polars as pl
from datetime import datetime
import time
import os

# Lade messorte.json
with open('../data/messorte.json', encoding='utf-8') as f:
    messorte_data = json.load(f)

# Mapping für Dropdowns
site_to_stations = {entry["site"]: entry["stations"] for entry in messorte_data}
site_options = [{'label': s['site'], 'value': s['site']} for s in messorte_data]


# Lade Daten mit Polars
from dateutil import parser

def get_df(station_no):
    file_path = f"../data/{station_no}.csv"
    if not os.path.exists(file_path):
        print(f"⚠️ Datei nicht gefunden für Station {station_no}: {file_path}")
        return pl.DataFrame(schema=[('Timestamp', pl.Datetime), ('Value', pl.Float64)])

    try:
        # Lade CSV als Strings (Timestamp als String, Value als Float)
        df = (pl.read_csv(f"{file_path}",
                          separator=';',
                          skip_rows=3,
                          new_columns=['x', 'y'])
        .with_columns([
            pl.col('x'),
            pl.col('y').cast(pl.Float32)
        ]))

        return df

    except Exception as e:
        print(f"❌ Fehler beim Parsen der Datei {file_path}: {e}")
        return pl.DataFrame(schema=[('Timestamp', pl.Datetime), ('Value', pl.Float64)])


app = dash.Dash(__name__)
app.title = "Multi-Zeitreihen-Viewer (Polars)"


def dropdown_pair(index):
    return html.Div([
        html.Div([
            dcc.Dropdown(
                id=f'site-dropdown-{index}',
                options=site_options,
                placeholder=f"Ort {index + 1} wählen",
                style={'width': '100%'}
            )
        ], style={'width': '48%', 'display': 'inline-block', 'paddingRight': '2%'}),
        html.Div([
            dcc.Dropdown(
                id=f'station-dropdown-{index}',
                options=[],  # Start leer
                placeholder=f"Station {index + 1} wählen",
                style={'width': '100%'}
            )
        ], style={'width': '48%', 'display': 'inline-block'})
    ], style={'marginBottom': '10px'})


app.layout = html.Div([
    html.H2("📊 Vergleich von bis zu 4 Zeitreihen aus lokalen Dateien mit Polars"),
    *[dropdown_pair(i) for i in range(4)],
    dcc.Graph(id='multi-plot', style={'height': '600px'}),
    html.Div(id='load-time-display', style={'marginTop': '10px', 'fontWeight': 'bold', 'fontSize': '18px'})
])

# Callback für dynamische Stations-Optionen pro Ort
for i in range(4):
    @app.callback(
        Output(f'station-dropdown-{i}', 'options'),
        Input(f'site-dropdown-{i}', 'value')
    )
    def update_station_dropdown(site_value, idx=i):
        if not site_value:
            return []
        stations = site_to_stations.get(site_value, [])
        return [{'label': s['station_name'], 'value': s['station_no']} for s in stations]


# Callback zum Plotten mit Ladezeitmessung
@app.callback(
    Output('multi-plot', 'figure'),
    Output('load-time-display', 'children'),
    [Input(f'station-dropdown-{i}', 'value') for i in range(4)],
    [State(f'site-dropdown-{i}', 'value') for i in range(4)]
)
def update_plot(station0, station1, station2, station3,
                site0, site1, site2, site3):
    start_time = time.time()

    station_nos = [station0, station1, station2, station3]
    site_values = [site0, site1, site2, site3]

    fig = go.Figure()
    colors = ['#1f77b4', '#2ca02c', '#ff7f0e', '#d62728']

    for i, (station_no, site) in enumerate(zip(station_nos, site_values)):
        if station_no and site:
            df = get_df(station_no)
            if df.is_empty():
                print(f"Keine Daten für Station {station_no} ({site})")
                continue

            stations = site_to_stations.get(site, [])
            station_name = next((s['station_name'] for s in stations if s['station_no'] == station_no), station_no)

            # Polars -> Plotly-kompatibel: Listen extrahieren
            fig.add_trace(go.Scattergl(x=df['x'].to_list(), y=df['y'].to_list(), mode='lines', name=f'Station: {i}'))

    fig.update_layout(
        title="Zeitverlauf der ausgewählten Stationen",
        xaxis_title="Zeit",
        yaxis_title="Messwert",
        height=600
    )

    duration_ms = (time.time() - start_time) * 1000
    load_time_text = f"Ladezeit: {duration_ms:.2f} ms"
    print(load_time_text)

    return fig, load_time_text


if __name__ == '__main__':
    app.run(debug=True)
