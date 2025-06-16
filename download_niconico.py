# download_niconico.py (安全装置の判定を削除したバージョン)

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
    print("1/3: ツールの更新を確認・実行します...")
    try:
        # pipとyt-dlpを一度に更新
        subprocess.run(["python3", "-m", "pip", "install", "-U", "pip", "yt-dlp"], check=True, capture_output=True, text=True)
        print("- pip, yt-dlpの更新完了")
        # ffmpegの更新
        subprocess.run(["pkg", "update", "ffmpeg"], check=True, capture_output=True, text=True)
        print("- ffmpegの更新完了")
    except subprocess.CalledProcessError as e:
        print(f"ツールの更新中に情報メッセージが出力されました: {e.stderr.strip()}")
    except FileNotFoundError as e:
        print(f"エラー: コマンドが見つかりません: {e.name}。a-shellが正しく設定されていません。")
        sys.exit(1)

def main():
    """メインのダウンロード処理"""
    print("\n2/3: 初期設定とダウンロードを開始します...")
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
    
    cookie_filepath = ""
    try:
        # 一時ファイルにクッキーを書き出す
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".txt", encoding='utf-8') as temp_file:
            temp_file.write(COOKIE_DATA)
            cookie_filepath = temp_file.name
        print("クッキーを一時ファイルに保存しました。")
        
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
        # スクリプトの終了時に、一時クッキーファイルが作られていたら必ず削除する
        if cookie_filepath and Path(cookie_filepath).exists():
            Path(cookie_filepath).unlink()
            print("一時ファイルをクリーンアップしました。")

    print("========================================")
    print("3/3: ダウンロードが完了しました！")
    print(f"保存先: ファイルアプリ -> このiPhone内 -> a-shell -> {DOWNLOAD_DIR.name}")


# --- スクリプト実行開始 ---
check_and_update_tools()
main()
