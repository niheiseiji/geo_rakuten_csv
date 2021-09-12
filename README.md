# 位置情報APIとホテル検索APIでホテル一覧CSVを出力する
## 実装した処理の流れ  
１．場所をコマンドライン引数で指定しgoogle Geocoding APIで緯度経度を取得  
２．取得した緯度経度からコマンドライン引数で指定した距離県内にあるホテル一覧を楽天トラベ
ルAPIで取得  
３．取得したホテル一覧をCSVで出力する  

## 使用例
geo_rakuten_csv> python .\geo_travel_csv.py 東京駅 2 #東京駅から2km以内の宿を検索  
出力されるCSVのサンプルはhotel.csvを参照
