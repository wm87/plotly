import time
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import plotly.graph_objs as go
import polars as pl
from dash import dcc, html
from dash.dependencies import Input, Output
from dateutil.parser import parse as dt_parse


class GUIProj1V2:
    data = {}

    def __init__(self, app, data_list, file_path, days):

        self.app = app
        self.file_path = file_path
        self.days = days
        self.data = data_list

        self.layout = html.Div([
            # first part
            html.Div([
                html.Div(style={'height': '10px'}),
                html.H1('Messwerte mit Datumsfilter', style={'text-align': 'center', 'font-size': '32px'}),
                html.Hr(style={'width': '100%', 'display': 'inline-block'}),
                html.Div(style={'height': '10px'}),

                html.Div([
                    *[html.Div([
                        html.Label(f'Ortschaft {i}', style={'font-weight': 'bold'}),
                        dcc.Dropdown(id=f'proj1_v2_d{i}',
                                     options=[{'label': d['site'], 'value': d['key']} for d in self.data],
                                     style={'width': '100%'})
                    ], style={'flex': '1', 'margin-right': '10px'}) for i in range(1, 5)]
                ], style={'display': 'flex', 'justify-content': 'space-between', 'align-items': 'center',
                          'margin': '10px 0'}),

                html.Div([
                    *[html.Div([
                        html.Label(f'Station {i}', style={'font-weight': 'bold'}),
                        dcc.Dropdown(id=f'proj1_v2_dd2{i}',
                                     options=[
                                         {'label': station['station_name'], 'value': station['station_no'] + '.csv'}
                                         for d in self.data for station in d['stations']],
                                     style={'width': '100%'})
                    ], style={'flex': '1', 'margin-right': '10px'}) for i in range(1, 5)]
                ], style={'display': 'flex', 'justify-content': 'space-between', 'align-items': 'center',
                          'margin': '10px 0'}),

                dcc.Graph(id='proj1_v2_graph1'),

                html.Div([
                    html.Div([
                        html.Label('Von', style={'font-weight': 'bold', 'margin-right': '10px'}),
                        dcc.DatePickerSingle(
                            id='date-picker-single-1',
                            min_date_allowed=datetime.now().date() - timedelta(days=self.days),
                            max_date_allowed=datetime.now().date(),
                            initial_visible_month=datetime.now().date(),
                            date=datetime.now().date() - timedelta(days=self.days),
                            display_format='DD.MM.YYYY'
                        )
                    ], style={'display': 'flex', 'align-items': 'center', 'margin-right': '10px'}),
                    html.Div([
                        html.Label('Bis', style={'font-weight': 'bold', 'margin-right': '10px'}),
                        dcc.DatePickerSingle(
                            id='date-picker-single-2',
                            min_date_allowed=datetime.now().date() - timedelta(days=self.days),
                            max_date_allowed=datetime.now().date(),
                            initial_visible_month=datetime.now().date(),
                            date=datetime.now().date(),
                            display_format='DD.MM.YYYY'
                        )
                    ], style={'display': 'flex', 'align-items': 'center'})
                ], style={'display': 'flex', 'justify-content': 'center', 'margin': '10px 0'}),
            ])
        ])

        self.bind_callbacks()

    def timer(self, param):
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

    def get_dropdown_pairs(self):
        return [
            ('proj1_v2_dd21', 'proj1_v2_d1'),
            ('proj1_v2_dd22', 'proj1_v2_d2'),
            ('proj1_v2_dd23', 'proj1_v2_d3'),
            ('proj1_v2_dd24', 'proj1_v2_d4')
        ]

    def get_graph_pairs(self):
        return [
            ('proj1_v2_graph1', ['date-picker-single-1', 'date-picker-single-2'],
             ['proj1_v2_dd21', 'proj1_v2_dd22', 'proj1_v2_dd23', 'proj1_v2_dd24'])
        ]

    def bind_callbacks(self):

        def update_dropdown(selected_site):
            filtered_data = next((d for d in self.data if d['key'] == selected_site), None)
            if filtered_data:
                return [{'label': station['station_name'], 'value': f"{station['station_no']}.csv"} for station in
                        filtered_data['stations']]
            else:
                return []

        def create_update_dropdown_callback(dd_output, dd_input):
            @self.app.callback(
                Output(dd_output, 'options'),
                Input(dd_input, 'value')
            )
            def update_dropdown_callback(selected_site):
                return update_dropdown(selected_site)

        dropdown_pairs = self.get_dropdown_pairs()

        for dropdown_output, dropdown_input in dropdown_pairs:
            create_update_dropdown_callback(dropdown_output, dropdown_input)

        def create_update_graph_callback(graph_id, date_picker_ids, dropdown_ids):
            @self.app.callback(
                Output(graph_id, 'figure'),
                [Input(date_picker_id, 'date') for date_picker_id in date_picker_ids] +
                [Input(dropdown_id, 'value') for dropdown_id in dropdown_ids]
            )
            @self.timer(param=graph_id)
            def update_graph(date1, date2, *selected_stations):

                stationdata = []
                if date1 and date2 and any(selected_stations):
                    start_date = dt_parse(date1.split(' ')[0]).replace(tzinfo=ZoneInfo('UTC'))
                    end_date = dt_parse(date2.split(' ')[0]).replace(tzinfo=ZoneInfo('UTC'))

                    for i, selected_station in enumerate(selected_stations, start=1):
                        if selected_station:
                            # Einlesen der CSV-Datei und direkte Konvertierung der Datentypen
                            df = (pl.read_csv(f"{self.file_path}{selected_station}",
                                              separator=';',
                                              skip_rows=3,
                                              new_columns=['x', 'y'])
                            .with_columns([
                                pl.col('x').str.strptime(pl.Datetime).dt.convert_time_zone('UTC'),
                                pl.col('y').cast(pl.Float32)
                            ]))

                            # Konvertiere die Zeitzone der Datumsangaben in UTC
                            start_date_utc = start_date.astimezone(ZoneInfo('UTC'))
                            end_date_utc = end_date.astimezone(ZoneInfo('UTC'))

                            filtered_df = df.filter(
                                (pl.col('x') >= pl.lit(start_date_utc)) &
                                (pl.col('x') <= pl.lit(end_date_utc))
                            )

                            # Füge die Daten dem Plotly-Diagramm hinzu
                            stationdata.append(
                                go.Scattergl(x=filtered_df['x'].to_list(), y=filtered_df['y'].to_list(), mode='lines',
                                             name=f'Station: {i}'))

                fig = go.Figure(data=stationdata)
                fig.update_layout(title='Stations')
                fig.update_xaxes(title_text='Time')
                fig.update_yaxes(title_text='Measurement')
                fig.update_layout(showlegend=True)
                return fig

        graph_callbacks = self.get_graph_pairs()

        for graph, date_pickers, dropdowns in graph_callbacks:
            create_update_graph_callback(graph, date_pickers, dropdowns)

    def get_layout(self):

        return self.layout

    def get_app(self):

        return self.app
