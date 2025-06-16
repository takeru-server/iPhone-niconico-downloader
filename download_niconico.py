# download_niconico.py (プレースホルダー版)

import sys
import subprocess
from pathlib import Path
import tempfile

# --- プレースホルダー (この部分がショートカットで置換される) ---
COOKIE_DATA = "cwr_s=eyJzZXNzaW9uSWQiOiJhY2EyZjdjZi02MWVhLTQwY2UtYjNiMi02NWRiOTJhOTE3ZWIiLCJyZWNvcmQiOmZhbHNlLCJldmVudENvdW50IjoxODQsInBhZ2UiOnsicGFnZUlkIjoiL3dhdGNoL3NtMjA4Mzc0MjUiLCJwYXJlbnRQYWdlSWQiOiIvIiwiaW50ZXJhY3Rpb24iOjEsInJlZmVycmVyIjoiaHR0cHM6Ly9zcC5uaWNvdmlkZW8uanAvbXkvaGlzdG9yeS92aWRlbz9jbW5oZF9yZWY9ZGV2aWNlJTNEc3AlMjZzaXRlJTNEc3BuaWNvbmljbyUyNnBvcyUzRHVzZXJwYW5lbCUyNnBhZ2UlM0RyYW5raW5nIiwicmVmZXJyZXJEb21haW4iOiJzcC5uaWNvdmlkZW8uanAiLCJzdGFydCI6MTc1MDA0MzMzNTk3Mn19; cwr_u=aa4335e3-ce49-4b11-b7e0-63dc96b58862; common-header-oshirasebox-new-allival=false; lastViewedRanking=%7B%22type%22%3A%22for-you%22%7D; _ss_pp_id=8fec9ca6326026b07911749441939818; _td=5dbaf9c0-618a-4a13-9a0b-b7b3a3ebeb0a; nicosid=1747657249.4171874428"
VIDEO_URL = "https://sp.nicovideo.jp/watch/sm20837425?ref=my_history"

# --- 設定 ---
DOWNLOAD_DIR = Path.home() / "Documents" / "NicoNico"

def check_and_update_tools():
    """yt-dlpとffmpegのインストール・更新を行う"""
    print("1/4: ツールの更新を確認・実行します...")
    try:
        # pipとyt-dlpの更新
        subprocess.run(["python3", "-m", "pip", "install", "-U", "pip", "yt-dlp"], check=True, capture_output=True, text=True)
        print("- pip, yt-dlpの更新完了")
        # ffmpegの更新
        subprocess.run(["pkg", "update", "ffmpeg"], check=True, capture_output=True, text=True)
        print("- ffmpegの更新完了")
    except subprocess.CalledProcessError as e:
        print(f"ツールの更新中にエラーが発生しました: {e.stderr}")
    except FileNotFoundError as e:
        print(f"コマンドが見つかりません: {e.name}")
        sys.exit(1)

def main():
    """メインのダウンロード処理"""
    # 【重要】安全装置のロジックを修正
    # 変数の中身が、元のプレースホルダーと完全に一致する場合のみエラーとする
    if COOKIE_DATA == "cwr_s=eyJzZXNzaW9uSWQiOiJhY2EyZjdjZi02MWVhLTQwY2UtYjNiMi02NWRiOTJhOTE3ZWIiLCJyZWNvcmQiOmZhbHNlLCJldmVudENvdW50IjoxODQsInBhZ2UiOnsicGFnZUlkIjoiL3dhdGNoL3NtMjA4Mzc0MjUiLCJwYXJlbnRQYWdlSWQiOiIvIiwiaW50ZXJhY3Rpb24iOjEsInJlZmVycmVyIjoiaHR0cHM6Ly9zcC5uaWNvdmlkZW8uanAvbXkvaGlzdG9yeS92aWRlbz9jbW5oZF9yZWY9ZGV2aWNlJTNEc3AlMjZzaXRlJTNEc3BuaWNvbmljbyUyNnBvcyUzRHVzZXJwYW5lbCUyNnBhZ2UlM0RyYW5raW5nIiwicmVmZXJyZXJEb21haW4iOiJzcC5uaWNvdmlkZW8uanAiLCJzdGFydCI6MTc1MDA0MzMzNTk3Mn19; cwr_u=aa4335e3-ce49-4b11-b7e0-63dc96b58862; common-header-oshirasebox-new-allival=false; lastViewedRanking=%7B%22type%22%3A%22for-you%22%7D; _ss_pp_id=8fec9ca6326026b07911749441939818; _td=5dbaf9c0-618a-4a13-9a0b-b7b3a3ebeb0a; nicosid=1747657249.4171874428" or VIDEO_URL == "https://sp.nicovideo.jp/watch/sm20837425?ref=my_history":
        print("エラー: スクリプト内のクッキーまたはURLが正しく置換されませんでした。")
        print("ショートカットの設定を確認してください。")
        sys.exit(1)

    print("\n2/4: 初期設定を開始します...")
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
    print(f"ダウンロードフォルダを確認: {DOWNLOAD_DIR}")

    # クッキーを一時ファイルに書き込む (安全な方法)
    # withブロックを使えば、処理が終わった後にファイルが自動で閉じられる
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

    try:
        # check=Trueで、コマンドが失敗した場合にエラーを発生させる
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
