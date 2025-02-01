
-- Memo: ORMのマイグレーションがなぜか出来ないので自分でSQL文を書く

-- ユーザー (User) テーブル
CREATE TABLE IF NOT EXISTS "user" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- 自動増分ID（データベース内部での一意ID）
    uid TEXT UNIQUE NOT NULL,               -- Firebase UID（ユーザーの一意識別子）
    email TEXT UNIQUE NOT NULL,             -- メールアドレス
    email_verified BOOLEAN NOT NULL,  -- メール確認フラグ
    sign_in_provider TEXT,                   -- サインインプロバイダ（ENUMで管理）
    upload_count INTEGER DEFAULT 0,         -- アップロード数
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP, -- アカウント作成日時
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP -- ユーザー情報の最終更新日時
);

-- 写真 (Photo) テーブル
CREATE TABLE IF NOT EXISTS "photo" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL, 
    url TEXT NOT NULL,
    title TEXT NOT NULL,
    is_deleted BOOLEAN DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES "user"(id) ON DELETE CASCADE
);

-- アルバム (Album) テーブル
CREATE TABLE IF NOT EXISTS "album" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES "user"(id) ON DELETE CASCADE
);

-- アルバム写真 (AlbumPhoto) テーブル (中間テーブル)
CREATE TABLE IF NOT EXISTS "album_photo" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    album_id INTEGER NOT NULL,
    photo_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(album_id) REFERENCES "album"(id) ON DELETE CASCADE,
    FOREIGN KEY(photo_id) REFERENCES "photo"(id) ON DELETE CASCADE,
    UNIQUE(album_id, photo_id)
);


-- 初期データ投入
INSERT INTO "user" (uid, email, email_verified, sign_in_provider, upload_count, created_at, updated_at)
VALUES 
('firebase_uid_1', 'user1@example.com', TRUE, 'google', 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('firebase_uid_2', 'user2@example.com', TRUE, 'facebook', 3, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('firebase_uid_3', 'user3@example.com', FALSE, 'twitter', 8, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('firebase_uid_4', 'user4@example.com', TRUE, 'github', 2, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT INTO "photo" (user_id, url, title, is_deleted, created_at, updated_at)
VALUES
(1, 'https://example.com/photo1.jpg', 'Vacation Photo 1', FALSE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(1, 'https://example.com/photo2.jpg', 'Vacation Photo 2', FALSE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(2, 'https://example.com/photo3.jpg', 'Holiday Photo', FALSE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(3, 'https://example.com/photo4.jpg', 'Nature Walk', FALSE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(4, 'https://example.com/photo5.jpg', 'Profile Picture', FALSE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
