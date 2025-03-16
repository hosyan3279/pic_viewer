from typing import List

from domain.entities.image import Image
from application.usecases.browse_folder_usecase import BrowseFolderUseCase
from application.usecases.view_image_usecase import ViewImageUseCase
from application.viewmodels.signal import Signal

class MainWindowViewModel:
    """メイン画面のビューモデル"""
    
    def __init__(self, browse_folder_use_case: BrowseFolderUseCase,
                view_image_use_case: ViewImageUseCase):
        self.browse_folder_use_case = browse_folder_use_case
        self.view_image_use_case = view_image_use_case
        
        # 状態
        self.current_folder_path = ""
        self.current_images = []
        self.current_image_index = -1
        self.current_image = None
        
        # シグナル
        self.on_folder_changed = Signal()
        self.on_image_selected = Signal()
        self.on_images_loaded = Signal()
        self.on_error = Signal()
    
    def load_folder(self, folder_path: str):
        """フォルダを読み込む"""
        try:
            result = self.browse_folder_use_case.execute(
                folder_path, 0, 1000  # とりあえず大きなサイズ
            )
            
            self.current_folder_path = folder_path
            self.current_images = result["images"]
            self.current_image_index = -1
            self.current_image = None
            
            self.on_folder_changed.emit(folder_path)
            self.on_images_loaded.emit(self.current_images)
        
        except Exception as e:
            self.on_error.emit(str(e))
    
    def select_image(self, image_id: str):
        """画像を選択する"""
        try:
            for i, image in enumerate(self.current_images):
                if image.id == image_id:
                    self.current_image_index = i
                    self.current_image = image
                    break
            
            if self.current_image:
                self.on_image_selected.emit(self.current_image)
        
        except Exception as e:
            self.on_error.emit(str(e))
    
    def select_image_at_index(self, index: int):
        """インデックスで画像を選択する"""
        if 0 <= index < len(self.current_images):
            self.current_image_index = index
            self.current_image = self.current_images[index]
            self.on_image_selected.emit(self.current_image)
    
    def next_image(self):
        """次の画像を選択する"""
        if not self.current_images:
            return
        
        if self.current_image_index < len(self.current_images) - 1:
            self.select_image_at_index(self.current_image_index + 1)
    
    def previous_image(self):
        """前の画像を選択する"""
        if not self.current_images:
            return
        
        if self.current_image_index > 0:
            self.select_image_at_index(self.current_image_index - 1)
