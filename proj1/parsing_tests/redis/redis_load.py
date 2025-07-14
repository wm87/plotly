# save_to_redis_zset.py

import csv
import os
import redis
from datetime import datetime

r = redis.Redis(host='localhost', port=6379, db=0)
r.flushdb()

csv_dir = '../../data/'

def parse_and_store_zset(filename):
    with open(filename, encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        metadata = {}
        records = []

        for row in reader:
            if row[0].startswith('#'):
                key, value = row[0][1:], row[1]
                metadata[key] = value
            else:
                timestamp_str, val_str = row
                dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                ts_unix = dt.timestamp()
                records.append((ts_unix, val_str))

        file_id = metadata.get('id', os.path.basename(filename))
        redis_key = f"zset:{file_id}"

        # Store as Redis Sorted Set
        for score, value in records:
            r.zadd(redis_key, {value: score})

        print(f"✅ Gespeichert: {redis_key} mit {len(records)} Einträgen")

def load_all():
    for file in os.listdir(csv_dir):
        if file.endswith('.csv'):
            parse_and_store_zset(os.path.join(csv_dir, file))

if __name__ == '__main__':
    load_all()
