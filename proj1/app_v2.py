import json
from dash import Dash
from dash import html
from proj1.gui.proj1_v2 import GUIProj1V2

if __name__ == '__main__':

    app = Dash(__name__)
    layout_list = []

    try:
        file_path = 'data/'
        with open(file_path + 'messorte.json', 'r') as data:
            module_proj1 = GUIProj1V2(app, json.load(data), file_path, 365)
            app = module_proj1.get_app()
            layout_list.append(module_proj1.get_layout())
    except FileNotFoundError as e:
        print(f"Error: {e}")
        layout_list.append(html.Div([
            html.Div(style={'height': '10px'}),
            html.Hr(style={'width': '100%', 'display': 'inline-block'}),
            html.H1('Modul proj1 not found', style={'text-align': 'center', 'font-size': '32px'}),
            html.Div(style={'height': '10px'})
        ]))

    app.layout = layout_list
    app.run(debug=True, host='127.0.0.1', port=5002)
