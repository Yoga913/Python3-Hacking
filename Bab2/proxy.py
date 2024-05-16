import sys
import socket
import threading


# Ini adalah fungsi dumping hex cantik yang langsung diambil dari
# http://code.activestate.com/recipes/142812-hex-dumper/

def hexdump(src, length=16):
    result = []
    digits = 4 if isinstance(src, str) else 2

    for i in range(0, len(src), length):
        s = src[i:i + length]
        hexa = b' '.join([b"%0*X" % (digits, ord(x)) for x in s])
        text = b''.join([x if 0x20 <= ord(x) < 0x7F else b'.' for x in s])
        result.append(
            b"%04X   %-*s   %s" % (i, length * (digits + 1), hexa, text))

    print(b'\n'.join(result))


def receive_from(connection):
    buffer = b''

    # Kami menetapkan time-out 2 detik. Tergantung pada target Anda, ini mungkin perlu:
    # untuk disesuaikan
    connection.settimeout(2)

    try:

        # Teruslah membaca buffer sampai tidak ada lagi data atau kami
        # batas waktu
        while True:
            data = connection.recv(4096)
            if not data:
                break
            buffer += data

    except TimeoutError:
        pass

    return buffer


# Ubah permintaan apa pun yang ditujukan untuk host jarak jauh
def request_handler(buffer):
    # melakukan modifikasi paket
    return buffer


# Ubah respons apa pun yang ditujukan untuk host lokal
def response_handler(buffer):
    # Melakukan modivikasi paket
    return buffer


def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    # Sambungkan Ke host Jarak Jauh
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    # Terima data dari ujung jarak jauh jika perlu
    if receive_first:
        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)

        # send it to our response handler
        remote_buffer = response_handler(remote_buffer)

        # jika kami memiliki data untuk dikirim ke klien lokal kami, kirimkan
        if len(remote_buffer):
            print("[<==] Mengirim% d byte ke localhost." % len(remote_buffer))
            client_socket.send(remote_buffer)

    # Sekarang mari kita loop dan membaca dari lokal, kirim ke remote, kirim ke lokal
    # bilas cuci ulangi
    while True:
        # read from local host
        local_buffer = receive_from(client_socket)

        if len(local_buffer):
            print("[==>] Menerima %d byte dari localhost." % len(local_buffer))
            hexdump(local_buffer)

            # kirimkan ke penangan permintaan kami
            local_buffer = request_handler(local_buffer)

            # Kirim data ke host jarak jauh
            remote_socket.send(local_buffer)
            print("[==>] Dikirim Ke remot.")

        # Terima kembali responsnya
        remote_buffer = receive_from(remote_socket)

        if len(remote_buffer):
            print("[<==] Menerima %d byte dari remote." % len(remote_buffer))
            hexdump(remote_buffer)

            # Kirim ke penangan respons kami
            remote_buffer = response_handler(remote_buffer)

            # Kirim respons ke soket lokal
            client_socket.send(remote_buffer)

            print("[<==] Dikirim ke localhost.")

        # jika tidak ada lagi data di kedua sisi, tutup koneksi
        if not len(local_buffer) or not len(remote_buffer):
            client_socket.close()
            remote_socket.close()
            print("[*] Tidak ada lagi data. Menutup koneksi.")
            break


def server_loop(local_host, local_port, remote_host, remote_port,
                receive_first):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((local_host, local_port))
    except socket.error as exc:
        print("[!!] Gagal Mendengarkan di %s:%d" % (local_host,
                                                  local_port))
        print("[!!] Periksa soket mendengarkan lainnya atau perbaiki "
              "izin.")
        print(f"[!!] Kesalahan pengecualian tertangkap: {exc}")
        sys.exit(0)

    print("[*] Mendengarkan di %s:%d" % (local_host, local_port))

    server.listen(5)

    while True:
        client_socket, addr = server.accept()

        # Mencetak informasi koneksi lokal
        print("[==>] Menerima koneksi masuk dari %s:%d" % (
            addr[0], addr[1]))

        # Memulai utas untuk berbicara dengan host jarak jauh
        proxy_thread = threading.Thread(target=proxy_handler, args=(
            client_socket, remote_host, remote_port, receive_first))
        proxy_thread.start()


def main():
    # Tidak ada penguraian baris perintah mewah di sini
    if len(sys.argv[1:]) != 5:
        print("Penggunaan: ./proxy.py [localhost] [localport] [remotehost] "
              "[remoteport] [receive_first]")
        print("Contoh: ./proxy.py 127.0.0.1 9000 10.12.132.1 9000 True")
        sys.exit(0)

    # Menyiapkan parameter mendengarkan lokal
    local_host = sys.argv[1]
    local_port = int(sys.argv[2])

    # Siapkan target jarak jauh
    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])

    # Ini memberitahu proxy kami untuk menghubungkan dan menerima data
    # sebelum mengirim ke host jarak jauh
    receive_first = sys.argv[5]

    if "True" in receive_first:
        receive_first = True
    else:
        receive_first = False

    # Sekarang putar soket mendengarkan kami
    server_loop(local_host, local_port, remote_host, remote_port, receive_first)


main()

# ============================================================================================= 
# Program ini adalah sebuah *proxy server* sederhana yang memungkinkan untuk memantau dan memodifikasi lalu lintas data antara klien lokal dan server jarak jauh. Berikut adalah penjelasan singkat tentang alur kerjanya:

# 1. **Fungsi `hexdump(src, length=16)`**: Ini adalah fungsi untuk mencetak data dalam format heksadesimal yang mudah dibaca. Fungsi ini mengambil input data `src` dan opsional `length` yang menentukan jumlah byte yang dicetak dalam satu baris.

# 2. **Fungsi `receive_from(connection)`**: Fungsi ini digunakan untuk menerima data dari koneksi yang diberikan (`connection`) dan mengembalikan data yang diterima.

# 3. **Fungsi `request_handler(buffer)` dan `response_handler(buffer)`**: Fungsi-fungsi ini digunakan untuk memodifikasi data yang dikirim dan diterima. Pada implementasi ini, mereka hanya mengembalikan data tanpa modifikasi.

# 4. **Fungsi `proxy_handler(client_socket, remote_host, remote_port, receive_first)`**: Fungsi ini menangani koneksi dari klien lokal. Itu membuat koneksi ke server jarak jauh, menerima data dari klien lokal, mengirimkannya ke server jarak jauh, menerima respons dari server jarak jauh, dan mengirimkannya kembali ke klien lokal. Saat melakukan operasi ini, fungsi ini juga memanggil fungsi `request_handler` dan `response_handler` untuk memodifikasi data sesuai kebutuhan.

# 5. **Fungsi `server_loop(local_host, local_port, remote_host, remote_port, receive_first)`**: Fungsi ini membuat server *socket* lokal dan memulai proses *listening*. Ketika koneksi diterima, itu memulai *thread* baru yang menjalankan `proxy_handler` untuk menangani koneksi tersebut.

# 6. **Fungsi `main()`**: Fungsi utama program ini. Ini memeriksa argumen baris perintah, memformatnya, dan memulai *proxy server*.

# Dengan cara ini, program memungkinkan untuk memantau dan memodifikasi lalu lintas data antara klien lokal dan server jarak jauh. Program ini dapat digunakan untuk berbagai tujuan seperti *packet sniffing*, *packet modification*, atau *traffic interception*.
