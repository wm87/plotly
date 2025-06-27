from datetime import datetime
import pandas as pd
import redis

r = redis.Redis(host='localhost', port=6379, db='0')
r.ping()

# start timer
startzeit = datetime.now()

# Schlüssel für die gesuchte CSV-Datei
key_prefix = '001'

# Lesen Sie alle Werte für diesen Schlüssel
values = r.lrange(key_prefix, 0, -1)

# Konvertieren Sie die Werte zurück in Listen
values_as_lists = [value.decode('utf-8').split(',') for value in values]

# Erstellen Sie ein DataFrame aus den Listen
df = pd.DataFrame(values_as_lists, columns=['x', 'y'])
# print(df)

# stop timer
endzeit = datetime.now()
laufzeit_ms = (endzeit - startzeit).total_seconds() * 1000
print(f"{laufzeit_ms:.1f} ms")
