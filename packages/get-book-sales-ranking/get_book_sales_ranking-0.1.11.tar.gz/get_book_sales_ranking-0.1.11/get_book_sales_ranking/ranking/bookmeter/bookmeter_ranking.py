# import requests
# from bs4 import BeautifulSoup as bs
# import datetime
# import re
# import aiohttp

# from get_book_sales_ranking.ranking.bookmeter.bookmeter_individual import get_individual_bookmeter_data
# from get_book_sales_ranking.api.rakuten_api import fetch_rakuten

# HOST="bookmeter.com"
# URL="https://"+HOST

# BASE_URL2= URL+"/rankings/latest/wish_book"


# HEADERS={ "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"}

# # priceから数字を抽出する関数
# def extract_numbers(text):
#   return re.findall(r"\d+", text)

# # rakuten_apiからデータを取得する関数
# async def get_book_info(isbn):
#     book_data = await fetch_rakuten(isbn)
#     if book_data:
#         return book_data
#     else:
#         print("データの取得に失敗しました。")
#         return None


# class SearchType:
#   bunko=2
#   tankoubon=1
#   comic=9
#   all=0

# class SearchType_bookmeter:
#   bunko="bunko"
#   tankoubon="tankoubon"
#   comic="comic"

# today=datetime.date.today()



# year=today.year
# month=today.month - 1
# if month == 0:
#   year -= 1
#   month = 12


# def extract_rank(text):
#     pattern = r"(\d+)位"
#     match = re.search(pattern, text)
#     if match:
#         return match.group(1)
#     else:
#         return None



# def extract_author(text):
#     pattern1 = r"\u3000"
#     pattern2 = r" "
#     match1 = re.search(pattern1, text)
#     match2 = re.search(pattern2, text)
#     if match1:
#         return re.sub(r"[\u3000]", "", text)
#     elif match2:
#         return re.sub(r"[ ]", "", text)
#     else:
#         return text


# async def _search(type_=SearchType_bookmeter.tankoubon):
#     async with aiohttp.ClientSession() as session:
#         SEARCH_URL2= BASE_URL2 + "/" + type_ + "/" + "week"
#         async with session.get(SEARCH_URL2, headers=HEADERS) as response:
#             return await response.text()



# async def toData(l):
#   productRanking=l.select_one(".book__ranking").find("span").text


#   productImage=l.select_one(".book__cover").find("a").find("img").get("src")


#   productUrl=URL + l.select_one(".book__cover").find("a").get("href")


#   productDetail=l.select_one(".book__detail")


#   productTitle=productDetail.select_one(".detail__title").find("a").text
#   productAuthor=productDetail.select_one(".detail__authors").find("li").find("a").text

#   productEvaluation=productDetail.select_one(".detail__options").find("dd").text

#   # isbnをamazonのurlから取得する
#   isbn = await get_individual_bookmeter_data(productUrl)
#   book_info = await get_book_info(isbn['isbn'])


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


#   extracted_price = extract_numbers(str(productPrice))


#   return {
#     "ranking":int(extract_rank(productRanking)),
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
#   for l in soup.select(".list__book")[:20]:
#     yield await toData(l)
# async def search_bookmeter_ranking(type_=SearchType_bookmeter.bunko ,session=requests):
#   text= await _search(type_)
#   soup=bs(text,"html.parser")
#   async for data in getData(soup):
#     yield data




# async def bookmeter_main():
#   booklog_ranking = [data async for data in search_bookmeter_ranking()][:20]
#   return booklog_ranking








# 08/04
# 2024/07/24
# 本コードのコピー
# ブックメーターのランキング
import requests
from bs4 import BeautifulSoup as bs
import datetime
import re
import aiohttp

from get_book_sales_ranking.ranking.bookmeter.bookmeter_individual import get_individual_bookmeter_data
from get_book_sales_ranking.data_fix.matome_jikkou import jikkou_kari

from get_book_sales_ranking.data_fix.fix_isbn import convert_10_to_13

HOST="bookmeter.com"
URL="https://"+HOST
# BASE_URL=URL+"/rankings/monthly"

BASE_URL2= URL+"/rankings/latest/wish_book"


HEADERS={ "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"}

# priceから数字を抽出する関数
def extract_numbers(text):
  return re.findall(r"\d+", text)


class SearchType:
  bunko=2
  tankoubon=1
  comic=9
  all=0

class SearchType_bookmeter:
  bunko="bunko"
  tankoubon="tankoubon"
  comic="comic"

today=datetime.date.today()



year=today.year
month=today.month - 1
if month == 0:
  year -= 1
  month = 12


def extract_rank(text):
    pattern = r"(\d+)位"
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    else:
        return None



def extract_author(text):
    pattern1 = r"\u3000"
    pattern2 = r" "
    match1 = re.search(pattern1, text)
    match2 = re.search(pattern2, text)
    if match1:
        return re.sub(r"[\u3000]", "", text)
    elif match2:
        return re.sub(r"[ ]", "", text)
    else:
        return text


async def _search(type_=SearchType_bookmeter.tankoubon):
    async with aiohttp.ClientSession() as session:
        book_size = type_
        SEARCH_URL2= BASE_URL2 + "/" + type_ + "/" + "week"
        print(SEARCH_URL2)
        async with session.get(SEARCH_URL2, headers=HEADERS) as response:
            return await response.text()



async def toData(l):
  # print("l",l)
  productRanking=l.select_one(".book__ranking").find("span").text


  productImage=l.select_one(".book__cover").find("a").find("img").get("src")


  productUrl=URL + l.select_one(".book__cover").find("a").get("href")


  productDetail=l.select_one(".book__detail")


  productTitle=productDetail.select_one(".detail__title").find("a").text
  productAuthor=productDetail.select_one(".detail__authors").find("li").find("a").text


  productEvaluation=productDetail.select_one(".detail__options").find("dd").text

  # isbnをamazonのurlから取得する
  isbn = await get_individual_bookmeter_data(productUrl)
  book_info = await jikkou_kari(isbn['isbn'])

  extracted_price = extract_numbers(str(book_info['price']))

  book_type = book_info['book_type']
  page_count = book_info['page_count']

  fixed_isbn = convert_10_to_13(str(isbn['isbn']))

  return {
    "booktype": book_type,
    "page": page_count,

    "ranking":int(extract_rank(productRanking)),
    "title":productTitle,
    # "isbn":convert_10to_13(isbn['isbn']),
    "isbn":fixed_isbn,
    "author":productAuthor,
    "price":int(extracted_price[0]),
    "caption":book_info['caption'],
    "publisher":book_info['publisher'],
    "salesDate":book_info['publishedDate'],
    "image":productImage
  }



async def getData(soup):
  for l in soup.select(".list__book")[:20]:
    yield await toData(l)
async def search_bookmeter_ranking(type_=SearchType_bookmeter.bunko ,session=requests):
  text= await _search(type_)
  soup=bs(text,"html.parser")
  async for data in getData(soup):
    # SEARCH_URL=BASE_URL + "/" + type_ + "/" + str(year) + "/" + str(month)
    SEARCH_URL2= BASE_URL2 + "/" + type_ + "/" + "week"
    yield data




async def bookmeter_main():
  booklog_ranking = [data async for data in search_bookmeter_ranking()][:20]
  # print("booklog_ranking",booklog_ranking)
  return booklog_ranking