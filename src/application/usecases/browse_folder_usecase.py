from typing import Dict, List

from domain.entities.folder import Folder
from domain.entities.image import Image
from domain.repositories.folder_repository import FolderRepository
from domain.repositories.image_repository import ImageRepository

class BrowseFolderUseCase:
    """フォルダ内の画像を閲覧するユースケース"""
    
    def __init__(self, folder_repository: FolderRepository,
                image_repository: ImageRepository):
        self.folder_repository = folder_repository
        self.image_repository = image_repository
    
    def execute(self, folder_path: str, page: int = 0, 
               page_size: int = 100) -> Dict:
        """フォルダ内の画像とサブフォルダを取得する"""
        folder = self.folder_repository.get_by_path(folder_path)
        if not folder:
            raise ValueError(f"Folder not found: {folder_path}")
        
        subfolders = self.folder_repository.get_subfolders(folder.id)
        images = self.image_repository.get_images_in_folder(
            folder_path, page, page_size
        )
        
        return {
            "folder": folder,
            "subfolders": subfolders,
            "images": images,
            "page": page,
            "page_size": page_size,
            "total_images": len(images)  # 本来は総数をリポジトリから取得
        }
