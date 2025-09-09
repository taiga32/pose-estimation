# Pose Estimation with MediaPipe and Rerun

MediaPipeを使用した姿勢推定とRerunによる可視化を行うプロジェクト

## 概要

このプロジェクトは、動画ファイルから人物の姿勢（ポーズ）を検出し、Rerunを使用してリアルタイムで可視化するツールです。

## 必要要件
- uv (Pythonパッケージマネージャー)

## セットアップ

### 1. uvのインストール

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# または pip でインストール
pip install uv
```

### 2. 依存関係のインストール

```bash
# プロジェクトディレクトリで実行
uv sync
```

### 3. データの準備

動画ファイルを `data/original/` ディレクトリに配置します：

```bash
# ディレクトリ作成
mkdir -p data/original

# MP4ファイルを配置
cp your_video.mp4 data/original/
```

## 実行方法

```bash
# Python環境をアクティベート
uv run python main.py
```

実行すると：
1. `data/original/` 内の最初のMP4ファイルが読み込まれます
2. Rerunビューアが自動的に起動します
3. 動画のフレームごとに姿勢推定が実行され、結果がRerunで可視化されます

## 主な機能

- **姿勢推定**: MediaPipe Poseを使用した人体の33個のランドマーク検出
- **リアルタイム可視化**: Rerunによる動画と姿勢データの同期表示
- **進捗表示**: 20フレームごとに処理状況をコンソールに出力

## プロジェクト構成

```
pose-estimation/
├── README.md           # このファイル
├── main.py            # メインスクリプト
├── pyproject.toml     # プロジェクト設定と依存関係
├── uv.lock           # 依存関係のロックファイル
└── data/
    └── original/     # 入力動画ファイルを配置
```

## 依存パッケージ

- `mediapipe`: 姿勢推定用のライブラリ
- `rerun-sdk`: データ可視化ツール
- `yt-dlp`: YouTube動画のダウンロード（オプション）
- `opencv-python`: 動画処理（MediaPipeが自動インストール）
- `numpy`: 数値計算

## トラブルシューティング

### エラー: MP4ファイルが見つからない
`data/original/` ディレクトリにMP4ファイルが配置されているか確認してください。

### Rerunビューアが起動しない
Rerunの最新バージョンがインストールされているか確認：
```bash
uv pip list | grep rerun
```
