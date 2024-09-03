# # 2024/07/11/05:30
# # 本コードのコピー
# # ブクログのランキングデータ
# # import requests
# from bs4 import BeautifulSoup as bs
# import datetime
# import re
# import aiohttp

# from get_book_sales_ranking.ranking.booklog.week_url import booklog_week_url
# from get_book_sales_ranking.api.rakuten_api import fetch_rakuten


# HOST="booklog.jp"
# URL="https://"+HOST
# BASE_URL=URL+"/ranking/weekly"
# HEADERS={ "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"}


# # urlからisbnを抽出する関数
# import re
# def extract_number(input_string):
#     # pattern = r'/item/1/(\d+)'
#     pattern = r'/item/1/([0-9X]+)'  # 数字またはXが1回以上連続するパターン
#     match = re.search(pattern, input_string)
#     if match:
#         return match.group(1)
#     else:
#         return None

# # priceから数字を抽出する関数
# def extract_numbers(text):
#   return re.findall(r"\d+", text)

# # rakuten_apiからデータを取得する関数
# async def get_book_info(get_isbn):
#     book_data = await fetch_rakuten(get_isbn)
#     if book_data:
#         return book_data
#     else:
#         print("データの取得に失敗しました。")
#         return None


# class SearchType:
#   book = "book"
#   bunko = "bunko"
#   shinsho = "shinsho"
#   comic = "comic"
#   honour = "honour"


# today=datetime.date.today()

# from datetime import datetime, timedelta
# from calendar import Calendar

# date=datetime.now() - timedelta(days=1)

# calendar = Calendar(firstweekday=0)
# month_calendar = calendar.monthdays2calendar(date.year, date.month)


# count=1
# for week in month_calendar:
#   for day in week:
#     if day[0] == date.day:
#       break
#   else:
#     count+=1
#     continue
#   break

# year=str(today.year)
# month=date.month
# if month == 0:
#   year = str(today.year - 1)
#   month = 12
# elif month == 1:
#   month = "01"
# elif month == 2:
#   month = "02"
# elif month == 3:
#   month = "03"
# elif month == 4:
#   month = "04"
# elif month == 5:
#   month = "05"
# elif month == 6:
#   month = "06"
# elif month == 7:
#   month = "07"
# elif month == 8:
#   month = "08"
# elif month == 9:
#   month = "09"
# week = count


# async def _search(type_=SearchType.book):
#     async with aiohttp.ClientSession() as session:
#         SEARCH_URL = booklog_week_url()
#         # SEARCH_URL=BASE_URL + "/" + str(year) + str(month) + "/" + str(count) + "/" + type_
#         print("SEARCH_URL", SEARCH_URL)
#         async with session.get(SEARCH_URL, headers=HEADERS) as response:
#             return await response.text()


# async def toData(l):
#   productRanking=l.select_one(".ranking").select_one(".rank-num").find("span").text

#   productImage=l.select_one(".thumb").find("a").find("img").get("src")

#   productUrl= URL + l.select_one(".thumb").find("a").get("href")

#   productTitle= l.select_one(".desc").find("h3").find("a").text
#   productAuthor= l.select_one(".descMini").select_one(".itemInfoElmBox").find("span").find("a").text



#   # isbnを取得するための前段階
#   get_isbn = str(extract_number(l.select_one(".thumb").find("a").get("href")))
#   # rakuten_apiからデータを取得
#   book_info = await get_book_info(get_isbn)



#   if book_info and book_info['rakuten_api_library'] == True:
#     productIsbn = book_info['isbn']
#     productPrice = book_info['itemPrice']
#     productCaption = book_info['itemCaption']
#     productPublisher = book_info['publisherName']
#     productSalesDate = book_info['salesDate']
#     productPageCount = ""

#   elif book_info and book_info['rakuten_api_library'] == False:
#     if book_info['price'] == "":
#       book_info['price'] = 0
#     if book_info['page_count'] == "":
#       book_info['page_count'] = 0

#     productIsbn = book_info['isbn']
#     productPrice = book_info['price']
#     productCaption = book_info['caption']
#     productPublisher = book_info['publisher']
#     productSalesDate = book_info['publishedDate']
#     productPageCount = book_info['page_count']

#   else:
#     productIsbn = get_isbn
#     productPrice = 0
#     productCaption = ""
#     productPublisher = ""
#     productSalesDate = ""
#     productPageCount = ""


#   extracted_price = extract_numbers(str(productPrice))


#   return {
#     "ranking":int(productRanking),
#     "title":productTitle,
#     "isbn":productIsbn,
#     "author":productAuthor,
#     "price":int(extracted_price[0]),
#     "caption":productCaption,
#     "publisher":productPublisher,
#     "salesDate":productSalesDate,
#     "image":productImage
#   }


# async def getData(soup):
#   kari1 = soup.select_one(".autopagerize_page_element.t20M")
#   kari2 = kari1.select_one(".ranking-list")
#   for l in kari2.select(".clearFix")[:20]:
#     yield await toData(l)
# async def search_booklog_ranking(type_=SearchType.book):
#   text= await _search(type_)
#   soup= bs(text,"html.parser")
#   async for data in getData(soup):
#     yield data



# async def booklog_main():
#   booklog_ranking = [data async for data in search_booklog_ranking()][:20]
#   return booklog_ranking









