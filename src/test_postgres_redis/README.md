* .envを作成し下記を記載する
```
POSTGRES_VERSION=16.2
CONTAINER_NAME=pgsql_db # お好きに
HOSTNAME=pgsql-db # お好きに
USER_NAME=postgres
USER_PASS=postgres
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