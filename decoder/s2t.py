from a2s import decode_dtmf_wav

decoding_chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ \nабвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЭЮЯ"
chars = "0123456789ABCD*#"
de_list = list(decoding_chars)

def read_wav(path):

  text = decode_dtmf_wav(path)
  lt = []
  lc = []

  flt = list(text)
  count = 0

  for c in flt:

    if count == 0:
      lc.append(c)
      count += 1
      continue
    else:
      lc.append(c)
      count -= 1
      ch = ''.join(lc)
      lt.append(ch)

      for i in range(len(lc)):
        lc.pop()

  return lt

def decode(etext):

  decoded_chars = []

  for echar in etext:

    lech = list(echar)

    first = chars.index(lech[0])
    second = chars.index(lech[1])

    i = first * 16 + second
    decoded_chars.append(de_list[i])

  return ''.join(decoded_chars)

ph = "./encoder/output/example.wav"
et = read_wav(ph)
dt = decode(et)
print(dt)

tp = "./decoder/output/example.txt"
with open(tp, "w", encoding="utf-8") as file:
  file.write(dt)
