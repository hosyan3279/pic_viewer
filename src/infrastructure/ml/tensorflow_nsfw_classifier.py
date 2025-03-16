import os
import uuid
from datetime import datetime
from typing import Dict, Tuple, Optional
import numpy as np
from nudenet import NudeDetector

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
            # NudeDetectorの初期化
            self.model = NudeDetector()
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
            # NudeNetでの検出実行
            detection_result = self.model.detect(image.path)

            # 結果を解析
            if not detection_result:
                # 検出結果がない場合（安全な画像）
                nsfw_score = 0.0
                is_nsfw = False
            else:
                # 検出された部位のうち、最も信頼度が高いものを取得
                max_score = max([det.get('score', 0.0) for det in detection_result]) if detection_result else 0.0
                nsfw_score = max_score
                is_nsfw = nsfw_score > 0.5

            # デバッグ出力
            print(f"NudeNet detection found {len(detection_result)} objects with max score: {nsfw_score}")

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
