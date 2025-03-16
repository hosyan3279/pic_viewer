from PyQt6.QtWidgets import QTreeView
from PyQt6.QtCore import pyqtSignal, QDir, Qt
from PyQt6.QtGui import QFileSystemModel

class FolderTreeWidget(QTreeView):
    """フォルダツリーを表示するウィジェット"""
    
    folder_selected = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        
        self.setHeaderHidden(True)
        
        # ファイルシステムモデルの設定
        self.model = QFileSystemModel()
        self.model.setFilter(QDir.Filter.AllDirs | QDir.Filter.NoDotAndDotDot)
        self.model.setRootPath("")
        
        self.setModel(self.model)
        
        # ルートインデックスの設定
        self.setRootIndex(self.model.index(QDir.homePath()))
        
        # 名前の列だけ表示
        for i in range(1, self.model.columnCount()):
            self.hideColumn(i)
        
        # 選択モードの設定
        self.setSelectionMode(QTreeView.SelectionMode.SingleSelection)
        
        # シグナルの接続
        self.clicked.connect(self._on_folder_clicked)
    
    def _on_folder_clicked(self, index):
        """フォルダがクリックされたときの処理"""
        path = self.model.filePath(index)
        self.folder_selected.emit(path)
