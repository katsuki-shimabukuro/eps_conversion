import os
import sys
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader

def create_pdf_from_images(folder_path):
    # 出力するPDFのファイル名（対象フォルダ内に作成します）
    output_pdf_path = os.path.join(folder_path, "output.pdf")

    # 指定フォルダからJPEG画像を取得 (.jpg, .jpeg)
    valid_extensions = ('.jpg', '.jpeg')
    image_files = [
        os.path.join(folder_path, f) for f in os.listdir(folder_path)
        if f.lower().endswith(valid_extensions)
    ]
    
    if not image_files:
        print("指定されたフォルダにJPEG画像が見つかりませんでした。")
        return

    # 順番がバラバラにならないよう名前順でソート
    image_files.sort()

    # PDFのセットアップ
    c = canvas.Canvas(output_pdf_path, pagesize=A4)
    a4_width, a4_height = A4
    
    # レイアウト設定 (2列 x 3行 = 1ページ6枚)
    cols = 2
    rows = 3
    images_per_page = cols * rows
    
    # ページ全体の余白と、1枚あたりのセルサイズを計算
    margin_x = 30
    margin_y = 30
    cell_width = (a4_width - margin_x * 2) / cols
    cell_height = (a4_height - margin_y * 2) / rows

    for i, img_path in enumerate(image_files):
        # 7枚目以降など、ページ規定枚数に達したら新しいページを追加
        if i > 0 and i % images_per_page == 0:
            c.showPage()
        
        # 現在のページ内での位置インデックス (0 〜 5)
        page_idx = i % images_per_page
        col_idx = page_idx % cols
        row_idx = page_idx // cols
        
        # セルの左下座標を計算 (ReportLabは左下が原点[0,0])
        # 行は上から下へ配置するため、Y座標は上からマイナスしていく
        cell_x = margin_x + col_idx * cell_width
        cell_y = a4_height - margin_y - (row_idx + 1) * cell_height
        
        try:
            # 画像を読み込み、サイズを取得
            img = Image.open(img_path)
            img_w, img_h = img.size
            
            # 縦横比を維持したまま、セルに収まる縮小率(スケール)を計算
            scale = min(cell_width / img_w, cell_height / img_h)
            
            # 画像同士がくっつかないよう、セルに対して少し(95%)小さく描画サイズを決定
            draw_w = img_w * scale * 0.95
            draw_h = img_h * scale * 0.95
            
            # セル内で画像を中央揃えにするためのオフセット調整
            offset_x = (cell_width - draw_w) / 2
            offset_y = (cell_height - draw_h) / 2
            
            # 画像のみをPDFに描画（テキストやファイル名は出力しない）
            c.drawImage(ImageReader(img), cell_x + offset_x, cell_y + offset_y, width=draw_w, height=draw_h)
            
        except Exception as e:
            print(f"画像 {img_path} の処理中にエラーが発生しました: {e}")
            
    # PDFを保存
    c.save()
    print(f"処理が完了しました。PDFを保存しました: {output_pdf_path}")

if __name__ == "__main__":
    # コマンドライン引数でフォルダパスを受け取る
    if len(sys.argv) != 2:
        print("使用方法: python img_to_pdf.py <画像フォルダのパス>")
        sys.exit(1)
        
    target_folder = sys.argv[1]
    
    if not os.path.isdir(target_folder):
        print("エラー: 有効なフォルダパスを指定してください。")
        sys.exit(1)
        
    create_pdf_from_images(target_folder)