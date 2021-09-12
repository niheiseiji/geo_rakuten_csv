import sys
import googlemaps
import requests
import pandas as pd
import setting # 設定ファイル

GOOGLE_API_KEY = (setting.GOOGLE_API_KEY)
RAKUTEN_REQUEST_URL = 'https://app.rakuten.co.jp/services/api/Travel/SimpleHotelSearch/20170426?'
RAKUTEN_APP_ID = (setting.RAKUTEN_APP_ID)

# 検索地点の緯度経度を取得
def get_geocode(search_place: str):
    gmaps = googlemaps.Client(key=GOOGLE_API_KEY)
    gmap_list = gmaps.geocode(search_place) # 場所がないとき空配列を返す
    # 場所が見つからないとき
    if len(gmap_list) == 0:
        print('お探しの場所が見つかりませんでした')
        sys.exit()
    ll = gmap_list[0]["geometry"]["location"]
    return ll

# 検索地点から探索範囲内のホテルを取得
def get_hotels(lat: float, lng: float, search_range: int):
    params = {
        'applicationId': RAKUTEN_APP_ID,
        'format': 'json',
        'latitude': lat,
        'longitude': lng,
        'searchRadius': search_range,
        'datumType': 1 # 世界測地系、単位は度
    }

    try:
        res = requests.get(RAKUTEN_REQUEST_URL, params)
        result = res.json()
        # 取得件数0のとき
        if res.status_code != requests.codes.ok:
            print('指定された場所の周辺にホテルが見つかりませんでした。')
            sys.exit()
        hotels = result['hotels']
        return hotels
    except requests.exceptions.RequestException as e:
        print("error: {}", e, format(res.status_code))

# ホテル一覧をCSVで出力
def output_hotels_csv(hotels: list):
    df = pd.DataFrame()
    for i, hotel in enumerate(hotels):
        hotel_info = hotel['hotel'][0]['hotelBasicInfo']
        _df = pd.DataFrame(hotel_info, index=[i])
        df = df.append(_df)

    df.columns
    df[['hotelName', 'hotelMinCharge', 'reviewAverage', 'reviewCount','telephoneNo', 'hotelInformationUrl', 'access' , 'parkingInformation']].to_csv('hotel.csv', index=False)

# 探索範囲のデフォルト値(km)
range = 1

# コマンドライン引数を受け取る
argc = len(sys.argv)
if argc == 2:
    place = sys.argv[1]
elif argc == 3:
    place = sys.argv[1]
    range = sys.argv[2]
else:
    sys.exit("usage: python {} [search place] [search range]".format(sys.argv[0]))

ll = get_geocode(place)
hotel_list = get_hotels(ll['lat'], ll['lng'], range)
output_hotels_csv(hotel_list)
