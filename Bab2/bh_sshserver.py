# Program ini adalah implementasi sederhana dari sebuah server SSH menggunakan Python dan modul Paramiko.
#  Server ini akan mendengarkan koneksi pada alamat dan port yang ditentukan, dan kemudian akan menerima koneksi SSH dari klien yang terhubung.

import socket
import paramiko
import threading
import sys 
# 1. **Import Library**: 
# Program mengimpor modul :
# `socket`, `paramiko`, `threading`, dan `sys`, yang diperlukan untuk membuat server SSH.

#using the server host key frorm the paramiko demo
host_key = paramiko.RSAKey(filename='test_rsa.key')
# 2. **Membuat Kunci Host**: Program menginisialisasi kunci RSA dari file yang disebut `test_rsa.key` yang akan digunakan untuk otentikasi server.


class Server(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()
        # 3. **Kelas Server**:
        #      - Program mendefinisikan kelas `Server` yang merupakan subclass dari `paramiko.ServerInterface`.
        #      - Kelas ini digunakan untuk mengimplementasikan kebijakan otentikasi dan mengelola permintaan klien.

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
        # 4. **Fungsi `check_channel_request`**: 
        #      - Fungsi ini memeriksa permintaan saluran baru dari klien dan memutuskan apakah permintaan tersebut diterima atau ditolak. 
        # Dalam kasus ini, hanya jenis saluran sesi yang diizinkan.

    def check_auth_password(self, username, password):
        if username == 'root' and password == 'toor':
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED
        # 5. **Fungsi `check_auth_password`**: 
        #      - Fungsi ini memeriksa otentikasi berdasarkan nama pengguna dan kata sandi yang diberikan oleh klien. 
        # Jika nama pengguna adalah 'root' dan kata sandinya adalah 'toor', otentikasi berhasil.


server = sys.argv[1]
ssh_port = int(sys.argv[2])
# 6. **Membaca Alamat dan Port**: 
#     - Program membaca alamat IP server 
#     - dan port SSH dari argumen baris perintah.

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((server, ssh_port))
    sock.listen(100)
    print("[+] Mendaengarkan Koneksi...")
    client, addr = sock.accept()
except Exception as e:
    print("[-] Mendengarkan Gagal: " + str(e))
    sys.exit(1)

print("[+] Punya Koneksi!")
# 7. **Mendengarkan Koneksi**: 
#    - Program membuat socket, 
#    - mengikatnya ke alamat dan port yang ditentukan, 
#    - dan mulai mendengarkan koneksi masuk.
# Ketika koneksi diterima, program mencetak pesan bahwa koneksi diterima.
try:
    #noinspection PyTypeChecker
    bhSession = paramiko.Transport(client)
    bhSession.add_server_key(host_key)
    server = Server()
    # 8. **Memulai Session SSH**: 
    #      - Program membuat objek `Transport` dari Paramiko dan menambahkan kunci host ke dalamnya. 
    #        Kemudian, server SSH dimulai dengan menggunakan objek `Server` yang telah didefinisikan sebelumnya.
    try:
        bhSession.start_server(server=server)
    except paramiko.SSHException:
        print("[-] Negosiasi SSH gagal.")
    chan = bhSession.accept(20)
    print(chan.recv(1024))
    chan.send("Selamat datang di bh_ssh!")
    # 9. **Menerima Koneksi SSH**:
    #     # Program menerima koneksi SSH dari klien dan mencetak pesan selamat datang. 
    #       Kemudian, program memulai loop tak terbatas untuk menerima perintah dari pengguna.
    while True:
        try:
            command = input("Masukkan perintah: ").strip("\n")
            if command != 'exit':
                chan.send(command)
                print(chan.recv(1024).decode(errors="ignore") + "\n")
            else:
                chan.send("exit")
                print("Keluar...")
                bhSession.close()
                raise Exception("exit")
        except KeyboardInterrupt:
            bhSession.close()
        except Exception as e:
            print("[-] Pengecualian tertangkap: " + str(e))
            bhSession.close()
finally:
    sys.exit(1)
    # 10. **Menerima Perintah dari Pengguna**:
    #       - Program menunggu pengguna untuk memasukkan perintah dari konsol. 
    #       - Perintah yang dimasukkan akan dikirim ke klien melalui koneksi SSH.
    #       - Program akan menerima output dari klien dan mencetaknya ke konsol.
    #  Jika pengguna memasukkan perintah 'exit', program akan keluar dari loop dan menutup koneksi SSH.

#  keseluruhan tujuan dari program ini adalah untuk membuat server SSH sederhana yang dapat menerima koneksi dari klien SSH dan menerima perintah dari pengguna.
# ====================================================================================================================================================================
