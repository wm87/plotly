import timeit

import pandas as pd
import pyarrow as pa
import pyarrow.csv as pv

# Options to skip the first three rows and change the delimiter
read_options = pv.ReadOptions(skip_rows=3, column_names=['x', 'y'])  # Manually specify column names
parse_options = pv.ParseOptions(delimiter=';')  # Change the delimiter to semicolon
convert_options = pv.ConvertOptions(column_types={'x': pa.timestamp('ms', tz='UTC'), 'y': pa.float32()})

# Read the CSV file with pandas
df = pd.read_csv('../data/001.csv', delimiter=';', skiprows=3, names=['x', 'y'])

# Save the preprocessed CSV file
df.to_csv('001_preprocessed.csv', index=False, sep=';')

# start timer
startzeit = timeit.default_timer()

# Now read the preprocessed CSV file with PyArrow
df = pv.read_csv('001_preprocessed.csv',
                 read_options=read_options,
                 parse_options=parse_options,
                 convert_options=convert_options)

# print(table.schema)
print(df)

# stop timer
endzeit = timeit.default_timer()
laufzeit_ms = (endzeit - startzeit) * 1000
print(f"{laufzeit_ms:.1f} ms")
