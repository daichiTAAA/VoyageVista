* .envを作成し下記を記載する
```
PG_VERSION=16.2
PG_CONTAINER_NAME=pgsql_db # お好きに
PG_HOST=pgsql-db # お好きに
PG_PASSWORD=postgres
USER_PASS=postgres

REDIS_PASSWORD=my_redis_password
```

* volumeを作成する
```bash
docker volume create db_vol
```

* docker composeでPostgreSQLを起動する
```bash
cd src/test_postgres_redis
docker compose up
```

* test_postgres.pyを実行する
```bash
python test_postgres.py
```

* PostgreSQLコンテナを終了する
```bash
cd src/test_postgres_redis
docker compose down
```