HOST="booklog.jp"
URL="https://"+HOST
BASE_URL=URL+"/ranking/weekly"
HEADERS={ "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"}
class SearchType:
  book = "book"
  bunko = "bunko"
  shinsho = "shinsho"
  comic = "comic"
  honour = "honour"

import datetime
today_kari=datetime.date.today()
from datetime import datetime, timedelta
from calendar import Calendar

date_kari=datetime.now() - timedelta(hours=12)
calendar_kari = Calendar(firstweekday=0)
month_calendar_kari = calendar_kari.monthdays2calendar(date_kari.year, date_kari.month)

count_kari=1
for week in month_calendar_kari:
  for day in week:
    if day[0] == date_kari.day:
      break
  else:
    count_kari+=1
    continue
  break

year_kari=str(today_kari.year)
month_kari=date_kari.month
if month_kari == 0:
  year_kari -= 1
  month_kari = 12
elif month_kari == 1:
  month = "01"
elif month_kari == 2:
  month_kari = "02"
elif month_kari == 3:
  month_kari = "03"
elif month_kari == 4:
  month_kari = "04"
elif month_kari == 5:
  month_kari = "05"
elif month_kari == 6:
  month_kari = "06"
elif month_kari == 7:
  month_kari = "07"
elif month_kari == 8:
  month_kari = "08"
elif month_kari == 9:
  month_kari = "09"
week_kari = count_kari

type_ = SearchType.book
# SEARCH_URL=BASE_URL + "/" + str(year_kari) + str(month_kari) + "/" + str(count_kari) + "/" + type_
SEARCH_URL=BASE_URL + "/" + str(year_kari) + str(month_kari) + "/" + str(count_kari-1) + "/" + type_


date1 = today_kari.day
day1 = today_kari.weekday()
print("day",day1)
print("date",date1)


if date_kari.weekday() != 0 and count_kari == 1:
    print("if[a]")
    date=datetime.now() - timedelta(hours=12) - timedelta(days=date_kari.weekday())
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

    year=str(today_kari.year)
    month=date.month
    if month == 0:
        year -= 1
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

    type_ = SearchType.book
    # SEARCH_URL=BASE_URL + "/" + str(year) + str(month) + "/" + str(count) + "/" + type_
    SEARCH_URL=BASE_URL + "/" + str(year) + str(month) + "/" + str(count-1) + "/" + type_
    # print("SEARCH_URL", SEARCH_URL)

# 現在が第１週かつ月曜のとき
if date_kari.weekday() == 0 and count_kari == 1:
    print("if[b]")
    date=datetime.now() - timedelta(hours=12) - timedelta(days=1)
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

    year=str(today_kari.year)
    month=date.month
    if month == 0:
        year -= 1
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

    type_ = SearchType.book
    # SEARCH_URL=BASE_URL + "/" + str(year) + str(month) + "/" + str(count) + "/" + type_
    SEARCH_URL=BASE_URL + "/" + str(year) + str(month) + "/" + str(count) + "/" + type_
    # print("SEARCH_URL", SEARCH_URL)

print("SEARCH_URL",SEARCH_URL)

def booklog_week_url():
   return SEARCH_URL