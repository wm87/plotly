from datetime import datetime
import pandas as pd
import redis

r = redis.Redis(host='localhost', port=6379, db='0')
response = r.ping()

# start timer
startzeit = datetime.now()

# Schlüssel für die gesuchte CSV-Datei
key_prefix = '001'

# Alle Schlüssel abrufen, die mit dem Dateinamen beginnen
keys = r.keys(f'{key_prefix}')

# Jeden Stream in eine Liste von Werten umwandeln
values = []
for key in keys:
    # Jeden Wert in Byte-String umwandeln
    # print(key)
    entries = r.xrange(key, count=3000)  # Angenommen, es gibt 3000 Einträge pro Stream
    for entry in entries:
        id, fields = entry
        x_value = fields[b'x'].decode('utf-8')
        y_value = fields[b'y'].decode('utf-8')
        values.append([x_value, y_value])

# Die Werte in einem DataFrame speichern
df = pd.DataFrame(values, columns=['x', 'y'])
# print(df)

# stop timer
endzeit = datetime.now()
laufzeit_ms = (endzeit - startzeit).total_seconds() * 1000
print(f"{laufzeit_ms:.1f} ms")
