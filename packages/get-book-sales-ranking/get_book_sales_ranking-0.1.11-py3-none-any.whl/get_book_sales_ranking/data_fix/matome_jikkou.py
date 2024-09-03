import asyncio

from get_book_sales_ranking.api.google_api import get_book_data_google
from get_book_sales_ranking.api.sru_api import get_book_data_sru
from get_book_sales_ranking.api.opendb_api import get_book_data_opendb
from get_book_sales_ranking.api.opensearch_api import get_book_data_opensearch


# # 実行部分の関数
# async def jikkou(isbn):
#     google_fetched = get_book_data_google(isbn)
#     sru_fetched = get_book_data_sru(isbn)
#     opendb_fetched = get_book_data_opendb(isbn)
#     opensearch_fetched = get_book_data_opensearch(isbn)

#     results = await asyncio.gather(
#       google_fetched, 
#       sru_fetched, 
#       opendb_fetched, 
#       opensearch_fetched
#     )

#     google_fetched_data, sru_fetched_data, opendb_fetched_data, opensearch_fetched_data = results

#     google_fetch = google_fetched_data['google_data']
#     sru_fetch = sru_fetched_data['sru_data']
#     opendb_fetch = opendb_fetched_data['opendb_data']
#     opensearch_fetch = opensearch_fetched_data['opensearch_data']

#     print(f"google_fetch: {google_fetch}, sru_fetch: {sru_fetch}, opendb: {opendb_fetch}, opensearch: {opensearch_fetch}")



#     if google_fetch == True:
#       # google_ok+sru_ok
#       if sru_fetched_data['sru_data'] == True:
#           print("google+sru")
#           return {
#               "isbn": isbn,
#               "caption": google_fetched_data['description'],
#               "publishedDate": google_fetched_data['publishedDate'],
#               "publisher": sru_fetched_data['publisher'],
#               "price": sru_fetched_data['price'],
#               "page_count": sru_fetched_data['page_count'],
#           }

#       if opendb_fetch and opendb_fetched_data['price'] == "" and (sru_fetch or opensearch_fetch):
#         if sru_fetch == True:
#           print("google+opendb[price==""] [sru]")
#           price = sru_fetched_data['price']
#           page_count = sru_fetched_data['page_count']
#         elif sru_fetch == False and opensearch_fetch == True:
#           print("google+opendb[price==""] [opensearch]")
#           price = opensearch_fetched_data['price']
#           page_count = opensearch_fetched_data['page_count']
#         else:
#           print("google+opendb[price==""] [opendb]")
#           price = opendb_fetched_data['price']
#           page_count = opendb_fetched_data['page_count']

#         return {
#             "isbn": isbn,
#             "caption": google_fetched_data['description'],
#             "publishedDate": google_fetched_data['publishedDate'],
#             "publisher": opendb_fetched_data['publisher'],
#             "price": price,
#             "page_count": page_count,
#         }

#       if opendb_fetch == True and opendb_fetched_data['price'] != "":
#         if sru_fetch == True:
#           print("google+opendb[price!=""] [sru]")
#           page_count = sru_fetched_data['page_count']
#         else:
#           print("google+opendb[price!=""] [opendb]")
#           page_count = opendb_fetched_data['page_count']
#         return {
#             "isbn": isbn,
#             "caption": google_fetched_data['description'],
#             "publishedDate": google_fetched_data['publishedDate'],
#             "publisher": opendb_fetched_data['publisher'],
#             "price": opendb_fetched_data['price'],
#             "page_count": page_count,
#         }


#       if opensearch_fetch == True and opensearch_fetched_data['price'] == "" and (sru_fetch == True or opendb_fetch == True):
#         if sru_fetch == True:
#           print("google+opensearch[price==""] [sru]")
#           price = sru_fetched_data['price']
#           page_count = sru_fetched_data['page_count']
#         else:
#           print("google+opensearch[price==""] [opendb]")
#           price = opendb_fetched_data['price']
#           page_count = opendb_fetched_data['page_count']

#         return {
#             "isbn": isbn,
#             "caption": google_fetched_data['description'],
#             "publishedDate": google_fetched_data['publishedDate'],
#             "publisher": opensearch_fetched_data['publisher'],
#             "price": price,
#             "page_count": page_count,
#         }

