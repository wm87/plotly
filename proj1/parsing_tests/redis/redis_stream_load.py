import csv
import glob
import os
import redis

# Verbindung zu Redis herstellen
r = redis.Redis(host='localhost', port=6379, db='0')
response = r.ping()

r.flushdb()

file_path = '../../data/'

# Durchlaufen Sie das Unterverzeichnis und listen Sie alle CSV-Dateien auf
for dateipfad in glob.glob(os.path.join(file_path, '*.csv')):
    dateiname = os.path.basename(dateipfad)  # Holt den Dateinamen mit Endung
    dateiname_ohne_endung = os.path.splitext(dateiname)[0]  # Entfernt die Endung
    print(f'{dateiname_ohne_endung}')
    with open(dateipfad, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Überspringen Sie die Kopfzeile
        # Den Dateinamen (ohne die Erweiterung) als den Stream-Namen verwenden
        stream_name = dateiname_ohne_endung
        for i, row in enumerate(reader):
            r.xadd(stream_name, {'x': row[0], 'y': float(row[1])})
