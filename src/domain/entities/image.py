from datetime import datetime
from typing import Optional

class Image:
    """画像ファイルを表すエンティティ"""
    
    def __init__(self, id: str, path: str, filename: str, file_type: str, 
                 size: int, width: int, height: int, created_at: datetime,
                 modified_at: datetime):
        self.id = id                # 一意のID
        self.path = path            # ファイルパス
        self.filename = filename    # ファイル名
        self.file_type = file_type  # ファイル種別 (jpg, png, gif, mp4 etc.)
        self.size = size            # ファイルサイズ (bytes)
        self.width = width          # 画像の幅
        self.height = height        # 画像の高さ
        self.created_at = created_at        # 作成日時
        self.modified_at = modified_at      # 最終更新日時
    
    @property
    def is_video(self) -> bool:
        """ファイルが動画かどうかを判定する"""
        return self.file_type.lower() == 'mp4'
    
    @property
    def aspect_ratio(self) -> float:
        """アスペクト比を計算する"""
        if self.height == 0:
            return 0
        return self.width / self.height
