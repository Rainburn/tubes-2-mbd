# import from simple locking
# import from occ
# import from mvcc

file = open("data-input.txt", "r")
arr = file.read().split("; ")

array_transaksi = []
for data in arr:
    jenis = data[0]
    if jenis != "C":
        item = data[-2]
        transaksi = data[1:-3]
    else:
        item = ""
        transaksi = data[1:]

    array_transaksi.append((jenis, transaksi, item))

print(array_transaksi)
file.close()
print("Pilihan input :\n1. Simple Locking\n2. OCC\n3. MVCC")
inputUser = str(input("Input : "))
# if inputUser=="1":

# else if inputUser=="2":

# else :
