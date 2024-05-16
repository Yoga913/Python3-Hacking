import sys
import volatility.conf as conf
import volatility.registry as registry
import volatility.commands as commands
import volatility.addrspace as addrspace
from volatility.plugins.registry.registryapi import RegistryApi
from volatility.plugins.registry.lsadump import HashDump

memory_file = "WinXPSP2.vmem"

sys.path.append("/Downloads/volatility-2.3.1")

registry.PluginImporter()
config = conf.ConfObject()

config.parse_options()
config.PROFILE = "WinXPSP2x86"
config.LOCATION = "file://%s" % memory_file

registry.register_global_options(config, commands.Command)
registry.register_global_options(config, addrspace.BaseAddressSpace)

registry = RegistryApi(config)
registry.populate_offsets()

sam_offset = None
sys_offset = None

for offset in registry.all_offsets:

    if registry.all_offsets[offset].endswith("\\SAM"):
        sam_offset = offset
        print("[*] SAM: 0x%08x" % offset)

    if registry.all_offsets[offset].endswith("\\system"):
        sys_offset = offset
        print("[*] System: 0x%08x" % offset)

    if sam_offset is not None and sys_offset is not None:
        config.sys_offset = sys_offset
        config.sam_offset = sam_offset
        hashdump = HashDump(config)

        for hash in hashdump.calculate():
            print(hash)
        break

if sam_offset is None or sys_offset is None:
    print("[*] Failed to find the system or SAM offsets.")


# ============================================================================== # 
    
# Program ini bertujuan untuk mengekstrak dan menampilkan hash dari database SAM (Security Account Manager) dan file sistem pada sebuah memori snapshot dari sistem Windows XP SP2. Berikut adalah penjelasan alur programnya:

# 1. **Impor Modul dan Pengaturan Awal:**
#    - Program mengimpor modul-modul yang diperlukan seperti `sys`, `volatility.conf`, `volatility.registry`, dan lain-lain.
#    - Variabel `memory_file` menunjukkan lokasi file memori yang akan dianalisis.

# 2. **Konfigurasi Volatility:**
#    - Pengaturan konfigurasi untuk memproses file memori menggunakan Volatility ditetapkan, seperti profile sistem (Windows XP SP2) dan lokasi file memori yang akan dianalisis.

# 3. **Membuat Objek RegistryApi:**
#    - Objek `RegistryApi` diciptakan untuk melakukan analisis struktur registri pada memori snapshot.

# 4. **Populasi Offset:**
#    - Metode `populate_offsets()` dari objek `RegistryApi` digunakan untuk mengidentifikasi dan menyimpan offset dari berbagai kunci registri yang ada dalam memori snapshot.

# 5. **Mencari Offset SAM dan System:**
#    - Program mencari offset dari kunci registri SAM (Security Account Manager) dan System.
#    - Setelah ditemukan, offset-offset ini disimpan dalam variabel `sam_offset` dan `sys_offset`.

# 6. **Ekstraksi Hash:**
#    - Jika offset SAM dan System telah ditemukan, program menetapkan offset-offset ini dalam konfigurasi.
#    - Objek `HashDump` dari Volatility digunakan untuk mengekstrak hash dari database SAM.
 #   - Setiap hash yang diekstrak ditampilkan.

# 7. **Penanganan Kesalahan:**
#    - Jika offset SAM atau System tidak ditemukan, program mencetak pesan kesalahan.

### Ringkasan Penggunaan:

# 1. **Persiapan File Memori:**
#    - Pastikan bahwa file memori yang akan dianalisis telah disediakan dan lokasinya telah ditentukan.

# 2. **Menjalankan Program:**
#    - Jalankan skrip Python ini dengan menyediakan lokasi file memori sebagai input.

# 3. **Memantau Output:**
#    - Program akan menampilkan hash yang diekstrak dari database SAM, jika offset SAM dan System berhasil ditemukan.

# 4. **Penanganan Kesalahan:**
#    - Jika offset SAM atau System tidak ditemukan, program akan mencetak pesan kesalahan yang sesuai.

