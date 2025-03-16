from datetime import datetime

class ImageClassification:
    """画像の分類結果を表すエンティティ"""
    
    def __init__(self, id: str, image_id: str, is_nsfw: bool, 
                 nsfw_score: float, classification_method: str,
                 classified_at: datetime):
        self.id = id                          # 一意のID
        self.image_id = image_id              # 画像ID
        self.is_nsfw = is_nsfw                # NSFWフラグ
        self.nsfw_score = nsfw_score          # NSFWスコア (0-1)
        self.classification_method = classification_method  # 分類手法
        self.classified_at = classified_at    # 分類日時
