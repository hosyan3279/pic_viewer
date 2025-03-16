import os
from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QSplitter, QMessageBox,
    QFileDialog, QPushButton, QInputDialog
)
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt

from domain.entities.image import Image
from application.viewmodels.main_window_viewmodel import MainWindowViewModel
from application.viewmodels.image_viewmodel import ImageViewModel
from application.viewmodels.classification_viewmodel import ClassificationViewModel
from presentation.widgets.folder_tree_widget import FolderTreeWidget
from presentation.widgets.image_list_widget import ImageListWidget
from presentation.widgets.image_view_widget import ImageViewWidget
from presentation.widgets.classification_widget import ClassificationWidget

class MainWindow(QMainWindow):
    """アプリケーションのメインウィンドウ"""
    
    def __init__(self, main_view_model: MainWindowViewModel, 
                 image_view_model: ImageViewModel,
                 classification_view_model: ClassificationViewModel):
        super().__init__()
        
        self.main_view_model = main_view_model
        self.image_view_model = image_view_model
        self.classification_view_model = classification_view_model
        
        self.setWindowTitle("画像ビューワー")
        self.resize(1200, 800)
        
        self._setup_ui()
        self._setup_menu_bar()
        self._setup_tool_bar()
        self._connect_signals()
    
    def _setup_ui(self):
        """UIのセットアップ"""
        # ウィジェットの作成
        self.folder_tree = FolderTreeWidget()
        self.image_list = ImageListWidget()
        self.image_view = ImageViewWidget()
        self.classification_widget = ClassificationWidget()
        
        # 分類ボタン
        self.classify_button = QPushButton("画像を分類")
        self.classify_button.clicked.connect(self._classify_current_image)
        
        # レイアウトのセットアップ
        # 左側（フォルダツリーとイメージリスト）
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.addWidget(self.folder_tree)
        left_layout.addWidget(self.image_list)
        left_layout.setStretch(0, 1)
        left_layout.setStretch(1, 2)
        
        # 右側（画像ビュー）
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.addWidget(self.image_view)
        
        # 分類パネル
        classification_panel = QWidget()
        classification_layout = QVBoxLayout(classification_panel)
        classification_layout.addWidget(self.classification_widget)
        classification_layout.addWidget(self.classify_button)
        right_layout.addWidget(classification_panel)
        
        # スプリッターの設定
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([300, 900])
        
        # 中央ウィジェットの設定
        central_widget = QWidget()
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(splitter)
        central_widget.setLayout(central_layout)
        self.setCentralWidget(central_widget)
    
    def _setup_menu_bar(self):
        """メニューバーのセットアップ"""
        menubar = self.menuBar()
        
        # ファイルメニュー
        file_menu = menubar.addMenu("ファイル")
        
        open_folder_action = QAction("フォルダを開く", self)
        open_folder_action.triggered.connect(self._open_folder_dialog)
        file_menu.addAction(open_folder_action)
        
        open_file_action = QAction("ファイルを開く", self)
        open_file_action.triggered.connect(self._open_file_dialog)
        file_menu.addAction(open_file_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("終了", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 表示メニュー
        view_menu = menubar.addMenu("表示")
        
        zoom_in_action = QAction("拡大", self)
        zoom_in_action.triggered.connect(self.image_view_model.zoom_in)
        view_menu.addAction(zoom_in_action)
        
        zoom_out_action = QAction("縮小", self)
        zoom_out_action.triggered.connect(self.image_view_model.zoom_out)
        view_menu.addAction(zoom_out_action)
        
        view_menu.addSeparator()
        
        rotate_cw_action = QAction("時計回りに回転", self)
        rotate_cw_action.triggered.connect(self.image_view_model.rotate_clockwise)
        view_menu.addAction(rotate_cw_action)
        
        rotate_ccw_action = QAction("反時計回りに回転", self)
        rotate_ccw_action.triggered.connect(self.image_view_model.rotate_counterclockwise)
        view_menu.addAction(rotate_ccw_action)
        
        # 任意角度回転のアクションを追加
        rotate_angle_action = QAction("角度を指定して回転", self)
        rotate_angle_action.triggered.connect(self._rotate_by_angle)
        view_menu.addAction(rotate_angle_action)
        
        # 全画面表示のアクションを追加
        fullscreen_action = QAction("全画面表示", self)
        fullscreen_action.triggered.connect(self._toggle_fullscreen)
        view_menu.addAction(fullscreen_action)
        
        # フィット表示のアクションを追加
        fit_to_window_action = QAction("ウィンドウに合わせる", self)
        fit_to_window_action.setCheckable(True)
        fit_to_window_action.setChecked(True)
        fit_to_window_action.triggered.connect(self._toggle_fit_to_window)
        view_menu.addAction(fit_to_window_action)
        
        view_menu.addSeparator()
        
        reset_view_action = QAction("表示をリセット", self)
        reset_view_action.triggered.connect(self.image_view_model.reset_view)
        view_menu.addAction(reset_view_action)
        
        # 分類メニュー
        classify_menu = menubar.addMenu("分類")
        
        classify_action = QAction("現在の画像を分類", self)
        classify_action.triggered.connect(self._classify_current_image)
        classify_menu.addAction(classify_action)
    
    def _setup_tool_bar(self):
        """ツールバーのセットアップ"""
        toolbar = self.addToolBar("メインツールバー")
        
        # 前の画像
        prev_action = QAction(QIcon.fromTheme("go-previous"), "前の画像", self)
        prev_action.triggered.connect(self.main_view_model.previous_image)
        toolbar.addAction(prev_action)
        
        # 次の画像
        next_action = QAction(QIcon.fromTheme("go-next"), "次の画像", self)
        next_action.triggered.connect(self.main_view_model.next_image)
        toolbar.addAction(next_action)
        
        toolbar.addSeparator()
        
        # ズームイン
        zoom_in_action = QAction(QIcon.fromTheme("zoom-in"), "拡大", self)
        zoom_in_action.triggered.connect(self.image_view_model.zoom_in)
        toolbar.addAction(zoom_in_action)
        
        # ズームアウト
        zoom_out_action = QAction(QIcon.fromTheme("zoom-out"), "縮小", self)
        toolbar.addAction(zoom_out_action)
        
        toolbar.addSeparator()
        
        # 回転
        rotate_cw_action = QAction(QIcon.fromTheme("object-rotate-right"), "時計回りに回転", self)
        rotate_cw_action.triggered.connect(self.image_view_model.rotate_clockwise)
        toolbar.addAction(rotate_cw_action)
        
        rotate_ccw_action = QAction(QIcon.fromTheme("object-rotate-left"), "反時計回りに回転", self)
        rotate_ccw_action.triggered.connect(self.image_view_model.rotate_counterclockwise)
        toolbar.addAction(rotate_ccw_action)
        
        toolbar.addSeparator()
        
        # 分類
        classify_action = QAction(QIcon.fromTheme("view-filter"), "画像を分類", self)
        classify_action.triggered.connect(self._classify_current_image)
        toolbar.addAction(classify_action)
    
    def _connect_signals(self):
        """シグナルの接続"""
        # フォルダツリーのシグナル
        self.folder_tree.folder_selected.connect(self.main_view_model.load_folder)
        
        # イメージリストのシグナル
        self.image_list.image_selected.connect(self.main_view_model.select_image)
        
        # メインビューモデルのシグナル
        self.main_view_model.on_folder_changed.connect(self._update_folder_path)
        self.main_view_model.on_images_loaded.connect(self.image_list.set_images)
        self.main_view_model.on_image_selected.connect(self._handle_image_selected)
        self.main_view_model.on_error.connect(self._show_error)
        
        # 画像ビューモデルのシグナル
        self.image_view_model.on_image_loaded.connect(self.image_view.set_image)
        self.image_view_model.on_zoom_changed.connect(self.image_view.set_zoom)
        self.image_view_model.on_rotation_changed.connect(self.image_view.set_rotation)
        self.image_view_model.on_error.connect(self._show_error)
        
        # 分類ビューモデルのシグナル
        self.classification_view_model.on_classification_changed.connect(self.classification_widget.set_classification)
        self.classification_view_model.on_classification_started.connect(self._classification_started)
        self.classification_view_model.on_classification_completed.connect(self._classification_completed)
        self.classification_view_model.on_error.connect(self._show_error)
    
    def _open_folder_dialog(self):
        """フォルダ選択ダイアログを開く"""
        folder_path = QFileDialog.getExistingDirectory(
            self, "フォルダを開く", "", QFileDialog.Option.ShowDirsOnly
        )
        if folder_path:
            self.main_view_model.load_folder(folder_path)
    
    def _open_file_dialog(self):
        """ファイル選択ダイアログを開く"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "ファイルを開く", "", "画像と動画 (*.jpg *.png *.jpeg *.gif *.bmp *.webp *.mp4 *.avi *.mov)"
        )
        if file_path:
            self.open_file(file_path)
    
    def _update_folder_path(self, folder_path: str):
        """フォルダパスを更新する"""
        self.setWindowTitle(f"画像ビューワー - {folder_path}")
    
    def _handle_image_selected(self, image: Image):
        """画像が選択されたときの処理"""
        self.image_view_model.load_image(image.id)
    
    def _show_error(self, error_msg: str):
        """エラーメッセージを表示する"""
        QMessageBox.critical(self, "エラー", error_msg)
    
    def _classify_current_image(self):
        """現在の画像を分類する"""
        if not self.main_view_model.current_image:
            self._show_error("分類する画像が選択されていません")
            return
        
        # 分類実行
        self.classification_view_model.classify_image(self.main_view_model.current_image.id)
    
    def _classification_started(self, image_id: str):
        """分類開始時の処理"""
        self.statusBar().showMessage("画像を分類中...")
        self.classify_button.setEnabled(False)
    
    def _classification_completed(self, classification):
        """分類完了時の処理"""
        self.statusBar().showMessage("分類完了")
        self.classify_button.setEnabled(True)
    
    def _rotate_by_angle(self):
        """角度を指定して回転"""
        angle, ok = QInputDialog.getInt(self, "回転角度", "回転角度を入力してください:", 0, -360, 360, 1)
        if ok:
            self.image_view_model.rotate(angle)
    
    def _toggle_fullscreen(self):
        """全画面表示を切り替える"""
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()
    
    def _toggle_fit_to_window(self, checked: bool):
        """フィット表示を切り替える"""
        self.image_view.set_fit_to_window(checked)
        
    def open_file(self, file_path: str):
        """ファイルを開く"""
        if not file_path:
            return
        
        # ファイル拡張子を取得
        ext = os.path.splitext(file_path)[1].lower()
        
        # 画像または動画として処理
        if ext in ['.jpg', '.png', '.jpeg', '.gif', '.bmp', '.webp', '.mp4', '.avi', '.mov']:
            # Imageオブジェクトを作成
            image = Image(id=file_path, path=file_path, is_video=ext in ['.mp4', '.avi', '.mov'])
            
            # 画像を選択
            self.main_view_model.select_image(image)
        else:
            self._show_error("サポートされていないファイル形式です")
