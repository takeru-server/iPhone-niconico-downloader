# download_niconico.py (プレースホルダー版)

import sys
import subprocess
from pathlib import Path
import tempfile

# --- プレースホルダー (この部分がショートカットで置換される) ---
# この文字列は絶対にクッキーやURLに含まれない、ユニークなものにする
COOKIE_DATA = "__COOKIE_PLACEHOLDER__"
VIDEO_URL = "__URL_PLACEHOLDER__"

# --- 設定 ---
DOWNLOAD_DIR = Path.home() / "Documents" / "NicoNico"

def check_and_update_tools():
    """yt-dlpとffmpegのインストール・更新を行う"""
    print("1/4: ツールの更新を確認・実行します...")
    try:
        # yt-dlpの更新
        subprocess.run(["pip", "install", "-U", "yt-dlp"], check=True, capture_output=True, text=True)
        print("- yt-dlpの更新完了")
        # ffmpegの更新 (a-shellのパッケージマネージャ)
        subprocess.run(["pkg", "update", "ffmpeg"], check=True, capture_output=True, text=True)
        print("- ffmpegの更新完了")
    except subprocess.CalledProcessError as e:
        print(f"ツールの更新中にエラーが発生しました: {e.stderr}")
        # 続行不能なエラーではないので、処理は続ける
    except FileNotFoundError as e:
        print(f"コマンドが見つかりません: {e.name}。a-shell環境が正しく設定されているか確認してください。")
        sys.exit(1)

def main():
    """メインのダウンロード処理"""
    # プレースホルダーが置換されているかチェック (安全装置)
    if "__COOKIE_PLACEHOLDER__" in COOKIE_DATA or "__URL_PLACEHOLDER__" in VIDEO_URL:
        print("エラー: スクリプト内のクッキーまたはURLが正しく置換されませんでした。")
        print("ショートカットの設定を確認してください。")
        sys.exit(1)

    print("\n2/4: 初期設定を開始します...")
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
    print(f"ダウンロードフォルダを確認: {DOWNLOAD_DIR}")

    # クッキーを一時ファイルに書き込む (安全な方法)
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".txt") as temp_file:
        temp_file.write(COOKIE_DATA)
        cookie_filepath = temp_file.name
    print("クッキーを一時ファイルに保存しました。")

    print("\n3/4: ダウンロードを開始します...")
    print("========================================")

    command = [
        "yt-dlp",
        "-P", str(DOWNLOAD_DIR),
        "--cookies", cookie_filepath,
        "-f", "bestvideo[height>=1080]+bestaudio/best",
        "--merge-output-format", "mp4",
        "--embed-thumbnail",
        "--no-mtime",
        "--progress",
        VIDEO_URL
    ]

    try:
        subprocess.run(command, check=True)
    except Exception as e:
        print(f"ダウンロード処理中にエラーが発生しました: {e}")
    finally:
        # 一時クッキーファイルを必ず削除する
        Path(cookie_filepath).unlink()
        print("一時ファイルをクリーンアップしました。")

    print("========================================")
    print("4/4: ダウンロードが完了しました！")
    print(f"保存先: ファイルアプリ -> このiPhone内 -> a-shell -> {DOWNLOAD_DIR.name}")


# --- スクリプト実行部分 ---
check_and_update_tools()
main()
