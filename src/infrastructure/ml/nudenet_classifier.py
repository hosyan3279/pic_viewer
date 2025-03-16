import os
import uuid
from datetime import datetime
from typing import Dict, Tuple, Optional
import numpy as np

from domain.entities.image import Image
from domain.entities.image_classification import ImageClassification
from domain.services.image_classification_service import ImageClassificationService

class NudeNetClassifier(ImageClassificationService):
    """NudeNetを使用したNSFW分類器の実装"""
    
    def __init__(self):
        self.model = None
        self.loaded = False
        self._lazy_import_nudenet()
    
    def _lazy_import_nudenet(self):
        """NudeNetを遅延インポート"""
        try:
            # この時点ではまだインポートしない
            self.NudeDetector = None
        except Exception as e:
            print(f"Error preparing NudeNet: {e}")
    
    def _load_model(self) -> bool:
        """NudeNet検出器をロードする"""
        try:
            # NudeNetをインポート（遅延インポート）
            from nudenet import NudeDetector
            self.NudeDetector = NudeDetector
            
            # モデルの初期化
            self.model = self.NudeDetector()
            self.loaded = True
            print("NudeNet model loaded successfully")
            return True
        except Exception as e:
            print(f"Error loading NudeNet model: {e}")
            return False
    
    def classify_is_nsfw(self, image: Image, classifier_type: str = "nudenet") -> ImageClassification:
        """画像を分類する（NudeDetectorを使用）"""
        try:
            if not self.loaded:
                if not self._load_model():
                    raise ValueError("Failed to load NudeNet model")
            
            # NudeDetectorでの検出実行
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
            # エラーが発生した場合は、フォールバックとしてシンプルな分類を行う
            return self._fallback_classification(image)
    
    def _fallback_classification(self, image: Image) -> ImageClassification:
        """NudeNetが失敗した場合のフォールバック分類"""
        # ファイル名から簡単な判定を行う
        filename_lower = image.filename.lower()
        is_nsfw = any(word in filename_lower for word in ['nsfw', 'adult', 'xxx', '18+', 'nude'])
        nsfw_score = 0.8 if is_nsfw else 0.2
        
        return ImageClassification(
            id=str(uuid.uuid4()),
            image_id=image.id,
            is_nsfw=is_nsfw,
            nsfw_score=nsfw_score,
            classification_method="fallback",
            classified_at=datetime.now()
        )
