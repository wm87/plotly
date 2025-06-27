import time

import pandas as pd
import redis

r = redis.Redis(host='localhost', port=6379, db='0')
r.ping()

# start timer
tic = time.perf_counter()

# Schlüssel für die gesuchte CSV-Datei
key_prefix = '001'

# Alle Schlüssel abrufen, die mit dem Dateinamen beginnen
keys = r.keys(f'{key_prefix}:*')

# Jeden Hash in eine Liste von Werten umwandeln
values = [r.hgetall(key) for key in keys]

# Die Werte in einem DataFrame speichern
df = pd.DataFrame(values)
# print(df)

# stop timer
toc = time.perf_counter()
print(f"\nDownloaded all timeseries in {toc - tic:0.2f} seconds")