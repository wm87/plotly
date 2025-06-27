from datetime import datetime
import pandas as pd
import plotly.graph_objs as go
import redis
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

# Erstellen Sie eine Redis-Instanz mit den Verbindungsdetails
# Verbindung zu Redis herstellen
r = redis.Redis(host='localhost', port=6379, db='0')


class GUIProj1Redis:
    """
    Beschreibung Ihrer Klasse hier.

    :param parameter1: Beschreibung des ersten Parameters.
    :param parameter2: Beschreibung des zweiten Parameters.

    Weitere Informationen oder Beschreibung hier.

    :return: Beschreibung dessen, was zurückgegeben wird.
    """

    """
    cache = Cache(app.server, config={
        'CACHE_TYPE': 'filesystem',
        'CACHE_DIR': 'cache_directory',
        'CACHE_THRESHOLD': 2  # Set an appropriate threshold value
    })
    """

    data = {}

    def __init__(self, app, data_list, file_path):
        """
        Constructs all the necessary attributes for the object.
        """
        self.app = app
        self.file_path = file_path
        self.data = data_list
        self.layout = html.Div([
            html.Div([
                html.Div(style={'height': '10px'}),
                html.H1('Messwerte', style={'text-align': 'center', 'font-size': '32px'}),
                html.Hr(style={'width': '100%', 'display': 'inline-block'}),
                html.Div(style={'height': '10px'}),

                html.Div([
                    html.Div([
                        html.Label('Ortschaft 1', style={'display': 'block', 'font-weight': 'bold'}),
                        dcc.Dropdown(id='dropdown1',
                                     options=[{'label': d['site'], 'value': d['key']} for d in self.data],
                                     style={'width': '100%'}
                                     ),
                    ], style={'display': 'inline-block', 'width': 'calc(25% - 10px)', 'margin-right': '10px'}),

                    html.Div([
                        html.Label('Ortschaft 2', style={'display': 'block', 'font-weight': 'bold'}),
                        dcc.Dropdown(id='dropdown2',
                                     options=[{'label': d['site'], 'value': d['key']} for d in self.data],
                                     style={'width': '100%'}
                                     ),
                    ], style={'display': 'inline-block', 'width': 'calc(25% - 10px)', 'margin-right': '10px'}),

                    html.Div([
                        html.Label('Ortschaft 3', style={'display': 'block', 'font-weight': 'bold'}),
                        dcc.Dropdown(id='dropdown3',
                                     options=[{'label': d['site'], 'value': d['key']} for d in self.data],
                                     style={'width': '100%'}
                                     ),
                    ], style={'display': 'inline-block', 'width': 'calc(25% - 10px)', 'margin-right': '10px'}),

                    html.Div([
                        html.Label('Ortschaft 4', style={'display': 'block', 'font-weight': 'bold'}),
                        dcc.Dropdown(id='dropdown4',
                                     options=[{'label': d['site'], 'value': d['key']} for d in self.data],
                                     style={'width': '100%'}
                                     ),
                    ], style={'display': 'inline-block', 'width': 'calc(25% - 10px)'}),
                ], style={'display': 'flex', 'justify-content': 'space-between', 'align-items': 'center',
                          'width': '100%'}),

                html.Div(style={'height': '10px'}),

                html.Div([
                    html.Div([
                        html.Label('Station 1', style={'display': 'block', 'font-weight': 'bold'}),
                        dcc.Dropdown(id='dropdown21',
                                     options=[
                                         {'label': station['station_name'], 'value': station['station_no'] + '.csv'}
                                         for d in self.data for station in d['stations']],
                                     style={'width': '100%'}
                                     ),
                    ], style={'display': 'inline-block', 'width': 'calc(25% - 10px)', 'margin-right': '10px'}),

                    html.Div([
                        html.Label('Station 2', style={'display': 'block', 'font-weight': 'bold'}),
                        dcc.Dropdown(id='dropdown22',
                                     options=[
                                         {'label': station['station_name'], 'value': station['station_no'] + '.csv'}
                                         for d in self.data for station in d['stations']],
                                     style={'width': '100%'}
                                     ),
                    ], style={'display': 'inline-block', 'width': 'calc(25% - 10px)', 'margin-right': '10px'}),

                    html.Div([
                        html.Label('Station 3', style={'display': 'block', 'font-weight': 'bold'}),
                        dcc.Dropdown(id='dropdown23',
                                     options=[
                                         {'label': station['station_name'], 'value': station['station_no'] + '.csv'}
                                         for d in self.data for station in d['stations']],
                                     style={'width': '100%'}
                                     ),
                    ], style={'display': 'inline-block', 'width': 'calc(25% - 10px)', 'margin-right': '10px'}),

                    html.Div([
                        html.Label('Station 4', style={'display': 'block', 'font-weight': 'bold'}),
                        dcc.Dropdown(id='dropdown24',
                                     options=[
                                         {'label': station['station_name'], 'value': station['station_no'] + '.csv'}
                                         for d in self.data for station in d['stations']],
                                     style={'width': '100%'}
                                     ),
                    ], style={'display': 'inline-block', 'width': 'calc(25% - 10px)'}),
                ], style={'display': 'flex', 'justify-content': 'space-between', 'align-items': 'center',
                          'width': '100%'})
            ], style={'text-align': 'center', 'width': '100%'}),

            dcc.Graph(id='graph1')
        ])
        self.bind_callbacks()

    # Dekorator zur Messung der Ausführungszeit
    def timer(self, param):
        def decorator(funktion):
            def wrapper(*args, **kwargs):
                startzeit = datetime.now()
                ergebnis = funktion(*args, **kwargs)
                endzeit = datetime.now()
                laufzeit_ms = (endzeit - startzeit).total_seconds() * 1000
                print(f"{param}: {laufzeit_ms:.1f} ms")
                return ergebnis

            return wrapper

        return decorator

    def bind_callbacks(self):

        # @self.cache.memoize()
        def update_dropdown(selected_site):
            filtered_data = next((d for d in self.data if d['key'] == selected_site), None)
            if filtered_data:
                return [{'label': station['station_name'], 'value': f"{station['station_no']}.csv"} for station in
                        filtered_data['stations']]
            else:
                return []

        # obere droop-down-stationsreihe
        @self.app.callback(
            Output('dropdown21', 'options'),
            Input('dropdown1', 'value')
        )
        def update_dropdown21(selected_site):
            return update_dropdown(selected_site)

        @self.app.callback(
            Output('dropdown22', 'options'),
            Input('dropdown2', 'value')
        )
        def update_dropdown22(selected_site):
            return update_dropdown(selected_site)

        @self.app.callback(
            Output('dropdown23', 'options'),
            Input('dropdown3', 'value')
        )
        def update_dropdown23(selected_site):
            return update_dropdown(selected_site)

        @self.app.callback(
            Output('dropdown24', 'options'),
            Input('dropdown4', 'value')
        )
        def update_dropdown24(selected_site):
            return update_dropdown(selected_site)

        # Definiere die Callback-Funktionen, um das Diagramm zu aktualisieren
        @self.app.callback(
            Output('graph1', 'figure'),
            [Input('dropdown21', 'value'),
             Input('dropdown22', 'value'),
             Input('dropdown23', 'value'),
             Input('dropdown24', 'value')]
        )
        @self.timer(param="graph1")
        def update_graph1(selected_station1, selected_station2, selected_station3, selected_station4):
            stationdata = []
            if any(
                    [selected_station1, selected_station2, selected_station3, selected_station4]):

                for i, selected_station in enumerate(
                        [selected_station1, selected_station2, selected_station3, selected_station4], start=1):
                    if selected_station:
                        # Schlüssel für die gesuchte CSV-Datei
                        key_prefix = selected_station[:-4]

                        # Alle Schlüssel abrufen, die mit dem Dateinamen beginnen
                        keys = r.keys(f'{key_prefix}')

                        # Jeden Stream in eine Liste von Werten umwandeln
                        values = []
                        dfs = []  # Liste zum Speichern von DataFrames
                        batch_size = 1000  # Größe des Batches
                        for key in keys:
                            # Jeden Wert in Byte-String umwandeln
                            entries = r.xrange(key, count=3000)  # Angenommen, es gibt 3000 Einträge pro Stream
                            for entry in entries:
                                id, fields = entry
                                x_value = fields[b'x'].decode('utf-8')
                                y_value = float(fields[b'y'].decode('utf-8'))
                                values.append([x_value, y_value])

                                # Wenn die Größe des Batches erreicht ist, erstellen Sie einen DataFrame und leeren
                                # Sie die Werte
                                if len(values) == batch_size:
                                    df = pd.DataFrame(values, columns=['x', 'y'])
                                    dfs.append(df)
                                    values = []

                        # Fügen Sie die verbleibenden Werte hinzu, wenn es welche gibt
                        if values:
                            df = pd.DataFrame(values, columns=['x', 'y'])
                            dfs.append(df)

                        # Kombinieren Sie alle DataFrames
                        final_df = pd.concat(dfs, ignore_index=True)

                        """
                        df['x'] = pd.to_datetime(df['x'], utc=True).dt.tz_convert('Europe/Berlin')
                        mask = (df['x'] >= start_date) & (df['x'] <= end_date)
                        filtered_df = df.loc[mask]
                        stationdata.append(go.Scattergl(x=filtered_df['x'], y=filtered_df['y'], mode='lines', name=f'Station: {i}'))
                        """
                        stationdata.append(go.Scattergl(x=final_df['x'], y=final_df['y'], mode='lines', name=f'Station: {i}'))

            fig = go.Figure(data=stationdata)
            fig.update_layout(title='Stationen')
            fig.update_xaxes(title_text='x')
            fig.update_yaxes(title_text='y')
            fig.update_layout(showlegend=True)
            return fig

    def start(self, debug, host, port):
        self.app.run_server(debug=debug, host=host, port=port)

    def get_layout(self):
        return self.layout

    def get_app(self):
        return self.app
