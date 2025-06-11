#!/bin/sh

# --- 自己アップデート処理 ---
# 実行中のメッセージを分かりやすく表示
echo "1/3: Checking for tool updates..."
# pip, yt-dlp, ffmpegをアップデート。不要な出力は抑制。
python3 -m pip install --upgrade pip > /dev/null 2>&1
pip install -U yt-dlp > /dev/null 2>&1
pkg update ffmpeg > /dev/null 2>&1

# --- メイン処理 ---
# 引数からCookieとURLを受け取る
COOKIE="$0"
URL="$1"

# ダウンロード先のフォルダを定義し、なければ作成
DOWNLOAD_DIR="$HOME/Documents/NicoNico"
mkdir -p "$DOWNLOAD_DIR"

echo "2/3: Starting download..."
echo "========================================"

# yt-dlpを実行
yt-dlp \
    -P "$DOWNLOAD_DIR" \
    --add-header "Cookie: $COOKIE" \
    -f "bestvideo[height>=1080]+bestaudio/best" \
    --merge-output-format mp4 \
    --embed-thumbnail \
    --no-mtime \
    --progress \
    "$URL"

echo "========================================"
echo "3/3: Download completed!"
echo "File saved in: Files App -> a-shell -> Documents -> NicoNico"
