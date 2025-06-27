import time

import plotly.graph_objs as go
import polars as pl
from dash import dcc, html
from dash.dependencies import Input, Output


class GUIProj1V1:
    """
    A class to represent the GUI for measurements.

    Attributes
    ----------
    app : Dash
        The Dash application instance.
    file_path : str
        The file path for data storage.
    data : list
        A list of dictionaries containing data for the dropdown options.

    Methods
    -------
    __init__(self, app, data_list, file_path):
        Initializes the GUIProj1V1 class with the given app, data list, and file path.
        Methods
    timer(self, param):
        Decorator to measure the execution time of a function.
    bind_callbacks(self):
        Binds the callbacks for the dropdowns and graphs.
    start(self, debug, host, port):
        Starts the Dash server.
    get_layout(self):
        Returns the layout of the app.
    get_app(self):
        Returns the Dash app instance.
    """

    data = {}

    def __init__(self, app, data_list, file_path):
        """
        Constructs all the necessary attributes for the GUIProj1V1 object.

        Parameters
        ----------
        app : Dash
            The Dash application instance.
        data_list : list
            A list of dictionaries containing data for the dropdown options.
        file_path : str
            The file path for data storage.
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
                        dcc.Dropdown(id='proj1_v1_dd1',
                                     options=[{'label': d['site'], 'value': d['key']} for d in self.data],
                                     style={'width': '100%'}
                                     ),
                    ], style={'display': 'inline-block', 'width': 'calc(25% - 10px)', 'margin-right': '10px'}),

                    html.Div([
                        html.Label('Ortschaft 2', style={'display': 'block', 'font-weight': 'bold'}),
                        dcc.Dropdown(id='proj1_v1_dd2',
                                     options=[{'label': d['site'], 'value': d['key']} for d in self.data],
                                     style={'width': '100%'}
                                     ),
                    ], style={'display': 'inline-block', 'width': 'calc(25% - 10px)', 'margin-right': '10px'}),

                    html.Div([
                        html.Label('Ortschaft 3', style={'display': 'block', 'font-weight': 'bold'}),
                        dcc.Dropdown(id='proj1_v1_dd3',
                                     options=[{'label': d['site'], 'value': d['key']} for d in self.data],
                                     style={'width': '100%'}
                                     ),
                    ], style={'display': 'inline-block', 'width': 'calc(25% - 10px)', 'margin-right': '10px'}),

                    html.Div([
                        html.Label('Ortschaft 4', style={'display': 'block', 'font-weight': 'bold'}),
                        dcc.Dropdown(id='proj1_v1_dd4',
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
                        dcc.Dropdown(id='proj1_v1_dd21',
                                     options=[
                                         {'label': station['station_name'], 'value': station['station_no'] + '.csv'}
                                         for d in self.data for station in d['stations']],
                                     style={'width': '100%'}
                                     ),
                    ], style={'display': 'inline-block', 'width': 'calc(25% - 10px)', 'margin-right': '10px'}),

                    html.Div([
                        html.Label('Station 2', style={'display': 'block', 'font-weight': 'bold'}),
                        dcc.Dropdown(id='proj1_v1_dd22',
                                     options=[
                                         {'label': station['station_name'], 'value': station['station_no'] + '.csv'}
                                         for d in self.data for station in d['stations']],
                                     style={'width': '100%'}
                                     ),
                    ], style={'display': 'inline-block', 'width': 'calc(25% - 10px)', 'margin-right': '10px'}),

                    html.Div([
                        html.Label('Station 3', style={'display': 'block', 'font-weight': 'bold'}),
                        dcc.Dropdown(id='proj1_v1_dd23',
                                     options=[
                                         {'label': station['station_name'], 'value': station['station_no'] + '.csv'}
                                         for d in self.data for station in d['stations']],
                                     style={'width': '100%'}
                                     ),
                    ], style={'display': 'inline-block', 'width': 'calc(25% - 10px)', 'margin-right': '10px'}),

                    html.Div([
                        html.Label('Station 4', style={'display': 'block', 'font-weight': 'bold'}),
                        dcc.Dropdown(id='proj1_v1_dd24',
                                     options=[
                                         {'label': station['station_name'], 'value': station['station_no'] + '.csv'}
                                         for d in self.data for station in d['stations']],
                                     style={'width': '100%'}
                                     ),
                    ], style={'display': 'inline-block', 'width': 'calc(25% - 10px)'}),
                ], style={'display': 'flex', 'justify-content': 'space-between', 'align-items': 'center',
                          'width': '100%'})
            ], style={'text-align': 'center', 'width': '100%'}),

            dcc.Graph(id='proj1_v1_graph1'),
        ])
        self.bind_callbacks()

    def timer(self, param):
        """
        Decorator to measure the execution time of a function.

        Parameters
        ----------
        param : str
            A parameter to be printed with the execution time.

        Returns
        -------
        function
            The decorated function with execution time measurement.
        """

        # Dekorator zur Messung der Ausführungszeit
        def decorator(funktion):
            def wrapper(*args, **kwargs):
                start_time = time.perf_counter()
                result = funktion(*args, **kwargs)
                end_time = time.perf_counter()
                runtime_ms = (end_time - start_time) * 1000
                print(f"{param}: {runtime_ms:.2f} ms")
                return result

            return wrapper

        return decorator

    def bind_callbacks(self):
        """
        Binds the callbacks for the dropdowns and graphs in the Dash app.

        Methods
        -------
        update_dropdown(selected_site):
            Updates the dropdown options based on the selected site.
        create_dropdown_callback(output_id, input_id):
            Creates a generic callback function for dropdowns.
        create_update_graph_callback(graph_id, dropdown_ids):
            Creates a callback function to update the graph based on selected dropdown values.
        """

        def update_dropdown(selected_site):
            filtered_data = [d for d in self.data if d['key'] == selected_site]
            return [{'label': station['station_name'], 'value': station['station_no'] + '.csv'} for station in
                    filtered_data[0]['stations']] if filtered_data else []

        # Generische Callback-Funktion
        def create_dropdown_callback(output_id, input_id):
            @self.app.callback(
                Output(output_id, 'options'),
                Input(input_id, 'value')
            )
            def update(selected_site):
                return update_dropdown(selected_site)

            return update

        # Obere Drop-down-Stationsreihe
        create_dropdown_callback('proj1_v1_dd21', 'proj1_v1_dd1')
        create_dropdown_callback('proj1_v1_dd22', 'proj1_v1_dd2')
        create_dropdown_callback('proj1_v1_dd23', 'proj1_v1_dd3')
        create_dropdown_callback('proj1_v1_dd24', 'proj1_v1_dd4')

        # Definiere eine allgemeine Callback-Funktion, um das Diagramm zu aktualisieren
        def create_update_graph_callback(graph_id, dropdown_ids):
            @self.app.callback(
                Output(graph_id, 'figure'),
                [Input(dropdown_id, 'value') for dropdown_id in dropdown_ids]
            )
            @self.timer(param=graph_id)
            def update_graph(*selected_stations):
                stationdata = []
                for i, selected_station in enumerate(selected_stations, start=1):
                    if selected_station:
                        # Einlesen der CSV-Datei und direkte Konvertierung der Datentypen
                        df = (pl.read_csv(f"{self.file_path}{selected_station}",
                                          separator=';',
                                          skip_rows=3,
                                          new_columns=['x', 'y'])
                        .with_columns([
                            pl.col('x'),
                            pl.col('y').cast(pl.Float32)
                        ]))

                        stationdata.append(
                            go.Scattergl(x=df['x'].to_list(), y=df['y'].to_list(), mode='lines', name=f'Station: {i}'))
                fig = go.Figure(data=stationdata)
                fig.update_layout(title='Stationen')
                fig.update_xaxes(title_text='Zeit')
                fig.update_yaxes(title_text='Messwert')
                fig.update_layout(showlegend=True)
                return fig

        # Erstelle die Callback-Funktionen für die beiden Diagramme
        create_update_graph_callback('proj1_v1_graph1',
                                     ['proj1_v1_dd21', 'proj1_v1_dd22', 'proj1_v1_dd23', 'proj1_v1_dd24'])

    def start(self, debug, host, port):
        """
        Starts the Dash server.

        Parameters
        ----------
        debug : bool
            If True, enables debug mode.
        host : str
            The host IP address.
        port : int
            The port number.
        """
        self.app.run_server(debug=debug, host=host, port=port)

    def get_layout(self):
        """
        Returns the layout of the app.

        Returns
        -------
        html.Div
            The layout of the Dash app.
        """
        return self.layout

    def get_app(self):
        """
        Returns the Dash app instance.

        Returns
        -------
        Dash
            The Dash app instance.
        """
        return self.app
