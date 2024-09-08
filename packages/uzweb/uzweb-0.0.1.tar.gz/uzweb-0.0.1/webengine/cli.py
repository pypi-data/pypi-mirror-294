import argparse
import os
import subprocess

def add_https(script_name):
    # HTTPS uchun kerakli sertifikatlarni yaratish yoki sozlash
    # Bu qism sizning ehtiyojlaringizga qarab o'zgartirilishi mumkin
    cert_file = 'cert.pem'
    key_file = 'key.pem'

    if not os.path.exists(cert_file) or not os.path.exists(key_file):
        print("Sertifikat yoki maxfiy kalit mavjud emas. Yangi sertifikat yaratish...")
        # Sertifikat yaratish (bu qismini o'zingiz sozlashingiz kerak bo'lishi mumkin)
        subprocess.run(['openssl', 'req', '-new', '-newkey', 'rsa:2048', '-days', '365', '-nodes', '-x509', '-keyout', key_file, '-out', cert_file])

    # HTTPS orqali ishlashni boshlash
    print(f"HTTPS uchun {script_name} ni ishga tushirish...")
    # Misol uchun, Flask yoki boshqa server uchun HTTPS sozlamalarini qo‘shing
    subprocess.run(['python', script_name])  # HTTPS sozlamalari bilan serverni ishga tushuradi

def main():
    parser = argparse.ArgumentParser(description='UzWeb kutubxonasining terminal buyruqlari')
    parser.add_argument('command', type=str, help='Buyruq: add_https')
    parser.add_argument('script', type=str, help='Python skriptining nomi')
    args = parser.parse_args()

    if args.command == 'add_https':
        add_https(args.script)
    else:
        print(f"Buyruq {args.command} tanilmagan.")

if __name__ == "__main__":
    main()
