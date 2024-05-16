#  Program ini adalah implementasi sederhana dari alat pengganti Netcat (nc) menggunakan Python. 
# Ini memberikan kemampuan untuk berkomunikasi melalui koneksi jaringan TCP/IP.

import sys 
import socket
import getopt
import threading
import subprocess
# 1. **Import Library**:
#     Program mengimpor beberapa modul standar Python seperti `sys`, `socket`, `getopt`, `threading`, dan `subprocess`, yang digunakan untuk komunikasi jaringan dan eksekusi perintah shell.

#Tentukan Beberapa Fariabel Gobal
listen = False
command = False
upload = False
execute = ""
target = ""
upload_destination = ""
port = 0
# 2. **Pengaturan Variabel Global**:
#     Program mendefinisikan beberapa variabel global yang akan digunakan dalam program,
# seperti `listen`, `command`, `upload`, `execute`, `target`, `upload_destination`, dan `port`.


#Menjalan kan Perintah dan Mengembaikan Output
def run_command(cmd):
    #Pangkas Baris Baru
    cmd = cmd.rstrip()

    # Jalankan Perintah dan dapatkan hasil kembali
    try:
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT,
                                        shell=True)
    except subprocess.subprocess.CalledProcessError as e:
        output = e.output

    #KIrim output kembali ke kelien 
    return output
# 3. **Fungsi `run_command`**: 
#      - Fungsi ini menjalankan perintah shell yang diterima sebagai argumen dan mengembalikan outputnya.



#ini menangai koneksi klien masuk 
def client_handler(client_socket):
    global upload 
    global execute
    global command

    # Periksa unggahan 
    if len(upload_destination):

        #Baca di semua byte dan tulis ke tujuan kami
        file_buffer = ""

        #Terus membaca data sampai tidak ada yang tersedia
        while True:
            data = client_socket.recv(1024)

            if not data:
                break
            else:
                file_buffer += data

        #Sekarang kita mengambil byte ini dan mencoba menuliskannya
        try:
            file_descriptor = open(upload_destination, "wb")
            file_descriptor.write(file_buffer.encode('utf-8'))
            file_descriptor.close()

            # mengakui bahwa kami menulis file
            client_socket.send(
                "File Berhasi DIsimpan Ke %s\r\n" % upload_destination)
        except OSError:
                client_socket.send(
                    "Gagal Menyimpan File Ke %s\r\n" % upload_destination)

    # Periksa eksekusi perintah             
    if len(execute):
        # Jalankan perintah
        output = run_command(execute)

        client_socket.send(output)

    # Sekarang kita masuk ke loop lain jika shell perintah diminta
    if command:

        while True:
            #Tampilkan prompt sederhana
            client_socket.send(("<BHP:#>").encode('utf-8')) 

            # Sekarang kita menerima sampai kita melihat umpan baris (masukkan kunci)
            cmd_buffer = b''
            while b"\n" not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024)

            # Kami memiliki perintah yang valid jadi jalankan dan kirim kembali hasilnya
            response = run_command(cmd_buffer)

            # Kirim kembali respons
            client_socket.send(response)
# 4. **Fungsi `client_handler`**:
#      - Fungsi ini menangani koneksi masuk dari klien. 
# Jika ada permintaan upload, fungsi ini membaca data dari klien dan menyimpannya ke file. 
# Jika ada perintah yang harus dieksekusi, fungsi ini menjalankan perintah tersebut dan mengirimkan outputnya ke klien.
# Jika mode shell perintah diaktifkan, fungsi ini akan membaca perintah dari klien, mengeksekusinya, dan mengirimkan outputnya kembali.


#Ini untuk koneksi masuk
def server_loop():
    global target
    global port

    #Jika tidak ada target yang ditentukan maka kita mendengarkan di semua antarmuka
    if not len(target):
        target = "0.0.0.0"

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target, port))
    server.listen(5)

    while True:
        client_socket, addr = server.accept ()

    # sspin off thread untuk menangani klien baru kami
        client_thread = threading.Thread(target=client_handler,
                                    args=(client_socket,))

        client_thread.start()

# 5. **Fungsi `server_loop`**: 
# Fungsi ini menginisialisasi server dan mulai mendengarkan koneksi masuk.
# Setiap kali ada koneksi baru, fungsi ini memulai thread baru untuk menangani koneksi tersebut.