#       if opensearch_fetch == True and opensearch_fetched_data['price'] != "":
#         print("google+opensearch[price!='']")
#         return {
#             "isbn": isbn,
#             "caption": google_fetched_data['description'],
#             "publishedDate": google_fetched_data['publishedDate'],
#             "publisher": opensearch_fetched_data['publisher'],
#             "price": opensearch_fetched_data['price'],
#             "page_count": opensearch_fetched_data['page_count'],
#         }

#       # googleがokで他はダメな場合が抜けてた 2024/7/28
#       if opendb_fetch == False and opensearch_fetch == False and sru_fetch == False:
#         print("google only")
#         return {
#             "isbn": isbn,
#             "caption": google_fetched_data['description'],
#             "publishedDate": google_fetched_data['publishedDate'],
#             "publisher": google_fetched_data['publisher'],
#             "price": google_fetched_data['price'],
#             "page_count": google_fetched_data['page_count'],
#         }


#     elif google_fetch == False:
#       if sru_fetched_data['sru_data'] == True:
#           print("sru")
#           return {
#               "isbn": isbn,
#               "caption": "",
#               "publishedDate": sru_fetched_data['sales_date'],
#               "publisher": sru_fetched_data['publisher'],
#               "price": sru_fetched_data['price'],
#               "page_count": sru_fetched_data['page_count'],
#           }

#       if opendb_fetch == True:
#         print("opendb")
#         return {
#             "isbn": isbn,
#             "caption": "",
#             "publishedDate": opendb_fetched_data['sales_date'],
#             "publisher": opendb_fetched_data['publisher'],
#             "price": opendb_fetched_data['price'],
#             "page_count": opendb_fetched_data['page_count'],
#         }

#       if opensearch_fetch == True:
#         print("opensearch == True")
#         return {
#             "isbn": isbn,
#             "caption": "",
#             "publishedDate": opensearch_fetched_data['sales_date'],
#             "publisher": opensearch_fetched_data['publisher'],
#             "price": opensearch_fetched_data['price'],
#             "page_count": opensearch_fetched_data['page_count'],
#         }


#       if opensearch_fetch == True and opensearch_fetched_data['price'] == "" and (sru_fetch == True or opendb_fetch == True):
#         if sru_fetch == True:
#           print("opensearch+sru[price==''] [sru]")
#           price = sru_fetched_data['price']
#           page_count = sru_fetched_data['page_count']
#         else:
#           print("opensearch+opendb[price==''] [opendb]")
#           price = opendb_fetched_data['price']
#           page_count = opendb_fetched_data['page_count']

#         return {
#             "isbn": isbn,
#             "caption": "",
#             "publishedDate": opensearch_fetched_data['sales_date'],
#             "publisher": opensearch_fetched_data['publisher'],
#             "price": price,
#             "page_count": page_count,
#         }

#       if opensearch_fetch == True and opensearch_fetched_data['price'] != "":
#         print("opensearch[price!='']")
#         return {
#             "isbn": isbn,
#             "caption": "",
#             "publishedDate": opensearch_fetched_data['sales_date'],
#             "publisher": opensearch_fetched_data['publisher'],
#             "price": opensearch_fetched_data['price'],
#             "page_count": opensearch_fetched_data['page_count'],
#         }


#     else:
#       print("else")
#       return {
#           "isbn": isbn,
#           "caption": "",
#           "publishedDate": "",
#           "publisher": "",
#           "price": 0,
#           "page_count": "",
#       }









import asyncio
from get_book_sales_ranking.api.rakuten_api import fetch_rakuten_kari

