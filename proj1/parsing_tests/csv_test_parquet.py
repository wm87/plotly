import timeit
from pathlib import Path

import pandas as pd


# CSV-Datei einlesen
csvFile = Path('100000.csv')

# CSV-Datei in ein DataFrame einlesen
df = pd.read_csv(csvFile)

# DataFrame in eine Parquet-Datei schreiben
df.to_parquet('100000.parquet')


# start timer
startzeit = timeit.default_timer()
# Parquet-Datei in ein DataFrame einlesen
df_new = pd.read_parquet('100000.parquet')
print(df_new)

# stop timer
endzeit = timeit.default_timer()
laufzeit_ms = (endzeit - startzeit) * 1000
print(f"{laufzeit_ms:.1f} ms")
