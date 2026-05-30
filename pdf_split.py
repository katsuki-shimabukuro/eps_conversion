import os
from pathlib import Path
from pypdf import PdfReader, PdfWriter

def split_all_pdfs_in_dir():
    # 1. ユーザーから対象フォルダのパスを入力してもらう
    input_input = input("PDFが格納されているフォルダのパスを入力してください: ").strip()
    
    # クォーテーションマークの除去
    input_input = input_input.strip("'\"")

    # pathlib.Pathオブジェクトに変換
    print(f"指定されたフォルダ: {input_input}")
    target_dir = Path(input_input)
    print(f"指定されたフォルダ: {target_dir}")

    # フォルダの存在チェック
    if not target_dir.is_dir():
        print(f"エラー: 指定されたフォルダが見つからないか、ディレクトリではありません: {target_dir}")
        return

    # 2. フォルダ内の全PDFファイルを検索 (拡張子が .pdf または .PDF のもの)
    pdf_files = list(target_dir.glob("*.pdf")) + list(target_dir.glob("*.PDF"))

    if not pdf_files:
        print(f"指定されたフォルダ内にPDFファイルが見つかりませんでした: {target_dir}")
        return

    print(f"\n{len(pdf_files)} 個のPDFファイルが見つかりました。処理を開始します...\n")

    # 3. 各PDFファイルを順に処理
    for pdf_path in pdf_files:
        print(f"--- 処理中: {pdf_path.name} ---")
        
        # 各PDFと同じ層に「out」フォルダのパスを設定して作成
        output_dir = pdf_path.parent / "out"
        output_dir.mkdir(parents=True, exist_ok=True)

        try:
            reader = PdfReader(str(pdf_path))
            total_pages = len(reader.pages)
            base_name = pdf_path.stem

            # 1ページずつ分割して保存
            for page_num in range(total_pages):
                writer = PdfWriter()
                writer.add_page(reader.pages[page_num])

                output_filename = f"{base_name}_page_{page_num + 1}.pdf"
                output_path = output_dir / output_filename

                with open(output_path, "wb") as f_out:
                    writer.write(f_out)
                
            print(f"⇒ 成功: {total_pages} ページに分割して '{output_dir.name}' に保存しました。")

        except Exception as e:
            print(f"⇒ エラー（スキップします）: {pdf_path.name} の処理中に問題が発生しました: {e}")
        
        print() # 改行用

    print("すべてのPDFファイルの処理が完了しました！")

if __name__ == "__main__":
    split_all_pdfs_in_dir()