import csv
import glob
import os
import redis

# r = redis.Redis(host='localhost', port=6379, db=1, password='mysecretpw')
r = redis.Redis(host='localhost', port=6379, db='0')
response = r.ping()

r.flushdb()

file_path = '../data/'

# Durchlaufen Sie das Unterverzeichnis und listen Sie alle CSV-Dateien auf
for dateipfad in glob.glob(os.path.join(file_path, '*.csv')):
    dateiname = os.path.basename(dateipfad)  # Holt den Dateinamen mit Endung
    dateiname_ohne_endung = os.path.splitext(dateiname)[0]  # Entfernt die Endung
    print(f'{dateiname_ohne_endung}')
    with open(dateipfad, 'r') as f:
        reader = csv.reader(f)
        # Überspringen Sie die erste Zeile (Kopfzeile)
        next(reader)
        # Den Dateinamen (ohne die Erweiterung) als Präfix für die Schlüssel verwenden
        key_prefix = dateiname_ohne_endung
        # Lesen Sie alle Zeilen in eine Liste und speichern Sie die Liste in Redis
        all_rows = list(reader)
        # Konvertieren Sie jede Zeile in einen String, bevor Sie sie in Redis speichern
        all_rows_as_strings = [','.join(row) for row in all_rows]
        r.rpush(f'{key_prefix}', *all_rows_as_strings)