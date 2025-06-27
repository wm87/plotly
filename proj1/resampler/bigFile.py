import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Startdatum festlegen (vor 10 Jahren)
start = datetime.now() - timedelta(days=10*365)

# Erzeugen Sie eine Liste von Zeitstempeln für jede Minute der letzten 10 Jahre
timestamps = pd.date_range(start, periods=10*365*24*60, freq='min')

# Erzeugen Sie eine Sinuskurve für jeden Zeitstempel
# Hier verwenden wir die Zeitstempel als x-Werte für die Sinusfunktion.
# Sie können die Frequenz und Amplitude der Sinuskurve anpassen, indem Sie die Konstanten in der Funktion ändern.
values = np.sin(2 * np.pi * timestamps.to_series().dt.minute / 60)

# Erstellen Sie einen DataFrame
df = pd.DataFrame({'Datum': timestamps, 'Wert': values})

# Speichern Sie den DataFrame als CSV-Datei
df.to_csv('ts_sin.csv', index=False)
