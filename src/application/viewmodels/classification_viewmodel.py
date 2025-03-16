from typing import Dict, List, Optional

from domain.entities.image import Image
from domain.entities.image_classification import ImageClassification
from application.usecases.classify_image_usecase import ClassifyImageUseCase
from application.viewmodels.signal import Signal

class ClassificationViewModel:
    """分類機能のビューモデル"""
    
    def __init__(self, classify_image_use_case: ClassifyImageUseCase):
        self.classify_image_use_case = classify_image_use_case
        
        # 状態
        self.current_classification = None
        
        # シグナル
        self.on_classification_changed = Signal()
        self.on_classification_started = Signal()
        self.on_classification_completed = Signal()
        self.on_error = Signal()
    def classify_image(self, image_id: str, classifier_type: str = "default"):
        """画像を分類する"""
        self.on_classification_started.emit(image_id)

        try:
            classification = self.classify_image_use_case.execute(
                image_id, classifier_type
            )

            self.current_classification = classification
            self.on_classification_changed.emit(classification)
            self.on_classification_completed.emit(classification)

        except Exception as e:
            self.on_error.emit(str(e))
