from simple_locking import *
from occ import *
# import from mvcc

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
print(myfile)
file.close()
print("Pilihan input :\n1. Simple Locking\n2. OCC\n3. MVCC")

inputUser = str(input("Input : "))
print()

if inputUser == "1":
    array_hasil = execute(array_transaksi)
elif inputUser=="2":
    print("OCC")
    array_hasil = occ(array_transaksi)
# else :


for jenis2, item2, transaksi2 in array_hasil:
    if jenis2 != "C":
        print(jenis2+item2+"("+transaksi2+"); ", end="")
    else:
        print(jenis2+item2+"; ", end="")
