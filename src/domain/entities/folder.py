from typing import Optional

class Folder:
    """フォルダを表すエンティティ"""
    
    def __init__(self, id: str, path: str, name: str, parent_id: Optional[str] = None):
        self.id = id              # 一意のID
        self.path = path          # パス
        self.name = name          # フォルダ名
        self.parent_id = parent_id  # 親フォルダID
