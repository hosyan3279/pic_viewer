from typing import Dict, Optional

from domain.entities.image import Image
from domain.repositories.image_repository import ImageRepository

class ViewImageUseCase:
    """画像を表示するユースケース"""
    
    def __init__(self, image_repository: ImageRepository):
        self.image_repository = image_repository
    
    def execute(self, image_id: str) -> Dict:
        """画像を表示するために必要な情報を取得する"""
        image = self.image_repository.get_by_id(image_id)
        if not image:
            raise ValueError(f"Image not found: {image_id}")
        
        return {
            "image": image
        }
    
    def execute_by_path(self, image_path: str) -> Dict:
        """パスから画像を表示するために必要な情報を取得する"""
        image = self.image_repository.get_by_path(image_path)
        if not image:
            raise ValueError(f"Image not found: {image_path}")
        
        return {
            "image": image
        }
