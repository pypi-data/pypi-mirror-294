# def convert10To13(isbn: str) -> str:
def convert_10_to_13(isbn):
  print("isbn", isbn)
  if len(isbn) == 13:
    return isbn
  # 最初は978で確定なので初期値を入れておく
  odd_characters = ["9", "8"]
  guusuu = ["7"]

  # 奇数番目の文字を格納
  for i in range(1, len(isbn) - 1, 2):
      if isbn[i] == "X":
          odd_characters.append(10)
      else:
        odd_characters.append(isbn[i])

  # 偶数番目の文字を格納
  for i in range(0, len(isbn), 2):
      guusuu.append(isbn[i])

  # 配列の要素をintに変更
  odd_characters_number = list(map(int, odd_characters))
  print("odd_characters_number", odd_characters_number)

  guusuu_number = list(map(int, guusuu))
  print("guusuu_number", guusuu_number)

  odd_sum = sum(odd_characters_number)
  print("odd_sum", odd_sum)

  guusuu_sum = sum(guusuu_number)
  print("guusuu_sum", guusuu_sum)

  total_sum = odd_sum + 3 * guusuu_sum
  print("sum", total_sum)

  last_number = str(total_sum)[-1]
  print("last_number", last_number)

  check_number = "0" if int(last_number) == 0 else str(10 - int(last_number))
  print("check_number", check_number)

  isbn13 = f"978{isbn[:len(isbn)-1]}{check_number}"
  print("isbn13", isbn13)

  return isbn13