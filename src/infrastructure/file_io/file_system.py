import os
from datetime import datetime
from typing import Dict, List, Tuple

from PIL import Image as PILImage
import cv2

class FileSystemService:
    """ファイルシステム操作を行うサービス"""
    
    def list_directory(self, path: str) -> List[Dict]:
        """ディレクトリ内のファイルとフォルダを一覧表示する"""
        items = []
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            is_dir = os.path.isdir(item_path)
            if is_dir or self._is_supported_image(item):
                items.append({
                    "name": item,
                    "path": item_path,
                    "is_directory": is_dir,
                    "size": os.path.getsize(item_path) if not is_dir else 0,
                    "modified": datetime.fromtimestamp(os.path.getmtime(item_path))
                })
        return items
    
    def _is_supported_image(self, filename: str) -> bool:
        """サポートされている画像ファイルかどうかを判定する"""
        ext = os.path.splitext(filename)[1].lower()
        return ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.mp4']
    
    def get_image_metadata(self, path: str) -> Dict:
        """画像ファイルのメタデータを取得する"""
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")
        
        ext = os.path.splitext(path)[1].lower()
        if ext == '.mp4':
            return self._get_video_metadata(path)
        else:
            return self._get_image_metadata(path)
    
    def _get_image_metadata(self, path: str) -> Dict:
        """画像ファイルのメタデータを取得する"""
        try:
            with PILImage.open(path) as img:
                width, height = img.size
                format_name = img.format
                
                return {
                    "width": width,
                    "height": height,
                    "format": format_name,
                    "size": os.path.getsize(path),
                    "created": datetime.fromtimestamp(os.path.getctime(path)),
                    "modified": datetime.fromtimestamp(os.path.getmtime(path))
                }
        except Exception as e:
            raise ValueError(f"Error reading image metadata: {e}")
    
    def _get_video_metadata(self, path: str) -> Dict:
        """動画ファイルのメタデータを取得する"""
        try:
            video = cv2.VideoCapture(path)
            if not video.isOpened():
                raise ValueError("Could not open video file")
            
            width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
            frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = video.get(cv2.CAP_PROP_FPS)
            
            video.release()
            
            return {
                "width": width,
                "height": height,
                "format": "mp4",
                "size": os.path.getsize(path),
                "created": datetime.fromtimestamp(os.path.getctime(path)),
                "modified": datetime.fromtimestamp(os.path.getmtime(path)),
                "frame_count": frame_count,
                "fps": fps,
                "duration": frame_count / fps if fps > 0 else 0
            }
        except Exception as e:
            raise ValueError(f"Error reading video metadata: {e}")
    
    def create_thumbnail(self, image_path: str, 
                        target_path: str, size: Tuple[int, int]) -> bool:
        """画像のサムネイルを作成する"""
        try:
            ext = os.path.splitext(image_path)[1].lower()
            if ext == '.mp4':
                return self._create_video_thumbnail(image_path, target_path, size)
            else:
                return self._create_image_thumbnail(image_path, target_path, size)
        except Exception as e:
            print(f"Error creating thumbnail: {e}")
            return False
    
    def _create_image_thumbnail(self, image_path: str, 
                              target_path: str, size: Tuple[int, int]) -> bool:
        """画像のサムネイルを作成する"""
        try:
            with PILImage.open(image_path) as img:
                img.thumbnail(size)
                img.save(target_path)
            return True
        except Exception as e:
            print(f"Error creating image thumbnail: {e}")
            return False
    
    def _create_video_thumbnail(self, video_path: str, 
                              target_path: str, size: Tuple[int, int]) -> bool:
        """動画のサムネイルを作成する"""
        try:
            video = cv2.VideoCapture(video_path)
            if not video.isOpened():
                return False
            
            # 動画の先頭から少し進んだフレームを取得
            video.set(cv2.CAP_PROP_POS_FRAMES, min(30, video.get(cv2.CAP_PROP_FRAME_COUNT) - 1))
            success, frame = video.read()
            video.release()
            
            if not success:
                return False
            
            # サイズ変更
            height, width = frame.shape[:2]
            target_width, target_height = size
            
            # アスペクト比を維持しながらリサイズ
            if width > height:
                new_width = target_width
                new_height = int(height * target_width / width)
            else:
                new_height = target_height
                new_width = int(width * target_height / height)
            
            resized = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_AREA)
            
            # OpenCVはBGRなのでRGBに変換
            rgb_frame = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
            
            # PILで保存
            img = PILImage.fromarray(rgb_frame)
            img.save(target_path)
            
            return True
        except Exception as e:
            print(f"Error creating video thumbnail: {e}")
            return False
