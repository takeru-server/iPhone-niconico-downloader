#!/bin/sh

# --- 自己アップデート処理 ---
echo "1/3: Checking for tool updates..."
python3 -m pip install --upgrade pip > /dev/null 2>&1
pip install -U yt-dlp > /dev/null 2>&1
pkg update ffmpeg > /dev/null 2>&1

# --- メイン処理 ---
DOWNLOAD_DIR="$HOME/Documents/NicoNico"
mkdir -p "$DOWNLOAD_DIR"

# 変数を定義（ここが重要！）
# シェルに特殊文字と解釈させないよう、シングルクォートで囲むのが安全
COOKIE='Cookie'
URL='URL'
FORMAT_SPEC='bestvideo[height>=1080]+bestaudio/best'

echo "2/3: Starting download..."
echo "========================================"

# yt-dlpを実行（最も安全な形）
yt-dlp \
    -P "$DOWNLOAD_DIR" \
    --add-header "Cookie: $COOKIE" \
    -f "$FORMAT_SPEC" \
    --merge-output-format mp4 \
    --embed-thumbnail \
    --no-mtime \
    --progress \
    -- "$URL"

echo "========================================"
echo "3/3: Download completed!"
echo "File saved in: Files App -> a-shell -> Documents -> NicoNico"
