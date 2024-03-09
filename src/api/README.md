# 実行手順
* api/.envファイルを作成する
    ```
    PG_VERSION=16.2
    PG_CONTAINER_NAME=pgsql_db
    PG_HOST=pgsql-db
    PG_USER=postgres
    PG_PASSWORD=postgres
    PG_DATABASE=japan_tourism_info

    SECRET_KEY = "your-secret-key"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    ```

* volumeを作成する
    ```bash
    docker volume create db_vol
    ```

* docker composeで実行する
    ```bash
    cd src/api
    docker compose up --build
    ```
* Swagger UIの確認
  * 下記のURLでSwagger UIを使用したAPIリファレンスの確認やテスト実行が可能。
    * http://localhost:8000/docs


# Dockerコマンドを使用した初期設定・CLI実行方法
1. **コンテナIDを確認する**
    ```bash
    docker ps
    ```

2. **Databaseを作成する**
    ```bash
    docker exec -it {コンテナID} bash
    psql -U {PostgreSQLユーザー名}
    ```

3. **Database一覧を表示する**
   ```sql
   \l
   ```

4. **Databaseを選択する**
   ```sql
   \c データベース名
   ```

5. **現在選択しているデータベースを表示**
   ```sql
   SELECT current_database();
   ```

6. **現在選択しているデータベースのテーブル一覧を表示**
   ```sql
   \dt
   ```

7. **`users`テーブルを確認**：
   PostgreSQLのプロンプトが表示されたら、以下のコマンドを使用して`users`テーブルの構造を確認できます。
   ```sql
   \d users
   ```
   または、`users`テーブルの内容を表示するには、以下のSQLクエリを実行します。
   ```sql
   SELECT * FROM users;
   ```

8. **`users`テーブルから行を削除する方法**
   ```sql
   DELETE FROM users WHERE id = 10;
   ```

9. **終了する**
   ```sql
   \q
   exit
   ```

# テーブルをマイグレーションする
1. SERVICE名を確認する
    ```bash
    cd src/api
    docker compose ps
    ```
2. migrate_dbスクリプトを実行する
    ```bash
    cd src/api
    docker compose exec {SERVICE名} poetry run python -m migrate_db
    ```