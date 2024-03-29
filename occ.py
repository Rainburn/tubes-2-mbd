import random

global solved_item, local_dict
solved_item = []
local_dict = {}

# Mengekstrak data yang diperlukan untuk menjalankan OCC
def validateProtocol(array_transaksi):
  iterasi = 0
  arr_num = getNumTransaction(array_transaksi)
  arr_TS = getArrTS(arr_num, array_transaksi)
  arr_operation = getTransactionOperation(array_transaksi, arr_num)
  occ(array_transaksi, arr_num, arr_TS, arr_operation, iterasi)
  return changePrintFormat(solved_item)

# Protocol OCC
def occ(array_transaksi, arr_num, arr_TS, arr_operation, iterasi):
  stop = False
  # Menjalankan tiap transaksi
  while(len(array_transaksi)!=0):
    index = arr_num.index(array_transaksi[0][1])
    if(arr_TS[index][1] == iterasi):
      print("Transaksi", arr_TS[index][0], "Start")
    iterasi+=1
    if(array_transaksi[0][0] == 'R'):
      print("Transaksi", array_transaksi[0][1], "membaca item data", array_transaksi[0][2])
      solved_item.append(array_transaksi.pop(0))
    elif(array_transaksi[0][0] == 'W'):
      print("Transaksi", array_transaksi[0][1], "menulis item data", array_transaksi[0][2], "ke lokal variabel")
      if(array_transaksi[0][1] not in local_dict):
        local_dict[array_transaksi[0][1]] = []
      local_dict[array_transaksi[0][1]].append(array_transaksi[0][2])
      solved_item.append(array_transaksi.pop(0))

    # Jika transaksi akan commit, transaksi tersebut divalidasi
    elif(array_transaksi[0][0] == 'C'):
      print()
      x = array_transaksi[0][1]
      print('Melakukan Validasi Transaksi :', x)
      isValidThisTrans = isValidTransaction(array_transaksi, x, arr_TS, arr_num, arr_operation)

      # Jika validasi berhasil, data local akan ditulis ke dalam DB, transaksi akan commit dan selesai
      if(isValidThisTrans):
        print("Transaksi", x, "lolos validasi")
        if(x in local_dict):
          print("Transaksi", x, "Menuliskan local variabel item", local_dict[x], "ke database")
        print("Transaksi", x, "commit dan selesai\n")
      
      # Jika validasi gagal, maka akan di rollback dan berjalan secara konkuren dengan transaksi yang belum dieksekusi
      else:
        print("Transaksi", x, "gagal")
        print("Transaksi di-rollback, berjalan secara konkuren dengan transaksi yang lain\n")
        if(x in local_dict): 
          local_dict.pop(x)
        stop = True
      solved_item.append(array_transaksi.pop(0))

    # Jika rollback maka transaksi akan akan dihapus dari array penyelesaian
    # Akan dijalankan secara konkuren dengan transaksi lain 
    if(stop):
      rolledback_trans = []
      i = 0
      while i < len(solved_item):
        if (solved_item[i][1] == x):
          rolledback_trans.append(solved_item[i])
          solved_item.remove(solved_item[i])
          i -=1
        i+=1

      array_transaksi = concatConcurrency(array_transaksi, rolledback_trans)
      all_arr = solved_item + array_transaksi
      arr_TS = getArrTS(arr_num, all_arr)
      break
  
  # Jika masih ada transaksi yang harus dijalankan
  if(len(array_transaksi)!=0):
    occ(array_transaksi, arr_num, arr_TS, arr_operation, iterasi-len(rolledback_trans))


# Melalukan pengecekan apakah validasi berhasil atau tidak
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

# Melakukan Perbandingan ValidateTS antara transaksi yang sedang divalidasi dengan transaksi yang 
# memiliki ValidateTS lebih kecil darinya
def compareTS(TI, TJ, arr_num, arr_operation):
  # TJ adalah transaksi yang ingin divalidasi
  # finishTS(TI) < startTS(TJ)
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
          intersect_item = arr_operation[arr_num.index(TJ[0])][1][i]
      if(isNotIntersect):
        print("Transaksi", str(TJ[0]), "tidak membaca data yang dituliskan oleh Transaksi", str(TI[0]))
      else:
        print("Transaksi", str(TJ[0]), "membaca data yang dituliskan oleh Transaksi", str(TI[0]), "yaitu item data",intersect_item, "(Menyebabkan kegagalan)")
      return isNotIntersect
    
    # Jika tidak termasuk kedua kondisi di atas maka validasi gagal
    else:
      print("Pengecekan dengan transaksi", str(TI[0]),"Tidak memenuhi dua kondisi syarat validation based")
      return False

# Memasukkan Transaksi yang di rollback ke shcedule yang sedang berjalan
def concatConcurrency(array_transaksi, rolledback_trans):
  change_idx = True
  interval = 2
  idx = len(array_transaksi)//3
  for x in reversed(rolledback_trans):
    array_transaksi.insert(idx, x)
    if(idx - interval > 0 and change_idx):
      idx = idx - interval
    change_idx = random.choice([True, False])
  return array_transaksi

# Mencetak transasksi sesuai format yang ditentukan
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

# Mengembalikan data yang di-read dan di-write oleh setiap transaksi
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

# Mendapatkan startTS dan validateTS dari transaksi
def getArrTS(arr_num, array_transaksi):
  arr_TS = []
  for x in arr_num:
    arr_TS.append((x, getStartTS(array_transaksi, x), getCommitTS(array_transaksi, x), getCommitTS(array_transaksi, x)))
  return arr_TS

# Mengembalikan array berisi nomor transaksi
def getNumTransaction(arr):
  arr_num = []
  for x in arr:
    if x[1] not in arr_num:
      arr_num.append(x[1])
  return arr_num

# Mendapatkan strat transaksi
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

# Mengembalikan Commit transaksi
def getCommitTS(arr, num):
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
