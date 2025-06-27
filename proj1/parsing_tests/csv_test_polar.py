import timeit
from pathlib import Path
import polars as pl

# start timer
startzeit = timeit.default_timer()

# CSV-Datei einlesen
csvFile = Path('2900.csv')
#csvFile = Path('34000.csv')
#csvFile = Path('100000.csv')
df = (pl.read_csv(csvFile,
                  separator=',',
                  skip_rows=3,
                  new_columns=['x', 'y'])
.with_columns([
    pl.col('x'),
    pl.col('y').cast(pl.Float32)
]))
print(df)

# stop timer
endzeit = timeit.default_timer()
laufzeit_ms = (endzeit - startzeit) * 1000
print(f"{laufzeit_ms:.1f} ms")