#Jika kita tidak mendengarkan, kita adalah klien ... membuatnya begitu,
def client_sender(buffer):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((target, port))
        # Terhubung ke host target kami

        # Jika kami mendeteksi input dari STDIN, kirimkan
        #Jika tidak, kita akan menunggu pengguna untuk memasukkan beberapa 
        if len(buffer):
            client.send(buffer.encode('utf-8'))

        while True:
            #Sekarang kita tunggu datanya kembali
            recv_len = 1
            response = b''

            while recv_len:
                data = client.recv(4096)
                recv_len = 1
                response = b''

                if recv_len < 4096:
                    break

            print(response.decode('utf-8'), end=' ')

            # Tunggu lebih banyak masukan
            buffer = input("")
            buffer += "\n"

            #kirim
            client.send(buffer.encode('utf-8'))

    except socket.error as exc:
        #Hanya menangkap kesalahan enerik - Anda dapat melakukan pekerjaan rumah Anda untuk meningkatkan ini
        print("[*] Pengecualian Keluar.")
        print(f"[*] tertangkap pengecualian socket.error: {exc}")

        #Hancurkan koneksi
        client.close()  
# 6. **Fungsi `client_sender`**: 
#      - Fungsi ini digunakan untuk mengirim data ke server.
#      - Jika ada data yang dimasukkan dari `stdin`, data tersebut akan dikirimkan ke server.
#      - Kemudian, fungsi ini menunggu untuk menerima data dari server dan mencetaknya ke `stdout`.

def usage():
    print("Penggantian Netcat")
    print()
    print("penggunaan: bhpnet.py -t target_host -p port")
    print(
        "-l --listen - dengarkan di [host]:[port] untuk masuk "
        "Koneksi")
    print(
        "-e --execute=file_to_run - jalankan file yang diberikan setelah menerima "
        "Sebuah connectio")
    print("-c --command - menginisialisasi shell perintah")
    print(
        "-u --upload=destination - setelah menerima koneksi, unggah file "
        "dan menulis surat ke [tujuan]")
    print()
    print()
    print("Penggunaan: ")
    print("bhpnet.py -t 192.168.0.1 -p 5555 -l -c")
    print("bhpnet.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe")
    print("bhpnet.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\"")
    print("echo 'ABCDEFGHI' | ./bhpnet.py -t 192.168.11.12 -p 135")
    sys.exit(0)
# 7. **Fungsi `usage`**:
#      - Fungsi ini digunakan untuk mencetak pesan bantuan yang menjelaskan cara menggunakan program.



def main():
    global listen
    global port 
    global execute
    global upload_destination
    global target

    if not len(sys.argv[1:]):
        usage()

    # Baca opsi baris perintah
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:",
                                   ["help", "listen", "execute", "target",
                                    "port", "command", "upload"])
        for o, a in opts:
            if o in ("-h", "--help"):
                usage()
            elif o in ("-l", "--listen"):
                listen = True
            elif o in ("-e", "--execute"):
                execute = a
            elif o in ("-c", "--commandshell"):
                command = True
            elif o in ("-u", "--upload"):
                upload_destination = a
            elif o in ("-t", "--target"):
                target = a
            elif o in ("-p", "--port"):
                port = int(a)
            else:
                assert False, "Opsi Tidak DItangani"

    except getopt.GetoptError as err:
        print(str(err))
        usage()

    # apakah kita akan mendengarkan atau hanya mengirim data dari STDIN?
    if not listen and len(target) and port > 0:
        # baca di buffer dari baris perintah
        # ini akan memblokir, jadi kirim CTRL-D jika tidak mengirim input
        # untuk stdin
        buffer = sys.stdin.read()

        # Kirim data mati
        client_sender(buffer)

    # we are going to listen and potentially
    # upload things, execute commands and drop a shell back
    # depending on our command line options above
    if listen:
        server_loop()

# 8. **Fungsi `main`**: 
#      - Fungsi ini adalah titik masuk utama program. 
#      - Ini memproses argumen baris perintah,
#      - menentukan mode operasi (apakah untuk mendengarkan atau mengirim), 
#      - dan memanggil fungsi yang sesuai berdasarkan opsi yang diberikan.

main()

# 9. **Eksekusi Utama**: Program memanggil fungsi `main` untuk memulai eksekusi program.

# program ini memberikan fungsi dasar untuk berkomunikasi melalui jaringan TCP/IP, mengunggah dan mengunduh file, menjalankan perintah shell, serta membuka shell interaktif.

# ========================================================================
