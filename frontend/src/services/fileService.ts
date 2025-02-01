//ToDo: prismaのユーザーテーブルにファイル数を追加
//ToDo: exportする、スナックメッセージを表示

import { useFetch } from "@/hooks/useFetch";
import { showImageUpdatedMessage, showImageUploadedFailedMessage, showImageUploadedMessage } from "./message";

// 画像ファイルの検証条件
// Memo: この設定は見直す
const MAX_FILE_SIZE = 8 * 1024 * 1024; // 5MB
const ALLOWED_FILE_TYPES = ['image/jpeg', 'image/png', 'image/gif', 'image/svg+xml'];

export async function uploadFiles(files: File | File[]): Promise<void> {
    // 配列に変換（単一のファイルも配列として扱えるように）
    const fileArray = Array.isArray(files) ? files : [files];

    // 画像ファイルを最大3枚まで処理
    if (fileArray.length > 3) {
        throw new Error('最大で3つの画像ファイルしかアップロードできません');
    }

    // 各ファイルの検証
    const validFiles = fileArray.filter(file => validateFile(file));

    if (validFiles.length === 0) {
        throw new Error('有効な画像ファイルがありません');
    }

    // アップロード処理
    try {
        await Promise.all(validFiles.map(file => uploadFile(file)));
        console.log('ファイルアップロード成功');
    } catch (error) {
        console.error('ファイルアップロードに失敗しました:', error);
        throw error;
        
    }
}

// ファイルの検証
function validateFile(file: File): boolean {
    // ファイルサイズをチェック
    if (file.size > MAX_FILE_SIZE) {
        console.error(`ファイルサイズが大きすぎます: ${file.name}`);
        return false;
    }

    // ファイルタイプをチェック
    if (!ALLOWED_FILE_TYPES.includes(file.type)) {
        console.error(`許可されていないファイル形式です: ${file.name}`);
        return false;
    }

    return true;
}


// ファイルをアップロード
export async function uploadFile(file: File): Promise<void> {
    const formData = new FormData();
    formData.append('file', file);

    try {
        // useFetchを利用してファイルアップロードを行う
        const response = await useFetch<any>('/api/images/upload', {
            method: 'POST',
            body: formData, // FormDataを直接bodyに渡す
        });

        console.log(`ファイルアップロード成功: ${file.name}`);
    } catch (error) {
        console.error(`アップロードエラー: ${error}`);
        throw error;
    }
}


// 画像のリストを取得する関数
export async function fetchImageList(): Promise<any> {
    try {
        // useFetchを利用して画像リストを取得
        const response = await useFetch<any>('/api/images', {
            method: 'GET',  // GETリクエスト
        });

        // 取得した画像リストをコンソールに出力
        console.log('画像リスト:', response);
        return response.photos;  // レスポンスを返す
    } catch (error) {
        console.error('画像リスト取得エラー:', error);
        throw error;
    }
}