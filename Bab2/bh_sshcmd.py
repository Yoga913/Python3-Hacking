import paramiko # imput modul paramiko : Program ini menggunakan modul Paramiko, yang menyediakan fungsionalitas SSH dalam Python. 


def ssh_command(ip, user, passwd, command):   # fungsi'ssh_command: Fungsi ini menerima empat parameter: ip (alamat IP host yang akan dihubungi), user (nama pengguna SSH), passwd (kata sandi SSH), dan command (perintah yang akan dijalankan di host).
    client = paramiko.SSHClient()
    # client can also support using key files
    # client.load_host_keys('/home/user/.ssh/known_hosts')
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username=user, password=passwd)
    # inisialisasi ssh clien: Membuat objek klien SSH, mengatur kebijakan penanganan kunci host yang hilang, dan melakukan koneksi ke host dengan alamat IP, nama pengguna, dan kata sandi yang diberikan.
    ssh_session = client.get_transport().open_session() # membuka sesi ssh : Membuka sesi SSH setelah koneksi berhasil. Sesuai dengan kode, tidak ada penanganan error yang mencakup skenario jika sesi tidak dapat dibuka.
    if ssh_session.active:
        ssh_session.exec_command(command)
        print(ssh_session.recv(1024))  # menjalankan perintah : Jika sesi SSH aktif, fungsi exec_command digunakan untuk menjalankan perintah yang diberikan. Hasil dari perintah tersebut kemudian dicetak. Perhatikan bahwa output dari perintah hanya dicetak dalam bentuk string yang diterima sebanyak 1024 byte.
    return


ssh_command(' #ip# ', 'justin', 'lovesthepython', 'ClientConnected')
# penggunaan fungsi 'ssh_command' : Memanggil fungsi ssh_command dengan parameter yang sesuai: alamat IP kosong (seharusnya diisi dengan alamat IP tujuan), nama pengguna 'justin', kata sandi 'lovesthepython', dan perintah 'ClientConnected' yang akan dijalankan di host.
#             |
# ssh_command|   isi dengan api 

# -----------------------------------------------------------------------------------------------------------------------# 

# Program Python di atas menggunakan modul Paramiko untuk melakukan koneksi SSH ke suatu host dan menjalankan perintah.
# Manfaat:
# Program ini berguna untuk menjalankan perintah melalui koneksi SSH ke host tertentu. Contoh penggunaan umumnya adalah untuk otomatisasi atau remote administration pada sistem yang mendukung protokol SSH.

# Catatan:
# Program ini memiliki beberapa kelemahan yang dapat diperbaiki atau ditingkatkan untuk membuatnya lebih kuat dan aman. Berikut adalah beberapa kelemahan yang dapat diidentifikasi:

# Tidak Ada Penanganan Error yang Memadai:
# Program ini tidak memiliki penanganan error yang memadai. Jika ada kesalahan dalam proses koneksi atau eksekusi perintah, program tidak memberikan informasi yang berguna kepada pengguna.

# Penggunaan Kata Sandi Sebagai Parameter:
# Penggunaan kata sandi sebagai parameter dalam fungsi dapat menimbulkan risiko keamanan. Sebaiknya, disarankan untuk menggunakan kunci SSH alih-alih kata sandi untuk meningkatkan keamanan.

# Alamat IP Kosong:
# Pada pemanggilan fungsi terakhir, parameter ip diisi dengan string kosong (''). Ini menyebabkan program mencoba terhubung ke alamat IP yang tidak valid atau tidak ditentukan. Seharusnya, program ini memerlukan alamat IP yang valid sebagai parameter.

# Pemanggilan Fungsi Terbatas:
# Program hanya melakukan pemanggilan fungsi untuk menjalankan satu perintah tertentu. Untuk meningkatkan fleksibilitas, sebaiknya diimplementasikan dengan cara yang memungkinkan pengguna untuk menjalankan berbagai perintah atau serangkaian perintah.

# Ketidakamanan Perintah Eksekusi:
# Program saat ini hanya mencetak output dari perintah yang dijalankan tanpa memeriksa atau memvalidasi hasilnya. Ini dapat menjadi risiko keamanan jika perintah yang dijalankan tidak dapat dipercaya. Pengecekan dan validasi hasil perintah adalah praktik yang baik.

# Ketidakamanan Koneksi:

# Koneksi SSH dilakukan tanpa memeriksa atau menggunakan kunci host yang diketahui sebelumnya. Hal ini dapat meninggalkan sistem rentan terhadap serangan Man-in-the-Middle. Sebaiknya, gunakan kunci host yang diketahui atau terapkan verifikasi identitas host.
# Pemanggilan Fungsi Bersifat Blocking:

# Pemanggilan fungsi exec_command bersifat blocking, yang berarti program akan menunggu hingga perintah selesai sebelum melanjutkan eksekusi selanjutnya. Ini dapat menjadi masalah jika perintah yang dijalankan membutuhkan waktu yang lama.
# Untuk memperbaiki atau meningkatkan program, sebaiknya ditambahkan penanganan error yang baik, penggunaan kunci SSH, validasi input, dan langkah-langkah keamanan tambahan sesuai kebutuhan.
