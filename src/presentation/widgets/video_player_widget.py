from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSlider
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtGui import QIcon

class VideoPlayerWidget(QWidget):
    """動画再生ウィジェット"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # レイアウトの設定
        self.layout = QVBoxLayout(self)
        
        # ビデオウィジェットの作成
        self.video_widget = QVideoWidget()
        self.layout.addWidget(self.video_widget)
        
        # コントロールバーの作成
        self.controls_layout = QHBoxLayout()
        
        # 再生・一時停止ボタン
        self.play_button = QPushButton()
        self.play_button.setIcon(QIcon.fromTheme("media-playback-start"))
        self.play_button.clicked.connect(self.toggle_play)
        self.controls_layout.addWidget(self.play_button)
        
        # 停止ボタン
        self.stop_button = QPushButton()
        self.stop_button.setIcon(QIcon.fromTheme("media-playback-stop"))
        self.stop_button.clicked.connect(self.stop)
        self.controls_layout.addWidget(self.stop_button)
        
        # 音量スライダー
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(70)  # デフォルト値
        self.volume_slider.valueChanged.connect(self.set_volume)
        self.controls_layout.addWidget(self.volume_slider)
        
        self.layout.addLayout(self.controls_layout)
        
        # メディアプレーヤーの作成
        self.media_player = QMediaPlayer()
        
        # 音声出力の設定
        self.audio_output = QAudioOutput()
        self.audio_output.setVolume(0.7)  # デフォルト音量は70%
        self.media_player.setAudioOutput(self.audio_output)
        
        self.media_player.setVideoOutput(self.video_widget)
        
        # 再生状態の管理
        self.is_playing = False
        
        # シグナルの接続
        self.media_player.playbackStateChanged.connect(self.update_play_button)
    
    def set_video(self, path):
        """動画を設定する"""
        if not path:
            return
        
        self.media_player.setSource(QUrl.fromLocalFile(path))
        self.stop()
    
    def toggle_play(self):
        """再生・一時停止を切り替える"""
        if self.media_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.media_player.pause()
        else:
            self.media_player.play()
    
    def stop(self):
        """停止する"""
        self.media_player.stop()
    
    def set_volume(self, volume):
        """音量を設定する"""
        linear_volume = volume / 100.0
        self.audio_output.setVolume(linear_volume)
    
    def update_play_button(self, state):
        """再生ボタンの表示を更新する"""
        if state == QMediaPlayer.PlaybackState.PlayingState:
            self.play_button.setIcon(QIcon.fromTheme("media-playback-pause"))
        else:
            self.play_button.setIcon(QIcon.fromTheme("media-playback-start"))
