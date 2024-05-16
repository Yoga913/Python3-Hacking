import socket
import threading

bind_ip = "0.0.0.0"
bind_port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# inisialisasi variable server : Program menetapkan alamat dan port server, kemudian membuat objek socket menggunakan modul socket. Jenis socket yang digunakan adalah SOCK_STREAM untuk koneksi TCP.

server.bind((bind_ip, bind_port))

server.listen(5)

# mengikat dan mendengarkan koneksi : Server mengikat alamat dan port yang telah ditetapkan, lalu memulai mendengarkan koneksi. Jumlah maksimal antrian koneksi yang dapat ditangani adalah 5.

print("[*] Listening on %s:%d" % (bind_ip, bind_port))

# tampilan pesan awal : Program mencetak pesan yang menunjukkan bahwa server telah dimulai dan sedang mendengarkan koneksi.

# this is our client handling thread
def handle_client(client_socket):
    # just print out what the client sends
    request = client_socket.recv(1024)

    print("[*] Received: %s" % request)

    # send back a packet
    client_socket.send(b"ACK!")
    print(client_socket.getpeername())
    client_socket.close()

# fungsi handle klien : Fungsi ini menangani setiap koneksi klien. Data yang diterima dari klien dicetak, kemudian server mengirim balasan sederhana ("ACK!") ke klien, dan koneksi ditutup.

while True:
    client, addr = server.accept()

    print("[*] Accepted connection from: %s:%d" % (addr[0], addr[1]))

    # spin up our client thread to handle incoming data
    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()

# loop utama : Program memasuki loop utama yang terus mendengarkan koneksi. Setiap kali ada koneksi baru, server menerima koneksi tersebut dan membuat thread baru (client_handler) untuk menangani koneksi tersebut, sementara server tetap mendengarkan koneksi lainnya.

# ======================================================================================================================================================= # 
# Program Python di atas adalah contoh sederhana dari server TCP yang menerima koneksi dari klien dan menanggapi data yang dikirim oleh klien.

# Manfaat:
# Program ini menyediakan kerangka dasar untuk membuat server sederhana yang dapat menerima koneksi dari klien.
# Manfaatnya antara lain:
# Menyediakan titik awal untuk memahami konsep dasar server dan koneksi TCP.
# Dapat dijadikan dasar untuk mengembangkan server yang lebih kompleks, seperti server web atau aplikasi jaringan.

# Cara Penggunaan:
# Tentukan alamat dan port yang akan digunakan oleh server dengan mengubah nilai variabel bind_ip dan bind_port.
# Jalankan program untuk memulai server.
# Klien dapat terhubung ke server menggunakan alamat dan port yang sesuai.

# Pengembangan Potensial:
# Program ini dapat dikembangkan lebih lanjut dengan menambahkan fitur-fitur berikut:

# Manajemen Koneksi yang Lebih Baik: Mengelola koneksi dari banyak klien, menangani koneksi yang terputus, dan mengimplementasikan logika pemutusan koneksi yang aman.
# Protokol Komunikasi yang Lebih Canggih: Mengembangkan protokol komunikasi yang lebih kompleks antara server dan klien.
# Keamanan: Menambahkan lapisan keamanan seperti SSL/TLS untuk mengamankan komunikasi antara server dan klien.
# Manajemen Thread yang Lebih Efisien: Mengelola thread dengan lebih efisien dan mempertimbangkan penggunaan ThreadPool untuk meningkatkan kinerja.
