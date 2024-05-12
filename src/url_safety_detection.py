import validators
import requests
import time
import sys
import os
import shutil
from fpdf import FPDF
from pathlib import Path
import colorama
from colorama import Back, Fore, Style

colorama.init()

loading_simulation_time = 0.5
http_request_timeout = 5
max_retries = 3
retry_delay = 2

def apply_style(text, style):
    if style == "GREEN":
        return Fore.GREEN + text + Style.RESET_ALL
    elif style == "RED":
        return Fore.RED + text + Style.RESET_ALL
    elif style == "BRIGHT":
        return Style.BRIGHT + text + Style.RESET_ALL
    else:
        return text

def check_url_safety(url):
    if validators.url(url):
        try:
            print(apply_style("Memeriksa keselamatan URL", "BRIGHT") + apply_style(".", "BRIGHT"), end="")
            for _ in range(5):
                sys.stdout.write(".")
                sys.stdout.flush()
                time.sleep(loading_simulation_time)
            
            response = requests.get(url, timeout=http_request_timeout)
            if response.status_code == 200:
                return True, apply_style("URL aman.", "GREEN")
            else:
                return False, apply_style(f"URL tidak aman. Kode status: {response.status_code}", "RED")
        except requests.exceptions.RequestException as e:
            return False, apply_style(f"Gagal memeriksa URL: {str(e)}", "RED")
    else:
        return False, apply_style("URL tidak valid.", "RED")

def generate_report(url, is_safe, message):
    report = f"Report untuk URL: {url}\n"
    report += f"Status: {'Aman' if is_safe else 'Tidak Aman'}\n"
    report += f"Pesan: {message}\n"
    return report

def save_report_txt(report):
    if not os.path.exists("reports"):
        os.makedirs("reports")
    filename = f"report_{time.strftime('%Y-%m-%d_%H-%M-%S')}.txt"
    filepath = os.path.join("reports", filename)
    with open(filepath, "w") as file:
        file.write(report)
    print(Fore.GREEN + f"\nLaporan telah disimpan sebagai '{filename}' di folder 'reports'.")
    return filepath

def save_report_pdf(report):
    class PDF(FPDF):
        def header(self):
            self.set_font("Arial", "B", 12)
            self.cell(0, 10, "Laporan Hasil Deteksi URL", 0, 1, "C")

        def footer(self):
            self.set_y(-15)
            self.set_font("Arial", "I", 8)
            self.cell(0, 10, f"Halaman {self.page_no()}", 0, 0, "C")

    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, report)
    filename = f"report_{time.strftime('%Y-%m-%d_%H-%M-%S')}.pdf"
    filepath = os.path.join("reports", filename)
    pdf.output(filepath)
    print(Fore.GREEN + f"\nLaporan telah disimpan sebagai '{filename}' di folder 'reports'.")
    return filepath

def download_report():
    print("\n*****************************************************")
    print("UNDUH LAPORAN")
    print("*****************************************************")
    reports_dir = "reports"
    if os.path.exists(reports_dir):
        reports = os.listdir(reports_dir)
        if reports:
            print("Daftar Laporan:")
            for idx, report in enumerate(reports, 1):
                print(f"{idx}. {report}")
            
            choice = input("Pilih nomor laporan yang ingin diunduh (atau 'b' untuk kembali): ")
            if choice.lower() == 'b':
                return
                
            try:
                choice_idx = int(choice)
                if 1 <= choice_idx <= len(reports):
                    report_to_download = reports[choice_idx - 1]
                    download_path = os.path.join(reports_dir, report_to_download)
                    user_download_folder = Path.home() / "Downloads"
                    destination_path = user_download_folder / report_to_download
                    try:
                        shutil.copy(download_path, destination_path)
                        print(Fore.GREEN + f"Laporan '{report_to_download}' berhasil diunduh dan disimpan di '{destination_path}'.")
                    except IOError as e:
                        print(Fore.RED + f"Gagal menyimpan file: {str(e)}")
                else:
                    print(Fore.RED + "Nomor laporan tidak valid.")
            except ValueError:
                print(Fore.RED + "Masukkan nomor laporan yang valid.")
        else:
            print(Fore.YELLOW + "Tidak ada laporan yang tersedia untuk diunduh.")
    else:
        print(Fore.YELLOW + "Folder 'reports' tidak ditemukan.")

def about():
    print("\n*****************************************************")
    print("ABOUT")
    print("*****************************************************")
    print("Aplikasi ini membantu Anda memeriksa keselamatan URL.")
    print("Anda dapat memeriksa apakah sebuah URL aman atau tidak.")
    print("Anda juga dapat menyimpan laporan hasil pengecekan dalam format TXT atau PDF.")
    print("Dengan menggunakan aplikasi ini, Anda dapat lebih waspada terhadap URL yang mencurigakan.")
    print("*****************************************************")
    
    print("\n=====================================================")
    print("Versi 1.0")
    print("Developed by Themufid Dev")
    print("=====================================================")

