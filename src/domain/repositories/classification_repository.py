from abc import ABC, abstractmethod
from typing import List, Optional

from domain.entities.image_classification import ImageClassification

class ClassificationRepository(ABC):
    """分類結果のリポジトリインターフェース"""
    
    @abstractmethod
    def get_by_image_id(self, image_id: str) -> Optional[ImageClassification]:
        """画像IDで分類結果を取得する"""
        pass
    
    @abstractmethod
    def save(self, classification: ImageClassification) -> ImageClassification:
        """分類結果を保存する"""
        pass
    
    @abstractmethod
    def get_nsfw_images(self, page: int = 0, page_size: int = 100) -> List[str]:
        """NSFW画像のIDリストを取得する"""
        pass
    
    @abstractmethod
    def get_sfw_images(self, page: int = 0, page_size: int = 100) -> List[str]:
        """健全画像のIDリストを取得する"""
        pass
