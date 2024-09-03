import asyncio

from get_book_sales_ranking.ranking.booklog.booklog_ranking import search_booklog_ranking
from get_book_sales_ranking.ranking.bookmeter.bookmeter_ranking import search_bookmeter_ranking
from get_book_sales_ranking.ranking.bookoff.bookoff_ranking import search_bookoff_ranking


async def get_data():
    async def collect_data(search_func, limit=None):
        data = []
        async for item in search_func:
            data.append(item)
            if limit and len(data) >= limit:
                break
        return data

    booklog_ranking_data = collect_data(search_booklog_ranking())
    bookmeter_ranking_data = collect_data(search_bookmeter_ranking())
    bookoff_ranking_data = collect_data(search_bookoff_ranking(), limit=20)


    results = await asyncio.gather(
        bookoff_ranking_data,
        bookmeter_ranking_data,
        booklog_ranking_data
    )

    bookoff_ranking, bookmeter_ranking, booklog_ranking = results

    bookoff_ranking = bookoff_ranking[:20]

    return {"booklog_ranking": booklog_ranking, "bookmeter_ranking": bookmeter_ranking, "bookoff_ranking": bookoff_ranking}

def ranking_key(item):
    if item['ranking'] == 'id':
        return float('inf')
    return item['ranking']

def is_valid_item(item):
    return item["title"] != "" and item["author"] != "" and item["ranking"] != "id"


def rank_data(data, weight):
    for i, item in enumerate(data, 1):
        if is_valid_item(item):
            item['score'] = (len(data) - i + 1) * weight
        else:
            item['score'] = 0
    return data



async def merge_data():
    data = await get_data()
    data1 = data["booklog_ranking"]
    data2 = data["bookmeter_ranking"]
    data3 = data["bookoff_ranking"]

    sorted_data1 = sorted(data1, key=lambda x: x['ranking'])
    sorted_data2 = sorted(data2, key=lambda x: x['ranking'])
    sorted_data3 = sorted(data3, key=lambda x: x['ranking'])

    ranked_data1 = rank_data(sorted_data1, 3)
    ranked_data2 = rank_data(sorted_data2, 2)
    ranked_data3 = rank_data(sorted_data3, 1)

    merged = {}
    for dataset in [ranked_data1, ranked_data2, ranked_data3]:
        for item in dataset:
            if is_valid_item(item):
                # key = (item['title'], item['author'])
                key = (item['isbn'])
                if key in merged:
                    merged[key]['score'] += item['score']
                else:
                    merged[key] = item.copy()
    final_data_kari = list(merged.values())

    for index, item in enumerate(final_data_kari):
        item['ranking'] = index + 1

    return sorted(final_data_kari, key=lambda x: x['score'], reverse=True)
