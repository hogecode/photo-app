# app/models.py

from tortoise import fields
from tortoise.models import Model


class ConfigModel(Model):
    class Meta:
        abstract = True  # 抽象基底クラスにする


class User(Model):
    uid = fields.CharField(max_length=255, unique=True)  # Firebase UID
    email = fields.CharField(max_length=255, unique=True)
    email_verified = fields.BooleanField()
    sign_in_provider = fields.CharField(max_length=255, null=True)  
    upload_count = fields.IntField(default=0)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "user"


class Photo(Model):
    user = fields.ForeignKeyField("models.User", related_name="photos")
    url = fields.CharField(max_length=255)
    title = fields.CharField(max_length=255)
    is_deleted = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True) 

    class Meta:
        table = "photo"


class Album(ConfigModel):
    user = fields.ForeignKeyField("models.User", related_name="albums")
    name = fields.CharField(max_length=255)
    title = fields.CharField(max_length=255)
    description = fields.TextField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "album"


class AlbumPhoto(ConfigModel):
    album = fields.ForeignKeyField("models.Album", related_name="album_photos")
    photo = fields.ForeignKeyField("models.Photo", related_name="album_photos")
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "album_photo"