def view_reports():
    print("\n*****************************************************")
    print("VIEW REPORTS")
    print("*****************************************************")
    print("Daftar Laporan:")
    reports_dir = "reports"
    if os.path.exists(reports_dir):
        reports = os.listdir(reports_dir)
        if reports:
            for idx, report in enumerate(reports, 1):
                print(f"{idx}. {report}")
        else:
            print(Fore.YELLOW + "Tidak ada laporan yang tersedia.")
    else:
        print(Fore.YELLOW + "Folder 'reports' tidak ditemukan.")

def delete_report():
    print("\n*****************************************************")
    print("DELETE REPORT")
    print("*****************************************************")
    reports_dir = "reports"
    if os.path.exists(reports_dir):
        reports = os.listdir(reports_dir)
        if reports:
            print("Daftar Laporan:")
            for idx, report in enumerate(reports, 1):
                print(f"{idx}. {report}")
            
            choice = input("Pilih nomor laporan yang ingin dihapus (atau 'b' untuk kembali): ")
            if choice.lower() == 'b':
                return
                
            try:
                choice_idx = int(choice)
                if 1 <= choice_idx <= len(reports):
                    report_to_delete = reports[choice_idx - 1]
                    delete_path = os.path.join(reports_dir, report_to_delete)
                    os.remove(delete_path)
                    print(Fore.GREEN + f"Laporan '{report_to_delete}' berhasil dihapus.")
                else:
                    print(Fore.RED + "Nomor laporan tidak valid.")
            except ValueError:
                print(Fore.RED + "Masukkan nomor laporan yang valid.")
        else:
            print(Fore.YELLOW + "Tidak ada laporan yang tersedia untuk dihapus.")
    else:
        print(Fore.YELLOW + "Folder 'reports' tidak ditemukan.")

def change_settings():
    global loading_simulation_time, http_request_timeout, max_retries, retry_delay
    print("\n*****************************************************")
    print("CHANGE SETTINGS")
    print("*****************************************************")
    print("Pilihan Pengaturan:")
    print("1. Waktu Simulasi Loading")
    print("2. Timeout Permintaan HTTP")
    print("3. Maksimum Percobaan")
    print("4. Jeda Antar Percobaan")
    print("5. Kustomisasi Tampilan")
    print("6. Kembali ke Menu Utama")
    choice = input("Pilih opsi: ")
    if choice == "1":
        new_loading_time = input("Masukkan waktu simulasi loading baru (detik): ")
        try:
            loading_simulation_time = float(new_loading_time)
            print(Fore.GREEN + "Pengaturan waktu simulasi loading berhasil diubah.")
        except ValueError:
            print(Fore.RED + "Masukkan angka yang valid.")
    elif choice == "2":
        new_timeout = input("Masukkan timeout permintaan HTTP baru (detik): ")
        try:
            http_request_timeout = float(new_timeout)
            print(Fore.GREEN + "Pengaturan timeout permintaan HTTP berhasil diubah.")
        except ValueError:
            print(Fore.RED + "Masukkan angka yang valid.")
    elif choice == "3":
        new_max_retries = input("Masukkan jumlah maksimum percobaan baru: ")
        try:
            max_retries = int(new_max_retries)
            print(Fore.GREEN + "Pengaturan maksimum percobaan berhasil diubah.")
        except ValueError:
            print(Fore.RED + "Masukkan angka yang valid.")
    elif choice == "4":
        new_retry_delay = input("Masukkan jeda antar percobaan baru (detik): ")
        try:
            retry_delay = float(new_retry_delay)
            print(Fore.GREEN + "Pengaturan jeda antar percobaan berhasil diubah.")
        except ValueError:
            print(Fore.RED + "Masukkan angka yang valid.")
    elif choice == "5":
        customise_display()
    elif choice == "6":
        return
    else:
        print(Fore.RED + "Opsi tidak valid. Silakan pilih opsi yang tersedia.")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def change_background_color():
    clear_screen()
    print("\n*****************************************************")
    print("UBAH WARNA LATAR BELAKANG")
    print("*****************************************************")
    print("Pilih warna latar belakang:")
    print("1. Putih")
    print("2. Biru")
    print("3. Hijau")
    print("4. Kuning")
    print("5. Merah")
    print("6. Kembali")
    choice = input("Masukkan nomor warna: ")
    if choice == "1":
        print(Back.WHITE + Fore.BLACK + "Warna latar belakang telah diubah menjadi putih.")
    elif choice == "2":
        print(Back.BLUE + Fore.WHITE + "Warna latar belakang telah diubah menjadi biru.")
    elif choice == "3":
        print(Back.GREEN + Fore.BLACK + "Warna latar belakang telah diubah menjadi hijau.")
    elif choice == "4":
        print(Back.YELLOW + Fore.BLACK + "Warna latar belakang telah diubah menjadi kuning.")
    elif choice == "5":
        print(Back.RED + Fore.WHITE + "Warna latar belakang telah diubah menjadi merah.")
    elif choice == "6":
        return
    else:
        print(Fore.RED + "Opsi tidak valid. Silakan pilih nomor warna yang tersedia.")

