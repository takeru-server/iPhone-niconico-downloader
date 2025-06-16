# download_niconico.py (最終完成版)

import sys
import subprocess
from pathlib import Path
import tempfile

# --- プレースホルダー (このユニークな文字列をショートカットで置換します) ---
COOKIE_DATA = "__COOKIE_PLACEHOLDER__"
VIDEO_URL = "__URL_PLACEHOLDER__"

# --- 設定 ---
DOWNLOAD_DIR = Path.home() / "Documents" / "NicoNico"

def check_and_update_tools():
    """yt-dlpとffmpegのインストール・更新を行う"""
    print("1/4: ツールの更新を確認・実行します...")
    try:
        # pipとyt-dlpを一度に更新（あなたの改善案を採用）
        subprocess.run(["python3", "-m", "pip", "install", "-U", "pip", "yt-dlp"], check=True, capture_output=True, text=True)
        print("- pip, yt-dlpの更新完了")
        # ffmpegの更新
        subprocess.run(["pkg", "update", "ffmpeg"], check=True, capture_output=True, text=True)
        print("- ffmpegの更新完了")
    except subprocess.CalledProcessError as e:
        # エラーが出ても、既に最新版である場合が多いので、警告のみで処理は続行
        print(f"ツールの更新中に情報メッセージが出力されました: {e.stderr.strip()}")
    except FileNotFoundError as e:
        print(f"エラー: コマンドが見つかりません: {e.name}。a-shellが正しく設定されていません。")
        sys.exit(1)

def main():
    """メインのダウンロード処理"""
    # 安全装置：プレースホルダーが置換されずに残っていたら、エラーで停止
    if COOKIE_DATA == "__COOKIE_PLACEHOLDER__" or VIDEO_URL == "__URL_PLACEHOLDER__":
        print("エラー: スクリプト内のクッキーまたはURLが正しく置換されませんでした。")
        print("ショートカットの「テキストを置換」アクションの設定を確認してください。")
        sys.exit(1)

    print("\n2/4: 初期設定を開始します...")
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
    print(f"ダウンロードフォルダを確認: {DOWNLOAD_DIR}")

    # クッキーを一時ファイルに書き込む
    cookie_filepath = ""
    try:
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".txt", encoding='utf-8') as temp_file:
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
        
        # ダウンロード実行
        subprocess.run(command, check=True)

    except Exception as e:
        print(f"処理中にエラーが発生しました: {e}")
    finally:
        # 一時クッキーファイルが作られていたら、必ず削除する
        if cookie_filepath and Path(cookie_filepath).exists():
            Path(cookie_filepath).unlink()
            print("一時ファイルをクリーンアップしました。")

    print("========================================")
    print("4/4: ダウンロードが完了しました！")
    print(f"保存先: ファイルアプリ -> このiPhone内 -> a-shell -> {DOWNLOAD_DIR.name}")


# --- スクリプト実行部分 ---
check_and_update_tools()
main()
