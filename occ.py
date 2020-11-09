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

print(myfile)
def occ(array_transaksi):
  print("OCC")
  print(array_transaksi)
  base_array = array_transaksi.copy()
  arr_num = getNumTransaction(array_transaksi)
  arr_TS = getArrTS(arr_num, array_transaksi)
  arr_operation = getTransactionOperation(array_transaksi, arr_num)

  # Check for all transaction
  rolledback_queue = []
  for x in (arr_num):
    print('Transaksi :', x)
    isValidThisTrans = isValidTransaction(array_transaksi, x, arr_TS, arr_num, arr_operation)
    if(isValidThisTrans):
      print("Hasil : Transaksi", x, "berhasil")
    else:
      print("Hasil : Transaksi", x, "gagal")
      print("Transasksi di-rollback")
      for y in (array_transaksi):
        if (y[1] == x):
          rolledback_queue.append(y)
    print()
  
  if(rolledback_queue):
    occ(rolledback_queue)


def isValidTransaction(arr, num, arr_TS, arr_num, arr_operation):
  isCurrentValid = True
  check_queue = []
  if(arr_TS):
    print("Transaksi", num, "akan diperiksa terhadap Transaksi : ", end='')
    for x in arr_TS:
      if(int(x[3]) < arr_TS[arr_num.index(num)][3]):
        print(x[0], "", end='')
        check_queue.append(x)
    print()
  else:
    print("Transaksi", num, "Tidak diperiksa terhadap transaksi mana pun")

  # Check for current transaction to all transaction before
  i = 0
  while i < len(check_queue) and isCurrentValid:
    isCurrentValid = compareTS(check_queue[i], arr_TS[arr_num.index(num)], arr_num, arr_operation)
    i+=1
  return isCurrentValid

def compareTS(TI, TJ, arr_num, arr_operation):
  # finishTS(TI) < startTS(TJ)
  # startTS = 1, finishTS = 2, validateTS = 3
  if (TI[2] < TJ[1]):
    print("Transaksi", str(TJ[0]), "mulai setelah Transaksi", str(TI[0]), "selesai")
    return True
  else:
    if(TJ[1] < TI[2] and TI[2] < TJ[3]):
      print("Transaksi", str(TI[0]), "finish di antara start dan validate transaksi", str(TJ[0]))
      # check apakah dia melakukan read kepada item data yg di write transaksi sebelumnya
      isNotIntersect = True
      for i in range(len(arr_operation[arr_num.index(TJ[0])][1])):
        if(arr_operation[arr_num.index(TJ[0])][1][i] in arr_operation[arr_num.index(TI[0])][2]):
          isNotIntersect = False
      if(isNotIntersect):
        print("Transaksi", str(TJ[0]), "tidak membaca data yang dituliskan oleh Transaksi", str(TI[0]))
      else:
        print("Transaksi", str(TJ[0]), "membaca data yang dituliskan oleh Transaksi", str(TI[0]), "menyebabkan kegagalan")
      return isNotIntersect
    else:
      print("Pengecakan dengan transaksi", str(TI[0]),"Tidak memenuhi dua kondisi syarat validation based")
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