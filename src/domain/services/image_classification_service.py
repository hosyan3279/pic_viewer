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

    @staticmethod
    def create_classifier(classifier_type: str = "default") -> "ImageClassificationService":
        """classifier_typeに基づいて適切な分類器を作成する"""
        from infrastructure.ml.nudenet_classifier import NudeNetClassifier
        from infrastructure.ml.simple_nsfw_classifier import SimpleNSFWClassifier
        from infrastructure.ml.tensorflow_nsfw_classifier import TensorFlowNSFWClassifier

        if classifier_type == "nudenet":
            return NudeNetClassifier()
        elif classifier_type == "simple":
            return SimpleNSFWClassifier()
        elif classifier_type == "tensorflow":
            return TensorFlowNSFWClassifier()
        else:
            return NudeNetClassifier()
