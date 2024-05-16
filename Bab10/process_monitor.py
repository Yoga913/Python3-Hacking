import win32con
import win32api
import win32security
import wmi
import os

LOG_FILE = "process_monitor_log.csv"


def get_process_privileges(pid):
    try:
        # obtain a handle to the target process
        hproc = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION,
                                     False,
                                     pid)

        # open the main process token
        htok = win32security.OpenProcessToken(hproc, win32con.TOKEN_QUERY)

        # retrieve the list of privileges enabled
        privs = win32security.GetTokenInformation(
            htok,
            win32security.TokenPrivileges)

        # iterate over privileges and output the ones that are enabled
        priv_list = []
        for priv_id, priv_flags in privs:
            # check if the privilege is enabled
            if priv_flags == 3:
                priv_list.append(
                    win32security.LookupPrivilegeName(None, priv_id))

    except:
        priv_list.append("N/A")

    return "|".join(priv_list)


def log_to_file(message):
    fd = open(LOG_FILE, "ab")
    fd.write("%s\r\n" % message)
    fd.close()
    return


# create a log file header
if not os.path.isfile(LOG_FILE):
    log_to_file("Time,User,Executable,CommandLine,PID,ParentPID,Privileges")

# instantiate the WMI interface
c = wmi.WMI()

# create our process monitor
process_watcher = c.Win32_Process.watch_for("creation")

while True:
    try:
        new_process = process_watcher()
        proc_owner = new_process.GetOwner()
        proc_owner = "%s\\%s" % (proc_owner[0], proc_owner[2])
        create_date = new_process.CreationDate
        executable = new_process.ExecutablePath
        cmdline = new_process.CommandLine
        pid = new_process.ProcessId
        parent_pid = new_process.ParentProcessId

        privileges = get_process_privileges(pid)

        process_log_message = "%s,%s,%s,%s,%s,%s,%s" % (
            create_date, proc_owner, executable, cmdline, pid, parent_pid,
            privileges)

        print("%s\r\n" % process_log_message)

        log_to_file(process_log_message)
    except:
        pass


# ===================================================================== #
    
# Program ini merupakan sebuah monitor proses sederhana yang berjalan di lingkungan Windows. Berikut adalah penjelasan alur kerjanya:

# 1. **Impor Modul:**
#    - Program mengimpor beberapa modul yang diperlukan seperti `win32con`, `win32api`, `win32security`, `wmi`, dan `os` untuk melakukan operasi-operasi terkait sistem dan proses.

# 2. **Variabel `LOG_FILE`:**
#    - Variabel ini menentukan nama file log yang akan digunakan untuk mencatat aktivitas monitor proses.

# 3. **Fungsi `get_process_privileges(pid)`:**
#    - Fungsi ini berfungsi untuk mendapatkan hak istimewa (privileges) dari sebuah proses berdasarkan ID proses (PID).
#    - Program membuka proses target menggunakan `win32api.OpenProcess` dan mendapatkan token proses menggunakan `win32security.OpenProcessToken`.
#    - Kemudian, program mendapatkan informasi hak istimewa dengan `win32security.GetTokenInformation` dan mengambil nama hak istimewa yang diaktifkan.
#    - Nama hak istimewa tersebut digabungkan menjadi sebuah string yang dipisahkan oleh "|" dan dikembalikan.

# 4. **Fungsi `log_to_file(message)`:**
#    - Fungsi ini digunakan untuk mencatat pesan ke dalam file log.
#    - Program membuka file log menggunakan `open` dengan mode append binary ("ab"), menulis pesan ke dalamnya, dan menutup file setelah selesai.

# 5. **Inisialisasi Log File:**
#    - Program memeriksa apakah file log sudah ada. Jika tidak, maka program akan membuat file log baru dan menambahkan header ke dalamnya.

# 6. **Instansiasi WMI Interface:**
#    - Program membuat instance WMI (Windows Management Instrumentation) untuk berinteraksi dengan sistem Windows menggunakan `wmi.WMI()`.

# 7. **Membuat Process Watcher:**
#    - Program membuat watcher untuk memonitor pembuatan (creation) proses baru menggunakan `c.Win32_Process.watch_for("creation")`.

# 8. **Pemantauan Proses:**
#    - Program memulai loop tak terbatas (while True) untuk terus memantau proses baru yang tercipta.
#    - Setiap kali proses baru tercipta, watcher akan memberikan notifikasi kepada program, dan program akan mendapatkan informasi terkait proses tersebut menggunakan properti-properti dari objek proses yang diberikan.
#    - Informasi-informasi seperti waktu pembuatan, pemilik proses, path eksekusi, baris perintah (command line), ID proses, ID proses induk, dan hak istimewa proses akan dicatat.
#    - Informasi proses ini kemudian dicetak ke konsol dan juga disimpan ke dalam file log menggunakan fungsi `log_to_file`.
  
