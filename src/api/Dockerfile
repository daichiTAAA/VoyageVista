# 使用するベースイメージ
FROM python:3.10-slim

# 作業ディレクトリの設定
WORKDIR /app

# Poetryをインストール
ENV POETRY_VERSION=1.8.2
RUN pip install "poetry==$POETRY_VERSION"

# プロジェクトの設定ファイルをコピー
COPY pyproject.toml poetry.lock* /app/

# Poetry設定: 仮想環境をシステムのPython環境内に作成しないようにする
ENV POETRY_VIRTUALENVS_CREATE=false

# 依存関係のインストール
RUN poetry install --no-dev --no-interaction --no-ansi

# アプリケーションのコードをコピー
COPY . /app

# コマンドの実行
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]
