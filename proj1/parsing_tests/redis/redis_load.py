import csv
import os
import redis

# Redis-Verbindung
r = redis.Redis(host='localhost', port=6379, db=0)

# Optional: Verbindung prüfen
if r.ping():
    print("✅ Redis Verbindung erfolgreich")

# Optional: DB leeren
r.flushdb()

# Pfad zu CSV-Dateien
csv_dir = '../../data/'


def parse_csv_and_store(filename):
    with open(filename, encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        metadata = {}
        data = {}

        for row in reader:
            if row[0].startswith('#'):
                key, value = row[0][1:], row[1]
                metadata[key] = value
            else:
                timestamp, val = row
                data[timestamp] = val

        file_id = metadata.get('id', os.path.basename(filename))
        redis_key = f"timeseries:{file_id}"

        # Redis Hash speichern
        if data:
            r.hset(redis_key, mapping=data)
            print(f"📦 Gespeichert: {redis_key} mit {len(data)} Einträgen")


def load_all():
    for file in os.listdir(csv_dir):
        if file.endswith('.csv'):
            full_path = os.path.join(csv_dir, file)
            parse_csv_and_store(full_path)


if __name__ == '__main__':
    load_all()
