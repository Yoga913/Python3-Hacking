import portscanner

targets_ip = input('[+] * Masukkan Target Untuk Memindai Port Terbuka yang Rentan: ')
port_number = int(input('[+] * Enter Amount Of Ports You Want To Scan(500 - first 500 ports): '))
vul_file = input('[+] * Masukkan Jalur Ke File Dengan Perangkat Lunak Rentan: ')
print('\n')

target = portscanner.PortScan(targets_ip, port_number)
target.scan()

with open(vul_file, 'r') as file:
    count = 0
    for banner in target.banners:
        file.seek(0)
        for line in file.readlines():
            if line.strip() in banner:
                print('[!!] BANNER RENTAN: "' + banner + '" ON PORT: ' + str(target.open_ports[count]))
        count += 1

# =======================================================================================================================

# Kode ini tampaknya menggunakan modul portscanner yang disertakan untuk melakukan pemindaian port pada target IP yang ditentukan, kemudian membandingkan hasil pemindaian dengan daftar perangkat lunak yang rentan yang disimpan dalam file.

# Namun, kode yang disertakan tidak menyertakan definisi atau implementasi dari modul portscanner. Saya akan memberikan contoh implementasi yang sederhana menggunakan modul socket untuk melakukan pemindaian port


# implementasi sederhana : 
# import socket

# class PortScan:
#     def __init__(self, target_ip, port_count):
#         self.target_ip = target_ip
#         self.port_count = port_count
#         self.open_ports = []
#         self.banners = []

#     def scan(self):
#         for port in range(1, self.port_count + 1):
#             try:
#                 sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#                 sock.settimeout(0.5)  # Set timeout to 0.5 seconds
#                 result = sock.connect_ex((self.target_ip, port))
#                 if result == 0:
#                     self.open_ports.append(port)
#                     banner = self.get_banner(sock)
#                     self.banners.append(banner.decode())
#                 sock.close()
#             except KeyboardInterrupt:
#                 print("\n[!!] Exiting...")
#                 sys.exit(1)
#             except socket.gaierror:
#                 print("Hostname could not be resolved.")
#                 sys.exit(1)
#             except socket.error:
#                 print("Couldn't connect to server.")
#                 sys.exit(1)

#     def get_banner(self, sock):
#         return sock.recv(1024)

# Masukkan kode di sini

# Anda dapat menempatkan kode tersebut di file yang bernama portscanner.py. Kemudian, Anda dapat menggunakan kode yang Anda sebutkan untuk melakukan pemindaian port. Pastikan Anda telah menyertakan implementasi portscanner.py yang tepat di direktori yang sama dengan file yang berisi kode yang Anda tunjukkan.
