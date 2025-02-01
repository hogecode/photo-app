from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


# UserのPydanticモデル
class UserBase(BaseModel):
    uid: str  # Firebase UID
    email: str
    email_verified: bool
    sign_in_provider: Optional[str] = None
    upload_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True  # Tortoise ORM と連携するために必要
        from_attributes = True  # Tortoise ORMとの変換に必要


# PhotoのPydanticモデル
class PhotoBase(BaseModel):
    user: int  # 外部キーが参照するユーザーのID
    url: str
    title: str
    is_deleted: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True  # Tortoise ORMとの変換に必要


# Memo: 多分間違っている
class PhotoResponse(BaseModel):
    id: int
    url: str
    title: str

    class Config:
        orm_mode = True


class PhotosResponse(BaseModel):
    photos: List[PhotoResponse]


# AlbumのPydanticモデル
class AlbumBase(BaseModel):
    user_id: int
    name: str
    title: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True


# AlbumPhotoのPydanticモデル
class AlbumPhotoBase(BaseModel):
    album_id: int
    photo_id: int
    created_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True


# Userのリストを返すためのPydanticモデル
class UserListResponse(BaseModel):
    users: List[UserBase]