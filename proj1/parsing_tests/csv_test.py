import timeit
from pathlib import Path
import pandas as pd

startzeit = timeit.default_timer()
# CSV-Datei einlesen

csvFile = Path('2900.csv')
#csvFile = Path('34000.csv')
#csvFile = Path('100000.csv')
#df = pd.read_csv(csvFile, skiprows=3, header=None, engine="pyarrow")
df = pd.read_csv(csvFile, skiprows=3, header=None, engine="c")
print(df)

endzeit = timeit.default_timer()
laufzeit_ms = (endzeit - startzeit) * 1000
print(f"{laufzeit_ms:.1f} ms")
