import pandas as pd
import plotly.graph_objects as go;
from plotly_resampler import FigureResampler

column_names = ["x", "y"]
data = pd.read_csv('ts_sin.csv', delimiter=',', names=column_names, header=None, skiprows=3)

# 'x' und 'y' Spalten als Arrays extrahieren
x = pd.to_datetime(data['x'])
y = data['y'].values

# OPTION 2 - FigureResampler: dynamic aggregation via a Dash web-app
fig = FigureResampler(go.Figure())
fig.add_trace(go.Scattergl(name='noisy sine', showlegend=True), hf_x=x, hf_y=y)

fig.show_dash(mode='inline')
