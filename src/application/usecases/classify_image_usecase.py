from typing import Dict

from domain.entities.image import Image
from domain.entities.image_classification import ImageClassification
from domain.repositories.image_repository import ImageRepository
from domain.repositories.classification_repository import ClassificationRepository
from domain.services.image_classification_service import ImageClassificationService

class ClassifyImageUseCase:
    """画像を分類するユースケース"""
    
    def __init__(self, image_repository: ImageRepository,
                classification_repository: ClassificationRepository,
                classification_service: ImageClassificationService):
        self.image_repository = image_repository
        self.classification_repository = classification_repository
        self.classification_service = classification_service
    
    def execute(self, image_id: str, classifier_type: str = "default") -> ImageClassification:
        """画像を分類し、結果を保存する"""
        image = self.image_repository.get_by_id(image_id)
        if not image:
            raise ValueError(f"Image not found: {image_id}")
        
        # すでに分類済みかチェック
        existing_classification = self.classification_repository.get_by_image_id(image_id)
        if existing_classification:
            return existing_classification
        
        # 分類実行
        classification = self.classification_service.classify_is_nsfw(
            image, classifier_type
        )
        
        # 結果を保存
        saved_classification = self.classification_repository.save(classification)
        
        return saved_classification
