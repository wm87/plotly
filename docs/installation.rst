======================
Installationsanleitung
======================

Voraussetzungen
===============

Um eine Dash-Anwendung zu erstellen, benötigen Sie Python und einige spezifische Python-Module. Die folgenden Anweisungen gehen davon aus, dass Sie bereits Python auf Ihrem System installiert haben.

Python-Module installieren
==========================

Die folgenden Python-Module werden für die Erstellung einer Dash-Anwendung benötigt:

- dash
- dash_core_components
- dash_html_components
- plotly

Sie können diese Module mit pip, dem Python-Paketmanager, installieren. Öffnen Sie ein Terminalfenster und geben Sie den folgenden Befehl ein:

.. code-block:: bash

   pip install dash dash-core-components dash-html-components plotly

Beispiel für eine Dash-Anwendung
================================

Nachdem Sie die erforderlichen Module installiert haben, können Sie eine einfache Dash-Anwendung erstellen. Hier ist ein einfaches Beispiel:

.. code-block:: python

   import dash
   import dash_core_components as dcc
   import dash_html_components as html

   app = dash.Dash(__name__)

   app.layout = html.Div(children=[
       html.H1(children='Hallo Dash'),

       html.Div(children='''
           Dash: Eine Webanwendungsfremawork für Python.
       '''),

       dcc.Graph(
           id='example-graph',
           figure={
               'data': [
                   {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                   {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': 'Montréal'},
               ],
               'layout': {
                   'title': 'Dash Data Visualization'
               }
           }
       )
   ])

   if __name__ == '__main__':
       app.run_server(debug=True)

Dieser Code erstellt eine einfache Dash-Anwendung mit einem Diagramm. Sie können den Code in eine Python-Datei einfügen und ausführen, um die Anwendung zu starten.
