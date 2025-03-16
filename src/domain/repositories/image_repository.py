from abc import ABC, abstractmethod
from typing import List, Optional

from domain.entities.image import Image

class ImageRepository(ABC):
    """画像エンティティのリポジトリインターフェース"""
    
    @abstractmethod
    def get_by_id(self, image_id: str) -> Optional[Image]:
        """IDで画像を取得する"""
        pass
    
    @abstractmethod
    def get_by_path(self, path: str) -> Optional[Image]:
        """パスで画像を取得する"""
        pass
    
    @abstractmethod
    def get_images_in_folder(self, folder_path: str, 
                            page: int = 0, page_size: int = 100) -> List[Image]:
        """フォルダ内の画像を取得する"""
        pass
    
    @abstractmethod
    def save(self, image: Image) -> Image:
        """画像を保存する"""
        pass
    
    @abstractmethod
    def delete(self, image_id: str) -> bool:
        """画像を削除する"""
        pass
    
    @abstractmethod
    def search(self, query: str) -> List[Image]:
        """画像を検索する"""
        pass
