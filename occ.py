global solved_item
solved_item = []

def validateProtocol(array_transaksi):
  print(array_transaksi)
  arr_num = getNumTransaction(array_transaksi)
  arr_TS = getArrTS(arr_num, array_transaksi)
  arr_operation = getTransactionOperation(array_transaksi, arr_num)
  occ(array_transaksi, arr_num, arr_TS, arr_operation)

def occ(array_transaksi, arr_num, arr_TS, arr_operation):
  # Check for all transaction
  stop = False
  while(len(array_transaksi)!=0):
    if(array_transaksi[0][0] == 'R'):
      print("Transaksi", array_transaksi[0][1], "membaca item data", array_transaksi[0][2])
      solved_item.append(array_transaksi.pop(0))
    elif(array_transaksi[0][0] == 'W'):
      print("Transaksi", array_transaksi[0][1], "menulis item data", array_transaksi[0][2], "ke lokal variabel")
      solved_item.append(array_transaksi.pop(0))

    elif(array_transaksi[0][0] == 'C'):
      print()
      x = array_transaksi[0][1]
      print('Melakukan Validasi Transaksi :', x)
      isValidThisTrans = isValidTransaction(array_transaksi, x, arr_TS, arr_num, arr_operation)
      if(isValidThisTrans):
        print("Transaksi", x, "lolos validasi, menuliskan data ke db dan commit")
        print("Transaksi", x, "Selesai\n")
      else:
        print("Transaksi", x, "gagal")
        print("Transasksi di-rollback\n")
        stop = True
      solved_item.append(array_transaksi.pop(0))

    if(stop):
      print("stop")
      for y in (solved_item):
        if (y[1] == x):
          array_transaksi.append(y)
          solved_item.remove(y)

      all_arr = solved_item + array_transaksi
      print(all_arr)
      print(arr_TS)
      arr_TS = getArrTS(arr_num, all_arr)
      print(arr_TS)   
      break

  if(len(array_transaksi)!=0):
    occ(array_transaksi, arr_num, arr_TS, arr_operation)


def changePrintFormat(arr):
  readable_format = ""
  for x in arr:
    activity = x[0] + x[1]
    if(x[0] != 'C'):
      activity += "(" +x[2] + "); " 
    else:
      activity += "; "
    readable_format += activity
  return readable_format
  

def isValidTransaction(arr, num, arr_TS, arr_num, arr_operation):
  isCurrentValid = True
  check_queue = []
  for x in arr_TS:
    if(int(x[3]) < arr_TS[arr_num.index(num)][3]):
      check_queue.append(x)
  
  if (check_queue):
    print("Transaksi", num, "akan diperiksa terhadap Transaksi : ", end='')
    for x in check_queue:
      print(x[0], end=' ')
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
        print("Transaksi", str(TJ[0]), "membaca data yang dituliskan oleh Transaksi", str(TI[0]), "Menyebabkan kegagalan")
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


# serial = occ(array_transaksi)
# print(serial)