import os
import uuid
from datetime import datetime
from typing import Dict, List, Optional

from domain.entities.folder import Folder
from domain.entities.image import Image
from domain.entities.image_classification import ImageClassification
from domain.repositories.folder_repository import FolderRepository
from domain.repositories.image_repository import ImageRepository
from domain.repositories.classification_repository import ClassificationRepository
from infrastructure.file_io.file_system import FileSystemService

class InMemoryImageRepository(ImageRepository):
    """メモリ上の画像リポジトリ実装"""
    
    def __init__(self, file_system_service: FileSystemService):
        self.images: Dict[str, Image] = {}
        self.file_system_service = file_system_service
    
    def get_by_id(self, image_id: str) -> Optional[Image]:
        """IDで画像を取得する"""
        return self.images.get(image_id)
    
    def get_by_path(self, path: str) -> Optional[Image]:
        """パスで画像を取得する"""
        for image in self.images.values():
            if image.path == path:
                return image
        
        # 存在しない場合は作成する
        try:
            return self._create_image_from_path(path)
        except:
            return None
    
    def get_images_in_folder(self, folder_path: str, 
                            page: int = 0, page_size: int = 100) -> List[Image]:
        """フォルダ内の画像を取得する"""
        result = []
        
        # フォルダ内のファイルを取得
        try:
            items = self.file_system_service.list_directory(folder_path)
            
            for item in items:
                if not item["is_directory"] and self._is_supported_image(item["name"]):
                    # すでに存在するかチェック
                    image = self.get_by_path(item["path"])
                    if image:
                        result.append(image)
                    else:
                        # 存在しない場合は作成
                        try:
                            image = self._create_image_from_path(item["path"])
                            result.append(image)
                        except Exception as e:
                            print(f"Error creating image: {e}")
            
            # ページネーション
            start = page * page_size
            end = start + page_size
            
            return result[start:end]
        except Exception as e:
            print(f"Error getting images in folder: {e}")
            return []
    
    def save(self, image: Image) -> Image:
        """画像を保存する"""
        self.images[image.id] = image
        return image
    
    def delete(self, image_id: str) -> bool:
        """画像を削除する"""
        if image_id in self.images:
            del self.images[image_id]
            return True
        return False
    
    def search(self, query: str) -> List[Image]:
        """画像を検索する"""
        query = query.lower()
        result = []
        
        for image in self.images.values():
            if query in image.filename.lower():
                result.append(image)
        
        return result
    
    def _create_image_from_path(self, path: str) -> Image:
        """ファイルパスから画像エンティティを作成する"""
        metadata = self.file_system_service.get_image_metadata(path)
        
        file_name = os.path.basename(path)
        file_ext = os.path.splitext(file_name)[1].lower().lstrip('.')
        
        image = Image(
            id=str(uuid.uuid4()),
            path=path,
            filename=file_name,
            file_type=file_ext,
            size=metadata["size"],
            width=metadata["width"],
            height=metadata["height"],
            created_at=metadata.get("created", datetime.now()),
            modified_at=metadata.get("modified", datetime.now())
        )
        
        # 保存
        self.save(image)
        
        return image
    
    def _is_supported_image(self, filename: str) -> bool:
        """サポートされている画像ファイルかどうかを判定する"""
        ext = os.path.splitext(filename)[1].lower()
        return ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.mp4']


class InMemoryFolderRepository(FolderRepository):
    """メモリ上のフォルダリポジトリ実装"""
    
    def __init__(self):
        self.folders: Dict[str, Folder] = {}
    
    def get_by_id(self, folder_id: str) -> Optional[Folder]:
        """IDでフォルダを取得する"""
        return self.folders.get(folder_id)
    
    def get_by_path(self, path: str) -> Optional[Folder]:
        """パスでフォルダを取得する"""
        for folder in self.folders.values():
            if folder.path == path:
                return folder
        
        # 存在しない場合は作成する
        try:
            return self._create_folder_from_path(path)
        except:
            return None
    
    def get_subfolders(self, parent_id: str) -> List[Folder]:
        """親フォルダのサブフォルダを取得する"""
        return [folder for folder in self.folders.values() 
                if folder.parent_id == parent_id]
    
    def save(self, folder: Folder) -> Folder:
        """フォルダを保存する"""
        self.folders[folder.id] = folder
        return folder
    
    def _create_folder_from_path(self, path: str) -> Folder:
        """ファイルパスからフォルダエンティティを作成する"""
        if not os.path.isdir(path):
            raise ValueError(f"Not a directory: {path}")
        
        folder_name = os.path.basename(path)
        parent_path = os.path.dirname(path)
        
        # 親フォルダの取得または作成
        parent_id = None
        if parent_path and parent_path != path:  # ルートディレクトリでない場合
            parent = self.get_by_path(parent_path)
            if parent:
                parent_id = parent.id
        
        folder = Folder(
            id=str(uuid.uuid4()),
            path=path,
            name=folder_name,
            parent_id=parent_id
        )
        
        # 保存
        self.save(folder)
        
        return folder


class InMemoryClassificationRepository(ClassificationRepository):
    """メモリ上の分類結果リポジトリ実装"""
    
    def __init__(self):
        self.classifications: Dict[str, ImageClassification] = {}
        self.image_classifications: Dict[str, str] = {}  # image_id -> classification_id
    
    def get_by_image_id(self, image_id: str) -> Optional[ImageClassification]:
        """画像IDで分類結果を取得する"""
        classification_id = self.image_classifications.get(image_id)
        if classification_id:
            return self.classifications.get(classification_id)
        return None
    
    def save(self, classification: ImageClassification) -> ImageClassification:
        """分類結果を保存する"""
        self.classifications[classification.id] = classification
        self.image_classifications[classification.image_id] = classification.id
        return classification
    
    def get_nsfw_images(self, page: int = 0, page_size: int = 100) -> List[str]:
        """NSFW画像のIDリストを取得する"""
        nsfw_image_ids = []
        
        for classification in self.classifications.values():
            if classification.is_nsfw:
                nsfw_image_ids.append(classification.image_id)
        
        # ページネーション
        start = page * page_size
        end = start + page_size
        
        return nsfw_image_ids[start:end]
    
    def get_sfw_images(self, page: int = 0, page_size: int = 100) -> List[str]:
        """健全画像のIDリストを取得する"""
        sfw_image_ids = []
        
        for classification in self.classifications.values():
            if not classification.is_nsfw:
                sfw_image_ids.append(classification.image_id)
        
        # ページネーション
        start = page * page_size
        end = start + page_size
        
        return sfw_image_ids[start:end]
