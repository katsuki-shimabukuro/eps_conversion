# eps_ConvandComp
jpg, jpeg, pngの画像ファイルをepsに変換し、圧縮するコード

## eps_ConvandComp.pyの実行方法
#### 今いるフォルダを処理する場合
`python3 eps_compress.py`  

#### 別の場所にあるフォルダを処理する場合  
WSL内：`python3 eps_compress.py ./fig`  
Windows内：`python3 eps_compress.py /mnt/c/Users/なまえ/Desktop/my_eps_folder`  
※フォルダは任意。

# img to pdf
jpg画像ファイルをA4サイズに6枚ずつ添付して出力するコード

## img_to_pdf.pyの実行方法  
`python3 img_to_pdf.py フォルダ名`  

# pdf Compression  
pdfを圧縮して出力するコード  

## pdf_Compression.pyの実行方法
`python3 pdf_Compression.py <対象フォルダパス>`  

# pdf split
pdfを分割するコード

## pdf_split.pyの実行方法
`python3 pdf_split.py`
対象フォルダを聞かれるので、pdfファイルのあるフォルダを指定。  
このとき、フォルダの中にはpdfは1つであること。2つ以上はできるか不明。