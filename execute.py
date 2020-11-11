import random
import string
from simple_locking import *
from occ import *
from mvcc import *
import time


def schedule_generator():
    dictionary = {}
    array_akhir = []
    array_only_read = []
    jumlah_transaksi = int(input("Masukkan jumlah transaksi(Max=50) : "))
    for i in range(1, jumlah_transaksi+1):
        j = str(i)
        dictionary[j] = 0
        if (random.randint(1,10) < 8):
            array_only_read.append(j)
    tr = 0
    jumlah_proses = int(
        input("Masukkan jumlah proses dalam satu transaksi(Max=50) : "))
    pr = 0
    jumlah_item = int(input("Masukkan jumlah item transaksi(Max=26): "))
    it = 0
    while dictionary:
        transaksi = addProses(dictionary)
        if(transaksi in array_only_read):
            jenis = "R"
        else :
            jenis = findWriteRead()
        item = findItem(jumlah_item)
        if str(dictionary[transaksi]) == str(jumlah_transaksi):
            jenis = "C"
            item = ""
            dictionary.pop(transaksi)
            array_akhir.append(("C", transaksi, item))
        else:
            array_akhir.append((jenis, transaksi, item))
    return array_akhir

def addProses(dictionary):
    rand_string = random.choices(list(dictionary.keys()))
    element = dictionary[rand_string[0]]
    dictionary[rand_string[0]] = element+1
    return rand_string[0]


def findWriteRead():
    arr = ["W", "R"]
    rand_string = random.choice(arr)
    return str(rand_string)


def findItem(maxNumber):
    arr = list(string.ascii_uppercase)
    array = []
    for i in range(maxNumber):
        array.append(arr[i])
    rand_string = (random.choices(array))
    return str(rand_string[0])


def printQueue(queue):
    string = ""
    for jenis2, item2, transaksi2 in queue:
        if jenis2 != "C":
            string = string + jenis2+item2+"("+transaksi2+"); "
        else:
            string = string + jenis2+item2+"; "
    return string


array_transaksi = []
pilihan = int(
    input("1.Masukkan dari data-input.txt\n2.Schedule Generator\nPilih masukkan : "))

if pilihan == 1:
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
else:
    array_transaksi = schedule_generator()


print("Ini schedule transaksi anda")
print(printQueue(array_transaksi), end="\n")

print("Pilihan input :\n1. Simple Locking\n2. OCC\n3. MVCC")

inputUser = str(input("Input : "))
print()

array_hasil = []
if inputUser == "1":
    print("Harap menunggu ...")
    start_time = time.time()
    array_hasil, logs = simple_lock(array_transaksi)
    print("Transaksi selesai")
    times = time.time() - start_time
    print(array_hasil)
    print("Exec time : " + str(times), end="\n")


elif inputUser == "2":
    print("OCC")
    print("Harap menunggu ...")
    start_time = time.time()
    array_hasil = validateProtocol(array_transaksi)
    print("Schedlue selesai dieksekusi, hasil salah satu shedule yang memenuhi validasi")
    times = time.time() - start_time
    print(array_hasil)
    print("Exec time : " + str(times), end="\n")

elif inputUser == "3" :
    print("Multiversion Timestamp")
    print("Harap menunggu ...")
    start_time = time.time()
    array_hasil = multiversion_timestamp(array_transaksi)
    print("Ordering dengan multiversion timestamp selesai")
    times = time.time() - start_time
    print(array_hasil)
    print("Exec time : " + str(times), end="\n")
    