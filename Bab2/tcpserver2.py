import socket
import threading
from urllib import request

bind_ip = "0.0.0.0"
bind_port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((bind_ip, bind_port))

server.listen(5)

print("[*] Mendengarkan %s:%d" % (bind_ip, bind_port))


# Ini adalah utas penanganan klien kami 
def handle_client(client_socket):
    # Cukup cetak apa yang dikirim klien
    request = client_socket.recv(1024)

    print("[*] Diterima: %s" % request)

    # Kirim kembali paket
    client_socket.send(b"ACK!")
    print(client_socket.getpeername())
    client_socket.close()

while True:
    client, addr = server.accept()

    print("[*] Koneksi yang diterima dari: %s:%d" % (addr[0], addr[1]))

    # Putar utas klien kami untuk menangani data yang masuk
    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()

# ============================================================================

# Kode ini adalah server TCP sederhana yang dapat menerima koneksi dari klien dan menangani setiap koneksi dalam thread terpisah. Berikut adalah penjelasan singkatnya:

# 1. **Impor modul**: Kode mengimpor modul `socket` dan `threading` yang diperlukan untuk membuat server dan menangani klien dalam thread terpisah.

# 2. **Menetapkan IP dan Port**: IP yang diikat (`bind_ip`) disetel ke `"0.0.0.0"`, yang berarti server akan mendengarkan semua antarmuka jaringan yang tersedia di mesin. Port yang diikat (`bind_port`) disetel ke `9999`.

# 3. **Membuat Socket**: Objek socket server dibuat dengan menggunakan `socket.socket()` dengan parameter `socket.AF_INET` untuk alamat IPv4 dan `socket.SOCK_STREAM` untuk socket TCP.

# 4. **Mengikat dan Mendengarkan**: Server diikat ke alamat dan port yang ditentukan menggunakan metode `bind()`, dan kemudian memanggil `listen()` untuk mulai mendengarkan koneksi masuk. Argumen `5` di `listen()` menunjukkan bahwa server akan menerima hingga 5 koneksi yang tertunda sebelum menolak koneksi baru.

# 5. **Fungsi Penangan Klien**: Fungsi `handle_client()` akan dieksekusi dalam thread terpisah untuk menangani koneksi dari setiap klien. Fungsi ini menerima socket klien sebagai argumen.

# 6. **Menerima Koneksi**: Dalam loop tak terbatas, server menerima koneksi masuk menggunakan `accept()`, yang mengembalikan objek socket klien dan alamat IP dan port klien.

# 7. **Menangani Koneksi**: Setelah koneksi diterima, server mencetak alamat klien dan menyiapkan thread baru (`client_handler`) untuk menangani koneksi tersebut. Fungsi `handle_client()` akan dipanggil dalam thread terpisah untuk menangani setiap koneksi.

# 8. **Penangan Klien**: Fungsi `handle_client()` menerima data dari klien menggunakan `recv()`, mencetak pesan yang diterima, mengirimkan respons kembali ke klien menggunakan `send()`, dan menutup koneksi.

# Kode ini berjalan dalam loop tak terbatas, sehingga server akan tetap berjalan dan menerima koneksi selama program dijalankan.
