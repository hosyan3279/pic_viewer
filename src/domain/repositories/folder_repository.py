from abc import ABC, abstractmethod
from typing import List, Optional

from domain.entities.folder import Folder

class FolderRepository(ABC):
    """フォルダのリポジトリインターフェース"""
    
    @abstractmethod
    def get_by_id(self, folder_id: str) -> Optional[Folder]:
        """IDでフォルダを取得する"""
        pass
    
    @abstractmethod
    def get_by_path(self, path: str) -> Optional[Folder]:
        """パスでフォルダを取得する"""
        pass
    
    @abstractmethod
    def get_subfolders(self, parent_id: str) -> List[Folder]:
        """親フォルダのサブフォルダを取得する"""
        pass
    
    @abstractmethod
    def save(self, folder: Folder) -> Folder:
        """フォルダを保存する"""
        pass
