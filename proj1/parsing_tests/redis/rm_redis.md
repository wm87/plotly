# **How to start Redis?**

```bash
# stop container
docker-compose -f .\redis-docker-compose.yml down
```

```bash
# build and start container
docker-compose -f .\redis-docker-compose.yml up --build
```

```python
# load csv data to redis
python3 redis_load.py
```

```python
# run dash-app
python3 dash_app.py
```