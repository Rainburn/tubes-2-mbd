file = open("data-input.txt", "r")
myfile = file.read()
arr = myfile.split("; ")

array_transaksi = []
for data in arr:
    data = str(data)
    jenis = data[0]
    if jenis != "C":
        item = data[-2]
        transaksi = data[1:-3]
    else:
        item = ""
        transaksi = data[1:]

    array_transaksi.append((jenis, transaksi, item))
file.close()

print(array_transaksi)

def occ(array_transaksi):
  base_array = array_transaksi.copy()
  arrNum = getNumTransaction(array_transaksi)
  arr_TS = []
  for x in arrNum:
    arr_TS.append((x, getStartTS(array_transaksi, x)))

  arr_TS = sorted(arr_TS, key=lambda tup: tup[1])



def validation(arr, arr_TS):
  print("fauzan")

def getNumTransaction(arr):
  # Mengembalikan array berisi nomor transaksi
  arrNum = []
  for x in arr:
    if x[1] not in arrNum:
      arrNum.append(x[1])
  return arrNum

def getStartTS(arr, num):
  start = -1
  i = 0
  stop = False
  while i < len(arr) and not stop:
    if (arr[i][1] == str(num)):
      start = i
      stop = True
    i+=1
  return start

def getValidateTS(arr, num):
  # Mengembalikan index untuk validasi dari transaksi num pada arr
  last_read = -1
  first_write = -1
  i = 0
  write_exists = False
  while i < len(arr) and not write_exists:
    if (arr[i][1] == str(num)):
      if (arr[i][0] == 'R'):
        last_read = i
      elif (arr[i][0] == 'W'):
        first_write = i
        write_exists = True
    i+=1

  if (first_write != -1):
    return first_write
  else:
    return last_read + 1


occ(array_transaksi)