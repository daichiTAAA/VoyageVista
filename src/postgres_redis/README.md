* postgres_redisフォルダに.envファイルを作成し下記を記載する
.env
```
PG_VERSION=16.2
PG_CONTAINER_NAME=pgsql_db # お好きに
PG_HOST=pgsql-db # お好きに
PG_USER=postgres
PG_PASSWORD=postgres

REDIS_PASSWORD=my_redis_password
```

* volumeを作成する
```bash
docker volume create db_vol
docker volume create redis_vol
```

* docker composeでPostgreSQLとRedisを起動する
```bash
cd src/postgres_redis
docker compose up
```

* docker composeでPostgreSQLとRedisを終了する
```bash
cd src/postgres_redis
docker compose down
```