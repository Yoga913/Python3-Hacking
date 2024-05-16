from immlib import *


class CcHook(LogBpHook):

    def __init__(self):
        LogBpHook.__init__(self)
        self.imm = Debugger()

    def run(self, regs):
        self.imm.log("%08x" % regs['EIP'], regs['EIP'])
        self.imm.deleteBreakpoint(regs['EIP'])
        return


def main(args):
    imm = Debugger()

    calc = imm.getModule("calc.exe")
    imm.analyseCode(calc.getCodebase())

    functions = imm.getAllFunctions(calc.getCodebase())

    hooker = CcHook()

    for function in functions:
        hooker.add("%08x" % function, function)

    return "Tracking %d functions." % len(functions)


# =============================================================== #

# Program ini adalah contoh skrip Python yang menggunakan library `immlib` untuk melakukan hooking pada fungsi-fungsi tertentu dalam sebuah proses yang sedang berjalan. Berikut adalah penjelasan alur programnya:

# 1. **Impor Library:**
#    - Program mengimpor modul `immlib` yang digunakan untuk berinteraksi dengan debugger.

# 2. **Definisi Kelas `CcHook`:**
#    - Program mendefinisikan sebuah kelas `CcHook` yang merupakan turunan dari kelas `LogBpHook`.
#    - Konstruktor kelas ini menginisialisasi objek dengan memanggil konstruktor kelas induk `LogBpHook`.
#    - Kelas ini memiliki metode `run` yang akan dieksekusi ketika breakpoint yang diatur oleh hook tersebut terpanggil.
#    - Pada metode `run`, alamat instruksi (EIP) saat breakpoint terpanggil dicatat menggunakan debugger (`self.imm.log`) dan breakpoint tersebut dihapus.

# 3. **Fungsi `main`:**
#    - Program mendefinisikan sebuah fungsi `main` yang akan dieksekusi saat skrip dijalankan.
#    - Dalam fungsi `main`, debugger (`imm`) diinisialisasi.
#    - Selanjutnya, program mencari modul `calc.exe` dalam proses yang sedang berjalan menggunakan `imm.getModule`.
#    - Setelah modul ditemukan, kode modul tersebut dianalisis menggunakan `imm.analyseCode`.
#    - Program kemudian mendapatkan daftar semua fungsi dalam kode modul tersebut dengan `imm.getAllFunctions`.
#    - Objek `hooker` dari kelas `CcHook` dibuat.
#    - Setiap fungsi dalam daftar fungsi diberi hook menggunakan metode `add` dari objek `hooker`.
#    - Fungsi `main` mengembalikan string yang memberitahu jumlah fungsi yang sedang dilacak.

# 4. **Eksekusi:**
#    - Setelah semua persiapan selesai, fungsi `main` dijalankan saat skrip dijalankan.

# Alur program ini digunakan untuk melacak dan mencatat panggilan fungsi dalam sebuah proses, dengan mengatur breakpoint pada setiap fungsi yang ada. Ketika breakpoint terpanggil, program mencatat alamat instruksi saat itu dan kemudian melanjutkan eksekusi tanpa menunggu breakpoint tersebut dipanggil kembali.

# =============================================================================================================================================================================================================================================================================================================================== # 

# ### Fungsi:

# 1. **Hooking Fungsi:**
#    - Program ini berfungsi untuk melakukan hooking pada fungsi-fungsi tertentu dalam sebuah proses yang sedang berjalan.
#    - Hooking dilakukan dengan menetapkan breakpoint pada setiap fungsi yang akan dilacak, sehingga program akan dapat mencatat kapan setiap fungsi dipanggil.

# 2. **Pencatatan Aktivitas:**
#    - Setiap kali breakpoint terpanggil, program mencatat alamat instruksi saat itu, yang mewakili lokasi di mana fungsi dipanggil.
#    - Informasi pencatatan ini dapat digunakan untuk menganalisis alur eksekusi program dan menemukan pola atau perilaku tertentu.

### Manfaat:

# 1. **Analisis Perilaku Program:**
#    - Dengan mencatat panggilan fungsi, program ini memungkinkan pengguna untuk menganalisis perilaku program secara mendalam.
#    - Pengguna dapat melihat urutan fungsi yang dipanggil, frekuensi pemanggilan, dan argumen yang digunakan, yang berguna untuk pemecahan masalah dan pengoptimalan performa.

# 2. **Pemantauan Keamanan:**
#    - Program ini juga dapat digunakan untuk memantau aktivitas yang mencurigakan atau berpotensi berbahaya dalam sebuah proses.
#    - Pengguna dapat mengidentifikasi panggilan fungsi yang tidak biasa atau tidak diharapkan, yang dapat menjadi indikasi adanya serangan atau eksploitasi.

### Cara Penggunaan:

# 1. **Menyediakan Skrip:**
#    - Pengguna perlu memiliki skrip Python yang mengandung implementasi hooking seperti yang diberikan dalam contoh program ini.

# 2. **Menjalankan Skrip:**
#    - Skrip Python dapat dijalankan di lingkungan yang mendukung eksekusi skrip Python, seperti lingkungan pengembangan atau sistem operasi yang sesuai.

# 3. **Menyesuaikan Pengaturan:**
#    - Pengguna dapat menyesuaikan program sesuai dengan kebutuhan mereka, seperti menambahkan atau menghapus fungsi-fungsi yang akan dilacak.

# 4. **Analisis Hasil:**
#    - Setelah program dijalankan, pengguna dapat menganalisis hasil pencatatan aktivitas yang tersimpan, seperti alamat instruksi panggilan fungsi, untuk mengevaluasi perilaku program dan menemukan informasi yang berguna.

### Pengembangan:

# 1. **Penambahan Fitur:**
#    - Program ini dapat dikembangkan dengan menambahkan fitur-fitur tambahan, seperti kemampuan untuk melacak argumen fungsi atau menyimpan informasi tambahan terkait setiap panggilan fungsi.

# 2. **Peningkatan Performa:**
#    - Perlu dipertimbangkan untuk meningkatkan performa program, terutama jika program harus memantau banyak panggilan fungsi dalam waktu yang singkat.

# 3. **Pengoptimalan Keamanan:**
#    - Dalam pengembangan selanjutnya, perlu diperhatikan aspek keamanan untuk memastikan bahwa program ini tidak dapat disalahgunakan atau dieksploitasi oleh pihak yang tidak bertanggung jawab.

# 4. **Dokumentasi dan Pelatihan:**
#    - Penting untuk menyertakan dokumentasi yang baik dan memberikan pelatihan kepada pengguna tentang cara menggunakan program ini dengan benar dan efektif.

# Dengan memperhatikan aspek-aspek tersebut, program ini dapat dikembangkan lebih lanjut untuk meningkatkan fungsionalitasnya, keamanannya, dan membantu pengguna dalam analisis dan pemantauan aktivitas panggilan fungsi dalam program.
