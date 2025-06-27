

# Sphinx-Doc Anleitung für Python

## Schritt 1: Installation

Installieren Sie Sphinx mit pip:

```bash
pip install sphinx
```

## Schritt 2: Projekt erstellen

Erstellen Sie ein neues Sphinx-Projekt mit dem Befehl `sphinx-quickstart` in Ihrem Projektverzeichnis. Folgen Sie den Anweisungen im Terminal.

```bash
# auf Root-Eben wechseln
mkdir -p docs
cd docs
sphinx-quickstart
```

## Schritt 3: Projekt konfigurieren

### Sphinx index.rst Anpassungen
```rst
Welcome to Dummy-Project's documentation!
===============================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules
```

### Sphinx conf.py Anpassungen

```python
import os
import sys

sys.path.insert(0, os.path.abspath(''))

project = 'proj1'
copyright = '2025, Institution XY'
author = 'mwf102'
version = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx.ext.todo", "sphinx.ext.viewcode", "sphinx.ext.autodoc"]

html_theme = 'sphinx_rtd_theme'
```

## Schritt 4: Dokumentation schreiben

Schreiben Sie Ihre Dokumentation in reStructuredText (.rst) Dateien. Sie können diese Dateien in Ihrem Projektverzeichnis unter `/docs/source` finden. Die `index.rst` Datei ist die Hauptseite Ihrer Dokumentation.

```bash
# auf Root-Ebene wechseln, nicht noch docs/
sphinx-apidoc -o docs/ .
```


## Schritt 5: Dokumentation erstellen

Erstellen Sie die Dokumentation mit dem Befehl `make html` im `/docs` Verzeichnis. Die erstellte Dokumentation finden Sie im `/docs/build/html` Verzeichnis.

```bash
cd docs/

.\make.bat html

cd build/html
```

Öffnen Sie die `index.html` Datei in einem Webbrowser, um Ihre Dokumentation anzusehen.

## Dokumentation ansehen

[Doc Proj1](docs/_build/html/index.html)

