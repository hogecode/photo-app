
from tortoise import Tortoise

# 環境ごとのデータベース設定を取得
from app.settings import DATABASES, CURRENT_ENV

# 現在の環境に応じたデータベースURLを取得
db_config = DATABASES[CURRENT_ENV]
DATABASE_URL = db_config['url']


# Tortoise ORMの初期化
async def init_db():
    await Tortoise.init(
        db_url=DATABASE_URL,  # データベースのURL
        modules={'models': ['app.models']}  # モデルのモジュールパス
    )
    await Tortoise.generate_schemas()  # スキーマの生成


# リクエストごとの接続開始
async def close_db():
    await Tortoise.close_connections()

