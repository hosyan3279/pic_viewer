from domain.entities.image import Image
from application.usecases.view_image_usecase import ViewImageUseCase
from application.viewmodels.signal import Signal

class ImageViewModel:
    """画像表示のビューモデル"""
    
    def __init__(self, view_image_use_case: ViewImageUseCase):
        self.view_image_use_case = view_image_use_case
        
        # 状態
        self.current_image = None
        self.zoom_level = 1.0
        self.rotation = 0
        
        # シグナル
        self.on_image_loaded = Signal()
        self.on_zoom_changed = Signal()
        self.on_rotation_changed = Signal()
        self.on_error = Signal()
    
    def load_image(self, image_id: str):
        """画像を読み込む"""
        try:
            result = self.view_image_use_case.execute(image_id)
            
            self.current_image = result["image"]
            self.zoom_level = 1.0
            self.rotation = 0
            
            self.on_image_loaded.emit(self.current_image)
        
        except Exception as e:
            self.on_error.emit(str(e))
    
    def load_image_by_path(self, image_path: str):
        """パスから画像を読み込む"""
        try:
            result = self.view_image_use_case.execute_by_path(image_path)
            
            self.current_image = result["image"]
            self.zoom_level = 1.0
            self.rotation = 0
            
            self.on_image_loaded.emit(self.current_image)
        
        except Exception as e:
            self.on_error.emit(str(e))
    
    def zoom_in(self):
        """ズームイン"""
        self.zoom_level = min(self.zoom_level * 1.2, 5.0)
        self.on_zoom_changed.emit(self.zoom_level)
    
    def zoom_out(self):
        """ズームアウト"""
        self.zoom_level = max(self.zoom_level / 1.2, 0.1)
        self.on_zoom_changed.emit(self.zoom_level)
    
    def rotate_clockwise(self):
        """時計回りに回転"""
        self.rotation = (self.rotation + 90) % 360
        self.on_rotation_changed.emit(self.rotation)
    
    def rotate_counterclockwise(self):
        """反時計回りに回転"""
        self.rotation = (self.rotation - 90) % 360
        self.on_rotation_changed.emit(self.rotation)
    
    def reset_view(self):
        """表示をリセット"""
        self.zoom_level = 1.0
        self.rotation = 0
        self.on_zoom_changed.emit(self.zoom_level)
        self.on_rotation_changed.emit(self.rotation)
