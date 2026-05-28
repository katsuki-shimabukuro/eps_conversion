import sys
from pathlib import Path
import fitz  # PyMuPDF

def compress_pdfs_powerful():
    if len(sys.argv) < 2:
        print("使用法: python3 compress.py <対象フォルダパス>")
        return

    input_path = Path(sys.argv[1].strip())
    if not input_path.is_dir():
        print(f"エラー: '{input_path}' は有効なフォルダではありません。")
        return

    output_path = input_path / "out"
    output_path.mkdir(exist_ok=True)

    pdf_files = list(input_path.glob("*.pdf"))
    
    if not pdf_files:
        print("PDFファイルが見つかりませんでした。")
        return

    print(f"--- 強力圧縮開始: {len(pdf_files)} ファイル ---")

    for pdf_file in pdf_files:
        try:
            # PDFを開く
            doc = fitz.open(pdf_file)
            
            save_path = output_path / pdf_file.name

            # 圧縮して保存
            # garbage=4 : 重複オブジェクトの徹底削除
            # deflate=True : ストリームの圧縮
            # clean=True : コンテンツのクリーンアップ
            doc.save(
                save_path, 
                garbage=4, 
                deflate=True, 
                clean=True
            )
            doc.close()
            
            # サイズ比較を表示
            original_size = pdf_file.stat().st_size / 1024
            compressed_size = save_path.stat().st_size / 1024
            reduction = (1 - compressed_size / original_size) * 100
            
            print(f"成功: {pdf_file.name} ({original_size:.1f}KB -> {compressed_size:.1f}KB / -{reduction:.1f}%)")

        except Exception as e:
            print(f"失敗: {pdf_file.name} -> {e}")

    print(f"--- 完了！ 出力先: {output_path} ---")

if __name__ == "__main__":
    compress_pdfs_powerful()