# 08/04
# 実行部分の関数
async def jikkou_kari(isbn):
    rakuten_fetched = fetch_rakuten_kari(isbn)
    google_fetched = get_book_data_google(isbn)
    sru_fetched = get_book_data_sru(isbn)
    opendb_fetched = get_book_data_opendb(isbn)
    opensearch_fetched = get_book_data_opensearch(isbn)

    results = await asyncio.gather(
      rakuten_fetched,
      google_fetched, 
      sru_fetched, 
      opendb_fetched, 
      opensearch_fetched
    )

    # rakuten_fetched_data, google_fetched_data, sru_fetched_data, opendb_fetched_data, opensearch_fetched_data = results
    rakuten_fetch, google_fetch, sru_fetch, opendb_fetch, opensearch_fetch = results

    print(f"rakuten_fetch: {rakuten_fetch}, google_fetch: {google_fetch}, sru_fetch: {sru_fetch}, opendb: {opendb_fetch}, opensearch: {opensearch_fetch}")

    # 試し用
    isbn = isbn
    #caption
    print("google_data", type(google_fetch['google_data']))
    print("rakuten_api_library", type(rakuten_fetch['rakuten_api_library']))
    caption = ""
    if google_fetch['google_data'] == True and google_fetch['description'] != "":
      caption = google_fetch['description']
    if rakuten_fetch['rakuten_api_library'] == True and rakuten_fetch['itemCaption'] != "":
      caption = rakuten_fetch['itemCaption']


    # publishedDate
    publishedDate = ""
    if opendb_fetch['opendb_data'] == True and opendb_fetch['sales_date'] != "":
      publishedDate = opendb_fetch['sales_date']
    if opensearch_fetch['opensearch_data'] == True and opensearch_fetch['sales_date'] != "":
      publishedDate = opensearch_fetch['sales_date']
    if sru_fetch['sru_data'] == True and sru_fetch['sales_date'] != "":
      publishedDate = sru_fetch['sales_date']
    if google_fetch['google_data'] == True and google_fetch['publishedDate'] != "":
      publishedDate = google_fetch['publishedDate']
    if rakuten_fetch['rakuten_api_library'] == True and rakuten_fetch['salesDate'] != "":
      publishedDate = rakuten_fetch['salesDate']

    
    # publisher
    publisher = ""
    if opensearch_fetch['opensearch_data'] == True and opensearch_fetch['publisher'] != "":
      publisher = opensearch_fetch['publisher']
    if opendb_fetch['opendb_data'] == True and opendb_fetch['publisher'] != "":
      publisher = opendb_fetch['publisher']
    if sru_fetch['sru_data'] == True and sru_fetch['publisher'] != "":
      publisher = sru_fetch['publisher']
    if rakuten_fetch['rakuten_api_library'] == True and rakuten_fetch['publisherName'] != "":
      publisher = rakuten_fetch['publisherName']


    # price
    price = "0"
    if rakuten_fetch['rakuten_api_library'] == True and rakuten_fetch['itemPrice'] != 0 and rakuten_fetch['itemPrice'] != "" and rakuten_fetch['itemPrice'] != None:
      price = rakuten_fetch['itemPrice']
    if opendb_fetch['opendb_data'] == True and opendb_fetch['price'] != "" and opendb_fetch['price'] != 0:
      price = opendb_fetch['price']
    if opensearch_fetch['opensearch_data'] == True and opensearch_fetch['price'] != "" and opensearch_fetch['price'] != 0:
      price = opensearch_fetch['price']
    if sru_fetch['sru_data'] == True and sru_fetch['price'] != "" and sru_fetch['price'] != 0:
      price = sru_fetch['price']



    # page_count
    page_count = ""
    if google_fetch['google_data'] == True and google_fetch['page_count'] != "" and google_fetch['page_count'] != 0:
      page_count = google_fetch['page_count']
    if opendb_fetch['opendb_data'] == True and opendb_fetch['page_count'] != "" and opendb_fetch['page_count'] != 0:
      page_count = opendb_fetch['page_count']
    if sru_fetch['sru_data'] == True and sru_fetch['page_count'] != "" and sru_fetch['page_count'] != 0:
      page_count = sru_fetch['page_count']
    if opensearch_fetch['opensearch_data'] == True and opensearch_fetch['page_count'] and opensearch_fetch['page_count'] != 0:
      page_count = opensearch_fetch['page_count']
      
    

    # 文庫本か単行本かを見分ける　2024/08/09　5:02
    # book_type
    book_type = ""
    if opensearch_fetch['opensearch_data'] == True and opensearch_fetch['book_type'] != "":
      book_type = opensearch_fetch['book_type']
    if opendb_fetch['opendb_data'] == True and opendb_fetch['book_type'] != "":
      book_type = opendb_fetch['book_type']
    if sru_fetch['sru_data'] == True and sru_fetch['book_type'] != "":
      book_type = sru_fetch['book_type']
    if rakuten_fetch['rakuten_api_library'] == True and rakuten_fetch['size'] != "":
      book_type = rakuten_fetch['size']

    return {
        # 文庫本か単行本かを見分ける　2024/08/09　5:03
        # "book_type": book_type,
        "book_type": book_type,

        "isbn": isbn,
        "caption": caption,
        "publishedDate": publishedDate,
        "publisher": publisher,
        "price": price,
        "page_count": page_count,
    }