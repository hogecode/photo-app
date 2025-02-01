from io import BytesIO
from typing import Tuple, List
from fastapi import UploadFile
from cloudinary.uploader import upload
import cloudinary
from app.models import Photo
from tortoise.exceptions import DoesNotExist


async def validate_and_upload_image(
    file_content: bytes, user_id: int, file_name: str
) -> Tuple[str, str]:
    """画像をCloudinaryにアップロードし、画像URLを取得する"""

    if not file_content:
        raise ValueError(
            "ファイルが空です。正しい画像ファイルをアップロードしてください。"
        )

    try:
        # Cloudinaryに画像をアップロード
        result = upload(
            BytesIO(file_content),
            folder="uploads",
            resource_type="image",
            public_id=f"{user_id}/{file_name}"
        )

        # Cloudinaryから画像URLを取得
        image_url = result.get("url")
        if not image_url:
            raise ValueError("Cloudinaryから画像URLが取得できませんでした。")

        return (
            image_url,
            file_name
        )  

    except cloudinary.exceptions.Error as e:
        raise Exception(f"Cloudinaryのエラー: {str(e)}")


async def save_image_to_db(user_id: int, image_url: str, title: str):
    """画像情報をデータベースに保存"""
    try:
        # Photo テーブルにレコードを挿入
        photo = await Photo.create(
            user_id=user_id,
            url=image_url,
            title=title,
        )
        return photo
    except Exception as e:
        raise Exception(f"データベースへの保存中にエラーが発生しました: {str(e)}")
    

async def get_user_photos(user_id: int) -> List[Photo]:
    """指定したユーザーIDに関連する画像一覧を取得"""
    try:
        # user_id でフィルタリングし、関連する画像を全て取得
        photos = await Photo.filter(user_id=user_id, is_deleted=False).all()
        return photos
    except Exception as e:
        raise Exception(f"データベースエラー: {str(e)}")


async def replace_photo(photo_id: int, user_id: int, file: UploadFile) -> str:
    """画像の置き換え処理"""
    try:
        # 既存の画像を取得
        photo = await Photo.get(id=photo_id, user_id=user_id, is_deleted=False)

        # 新しい画像を読み込む
        file_content = await file.read()

        if not file_content:
            raise ValueError("ファイルが空です。正しい画像ファイルをアップロードしてください。")

        # Cloudinaryに新しい画像をアップロード
        result = cloudinary.uploader.upload(
            BytesIO(file_content),
            folder="uploads",
            resource_type="image",
        )

        # 新しい画像のURL
        new_image_url = result.get("url")
        if not new_image_url:
            raise ValueError("Cloudinaryから画像URLが取得できませんでした。")

        # 既存の画像のURLを更新
        photo.url = new_image_url
        photo.updated_at = "CURRENT_TIMESTAMP"  # 更新日時の設定
        await photo.save()

        # 新しい画像のURLを返す
        return new_image_url
    except DoesNotExist:
        raise ValueError("指定された画像が見つかりません。")
    except Exception as e:
        raise ValueError(f"エラーが発生しました: {str(e)}")
    

async def soft_delete_photo(photo_id: int, user_id: int) -> bool:
    """論理削除（is_deleted=True）"""
    try:
        photo = await Photo.get(id=photo_id, user_id=user_id, is_deleted=False)
        photo.is_deleted = True
        await photo.save()
        return True
    except DoesNotExist:
        return False
    

async def hard_delete_photo(photo_id: int, user_id: int) -> bool:
    """物理削除（完全に削除）"""
    try:
        photo = await Photo.get(id=photo_id, user_id=user_id, is_deleted=False)
        await photo.delete()
        return True
    except DoesNotExist:
        return False