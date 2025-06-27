# 📊  High Performance Analytics Dashboard - Plotly Dash App mit Polars, Redis & Sphinx

Dieses Repository enthält eine interaktive [Plotly Dash](https://dash.plotly.com/) Webanwendung, die große Datensätze performant mit [Polars](https://www.pola.rs/) verarbeitet. Auch [Redis](https://redis.io/) kann für Caching der Messwerte im RAM genutzt werden. Für die technische Dokumentation kommt [Sphinx](https://www.sphinx-doc.org/) zum Einsatz.

---

## 🚀 Features

✅ Interaktives Dashboard mit Plotly Dash

✅ Hochperformante Datenaggregation mit Polars

✅ Beispiel ***proj1_v2*** (GUI) mit Datumsfilterung

✅ Redis als Cache-Layer für schnelle Antworten mittels Docker

✅ Performance-Tests: CSV, Parquet, Polars und Pyarrow

✅ Sphinx für technische Dokumentation

✅ gut skalierbar für Datenmengen bis 100.000

✅ Leicht anzupassen

---

## ⚙️ Installation Redis mittels Docker

- Pfad: ***plotly\proj1\parsing_tests\redis***

```yaml
services:
  redis:
    image: redis:latest
    container_name: redis
    restart: always
    volumes:
      - redis_volume_data:/data
    ports:
      - "6379:6379"
  redis-insight:
    image: redis/redisinsight:latest
    restart: always
    ports:
      - "5540:5540"
    volumes:
      - redis-insight:/data

volumes:
  redis_volume_data:
  redis-insight:
 ```

## 🖥️ Hauptanwendung starten

```bash
cd plotly/

python3 main.py

# Die App ist dann unter http://127.0.0.1:5555 erreichbar.
```

### Einzelanwendung app_v1 starten

```bash
cd plotly/proj1/

python3 app_v1.py

# Die App ist dann unter http://127.0.0.1:5001 erreichbar.
```

### Einzelanwendung app_v2 starten

```bash
cd plotly/proj1/

python3 app_v2.py

# Die App ist dann unter http://127.0.0.1:5002 erreichbar.
```
