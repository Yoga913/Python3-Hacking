from burp import IBurpExtender
from burp import IIntruderPayloadGeneratorFactory
from burp import IIntruderPayloadGenerator
from java.util import List, ArrayList
import random


class BurpExtender(IBurpExtender, IIntruderPayloadGeneratorFactory):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        callbacks.registerIntruderPayloadGeneratorFactory(self)
        return

    @staticmethod
    def getGeneratorName():
        return "BHP Payload Generator"

    def createNewInstance(self, attack):
        return BHPFuzzer(self, attack)


class BHPFuzzer(IIntruderPayloadGenerator):
    def __init__(self, extender, attack):
        self._extender = extender
        self._helpers = extender._helpers
        self._attack = attack
        print("BHP Fuzzer initialized")
        self.max_payloads = 1000
        self.num_payloads = 0

        return

    def hasMorePayloads(self):
        print("hasMorePayloads called.")
        if self.num_payloads == self.max_payloads:
            print("No more payloads.")
            return False
        else:
            print("More payloads. Continuing.")
            return True

    def getNextPayload(self, current_payload):

        # convert into a string
        payload = "".join(chr(x) for x in current_payload)

        # call our simple mutator to fuzz the POST
        payload = self.mutate_payload(payload)

        # increase the number of fuzzing attempts
        self.num_payloads += 1
        return payload

    def reset(self):
        self.num_payloads = 0
        return

    @staticmethod
    def mutate_payload(original_payload):
        # pick a simple mutator or even call an external script
        # like Radamsa does
        picker = random.randint(1, 3)

        # select a random offset in the payload to mutate
        offset = random.randint(0, len(original_payload) - 1)
        payload = original_payload[:offset]

        # random offset insert a SQL injection attempt
        if picker == 1:
            payload += "'"

            # jam an XSS attempt in
        if picker == 2:
            payload += "<script>alert('BHP!');</script>"

            # repeat a chunk of the original payload a random number
        if picker == 3:
            chunk_length = random.randint(len(payload[offset:]),
                                          len(payload) - 1)
            repeater = random.randint(1, 10)
            for i in range(repeater):
                payload += original_payload[offset:offset + chunk_length]

        # add the remaining bits of the payload
        payload += original_payload[offset:]
        return payload


# ====================================================================================== # 
    
# Program tersebut adalah sebuah ekstensi untuk Burp Suite yang digunakan untuk melakukan fuzzing pada serangan Intruder. Berikut adalah penjelasan alur programnya:

# Import Library: Program mengimpor beberapa kelas dari pustaka Burp dan Java yang diperlukan.

# BurpExtender Class: Kelas ini mengimplementasikan IBurpExtender dan IIntruderPayloadGeneratorFactory. Ini adalah kelas utama yang akan dicatat oleh Burp Suite sebagai ekstensi.

# registerExtenderCallbacks: Metode ini dipanggil oleh Burp saat ekstensi dimuat. Di dalamnya, ekstensi mendaftarkan dirinya sebagai generator payload Intruder.
# getGeneratorName: Metode statis yang mengembalikan nama generator payload Intruder.
# BHPFuzzer Class: Kelas ini mengimplementasikan IIntruderPayloadGenerator dan bertanggung jawab untuk membuat payload yang akan digunakan oleh Intruder.

# __init__: Metode inisialisasi untuk mengatur variabel dan memberi tahu bahwa objek BHPFuzzer telah diinisialisasi.
# hasMorePayloads: Metode ini memeriksa apakah masih ada payload yang akan digunakan. Jika jumlah payload yang telah dibuat sama dengan jumlah maksimum payload yang diizinkan, maka tidak akan ada payload lagi.
# getNextPayload: Metode ini mengembalikan payload berikutnya yang akan digunakan oleh Intruder. Ini memanggil mutate_payload untuk menghasilkan variasi payload.
# reset: Metode ini digunakan untuk mereset hitungan payload.
# mutate_payload: Metode ini mengubah payload asli menjadi variasi payload dengan menggunakan beberapa strategi fuzzing yang berbeda. Ini termasuk memasukkan karakter khusus seperti tanda kutip untuk mencoba SQL injection, menyisipkan skrip XSS, dan mengulangi sebagian dari payload asli.
# Program ini memungkinkan pengguna untuk melakukan fuzzing pada serangan Intruder dengan menghasilkan berbagai variasi payload yang dapat digunakan untuk menguji keamanan aplikasi web.

# =================================================================================================================================================================================================================================================================================== # 
    
# Fungsi:
# Manfaat: Program ini adalah sebuah ekstensi untuk platform Burp Suite, yang merupakan alat penting dalam pengujian penetrasi aplikasi web. Fungsi utamanya adalah untuk memfasilitasi proses fuzzing pada serangan Intruder. Dengan menggunakan program ini, pengguna dapat secara otomatis menghasilkan berbagai variasi payload yang dapat digunakan untuk menguji keamanan aplikasi web terhadap berbagai jenis serangan seperti SQL injection, XSS, dan lainnya.

# Penggunaan:
# Instalasi Ekstensi: Pertama, pengguna perlu menginstal ekstensi ini ke dalam Burp Suite. Ini dapat dilakukan dengan mengimpor ekstensi ke dalam Burp Suite dan menjalankan aplikasi.

# Konfigurasi Payload Generator: Setelah ekstensi terinstal, pengguna dapat menemukan opsi "BHP Payload Generator" dalam Intruder tab pada Burp Suite. Di sana, pengguna dapat memilih opsi ini sebagai generator payload untuk serangan Intruder.

# Menjalankan Fuzzing: Setelah mengatur generator payload, pengguna dapat menjalankan serangan Intruder seperti biasa. Burp Suite akan menggunakan payload yang dihasilkan oleh ekstensi ini untuk menguji aplikasi web target terhadap serangan yang dipilih.

# Pengembangan:
# Penambahan Fungsionalitas: Pengembangan program ini dapat melibatkan penambahan fungsionalitas baru ke dalam generator payload. Ini bisa termasuk penambahan strategi fuzzing baru atau peningkatan kemampuan untuk menghasilkan payload yang lebih kompleks.

# Optimisasi Kinerja: Pengembangan juga dapat fokus pada optimisasi kinerja ekstensi, seperti mengurangi beban komputasi atau mempercepat proses penghasilan payload.

# Peningkatan Keamanan: Pengembangan ini juga bisa berfokus pada peningkatan keamanan ekstensi, seperti menerapkan filter untuk mencegah penghasilan payload yang dapat menyebabkan kerusakan atau melanggar aturan pengetesan yang ditetapkan.

# Komersialisasi atau Open Source: Program ini dapat dikembangkan lebih lanjut untuk digunakan secara komersial, dengan menambahkan fitur tambahan dan dukungan pelanggan, atau dipelihara sebagai proyek sumber terbuka untuk menerima kontribusi dari komunitas.

# Integrasi dengan Alat Lain: Pengembangan bisa juga berfokus pada integrasi ekstensi dengan alat lain dalam ekosistem keamanan, seperti otomatisasi proses pengujian penetrasi atau integrasi dengan platform manajemen keamanan lainnya.

# Dengan mengembangkan dan menggunakan program ini dengan cara yang efektif, pengguna dapat meningkatkan kemampuan mereka untuk mengidentifikasi dan mengatasi kerentanan dalam aplikasi web yang mereka uji.

# ================================================================================================================================================================================================================================================================= # 






