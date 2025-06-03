import subprocess
import sys
import argparse
import pathlib
import platform
import os

# --- 定数 ---
DEFAULT_COOKIES_FILENAME = "cookies.txt"

def is_iphone_environment():
    """iPhone (a-Shellのような環境) かどうかを簡易的に判定"""
    if platform.system() == "Darwin":
        # macOSでもplatform.system()はDarwinを返すため、より詳細な判定が必要だが、
        # a-Shell上では'iPad'や'iPhone'といった情報がplatform.platform()に含まれることがある。
        # ここでは単純化のため、Darwin以外を非iPhone的、DarwinをiPhone/macOSの可能性ありとする。
        # より確実なのはa-Shellの環境変数などを確認することだが、ここではシンプルに。
        # 簡単な判別として、ユーザーホームディレクトリの構造などで推測することも。
        # 今回は、デフォルトパスの分岐のために使う。
        return "iPhone" in platform.platform() or "iPad" in platform.platform()
    return False

def get_default_output_dir():
    """環境に応じてデフォルトの出力ディレクトリを返す"""
    if is_iphone_environment():
        # a-Shell の場合、Documents フォルダがアクセスしやすい
        return pathlib.Path.home() / "Documents"
    else:
        # PC (Windows, macOS, Linux) の場合、Downloads フォルダ
        return pathlib.Path.home() / "Downloads"

def install_or_update_ytdlp():
    """yt-dlpをインストールまたはアップデートする"""
    print("yt-dlp のインストール/アップデートを確認しています...")
    try:
        # a-Shell 環境など、pipが直接使えることを想定
        # subprocess.run(['pip', 'install', '--upgrade', 'yt-dlp'], check=True, capture_output=True, text=True)
        # より確実性を高めるため、python -m pip を使う
        subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'yt-dlp'],
                       check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print("yt-dlp は最新またはアップデートされました。")
        return True
    except subprocess.CalledProcessError as e:
        print(f"yt-dlp のインストール/アップデート中にエラーが発生しました:\n{e.stderr}")
        return False
    except FileNotFoundError:
        print("pip (python -m pip) コマンドが見つかりません。Python環境を確認してください。")
        return False

