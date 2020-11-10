def simple_lock(array_transaksi):
    waiting_queue = []
    array_with_lock = []
    xl = {}
    log = []

    i = 0

    # Dilakukan selama arraytransaksinya sudah dieksekusi semua dan waiting queue masih ada
    while len(array_transaksi) >= i or len(waiting_queue) > 0:

        if len(array_transaksi) > i:
            jenis, transaksi, item = array_transaksi[i]
        elif len(waiting_queue) != 0:
            jenis, transaksi, item = waiting_queue[0]
            waiting_queue.pop(0)

        # Jika item tidak di ekslusif lock
        if item not in xl and jenis != "C":
            found = False
            # Jika ada transaksi yang sama namun masih di waiting room, tidak bisa dieksekusi
            for jenis2, transaksi2, item2 in waiting_queue:
                if transaksi2 == transaksi and jenis2 != "C":
                    waiting_queue.append((jenis, transaksi, item))
                    string = "Operasi sebelumnya di transaksi yang sama masih di Waiting Queue, masukkan operasi ini ke waiting queue\nWaiting Queue = " + \
                        printQueue(waiting_queue)
                    log.append(string)
                    found = True
                    break
            # Jika tidak ada, bisa eksekusi (Berikan XL dan eksekusi)
            if found == False:
                xl[item] = transaksi
                array_with_lock.append(("XL", transaksi, item))
                array_with_lock.append((jenis, transaksi, item))
                string = "Lakukan ekslusif lock "+"XL"+transaksi + \
                    "("+item+")"+"\nEksekusi "+jenis+transaksi+"("+item+")"
                log.append(string)

        # Jika item di ekslusif lock
        elif item in xl and jenis != "C":
            found = False
            # Jika item yang diekslusif lock pada transaksi yang sama
            for item in xl:
                if xl[item] == transaksi:
                    array_with_lock.append((jenis, transaksi, item))
                    string = "Eksekusi "+jenis+transaksi+"("+item+")"
                    log.append(string)
                    found = True
                    break
            # Jika di ekslusif lock itemnya dan transaksinya berbeda
            if found == False:
                waiting_queue.append((jenis, transaksi, item))
                string = "Item " + item+" masih di XL trnasaksi lain, masukkan operasi ke waiting queue\nWaiting Queue = " + \
                    printQueue(waiting_queue)
                log.append(string)

        # Untuk jenis transaksi Commit
        elif jenis == "C":
            found = False
            idx = 0
            # Eksekusi semua yang menunggu di waiting room
            for jenis2, transaksi2, item2 in waiting_queue:
                # Jika transaksinya sama dan namun masih di XL sama transaksi lain, masukkan Commit ke Queue
                if transaksi2 == transaksi and item in xl:
                    waiting_queue.append((jenis, transaksi, item))
                    string = "Item " + item+" masih di XL transaksi lain, masukkan transaksi ke waiting queue\nWaiting Queue = " + \
                        printQueue(waiting_queue)
                    log.append(string)
                    found = True
                    break
                # Jika transaksinya sama dan namun tidak di XL sama transaksi lain, jalankan transaksi itu, masukkan Commit ke Queue
                elif transaksi2 == transaksi and item not in xl:
                    xl[item2] = transaksi2
                    array_with_lock.append(("XL", transaksi2, item2))
                    array_with_lock.append((jenis2, transaksi2, item2))
                    string = "Hapus dari waiting queue untuk " + jenis2+transaksi2 + \
                        "("+item2+")\nWaiting Queue = " + \
                        printQueue(waiting_queue)
                    string += "\nLakukan ekslusif lock XL"+transaksi2 + \
                        "("+item2+")\nEksekusi " + \
                        jenis2+transaksi2+"("+item2+")"
                    log.append(string)

                    waiting_queue.pop(idx)
                    waiting_queue.append((jenis, transaksi, item))

                    string = "Masukkan commit " + jenis + transaksi + \
                        " ke dalam waiting queue\nWaiting Queue = " + \
                        printQueue(waiting_queue)
                    log.append(string)

                    found = True
                    break
                idx = idx+1
            # Jika di waiting queue semua transaksinya tidak ada yang sama atau waiting queue sudah kosong
            if found == False:
                items = []
                # Buka semua ekslusif lock dan eksekusi Commit
                for item1 in xl:
                    if xl[item1] == transaksi:
                        items.append(item1)
                        array_with_lock.append(("UL", transaksi, item1))
                        string = "Unlock item "+"UL"+transaksi+"("+item1+")"
                        log.append(string)
                array_with_lock.append((jenis, transaksi, item))
                string = "Eksekusi "+jenis+transaksi
                log.append(string)
                for item2 in items:
                    xl.pop(item2)
        i = i+1
    return(printQueue(array_with_lock), log)

def printQueue(queue):
    string = ""
    for jenis2, item2, transaksi2 in queue:
        if jenis2 != "C":
            string = string + jenis2+item2+"("+transaksi2+"); "
        else:
            string = string + jenis2+item2+"; "
    return string
