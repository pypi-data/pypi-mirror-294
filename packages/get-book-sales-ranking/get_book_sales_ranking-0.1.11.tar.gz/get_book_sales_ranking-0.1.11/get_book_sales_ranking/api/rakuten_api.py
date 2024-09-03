# # 楽天api
# import asyncio
# import aiohttp
# from get_book_sales_ranking.data_fix.matome_jikkou import jikkou

# async def delay(ms: int):
#     await asyncio.sleep(ms / 1000)  # milliseconds to seconds

# async def fetch_with_timeout(url, timeout=10):
#     async with aiohttp.ClientSession() as session:
#         try:
#             async with session.get(url, timeout=timeout) as response:
#                 return await response.json()
#         except asyncio.TimeoutError:
#             print(f"リクエストがタイムアウトしました。(タイムアウト: {timeout}秒)")
#             return None
#         except aiohttp.ClientError as e:
#             print(f"リクエスト中にエラーが発生しました: {e}")
#             return None

# async def fetch_rakuten(isbn):
#     # 楽天ブックスAPIのURL
#     url = f"https://app.rakuten.co.jp/services/api/BooksBook/Search/20170404?format=json&isbn={isbn}&applicationId=1057691251432321112"
#     print("2秒間待機します...")
#     await delay(2000)
#     print("待機終了、データ取得を開始します。")

#     result = await fetch_with_timeout(url, timeout=30)
   
#     if result:
#         hits = result.get('hits')
#         if hits == 0:
#             print("データが見つかりませんでした。 rakuten")

#             product_data = await jikkou(isbn)
#             product_data['rakuten_api_library'] = False
#             return product_data
#         else:
#           data = result.get('Items')[0]['Item']
#           data['rakuten_api_library'] = True
#           return data

#     else:
#         print("データの取得に失敗しました。 rakuten")
#         return None








# 08/04
# 楽天api
import asyncio
import aiohttp
# python3 kari_flask.py用　shuna@LAPTOP-VHG04PF2:~/next-jikken/library-docker-glitch

async def delay(ms: int):
    await asyncio.sleep(ms / 1000)  # milliseconds to seconds

async def fetch_with_timeout(url, timeout=10):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=timeout) as response:
                return await response.json()
        except asyncio.TimeoutError:
            print(f"リクエストがタイムアウトしました。(タイムアウト: {timeout}秒)")
            return None
        except aiohttp.ClientError as e:
            print(f"リクエスト中にエラーが発生しました: {e}")
            return None

async def fetch_rakuten_kari(isbn):
    # 楽天ブックスAPIのURL
    url = f"https://app.rakuten.co.jp/services/api/BooksBook/Search/20170404?format=json&isbn={isbn}&applicationId=1057691251432321112"
    print("2秒間待機します...")
    await delay(2000)
    print("待機終了、データ取得を開始します。")

    # タイムアウトを10秒に設定してfetchを実行
    result = await fetch_with_timeout(url, timeout=30)


    if result:
        hits = result.get('hits')
        if hits == 0:
            print("データが見つかりませんでした。 rakuten")
            product_data = {}
            product_data['rakuten_api_library'] = False
            return product_data
        else:
          data = result['Items'][0]['Item']
          data['rakuten_api_library'] = True
          return data

    else:
        print("データの取得に失敗しました。 rakuten")
        product_data = {}
        product_data['rakuten_api_library'] = False
        return product_data