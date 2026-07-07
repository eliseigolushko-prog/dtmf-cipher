chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ \nабвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЭЮЯ"
encoding_chars = "0123456789ABCD*#"
en_list = list(encoding_chars)

def read_file(path) -> str:

  with open (path, 'r', encoding="utf-8") as file:

    text = str(file.read())

  return text

def encode(text) -> list:

  encoded_chars = []
  encoded_char = []

  for c in range(len(text)):

    char = text[c]
    ci = chars.index(char)

    first = int(ci / 16)
    encoded_char.append(en_list[first])

    ns = first
    ci_2 = ci - (ns * 16)

    encoded_char.append(en_list[ci_2])

    str_enc_ch = ''.join(map(str,encoded_char))
    encoded_chars.append(str_enc_ch)

    for ch in range(len(encoded_char)):
      encoded_char.pop()

  return encoded_chars

print(encode("Hello, guys!\n"))
