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
  print("OCC")
  base_array = array_transaksi.copy()
  arr_num = sorted(getNumTransaction(array_transaksi))
  arr_TS = getArrTS(arr_num, array_transaksi)
  arr_operation = getTransactionOperation(array_transaksi, arr_num)
  print(arr_TS)
  # print(getTransactionOperation(array_transaksi, arr_num))
  isValidTransaction(array_transaksi, '1', arr_TS, arr_num, arr_operation)
  # print(isValidTransaction(array_transaksi, 2, arr_TS))
  # print(isValidTransaction(array_transaksi, 3, arr_TS))

def isValidTransaction(arr, num, arr_TS, arr_num, arr_operation):
  isValid = True
  check_queue = []
  for x in arr_TS:
    if(int(x[0]) < int(num)):
      check_queue.append(x)
  
  i = 0
  while i < len(check_queue) and isValid:
    a = compareTS(check_queue[i], arr_TS[arr_num.index(num)], arr_num, arr_operation)
    print(a)
    i+=1

def compareTS(TI, TJ, arr_num, arr_operation):
  print(TI)
  print(TJ)
  # finishTS(TI) < startTS(TJ)
  # startTS = 1, finishTS = 2, validateTS = 3
  if (TI[2] < TJ[1]):
    print("Masuk apa")
    return True
  else:
    if(TJ[1] < TI[2] and TI[2] < TJ[3]):
      print("Masuk sana")
      # check apakah dia melakukan read kepada item data yg di write transaksi sebelumnya
      isNotIntersect = True
      print(arr_operation[arr_num.index(TI[0])])
      print(arr_operation[arr_num.index(TJ[0])])
      for i in range(len(arr_operation[arr_num.index(TJ[0])])):
        if(print(arr_operation[arr_num.index(TJ[0])])):
          if(arr_operation[arr_num.index(TJ[0])][1][i] in arr_operation[arr_num.index(TI[0])][2]):
            isNotIntersect = False
          print(isNotIntersect)
      return isNotIntersect
    else:
      print("Masuk sini")
      return False

def getTransactionOperation(arr, arr_num):
  arr_operation = []
  for i in range(len(arr_num)):
    arr_operation.append((arr_num[i], [], []))

  for x in arr:
    num_transaction = x[1]
    idx = arr_num.index(num_transaction)
    if(x[0] == 'R'):
      if(x[2] not in arr_operation[idx][1]):
        arr_operation[idx][1].append(x[2])
    elif(x[0] == 'W'):
      if(x[2] not in arr_operation[idx][2]):
        arr_operation[idx][2].append(x[2])
  
  return arr_operation


def getArrTS(arr_num, array_transaksi):
  arr_TS = []
  for x in arr_num:
    arr_TS.append((x, getStartTS(array_transaksi, x), getFinishTS(array_transaksi, x), getFinishTS(array_transaksi, x)))
  return arr_TS

def getNumTransaction(arr):
  # Mengembalikan array berisi nomor transaksi
  arr_num = []
  for x in arr:
    if x[1] not in arr_num:
      arr_num.append(x[1])
  return arr_num

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

def getFinishTS(arr, num):
  finish = -1
  i = 0
  stop = False
  while i < len(arr) and not stop:
    if (arr[i][1] == str(num)):
      if (arr[i][0] == 'C'):
        finish = i
        stop = True
    i+=1
  return finish

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

  if (last_read != -1):
    return last_read + 1
  else:
    return first_write


occ(array_transaksi)