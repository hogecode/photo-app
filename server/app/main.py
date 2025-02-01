# Refactor:そのうち設定をconfig.pyに移す

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
import cloudinary
from app.routers.ImageRouter import router as ImageRouter
from app.routers.UserRouter import router as UserRouter
from app.db import init_db, close_db
from app.models import User
from app.types import UserListResponse, UserBase  # 型定義のインポート
from tortoise.exceptions import DoesNotExist
import firebase_admin
from firebase_admin import credentials
from fastapi.openapi.models import SecuritySchemeType

# .env ファイルを読み込む
load_dotenv()

# 本番環境では以下のように設定
# heroku config:set
# GOOGLE_APPLICATION_CREDENTIALS="$(cat path/to/firebase.json)"
# heroku config:get GOOGLE_APPLICATION_CREDENTIALS
# 以下は本番環境でも同じ

# 環境変数から認証情報のパスを取得
cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

if cred_path:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)
else:
    print("認証情報のパスが設定されていません。")


# FastAPI アプリケーションの作成
app = FastAPI(
    title="Photo App",  # アプリケーション名
    description="Hello, hello",  # アプリケーションの説明
)

# CORS の設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では変える
    allow_credentials=True,
    allow_methods=["*"],  # 全ての HTTP メソッドを許可
    allow_headers=["*"],  # 全ての HTTP ヘッダーを許可
)


@app.get("/openapi.json")
async def custom_openapi():
    openapi_schema = app.openapi()

    # セキュリティスキームをBearerトークンに設定
    openapi_schema["components"]["securitySchemes"]["BearerAuth"] = {
        "type": SecuritySchemeType.HTTP,
        "scheme": "bearer",
        "bearerFormat": "JWT"  # ここでJWTを指定する
    }

    # API全体でBearerAuthを適用
    openapi_schema["security"] = [{"BearerAuth": []}]

    return openapi_schema


cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True,
)


# アプリケーションの起動時にデータベース接続を初期化
@app.on_event("startup")
async def startup():
    # データベースの初期化
    await init_db()


# アプリケーションの終了時にデータベース接続を閉じる
@app.on_event("shutdown")
async def shutdown():
    # データベースの接続を閉じる
    await close_db()


# ルーター一括インポート
app.include_router(ImageRouter)
app.include_router(UserRouter)


# サンプルエンドポイント
@app.get("/", response_model=dict)
async def root():
    return {"message": "Hello World"}


# サンプルエンドポイント
# ユーザー情報を全て取得するエンドポイント
@app.get("/users", response_model=UserListResponse)
async def get_users():
    # ユーザー全件取得
    try:
        users = await User.all()
        return UserListResponse(
            users=[UserBase.from_orm(user) for user in users])
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="No users found")