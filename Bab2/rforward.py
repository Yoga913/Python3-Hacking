#!/usr/bin/env python
#!/usr/bin/env python

"""
Skrip contoh yang menunjukkan cara melakukan forwarding port remote melalui paramiko.

Skrip ini terhubung ke server SSH yang diminta dan menyiapkan forwarding port remote
(opsi openssh -R) dari port remote melalui koneksi terowongan ke tujuan yang dapat dicapai dari mesin lokal.
"""

import getpass
import socket
import select
import sys
import threading
from optparse import OptionParser

import paramiko

SSH_PORT = 22
DEFAULT_PORT = 4000

g_verbose = True


def handler(chan, host, port):
    sock = socket.socket()
    try:
        sock.connect((host, port))
    except Exception as e:
        verbose("Permintaan penerusan ke %s:%d gagal: %r" % (host, port, e))
        return

    verbose(
        "Terhubung!  Terowongan terbuka %r -> %r -> %r"
        % (chan.origin_addr, chan.getpeername(), (host, port))
    )
    while True:
        r, w, x = select.select([sock, chan], [], [])
        if sock in r:
            data = sock.recv(1024)
            if len(data) == 0:
                break
            chan.send(data)
        if chan in r:
            data = chan.recv(1024)
            if len(data) == 0:
                break
            sock.send(data)
    chan.close()
    sock.close()
    verbose("Terowongan di tutup dari %r" % (chan.origin_addr,))


def reverse_forward_tunnel(server_port, remote_host, remote_port, transport):
    transport.request_port_forward("", server_port)
    while True:
        chan = transport.accept(1000)
        if chan is None:
            continue
        thr = threading.Thread(
            target=handler, args=(chan, remote_host, remote_port)
        )
        thr.setDaemon(True)
        thr.start()


def verbose(s):
    if g_verbose:
        print(s)


HELP = """\
Siapkan terowongan penerusan terbalik di server SSH, menggunakan paramiko. Sebuah
port pada server SSH (diberikan dengan -p) diteruskan melintasi sesi SSH
Kembali ke mesin lokal, dan keluar ke situs terpencil yang dapat dijangkau dari ini
jaringan. Ini mirip dengan opsi openssh -R.
"""


def get_host_port(spec, default_port):
    """Parsing 'HostName:22' menjadi host dan port, dengan port opsional"""
    args = (spec.split(":", 1) + [default_port])[:2]
    args[1] = int(args[1])
    return args[0], args[1]


def parse_options():
    global g_verbose

    parser = OptionParser(
        usage="Penggunaan: %prog [options] <ssh-server>[:<server-port>]",
        version="%prog 1.0",
        description=HELP,
    )
    parser.add_option(
        "-q",
        "--quiet",
        action="store_false",
        dest="verbose",
        default=True,
        help="memadamkan semua output informasi",
    )
    parser.add_option(
        "-p",
        "--remote-port",
        action="store",
        type="int",
        dest="port",
        default=DEFAULT_PORT,
        help="port di server untuk meneruskan (default: %d)" % DEFAULT_PORT,
    )
    parser.add_option(
        "-u",
        "--user",
        action="store",
        type="string",
        dest="user",
        default=getpass.getuser(),
        help="nama pengguna untuk otentikasi SSH (default: %s)"
        % getpass.getuser(),
    )
    parser.add_option(
        "-K",
        "--key",
        action="store",
        type="string",
        dest="keyfile",
        default=None,
        help="file kunci privat yang digunakan untuk autentikasi SSH",
    )
    parser.add_option(
        "",
        "--no-key",
        action="store_false",
        dest="look_for_keys",
        default=True,
        help="Jangan mencari atau menggunakan file kunci privat",
    )
    parser.add_option(
        "-P",
        "--password",
        action="store_true",
        dest="readpass",
        default=False,
        help="Baca kata sandi (untuk autentikasi kunci atau kata sandi) dari stdin",
    )
    parser.add_option(
        "-r",
        "--remote",
        action="store",
        type="string",
        dest="remote",
        default=None,
        metavar="host:port",
        help="host dan port jarak jauh untuk diteruskan ke",
    )
    options, args = parser.parse_args()

    if len(args) != 1:
        parser.error("Jumlah argumen salah.")
    if options.remote is None:
        parser.error("Alamat jarak jauh diperlukan (-r).")

    g_verbose = options.verbose
    server_host, server_port = get_host_port(args[0], SSH_PORT)
    remote_host, remote_port = get_host_port(options.remote, SSH_PORT)
    return options, (server_host, server_port), (remote_host, remote_port)


def main():
    options, server, remote = parse_options()

    password = None
    if options.readpass:
        password = getpass.getpass("masukkan kata sandi SSH: ")

    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.WarningPolicy())

    verbose("Menghubungkan ke host ssh %s:%d ..." % (server[0], server[1]))
    try:
        client.connect(
            server[0],
            server[1],
            username=options.user,
            key_filename=options.keyfile,
            look_for_keys=options.look_for_keys,
            password=password,
        )
    except Exception as e:
        print("*** Gagal terhubung ke %s:%d: %r" % (server[0], server[1], e))
        sys.exit(1)

    verbose(
        "Sekarang meneruskan port jarak jauh %d ke %s:%d ..."
        % (options.port, remote[0], remote[1])
    )

    try:
        reverse_forward_tunnel(
            options.port, remote[0], remote[1], client.get_transport()
        )
    except KeyboardInterrupt:
        print("C-c: Penerus Port di hentikan.")
        sys.exit(0)


if __name__ == "__main__":
    main()

# =================================================================================
# Program ini adalah sebuah *reverse SSH tunnel* yang memungkinkan pengguna untuk meneruskan port di mesin tujuan ke mesin lokal melalui koneksi SSH. Berikut adalah penjelasan singkat tentang bagaimana program ini berfungsi:

# 1. **Fungsi `handler(chan, host, port)`**: Fungsi ini menangani koneksi SSH dari *channel* yang diterima dan membuat koneksi ke host dan port tujuan yang ditentukan. Kemudian, fungsi ini mengalihkan data antara *channel* SSH dan koneksi baru.

# 2. **Fungsi `reverse_forward_tunnel(server_port, remote_host, remote_port, transport)`**: Fungsi ini membuat *reverse SSH tunnel* dengan menerima koneksi SSH dan meneruskan koneksi ke host dan port tujuan yang ditentukan. Ini membuat *thread* baru untuk menangani setiap koneksi yang diterima.

# 3. **Fungsi `verbose(s)`**: Fungsi ini digunakan untuk mencetak pesan jika mode verbose diaktifkan.

# 4. **Fungsi `get_host_port(spec, default_port)`**: Fungsi ini digunakan untuk memisahkan host dan port dari string spesifikasi (seperti `hostname:port`) dan mengembalikannya dalam format yang sesuai.

# 5. **Fungsi `parse_options()`**: Fungsi ini digunakan untuk mengurai argumen baris perintah dan mengembalikan opsi yang diproses.

# 6. **Fungsi `main()`**: Fungsi utama program ini. Ini memanggil fungsi `parse_options()` untuk mendapatkan opsi yang diproses, membuat koneksi SSH ke server tujuan, dan memulai *reverse SSH tunnel*.

# Program ini memungkinkan untuk meneruskan port di mesin tujuan ke mesin lokal melalui koneksi SSH. Ini dapat digunakan untuk mengakses layanan di mesin tujuan yang tidak dapat diakses langsung dari luar jaringan atau untuk mengamankan koneksi antara dua mesin.
