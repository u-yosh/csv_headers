


# csv_headers.py
フォルダ内にCSVファイルがあり、その状態をさっと確認したい時に使ってください。
先頭行を指定行数分表示します。
Tkinterが必要になります。


## 確認済みライブラリのバージョンと環境
Python 3.6.2
Tkinter 8.6.8
pandas 1.1.5

macOS Catalina 10.15.7


## スクリプト起動
```
python csv_headers.py
```


## 使い方
1.CSVの先頭からの行数（カラム名も含む）を指定します。
2.ボタンをクリックするとダイアログが表示されるので、調べたいCSVが入ったフォルダを選択します。

以下のように表示され、見えない範囲を表示するにはスクロールが必要です。
<img width="1197" alt="スクリーンショット 2023-03-03 18 14 41" src="https://user-images.githubusercontent.com/9311234/222681010-e3c8d4fa-9084-4864-806f-a1fa2f6f54b9.png">

検証に使ったCSVデータは以下のサイト様で生成しています。
https://tm-webtools.com/Tools/TestData
