from abc import ABC, abstractmethod
from typing import Dict, List, Tuple

from domain.entities.image import Image
from domain.entities.image_classification import ImageClassification

class ImageClassificationService(ABC):
    """画像分類に関するドメインサービスのインターフェース"""
    
    @abstractmethod
    def classify_is_nsfw(self, image: Image, classifier_type: str = "default") -> ImageClassification:
        """画像がNSFWかどうかを分類する"""
        pass
