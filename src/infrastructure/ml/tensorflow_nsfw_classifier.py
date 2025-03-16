import os
import uuid
from datetime import datetime
from typing import Dict, Tuple, Optional
import numpy as np
from nudenet import NudeClassifier

from domain.entities.image import Image
from domain.entities.image_classification import ImageClassification
from domain.services.image_classification_service import ImageClassificationService

class TensorFlowNSFWClassifier(ImageClassificationService):
    """NudeNetを使用したNSFW分類器の実装
    (クラス名はTensorFlowNSFWClassifierのままですが、内部実装はNudeNetを使用)
    """
    
    def __init__(self):
        self.model = None
        self.loaded = False
    
    def _load_model(self) -> bool:
        """NudeNet分類器をロードする"""
        try:
            # NudeClassifierの初期化
            self.model = NudeClassifier()
            self.loaded = True
            return True
        except Exception as e:
            print(f"Error loading NudeNet model: {e}")
            return False
    
    def classify_is_nsfw(self, image: Image, classifier_type: str = "default") -> ImageClassification:
        """画像を分類する"""
        if not self.loaded:
            if not self._load_model():
                raise ValueError("Failed to load NudeNet model")
        
        try:
            # NudeNetでの分類実行
            classification_result = self.model.classify(image.path)
            
            # 結果の解釈（パスをキーとして持つ辞書が返される）
            result = classification_result.get(image.path, {})
            
            # NSFW関連のクラスのスコアを合計
            nsfw_classes = ['NUDE', 'PORN', 'SEXY']
            nsfw_score = sum(result.get(class_name, 0.0) for class_name in nsfw_classes)
            
            # 正規化（0-1の範囲に）
            nsfw_score = min(nsfw_score, 1.0)
            
            # NSFWかどうかの判断
            is_nsfw = nsfw_score > 0.5
            
            # 分類結果を作成
            classification = ImageClassification(
                id=str(uuid.uuid4()),
                image_id=image.id,
                is_nsfw=is_nsfw,
                nsfw_score=float(nsfw_score),
                classification_method="NudeNet",
                classified_at=datetime.now()
            )
            
            return classification
        
        except Exception as e:
            print(f"Error classifying image with NudeNet: {e}")
            # エラーが発生した場合は、ダミーの結果を返す
            return ImageClassification(
                id=str(uuid.uuid4()),
                image_id=image.id,
                is_nsfw=False,
                nsfw_score=0.0,
                classification_method="error",
                classified_at=datetime.now()
            )
