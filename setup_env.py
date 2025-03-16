#!/usr/bin/env python3
"""
画像ビューワープロジェクトのセットアップスクリプト
- 仮想環境の作成
- 依存関係のインストール
- 初期プロジェクト構造の作成
"""

import os
import subprocess
import sys
import argparse
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description="画像ビューワープロジェクトのセットアップ")
    parser.add_argument("--venv", default="venv", help="仮想環境名")
    parser.add_argument("--project", default="image_viewer", help="プロジェクト名")
    parser.add_argument("--with-dev", action="store_true", help="開発用ツールもインストール")
    return parser.parse_args()


def create_venv(venv_name):
    """仮想環境を作成"""
    print(f"仮想環境「{venv_name}」を作成中...")
    subprocess.run([sys.executable, "-m", "venv", venv_name], check=True)
    print(f"仮想環境「{venv_name}」を作成しました")


def install_dependencies(venv_name, install_dev=False):
    """依存関係をインストール"""
    print("依存関係をインストール中...")
    
    # Pythonインタープリタのパスを構築
    if os.name == "nt":  # Windows
        python = os.path.join(venv_name, "Scripts", "python.exe")
        pip = os.path.join(venv_name, "Scripts", "pip.exe")
    else:  # macOS, Linux
        python = os.path.join(venv_name, "bin", "python")
        pip = os.path.join(venv_name, "bin", "pip")
    
    # pipの更新
    subprocess.run([pip, "install", "--upgrade", "pip"], check=True)
    
    # 基本的な依存関係のインストール
    subprocess.run([pip, "install", "-r", "requirements.txt"], check=True)
    
    # 開発用ツールのインストール
    if install_dev:
        dev_packages = ["black", "flake8", "pytest", "mypy", "isort"]
        subprocess.run([pip, "install"] + dev_packages, check=True)
    
    print("依存関係のインストールが完了しました")


def create_project_structure(project_name):
    """プロジェクト構造を作成"""
    print(f"プロジェクト「{project_name}」の構造を作成中...")
    
    # メインディレクトリ
    directories = [
        f"{project_name}/src/domain/entities",
        f"{project_name}/src/domain/usecases",
        f"{project_name}/src/domain/repositories",
        f"{project_name}/src/application/services",
        f"{project_name}/src/application/viewmodels",
        f"{project_name}/src/application/controllers",
        f"{project_name}/src/infrastructure/database",
        f"{project_name}/src/infrastructure/repositories",
        f"{project_name}/src/infrastructure/ml",
        f"{project_name}/src/infrastructure/file_io",
        f"{project_name}/src/presentation/views",
        f"{project_name}/src/presentation/ui",
        f"{project_name}/src/presentation/resources",
        f"{project_name}/tests/unit",
        f"{project_name}/tests/integration",
        f"{project_name}/tests/ui",
        f"{project_name}/resources/icons",
        f"{project_name}/resources/styles",
        f"{project_name}/resources/ui",
        f"{project_name}/models/nsfw",
        f"{project_name}/models/tagger",
        f"{project_name}/data/db",
        f"{project_name}/docs",
        f"{project_name}/scripts",
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        # 各ディレクトリに空の__init__.pyファイルを作成
        if "/src/" in directory or "/tests/" in directory:
            init_file = Path(directory) / "__init__.py"
            if not init_file.exists():
                init_file.touch()
    
    # メインエントリーポイントを作成
    main_py = Path(f"{project_name}/src/main.py")
    if not main_py.exists():
        with open(main_py, "w", encoding="utf-8") as f:
            f.write("""#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
画像ビューワーアプリケーションのエントリーポイント
\"\"\"

import sys
from PySide6.QtWidgets import QApplication
from presentation.views.main_window import MainWindow


def main():
    \"\"\"アプリケーションのメインエントリーポイント\"\"\"
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
""")
    
    # READMEファイルを作成
    readme = Path(f"{project_name}/README.md")
    if not readme.exists():
        with open(readme, "w", encoding="utf-8") as f:
            f.write(f"""# {project_name}

画像ビューワーアプリケーション - エロ絵と健全絵を分類する機能を持つ高機能画像ビューワー

## 特徴

- 複数の画像形式サポート (JPG, PNG, GIF, BMP, WEBP)
- 動画形式サポート (MP4)
- 画像の拡大/縮小、回転、フリップなどの基本操作
- エロ絵と健全絵の自動分類
- タグ付け機能とキャラクター認識
- カスタマイズ可能なUI
- 高速なパフォーマンス

## インストール

```bash
# 依存関係のインストール
pip install -r requirements.txt

# アプリケーションの実行
python src/main.py
```

## 開発

### 開発環境のセットアップ

```bash
# 仮想環境の作成とセットアップ
python setup_env.py --with-dev
```

### テストの実行

```bash
pytest
```

## ライセンス

[MIT](LICENSE)
""")
    
    print(f"プロジェクト「{project_name}」の構造を作成しました")


def setup_git(project_name):
    """Gitリポジトリを初期化"""
    print("Gitリポジトリを初期化中...")
    
    os.chdir(project_name)
    
    # .gitignoreファイルの作成
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# IDE
.idea/
.vscode/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Application specific
data/db/*.db
models/nsfw/*.h5
models/nsfw/*.pb
models/tagger/*.h5
models/tagger/*.pb
"""
    
    with open(".gitignore", "w", encoding="utf-8") as f:
        f.write(gitignore_content)
    
    # Gitリポジトリの初期化
    subprocess.run(["git", "init"], check=True)
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", "Initial commit"], check=True)
    
    os.chdir("..")
    print("Gitリポジトリを初期化しました")


def main():
    args = parse_args()
    
    print("=== 画像ビューワープロジェクトのセットアップを開始します ===")
    
    try:
        create_venv(args.venv)
        install_dependencies(args.venv, args.with_dev)
        create_project_structure(args.project)
        
        try:
            setup_git(args.project)
        except Exception as e:
            print(f"Gitの初期化に失敗しました: {e}")
            print("Gitをインストールして再試行してください。")
        
        print(f"\n=== セットアップが完了しました ===")
        print(f"以下のコマンドで開発を始めることができます:")
        
        if os.name == "nt":  # Windows
            activate_cmd = f"{args.venv}\\Scripts\\activate"
        else:  # macOS, Linux
            activate_cmd = f"source {args.venv}/bin/activate"
        
        print(f"\n# 仮想環境をアクティブ化")
        print(activate_cmd)
        print(f"\n# プロジェクトディレクトリに移動")
        print(f"cd {args.project}")
        print(f"\n# アプリケーションを実行")
        print(f"python src/main.py")
        
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        print("セットアップに失敗しました。")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