def download_video_with_ytdlp(video_url, cookies_path, output_dir):
    """yt-dlp を使って動画をダウンロードする"""
    print(f"動画URL: {video_url}")
    print(f"クッキーファイル: {cookies_path}")
    print(f"出力ディレクトリ: {output_dir}")

    if not output_dir.exists():
        print(f"出力ディレクトリ {output_dir} を作成します。")
        output_dir.mkdir(parents=True, exist_ok=True)

    # yt-dlp コマンドの構築
    # ニコニコ動画プレミアム会員向け:
    # -f 'bestvideo+bestaudio/best' : 最高画質と最高音声を試み、なければ次善を選ぶ
    # --merge-output-format mp4 : 映像と音声をMP4にマージ
    # --write-thumbnail : サムネイルを別ファイルとしてダウンロード
    # --embed-thumbnail : ダウンロードしたサムネイルを動画ファイルに埋め込む (ffmpegが必要)
    #     埋め込みが成功すれば、別途ffmpegを呼び出す必要はない
    # -o "{output_dir}/%(title)s [%(id)s].%(ext)s" : 出力ファイル名テンプレート
    #     %(title)s: 動画タイトル
    #     %(id)s: 動画ID (重複回避のため)
    #     %(ext)s: 拡張子
    # --cookies {cookies_path} : クッキーファイルを指定
    # --no-check-certificate : SSL証明書のエラーを無視 (環境による問題回避のため、注意して使用)
    # --no-playlist : プレイリスト内の動画をダウンロードしない (単一動画のみ対象)
    # --progress : ダウンロード進捗を表示

    # 注意: ニコニコ動画の最高画質・音質指定は `-f` オプションでより具体的にフォーマットコードを指定する方が確実な場合があります。
    # yt-dlp -F <動画URL> --cookies <クッキーファイル> で利用可能なフォーマットを確認できます。
    # 例: -f <video_format_code>+<audio_format_code>
    # ここでは一般的な 'bestvideo+bestaudio/best' を使用します。

    cmd = [
        'yt-dlp',
        '--cookies', str(cookies_path),
        '-f', 'bestvideo+bestaudio/best', # 最高画質・音質 (ニコニコの仕様によっては調整が必要)
        '--merge-output-format', 'mp4',
        '--write-thumbnail',
        '--embed-thumbnail', # ffmpegがシステムにインストールされている必要がある
        # '--convert-thumbnails', 'jpg', # embed-thumbnailがjpg以外を扱えない場合に備えても良いが、通常は不要
        '-o', str(output_dir / "%(title)s [%(id)s].%(ext)s"),
        '--no-check-certificate', # 環境によって必要になる場合がある
        '--no-playlist',
        '--progress',
        video_url
    ]

    print("\n実行コマンド:")
    print(' '.join(cmd)) # 実際のコマンドを表示 (デバッグ用)

    try:
        # universal_newlines=True は非推奨。代わりに text=True を使用。
        # capture_output=True にすると標準出力/エラーがキャプチャされる。進捗表示のためFalse。
        process = subprocess.Popen(cmd, stdout=sys.stdout, stderr=sys.stderr)
        process.wait() # プロセスの終了を待つ

        if process.returncode == 0:
            print("\nダウンロードが正常に完了しました。")
        else:
            print(f"\nダウンロード中にエラーが発生しました (yt-dlp 終了コード: {process.returncode})。")
            # エラーの詳細はyt-dlpが出力するはず

    except FileNotFoundError:
        print("yt-dlp コマンドが見つかりません。パスが通っているか、インストールされているか確認してください。")
    except Exception as e:
        print(f"yt-dlp の実行中に予期せぬエラーが発生しました: {e}")


def main():
    parser = argparse.ArgumentParser(description="ニコニコ動画をyt-dlpでダウンロードします（プレミアム会員向け）。")
    parser.add_argument("video_url", help="ダウンロードするニコニコ動画のURL。")
    parser.add_argument(
        "--cookies",
        default=None,
        help=f"クッキーファイルのパス。指定しない場合、スクリプトと同じディレクトリの '{DEFAULT_COOKIES_FILENAME}' を試みます。"
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="出力ディレクトリのパス。指定しない場合、環境に応じて自動設定されます。"
    )

    args = parser.parse_args()

    # 0. yt-dlpのインストール/アップデート試行
    if not install_or_update_ytdlp():
        print("yt-dlpの準備に失敗したため、処理を中断します。")
        sys.exit(1)

    # 1. クッキーファイルのパス解決
    if args.cookies:
        cookies_file_path = pathlib.Path(args.cookies).expanduser().resolve()
    else:
        # スクリプトのディレクトリを取得
        script_dir = pathlib.Path(__file__).parent.resolve()
        cookies_file_path = script_dir / DEFAULT_COOKIES_FILENAME

    if not cookies_file_path.is_file():
        print(f"エラー: クッキーファイルが見つかりません: {cookies_file_path}")
        print(f"ニコニコ動画にログインしたブラウザから {DEFAULT_COOKIES_FILENAME} という名前でエクスポートし、")
        print(f"スクリプトと同じディレクトリに置くか、--cookies オプションで正しいパスを指定してください。")
        sys.exit(1)

    # 2. 出力ディレクトリのパス解決
    if args.output_dir:
        output_directory = pathlib.Path(args.output_dir).expanduser().resolve()
    else:
        output_directory = get_default_output_dir()

    # 3. ダウンロード実行
    download_video_with_ytdlp(args.video_url, cookies_file_path, output_directory)

if __name__ == "__main__":
    main()