### Pengembangan:

# 1. **Peningkatan Keandalan:**
#    - Program ini dapat ditingkatkan dengan menambahkan penanganan kesalahan yang lebih baik atau teknik untuk mengidentifikasi offset SAM dan System secara lebih andal.

# 2. **Optimisasi Kinerja:**
#    - Dalam pengembangan selanjutnya, perlu dipertimbangkan untuk mengoptimalkan kinerja program, terutama dalam proses pencarian dan ekstraksi hash.

# 3. **Penambahan Fitur:**
#    - Program ini dapat diperluas dengan menambahkan fitur-fitur tambahan, seperti kemampuan untuk mengekstrak informasi lain dari memori snapshot atau memproses snapshot dari sistem operasi lain.

# Dengan memperhatikan aspek-aspek ini, program ini dapat dikembangkan lebih lanjut untuk meningkatkan fungsionalitasnya dan membantu dalam analisis keamanan sistem.

# ===================================================================================================================================================================================== # 

# ### Fungsi:

# 1. **Ekstraksi Hash dari Database SAM:**
#    - Program ini bertujuan untuk mengekstrak hash yang disimpan dalam database SAM (Security Account Manager) dari sebuah memori snapshot sistem Windows XP SP2.
#    - Hash-hashing ini biasanya digunakan untuk otentikasi pengguna pada sistem Windows.

# 2. **Penemuan Offset Registry:**
#    - Program mencari dan menentukan offset dari kunci registri SAM dan System dalam memori snapshot.
#    - Offset-offset ini penting karena mereka menunjukkan lokasi data terkait keamanan penting dalam sistem.

# 3. **Pencetakan Hash:**
#    - Setelah offset SAM dan System ditemukan, program mengekstrak hash dari database SAM dan mencetaknya untuk penggunaan lebih lanjut.

### Manfaat:

# 1. **Analisis Keamanan:**
#    - Program ini dapat digunakan oleh peneliti keamanan atau administrator sistem untuk menganalisis dan memeriksa keamanan sistem Windows XP SP2.
#    - Dengan mengekstrak hash dari database SAM, pengguna dapat memeriksa kekuatan keamanan kata sandi pengguna pada sistem.

# 2. **Forensik Digital:**
#    - Program ini juga berguna dalam bidang forensik digital, di mana peneliti dapat menggunakan hash yang diekstrak sebagai bukti digital untuk penyelidikan atau analisis lebih lanjut.

### Cara Penggunaan:

# 1. **Persiapan Memori Snapshot:**
#    - Pastikan memori snapshot dari sistem Windows XP SP2 telah disediakan dan lokasinya telah ditentukan sebelumnya.

# 2. **Menjalankan Program:**
#    - Jalankan skrip Python ini dengan menyediakan lokasi file memori snapshot sebagai input.

# 3. **Memantau Output:**
#    - Program akan mencetak hash yang diekstrak dari database SAM setelah berhasil menemukan offset SAM dan System.

### Pengembangan:

# 1. **Peningkatan Keselamatan:**
#    - Program ini dapat ditingkatkan dengan menambahkan fitur-fitur keamanan tambahan, seperti validasi input atau pemeriksaan integritas data.

# 2. **Optimisasi Kinerja:**
#    - Dalam pengembangan lebih lanjut, perlu dipertimbangkan untuk mengoptimalkan kinerja program, terutama dalam proses pencarian offset dan ekstraksi hash.

# 3. **Pengembangan Fitur:**
#    - Program ini dapat diperluas dengan menambahkan fitur-fitur tambahan, seperti kemampuan untuk mengekstrak informasi tambahan dari memori snapshot atau memproses snapshot dari sistem operasi lain.

# Dengan memperhatikan aspek-aspek ini, program ini dapat dikembangkan lebih lanjut untuk meningkatkan fungsionalitasnya, keamanannya, dan membantu dalam analisis keamanan sistem.
