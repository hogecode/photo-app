# ToDo: ユーザー情報を取得してDBに保存する関数も追加

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from firebase_admin import auth
from app.models import User
from tortoise.exceptions import DoesNotExist


# OAuth2PasswordBearerでトークンを受け取る
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Firebase IDトークンを検証してfirebaseユーザー情報を取得する関数
async def get_firebase_user(token: str):
    try:
        # Firebaseでトークンを検証
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
   

# Firebase IDトークンを検証してDBのユーザーIDを返す関数
async def get_user(token: str = Depends(oauth2_scheme)) -> str:
    """
    Firebase Authenticationのトークンを検証し、認証ユーザーIDを取得
    Example:
    @router.get("/profile/")
    async def get_profile(user_id: str = Depends(get_user)):
        return {"user_id": user_id}
    """
    try:
        # Firebaseでトークンを検証
        decoded_token = auth.verify_id_token(token)
        firebase_uid = decoded_token['uid']  # FirebaseのユーザーID

        # Firebase UIDを使ってDBからユーザーを検索
        user = await User.filter(uid=firebase_uid).first()

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # ユーザーIDを返す（DBのID）
        return user.id

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )


async def create_user_from_firebase_token(token: str):
    # Firebase IDトークンを検証
    decoded_token = auth.verify_id_token(token)
    uid = decoded_token['uid']
    email = decoded_token['email']
    email_verified = decoded_token['email_verified']

    # ユーザー情報をデータベースに保存
    user = await User.create(
        uid=uid,
        email=email,
        email_verified=email_verified
    )

    return user


async def delete_user(user_id: int) -> None:
    """
    ユーザーを削除する処理
    - ユーザーが存在しない場合はエラーを返す
    """
    try:
        # ユーザーを取得
        user = await User.get(id=user_id)

        # ユーザーを削除
        await user.delete()

    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ユーザーが見つかりません。",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"予期しないエラーが発生しました: {str(e)}"
        )
