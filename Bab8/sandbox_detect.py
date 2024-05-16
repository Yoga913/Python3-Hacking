import ctypes
import random
import time
import sys

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

keystrokes = 0
mouse_clicks = 0
double_clicks = 0


class LASTINPUTINFO(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_ulong)]


def get_last_input():
    struct_lastinputinfo = LASTINPUTINFO()
    struct_lastinputinfo.cbSize = ctypes.sizeof(LASTINPUTINFO)

    # get last input registered
    user32.GetLastInputInfo(ctypes.byref(struct_lastinputinfo))

    # now determine how long the machine has been running
    run_time = kernel32.GetTickCount()
    elapsed = run_time - struct_lastinputinfo.dwTime
    print("[*] It's been %d milliseconds since the last input event." % elapsed)
    return elapsed


def get_key_press():
    global mouse_clicks
    global keystrokes

    for i in range(0, 0xff):
        if user32.GetAsyncKeyState(i) == -32767:
            # 0x1 is the code for a left mouse click
            if i == 1:
                mouse_clicks += 1
                return time.time()
            else:
                keystrokes += 1
    return None


def detect_sandbox():
    global mouse_clicks
    global keystrokes

    max_keystrokes = random.randint(10, 25)
    max_mouse_clicks = random.randint(5, 25)

    double_clicks = 0
    max_double_clicks = 10
    double_click_threshold = 0.250
    first_double_click = None

    average_mousetime = 0
    max_input_threshold = 30000

    previous_timestamp = None
    detection_complete = False

    last_input = get_last_input()

    # if we hit our threshold let's bail out
    if last_input >= max_input_threshold:
        sys.exit(0)

    while not detection_complete:
        keypress_time = get_key_press()
        if keypress_time is not None and previous_timestamp is not None:

            # calculate the time between double clicks
            elapsed = keypress_time - previous_timestamp

            # the user double clicked
            if elapsed <= double_click_threshold:
                double_clicks += 1

                if first_double_click is None:

                    # grab the timestamp of the first double click
                    first_double_click = time.time()

                else:
                    # did they try to emulate a rapid succession of clicks?   
                    if double_clicks == max_double_clicks:
                        if keypress_time - first_double_click <= (
                                max_double_clicks * double_click_threshold):
                            sys.exit(0)

            # we are happy there's enough user input
            if keystrokes >= max_keystrokes \
                    and double_clicks >= max_double_clicks \
                    and mouse_clicks >= max_mouse_clicks:
                return
            previous_timestamp = keypress_time

        elif keypress_time is not None:
            previous_timestamp = keypress_time


detect_sandbox()
print("We are ok!")


# ============================================================================================== # 

# Program di atas adalah sebuah skrip Python yang bertujuan untuk mendeteksi apakah program sedang berjalan dalam lingkungan 'sandbox' atau bukan. 'Sandbox' adalah lingkungan yang terisolasi di mana program dijalankan untuk tujuan pengujian atau analisis keamanan.

# Berikut adalah penjelasan alur program:

# Import library yang diperlukan: ctypes untuk berinteraksi dengan API Windows, random untuk menghasilkan nilai acak, time untuk bekerja dengan waktu, dan sys untuk keluar dari program.

# Pendefinisian struktur LASTINPUTINFO menggunakan ctypes, yang akan digunakan untuk mendapatkan informasi tentang waktu dari input terakhir.

# Fungsi get_last_input(): Mendapatkan waktu sejak input terakhir dari pengguna dengan menggunakan fungsi Windows API GetLastInputInfo(). Kemudian, dihitung waktu yang sudah berlalu sejak input terakhir dan hasilnya dikembalikan.

# Fungsi get_key_press(): Memeriksa apakah ada penekanan tombol yang baru saja terjadi menggunakan GetAsyncKeyState() dari Windows API. Jika ada, jumlah klik mouse atau keystrokes ditingkatkan sesuai, dan waktu penekanan dikembalikan.

# Fungsi detect_sandbox(): Ini adalah inti dari program. Pertama, menginisialisasi variabel dan ambang batas maksimum untuk keystrokes, klik mouse, dan klik ganda. Kemudian, dilakukan loop untuk mendeteksi perilaku mencurigakan. Hal ini mencakup:

