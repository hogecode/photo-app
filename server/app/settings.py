# Memo: settings → db → modelの順でファイルを読む

import os

# データベース設定（開発用、テスト用、本番用など）
# Memo: 本番環境ではPostgreSQLの設定情報を環境変数で設定
DATABASES = {
    "development": {
        "url": "sqlite://dev.db",  # SQLiteのURL形式
    },
    "production": {
        "url": "postgres://db_user:db_password@localhost:5432/dev_db",
    },
}

# 現在の環境（開発、テスト、本番など）
CURRENT_ENV = os.getenv("APP_ENV", "development")  # 環境変数で切り替える
