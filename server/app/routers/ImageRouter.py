# ToDo: POST/ GET/を実装
# GET/:id DELETE/id(論理削除) /DELETE/id(物理削除)はいい

from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, status
from fastapi.responses import JSONResponse
import cloudinary
import cloudinary.uploader
from app.services.UserService import get_user
from app.services.PhotoService import (
  validate_and_upload_image, save_image_to_db, replace_photo, get_user_photos,
  soft_delete_photo, hard_delete_photo)
from tortoise.exceptions import IntegrityError
from app.types import PhotosResponse

router = APIRouter(
    prefix="/api/images",  # URLパスのプリフィックス
    tags=["Images"]    # Swagger UIでのタグ
)


# ToDo: Depends(get_user)でユーザーIDとURLをDBに保存
# 画像のアップロードを処理する関数
@router.post("/upload")
async def upload_image(
    file: UploadFile = File(...), user_id: str = Depends(get_user)
):
    try:
        # ファイルの内容を読み込む
        file_content = await file.read()
        
        # ファイル名を取得
        file_name = file.filename
        print(file_name)
        
        # 画像をCloudinaryにアップロードし、画像URLを取得
        image_url, title = await validate_and_upload_image(
            file_content, user_id, file_name
            )

        # 画像の情報をデータベースに保存
        photo = await save_image_to_db(user_id, image_url, title)

        # 保存した画像のIDを取得
        photo_id = photo.id

        # 成功したレスポンスを返す
        return JSONResponse(content=
                            {"id": photo_id, "url": image_url, "title": title}, status_code=200)

    except ValueError as e:
        # 値エラーの場合のレスポンス
        return JSONResponse(content={"error": str(e)}, status_code=400)

    except cloudinary.exceptions.Error as e:
        # Cloudinaryのエラーの場合のレスポンス
        return JSONResponse(
            content={
                "error": f"Cloudinaryのエラー: {str(e)}"}, status_code=500)

    except IntegrityError as e:
        # データベースエラーの場合のレスポンス
        return JSONResponse(
            content={
                "error": f"データベースのエラー: {str(e)}"}, status_code=500)

    except Exception as e:
        # その他の予期しないエラー
        return JSONResponse(content={"error": f"予期しないエラーが発生しました: {str(e)}"}, 
        status_code=500)


@router.get("/", response_model=PhotosResponse)
async def get_user_photos_list(user_id: str = Depends(get_user)):
    """
    ユーザーの画像一覧を取得するエンドポイント
    - user_id: 認証されたユーザーのID
    """
    try:
        photos = await get_user_photos(user_id)  # ユーザーに関連する画像一覧を取得
        return {"photos": photos}
  
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"エラーが発生しました: {str(e)}")


@router.put("/{photo_id}")
async def replace_image(photo_id: int, file: UploadFile = File(...), 
                        user_id: str = Depends(get_user)):
    """
    画像を新しいファイルで置き換えるエンドポイント
    - photo_id: 置き換える画像のID
    """
    try:
        new_image_url = await replace_photo(photo_id, user_id, file)
        return {"message": "画像が正常に置き換えられました。", "url": new_image_url}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"予期しないエラーが発生しました: {str(e)}"
        )


@router.delete("/{photo_id}/delete/soft")
async def delete_photo(photo_id: int, user_id: str = Depends(get_user)):
    """
    画像を論理削除するエンドポイント
    - photo_id: 削除する画像のID
    """
    success = await soft_delete_photo(photo_id, user_id)
    
    if success:
        return {"message": "画像が論理削除されました。"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="画像が見つからないか、すでに削除されています。"
        )
 

@router.delete("/{photo_id}/delete/force/")
async def force_delete_photo(photo_id: int, user_id: str = Depends(get_user)):
    """
    画像を物理削除するエンドポイント
    - photo_id: 削除する画像のID
    """
    success = await hard_delete_photo(photo_id, user_id)
    
    if success:
        return {"message": "画像が物理削除されました。"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="画像が見つからないか、すでに削除されています。"
        )