# Pengecekan waktu input terakhir. Jika waktu input terakhir melebihi ambang batas tertentu, program keluar.
# Loop utama untuk mendeteksi perilaku mencurigakan. Ini melibatkan pengecekan penekanan tombol, hitungan klik ganda, dan waktu antara klik ganda.
# Jika ada cukup input pengguna sesuai dengan ambang batas yang ditetapkan, program selesai.
# Panggilan fungsi detect_sandbox(): Ini memulai proses deteksi lingkungan 'sandbox'.

# Cetak "We are ok!": Jika program melewati semua pengujian dan tidak mendeteksi perilaku mencurigakan, pesan ini dicetak, menunjukkan bahwa program berjalan dalam lingkungan yang aman.

# Singkatnya, program ini mencoba untuk mendeteksi jika sedang berjalan dalam lingkungan 'sandbox' dengan melihat perilaku pengguna seperti penekanan tombol, klik mouse, dan lain-lain. Jika tidak ditemukan perilaku yang mencurigakan, maka program menganggap bahwa tidak sedang berjalan dalam 'sandbox'.

# ========================================================================================================================================================================================================================================================================================================================= # 

# Manfaat:
# Deteksi Lingkungan Sandbox: Program ini berguna untuk mendeteksi apakah program berjalan dalam lingkungan sandbox atau tidak. Hal ini penting dalam konteks keamanan karena sandbox sering digunakan untuk analisis malware atau pengujian aplikasi, sehingga deteksi dapat membantu dalam mencegah tindakan berbahaya.

# Perlindungan Aplikasi: Dengan mendeteksi lingkungan sandbox, aplikasi dapat mengambil tindakan lebih lanjut untuk melindungi diri dari analisis yang tidak diinginkan atau peretasan yang berpotensi merugikan.

# Pengujian Keamanan: Pengembang dan peneliti keamanan dapat menggunakan teknik ini untuk memeriksa apakah program mereka rentan terhadap analisis di lingkungan sandbox.

# Cara Penggunaan:

# Integrasi dengan Aplikasi:

# Program ini dapat diintegrasikan ke dalam aplikasi yang ingin memeriksa apakah sedang berjalan dalam lingkungan sandbox atau tidak.
# Pengguna dapat memanggil fungsi detect_sandbox() saat aplikasi dimulai atau pada titik tertentu dalam alur eksekusi untuk memeriksa lingkungan.

# Pemantauan Deteksi:

# Setelah fungsi detect_sandbox() dipanggil, hasilnya bisa digunakan untuk mengambil tindakan tertentu, seperti menampilkan pesan, melindungi fitur tertentu, atau keluar dari aplikasi jika deteksi sandbox terdeteksi.

# Pengembangan:

# Penyesuaian Ambang Batas:

# Pengembang dapat menyesuaikan ambang batas untuk keystrokes, klik mouse, atau klik ganda sesuai dengan kebutuhan aplikasi atau toleransi terhadap deteksi palsu.

# Integrasi dengan Teknik Lain:

# Teknik deteksi ini dapat diintegrasikan dengan teknik deteksi lainnya untuk meningkatkan akurasi dan keandalan deteksi lingkungan sandbox.

# Optimisasi Kinerja:

# Program dapat dioptimalkan untuk meningkatkan kinerja, misalnya dengan mengurangi beban CPU atau memori, sehingga tidak memengaruhi kinerja aplikasi secara keseluruhan.

# Peningkatan Keandalan:

# Pengembang dapat melakukan peningkatan untuk meningkatkan keandalan deteksi, seperti mengatasi kasus uji coba atau manipulasi yang mungkin dilakukan oleh pengguna jahat.

# Dokumentasi dan Pengujian:

# Penting untuk mendokumentasikan dengan baik kode dan cara penggunaan agar mudah dipahami oleh pengguna lain.
# Melakukan pengujian menyeluruh untuk memastikan bahwa deteksi berfungsi sebagaimana mestinya dalam berbagai situasi.

# Kerjasama Komunitas:

# Membuka kemungkinan kerjasama dengan komunitas keamanan untuk meningkatkan teknik deteksi dan berbagi informasi tentang ancaman keamanan yang terdeteksi.
# Dengan memperhatikan manfaat, cara penggunaan, dan pengembangan yang disebutkan di atas, program ini dapat digunakan secara efektif untuk mendeteksi lingkungan sandbox dan memberikan perlindungan tambahan bagi aplikasi yang relevan.