# 9. **Penanganan Kesalahan:**
#    - Program menangani kemungkinan terjadinya kesalahan dengan menggunakan blok `try-except`, di mana program akan tetap berjalan meskipun ada kesalahan yang terjadi.
  
# Alur kerja program ini memungkinkan pengguna untuk memantau pembuatan proses baru di sistem Windows dan mencatat informasi terkait proses tersebut ke dalam file log untuk tujuan audit atau analisis lebih lanjut.

# ======================================================================================================================================================================================================================= # 
    
# ### Fungsi:

# 1. **Memantau Proses:**
#    - Program ini berfungsi untuk memantau proses-proses yang baru dibuat di sistem operasi Windows.

# 2. **Mendapatkan Hak Istimewa Proses:**
#    - Program dapat mengambil informasi hak istimewa (privileges) dari proses-proses yang sedang berjalan, sehingga dapat membantu dalam pemantauan keamanan sistem.

# 3. **Mencatat Aktivitas ke dalam Log:**
#    - Setiap kali proses baru dibuat, program akan mencatat informasi terkait proses tersebut ke dalam file log, termasuk waktu pembuatan, pemilik proses, path eksekusi, baris perintah, ID proses, ID proses induk, dan hak istimewa proses.

### Manfaat:

# 1. **Deteksi Aktivitas Mencurigakan:**
#    - Program ini dapat membantu pengguna dalam mendeteksi aktivitas mencurigakan atau tidak biasa di sistem mereka, seperti pembuatan proses oleh aplikasi berbahaya atau malware.

# 2. **Pemantauan Keamanan:**
#    - Dengan memantau proses-proses yang aktif dan hak istimewa yang dimiliki oleh proses-proses tersebut, program ini dapat membantu pengguna dalam memonitor dan memastikan keamanan sistem mereka.

# 3. **Audit dan Analisis:**
#    - Informasi yang dicatat oleh program ini dapat digunakan untuk tujuan audit dan analisis lebih lanjut, seperti melacak aktivitas proses selama rentang waktu tertentu atau memeriksa hak istimewa yang dimiliki oleh proses tertentu.

### Cara Penggunaan:

# 1. **Menjalankan Program:**
#    - Pengguna dapat menjalankan program ini di lingkungan sistem operasi Windows dengan menjalankan skrip Python yang telah disediakan.
   
# 2. **Memantau Aktivitas Proses:**
#    - Setelah program dijalankan, ia akan mulai memantau aktivitas pembuatan proses baru di sistem.

# 3. **Melihat Log Aktivitas:**
#    - Pengguna dapat melihat log aktivitas yang dicatat oleh program dengan membuka file log yang telah ditentukan sebelumnya (`LOG_FILE`).
   
# 4. **Mengambil Tindakan Sesuai:**
#    - Jika terdapat aktivitas mencurigakan atau tidak diinginkan yang tercatat dalam log, pengguna dapat mengambil tindakan yang sesuai, seperti memeriksa lebih lanjut atau mengambil langkah-langkah untuk menangani masalah tersebut.

### Pengembangan:

# 1. **Penambahan Fitur:**
#    - Program ini dapat dikembangkan dengan menambahkan fitur-fitur tambahan, seperti kemampuan untuk memonitor proses-proses tertentu berdasarkan kriteria tertentu atau menangani peristiwa-peristiwa lain yang terkait dengan keamanan sistem.

# 2. **Peningkatan Kinerja:**
#    - Perlu dipertimbangkan untuk meningkatkan kinerja program, terutama jika program harus memantau banyak proses dalam waktu yang singkat.

# 3. **Keamanan:**
#    - Dalam pengembangan selanjutnya, perlu diperhatikan aspek keamanan untuk memastikan bahwa program ini tidak digunakan untuk tujuan yang merugikan atau memungkinkan adanya eksploitasi keamanan.

# 4. **Dokumentasi dan Pelatihan:**
#    - Penting untuk menyertakan dokumentasi yang baik dan memberikan pelatihan kepada pengguna tentang cara menggunakan program ini dengan benar dan efektif.

# Dengan memperhatikan aspek-aspek tersebut, program ini dapat dikembangkan lebih lanjut untuk meningkatkan fungsionalitasnya, keamanannya, dan membantu pengguna dalam memantau dan mengelola keamanan sistem mereka.
