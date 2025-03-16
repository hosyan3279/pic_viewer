from typing import Any, Callable, List

class Signal:
    """シンプルなシグナル実装"""
    
    def __init__(self):
        self.handlers: List[Callable] = []
    
    def connect(self, handler: Callable) -> None:
        """ハンドラを接続する"""
        if handler not in self.handlers:
            self.handlers.append(handler)
    
    def disconnect(self, handler: Callable) -> None:
        """ハンドラを切断する"""
        if handler in self.handlers:
            self.handlers.remove(handler)
    
    def emit(self, *args: Any, **kwargs: Any) -> None:
        """シグナルを発信する"""
        for handler in self.handlers:
            handler(*args, **kwargs)
