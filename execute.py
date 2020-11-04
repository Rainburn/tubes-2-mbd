
file = open("data-input.txt", "r")
arr = file.read().split("; ")

array_transaksi = []
for data in arr:
    jenis = data[0]
    transaksi = data[1]
    if jenis != "C":
        item = data[3]
    else:
        item = ""
    array_transaksi.append((jenis, transaksi, item))

print(array_transaksi)

file.close()
