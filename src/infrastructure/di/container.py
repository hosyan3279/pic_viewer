import os
import uuid
from typing import Dict

# ドメイン層
from domain.entities.folder import Folder
from domain.entities.image import Image
from domain.repositories.folder_repository import FolderRepository
from domain.repositories.image_repository import ImageRepository
from domain.repositories.classification_repository import ClassificationRepository
from domain.services.image_classification_service import ImageClassificationService

# インフラストラクチャ層
from infrastructure.file_io.file_system import FileSystemService
from infrastructure.repositories.in_memory_repositories import (
    InMemoryFolderRepository, InMemoryImageRepository, InMemoryClassificationRepository
)

# NudeNetの実装をインポート
try:
    from infrastructure.ml.nudenet_classifier import NudeNetClassifier
    use_nudenet = True
except ImportError as e:
    print(f"Warning: Could not import NudeNet. Using simple classifier instead. Error: {e}")
    from infrastructure.ml.simple_nsfw_classifier import SimpleNSFWClassifier
    use_nudenet = False

# アプリケーション層
from application.usecases.browse_folder_usecase import BrowseFolderUseCase
from application.usecases.view_image_usecase import ViewImageUseCase
from application.usecases.classify_image_usecase import ClassifyImageUseCase
from application.viewmodels.main_window_viewmodel import MainWindowViewModel
from application.viewmodels.image_viewmodel import ImageViewModel
from application.viewmodels.classification_viewmodel import ClassificationViewModel

# プレゼンテーション層
from presentation.views.main_window import MainWindow

class DIContainer:
    """依存性注入コンテナ"""
    
    def __init__(self):
        self._instances: Dict[str, object] = {}
    
    def register(self, key: str, instance: object):
        """インスタンスを登録する"""
        self._instances[key] = instance
    
    def resolve(self, key: str) -> object:
        """インスタンスを解決する"""
        if key not in self._instances:
            raise ValueError(f"Key not registered: {key}")
        return self._instances[key]
    
    def setup(self):
        """アプリケーションの依存性を設定する"""
        # インフラストラクチャ層の依存関係
        file_system_service = FileSystemService()
        image_repository = InMemoryImageRepository(file_system_service)
        folder_repository = InMemoryFolderRepository()
        classification_repository = InMemoryClassificationRepository()
        
        # NudeNetまたはシンプルな分類器を設定
        if use_nudenet:
            classification_service = NudeNetClassifier()
            print("Using NudeNet classifier")
        else:
            classification_service = SimpleNSFWClassifier()
            print("Using simple classifier")
        
        # アプリケーション層の依存関係
        browse_folder_usecase = BrowseFolderUseCase(folder_repository, image_repository)
        view_image_usecase = ViewImageUseCase(image_repository)
        classify_image_usecase = ClassifyImageUseCase(
            image_repository, classification_repository, classification_service
        )
        
        # ビューモデル
        main_view_model = MainWindowViewModel(browse_folder_usecase, view_image_usecase)
        image_view_model = ImageViewModel(view_image_usecase)
        classification_view_model = ClassificationViewModel(classify_image_usecase)
        
        # 登録
        self.register("file_system_service", file_system_service)
        self.register("image_repository", image_repository)
        self.register("folder_repository", folder_repository)
        self.register("classification_repository", classification_repository)
        self.register("classification_service", classification_service)
        self.register("browse_folder_usecase", browse_folder_usecase)
        self.register("view_image_usecase", view_image_usecase)
        self.register("classify_image_usecase", classify_image_usecase)
        self.register("main_view_model", main_view_model)
        self.register("image_view_model", image_view_model)
        self.register("classification_view_model", classification_view_model)
    
    def create_main_window(self) -> MainWindow:
        """メインウィンドウを作成する"""
        main_view_model = self.resolve("main_view_model")
        image_view_model = self.resolve("image_view_model")
        classification_view_model = self.resolve("classification_view_model")
        
        return MainWindow(main_view_model, image_view_model, classification_view_model)