def reset_background_color():
    print(Back.RESET)

def change_text_color():
    clear_screen()
    print("\n*****************************************************")
    print(apply_style("UBAH WARNA TEKS", "BRIGHT"))
    print("*****************************************************")
    print("Pilih warna teks:")
    print("1. Putih")
    print("2. Biru")
    print("3. Hijau")
    print("4. Kuning")
    print("5. Merah")
    print("6. Kembali")
    choice = input("Masukkan nomor warna: ")
    if choice == "1":
        print(Fore.WHITE + "Warna teks telah diubah menjadi putih.")
    elif choice == "2":
        print(Fore.BLUE + "Warna teks telah diubah menjadi biru.")
    elif choice == "3":
        print(Fore.GREEN + "Warna teks telah diubah menjadi hijau.")
    elif choice == "4":
        print(Fore.YELLOW + "Warna teks telah diubah menjadi kuning.")
    elif choice == "5":
        print(Fore.RED + "Warna teks telah diubah menjadi merah.")
    elif choice == "6":
        return
    else:
        print(Fore.RED + "Opsi tidak valid. Silakan pilih nomor warna yang tersedia.")

def reset_text_color():
    print(Fore.RESET)

def customise_display():
    while True:
        clear_screen()
        print("=====================================================")
        print(apply_style("KUSTOMISASI TAMPILAN", "BRIGHT"))
        print("=====================================================")
        print("Pilih opsi kustomisasi:")
        print("1. Ubah Warna Latar Belakang")
        print("2. Reset Warna Latar Belakang")
        print("3. Ubah Warna Teks")
        print("4. Reset Warna Teks")
        print("5. Kembali ke Menu Utama")
        choice = input("Masukkan nomor opsi: ")
        if choice == "1":
            change_background_color()
            input("Tekan Enter untuk melanjutkan...")
        elif choice == "2":
            reset_background_color()
            input("Tekan Enter untuk melanjutkan...")
        elif choice == "3":
            change_text_color()
            input("Tekan Enter untuk melanjutkan...")
        elif choice == "4":
            reset_text_color()
            input("Tekan Enter untuk melanjutkan...")
        elif choice == "5":
            break
        else:
            print(Fore.RED + "Opsi tidak valid. Silakan pilih opsi yang tersedia.")

def terminal_ui():
    print("=====================================================")
    print(apply_style("WELCOME TO URL DETECTION APP!", "BRIGHT"))
    print("=====================================================")
    while True:
        print("\nMenu:")
        print("1. Periksa URL")
        print("2. Tentang")
        print("3. Lihat Laporan")
        print("4. Hapus Laporan")
        print("5. Unduh Laporan")
        print("6. Ubah Pengaturan")
        print("7. Keluar")
        print("=====================================================")
        
        choice = input("Pilih menu: ")
        
        if choice == "1":
            print("Format URL: https://www.yourweb.com")
            url = input("Masukkan URL yang ingin Anda periksa: ")
            is_safe, message = check_url_safety(url)
            print("\n" + message)
            report = generate_report(url, is_safe, message)
            print("\nMenu:")
            print("1. Simpan Laporan (TXT)")
            print("2. Simpan Laporan (PDF)")
            print("3. Kembali ke Menu Utama")
            choice_report = input("Pilih opsi: ")
            if choice_report == "1":
                save_report_txt(report)
            elif choice_report == "2":
                save_report_pdf(report)
            elif choice_report == "3":
                continue
            else:
                print(Fore.RED + "Opsi tidak valid. Silakan pilih opsi yang tersedia.")
        elif choice == "2":
            about()
        elif choice == "3":
            view_reports()
        elif choice == "4":
            delete_report()
        elif choice == "5":
            download_report()
        elif choice == "6":
            change_settings()
        elif choice == "7":
            print("=====================================================")
            print(Fore.YELLOW + "\nTerima kasih telah menggunakan aplikasi ini.")
            print("=====================================================")
            break
        else:
            print(Fore.RED + "\nMenu tidak valid. Silakan pilih menu yang tersedia.")

if __name__ == "__main__":
    terminal_ui()