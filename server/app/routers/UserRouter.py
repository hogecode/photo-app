# ToDo: 空のボディーを受け取り、get_userでDBに保存するエンドポイント
# /registerのみでいい
# /login、/logoutはフロントエンドで実装

from fastapi import APIRouter, Depends, HTTPException, status
from app.services.UserService import (
  oauth2_scheme, delete_user, get_user, create_user_from_firebase_token)

router = APIRouter(
    prefix="/api/user",  # URLパスのプリフィックス
    tags=["User"]    # Swagger UIでのタグ
)


@router.post("/register")
async def register_user(token: str = Depends(oauth2_scheme)):
    """
    FirebaseのIDトークンを使ってユーザーを登録するエンドポイント
    - token: Authorization ヘッダーから受け取るFirebase IDトークン
    """
    # Firebaseトークンを検証してユーザー情報を取得
    # Memo: 本番環境ではuser.idは返さない
    try:
        user = await create_user_from_firebase_token(token)
        return {"message": "User registered successfully", "user_id": user.id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ToDo: セキュリティ面を見直す
@router.delete("/")
async def remove_user(user: str = Depends(get_user)):
    """
    ログイン中のユーザーを削除するエンドポイント
    - ユーザーIDはトークンから取得され、ログイン中のユーザーが削除されます
    """
    try:
        # ユーザー削除
        await delete_user(user_id=int(user))
        return {"message": "ユーザーが正常に削除されました。"}
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"エラーが発生しました: {str(e)}"
        )
