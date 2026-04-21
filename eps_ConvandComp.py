'''
今いるフォルダを処理する場合
python3 eps_compress.py

別の場所にあるフォルダを処理する場合
WSL内：python3 eps_compress.py ./fig
Windows内：python3 eps_compress.py /mnt/c/Users/なまえ/Desktop/my_eps_folder
'''

import subprocess
import os
import pathlib
import argparse
from PIL import Image

def process_images_to_compressed_eps(target_dir):
    image_dir = pathlib.Path(target_dir).resolve()
    output_dir = image_dir / "out"

    if not image_dir.exists() or not image_dir.is_dir():
        print(f"エラー: フォルダが見つかりません ({image_dir})")
        return

    # 出力フォルダの作成
    output_dir.mkdir(exist_ok=True)

    # --- 設定 ---
    TARGET_WIDTH = 1000 
    extensions = {'.jpg', '.jpeg', '.png'}
    count = 0

    print(f"\n--- 学会投稿用 EPS変換 & 圧縮ワークフロー ---")
    print(f"入力: {image_dir}")
    print(f"出力: {output_dir}\n")

    for img_path in image_dir.iterdir():
        if img_path.suffix.lower() in extensions:
            # 中間ファイル（圧縮前）のパス
            temp_eps = output_dir / f"temp_{img_path.stem}.eps"
            # 最終的な出力パス
            final_eps = output_dir / f"{img_path.stem}.eps"
            
            try:
                # 1. PILによるEPS変換とリサイズ
                img = Image.open(img_path)
                img = img.convert('RGB')

                if img.width > TARGET_WIDTH:
                    ratio = TARGET_WIDTH / float(img.width)
                    new_height = int(float(img.height) * float(ratio))
                    img = img.resize((TARGET_WIDTH, new_height), Image.Resampling.LANCZOS)
                
                # 一旦一時ファイルとして保存
                img.save(temp_eps, 'EPS', dpi=(300.0, 300.0))

                # 2. Ghostscriptによる圧縮処理
                gs_command = [
                    "gs", "-dNOPAUSE", "-dBATCH", "-dSAFER",
                    "-sDEVICE=eps2write",
                    "-dEPSCrop",
                    "-dCompressFonts=true",
                    f"-sOutputFile={final_eps}",
                    str(temp_eps)
                ]
                
                subprocess.run(gs_command, check=True, capture_output=True)

                # 3. 中間ファイルの削除
                if temp_eps.exists():
                    temp_eps.unlink()

                # 結果表示
                size_mb = final_eps.stat().st_size / (1024 * 1024)
                print(f"成功: {img_path.name} -> out/{final_eps.name} ({size_mb:.2f} MB)")
                count += 1
                
            except Exception as e:
                print(f"失敗: {img_path.name} (理由: {e})")
                if temp_eps.exists():
                    temp_eps.unlink()

    print(f"\n完了しました。{count}枚のファイルを処理しました。")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="画像をEPSに変換し、Ghostscriptで圧縮してoutフォルダに保存します")
    parser.add_argument("dir", nargs='?', default=".", help="対象フォルダパス（デフォルトは現在のフォルダ）")

    args = parser.parse_args()
    process_images_to_compressed_eps(args.dir)