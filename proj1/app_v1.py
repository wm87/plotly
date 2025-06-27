import json

from dash import Dash

from gui.proj1_v1 import GUIProj1V1

if __name__ == '__main__':

    app = Dash(__name__)
    layout_list = []

    try:
        file_path = 'data/'
        with open(file_path + 'messorte.json', 'r') as data:
            module_proj1 = GUIProj1V1(app, json.load(data), file_path)
    except FileNotFoundError as e:
        print(f"Error: {e}")

    app.layout = module_proj1.get_layout()
    app.run(debug=True, host='127.0.0.1', port=5001)