# 08/04
# 2024/07/11/05:30
# 本コードのコピー
# ブクログのランキングデータ
# import requests
from bs4 import BeautifulSoup as bs
import datetime
import re
import aiohttp

from get_book_sales_ranking.ranking.booklog.week_url import booklog_week_url
from get_book_sales_ranking.data_fix.matome_jikkou import jikkou_kari

from get_book_sales_ranking.data_fix.fix_isbn import convert_10_to_13

# # python3 -m clear_up用　shuna@LAPTOP-VHG04PF2:~/next-jikken/library-docker-glitch/get_data_7_25
# import sys
# sys.path.append("..")
# from api.rakuten_api import fetch_rakuten


# python3 kari_flask.py用　shuna@LAPTOP-VHG04PF2:~/next-jikken/library-docker-glitch
# from get_data_7_25.kari_matome_jikkou import jikkou_kari


HOST="booklog.jp"
URL="https://"+HOST
BASE_URL=URL+"/ranking/weekly"


HEADERS={ "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"}


# urlからisbnを抽出する関数
import re

def extract_number(input_string):
    # pattern = r'/item/1/(\d+)'
    pattern = r'/item/1/([0-9X]+)'
    match = re.search(pattern, input_string)
    if match:
        return match.group(1)
    else:
        return None

# priceから数字を抽出する関数
def extract_numbers(text):
  return re.findall(r"\d+", text)

def extract_author(text):
  # 改行コードで分割
  split_text = text.split('\n')
  # リストの最初の要素を取り出す
  extracted_text = split_text[1].strip()
  return extracted_text

class SearchType:
  book = "book"
  bunko = "bunko"
  shinsho = "shinsho"
  comic = "comic"
  honour = "honour"


today=datetime.date.today()

from datetime import datetime, timedelta
from calendar import Calendar

date=datetime.now() - timedelta(days=1)

calendar = Calendar(firstweekday=0)
month_calendar = calendar.monthdays2calendar(date.year, date.month)


count=1
for week in month_calendar:
  for day in week:
    if day[0] == date.day:
      break
  else:
    count+=1
    continue
  break

year=str(today.year)
month=date.month
if month == 0:
  year = str(today.year - 1)
  month = 12
elif month == 1:
  month = "01"
elif month == 2:
  month = "02"
elif month == 3:
  month = "03"
elif month == 4:
  month = "04"
elif month == 5:
  month = "05"
elif month == 6:
  month = "06"
elif month == 7:
  month = "07"
elif month == 8:
  month = "08"
elif month == 9:
  month = "09"
week = count


async def _search(type_=SearchType.book):
    async with aiohttp.ClientSession() as session:
        # SEARCH_URL=BASE_URL + "/" + str(year) + str(month) + "/" + str(count) + "/" + type_
        SEARCH_URL = booklog_week_url()
        print("SEARCH_URL", SEARCH_URL)
        async with session.get(SEARCH_URL, headers=HEADERS) as response:
            return await response.text()


async def toData(l):
  productRanking=l.select_one(".ranking").select_one(".rank-num").find("span").text

  productImage=l.select_one(".thumb").find("a").find("img").get("src")

  productUrl= URL + l.select_one(".thumb").find("a").get("href")



  productTitle= l.select_one(".desc").find("h3").find("a").text
  # productAuthor= l.select_one(".descMini").select_one(".itemInfoElmBox").find("span").find("a").text
  productAuthor= l.select_one(".desc").select_one(".descMini").select_one(".itemInfoElmBox").find("span").find("a")

  if l.select_one(".desc").select_one(".descMini").select_one(".itemInfoElmBox").find("span").find("a") == None:
    productAuthor = extract_author(l.select_one(".desc").select_one(".descMini").select_one(".itemInfoElmBox").find("span").text)
  else:
    productAuthor = l.select_one(".descMini").select_one(".itemInfoElmBox").find("span").find("a").text


  # isbnを取得するための前段階
  get_isbn = str(extract_number(l.select_one(".thumb").find("a").get("href")))

  book_info = await jikkou_kari(get_isbn)

  extracted_price = extract_numbers(str(book_info['price']))


  page_count = book_info['page_count']
  book_type = book_info['book_type']

  fixed_isbn = convert_10_to_13(str(get_isbn))

  return {
    "page": page_count,
    "booktype": book_type,

    "ranking":int(productRanking),
    "title":productTitle,
    # "isbn":convert10To13(get_isbn),
    "isbn":fixed_isbn,
    "author":productAuthor,
    "price":int(extracted_price[0]),
    "caption":book_info['caption'],
    "publisher":book_info['publisher'],
    "salesDate":book_info['publishedDate'],
    "image":productImage
  }


async def getData(soup):
  kari1 = soup.select_one(".autopagerize_page_element.t20M")
  kari2 = kari1.select_one(".ranking-list")
  for l in kari2.select(".clearFix")[:20]:
    yield await toData(l)
async def search_booklog_ranking(type_=SearchType.book):
  text= await _search(type_)
  soup= bs(text,"html.parser")
  async for data in getData(soup):
    SEARCH_URL=BASE_URL + "/" + str(year) + str(month) + "/" + str(count) + "/" + type_
    yield data



async def booklog_main():
  booklog_ranking = [data async for data in search_booklog_ranking()][:20]
  # print("booklog_ranking",booklog_ranking)
  return booklog_ranking