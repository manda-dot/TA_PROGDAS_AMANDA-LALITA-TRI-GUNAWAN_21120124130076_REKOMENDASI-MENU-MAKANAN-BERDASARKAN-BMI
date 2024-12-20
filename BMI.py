import tkinter as tk
from tkinter import messagebox
from collections import deque
from tkinter import font

class BMI:
    def __init__(self, berat, tinggi):
        self.berat = berat
        self.tinggi = tinggi
        self.bmi = self.hitung_bmi()
        self.kategori = self.tentukan_kategori()
        self.rekomendasi = self.rekomendasi_makanan()

    def hitung_bmi(self):
        tinggi_dalam_meter = self.tinggi / 100  
        return self.berat / (tinggi_dalam_meter ** 2)

    def tentukan_kategori(self):
        if self.bmi < 18.5:
            return "Kurus"
        elif 18.5 <= self.bmi < 24.9:
            return "Normal"
        else:
            return "Obesitas"

    def rekomendasi_makanan(self):
        if self.kategori == "Kurus":
            return [
                ("Semangkuk Sereal dengan Susu", "images/sereal.png"),
                ("Roti Panggang dengan Olesan Mentega", "images/roti.png"),
                ("Olahan Daging yang Digoreng", "images/daging.png")
            ]
        elif self.kategori == "Normal":
            return [
                ("Salad Bayam", "images/salad.png"),
                ("Sup Kacang Polong", "images/sup.png"),
                ("Tuna Sandwich", "images/sandwich.png")
            ]
        else:
            return [
                ("Daging Dada Ayam", "images/ayam.png"),
                ("Kentang Rebus", "images/kentang.png"),
                ("Sayur Bayam Bening", "images/bayam.png")
            ]


class BMIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi BMI")
        self.root.geometry("400x500")
        self.root.config(bg="#F1F1F1")  
        self.custom_font = font.Font(family="Helvetica", size=12)

        self.rekomendasi_queue = deque()
        self.main_frame = tk.Frame(self.root, bg="#F1F1F1")
        self.main_frame.pack(padx=40, pady=40)
        
        self.running = True
        self.start_loop()

    def start_loop(self):
        while self.running:
            self.halaman_utama()
            self.root.mainloop()  

    def halaman_utama(self):
        for widget in self.main_frame.winfo_children():
            widget.pack_forget()

        label_tinggi = tk.Label(self.main_frame, text="Tinggi Badan (cm):", font=self.custom_font, bg="#F1F1F1")
        label_tinggi.pack(pady=10)
        self.entry_tinggi = tk.Entry(self.main_frame, font=self.custom_font)
        self.entry_tinggi.pack(pady=10)

        label_berat = tk.Label(self.main_frame, text="Berat Badan (kg):", font=self.custom_font, bg="#F1F1F1")
        label_berat.pack(pady=10)
        self.entry_berat = tk.Entry(self.main_frame, font=self.custom_font)
        self.entry_berat.pack(pady=10)

        button_hitung = tk.Button(self.main_frame, text="Hitung BMI", command=self.proses_bmi, font=self.custom_font, bg="#4CAF50", fg="white", relief="raised")
        button_hitung.pack(pady=20)

        self.label_bmi = tk.Label(self.main_frame, text="BMI Anda: ", font=self.custom_font, bg="#F1F1F1")
        self.label_bmi.pack(pady=20)

        button_rekomendasi = tk.Button(self.main_frame, text="Lihat Rekomendasi Makanan", command=self.halaman_rekomendasi, font=self.custom_font, bg="#2196F3", fg="white", relief="raised")
        button_rekomendasi.pack(pady=20)

    def proses_bmi(self):
        try:
            berat = float(self.entry_berat.get())
            tinggi = float(self.entry_tinggi.get())

            bmi_obj = BMI(berat, tinggi)

            self.label_bmi.config(text=f"BMI Anda: {bmi_obj.bmi:.2f} ({bmi_obj.kategori})")

            self.rekomendasi_queue = deque(bmi_obj.rekomendasi)

        except ValueError:
            messagebox.showerror("Input Error", "Masukkan nilai yang valid untuk berat badan dan tinggi badan")

    def halaman_rekomendasi(self):
        for widget in self.main_frame.winfo_children():
            widget.pack_forget()

        label_rekomendasi_title = tk.Label(self.main_frame, text="Rekomendasi Makanan", font=self.custom_font, bg="#F1F1F1")
        label_rekomendasi_title.pack(pady=20)

        if self.rekomendasi_queue:
            makanan, gambar_path = self.rekomendasi_queue[0]

            label_rekomendasi_hasil = tk.Label(self.main_frame, text=f"{makanan}", font=self.custom_font, bg="#F1F1F1")
            label_rekomendasi_hasil.pack(pady=20)

            self.tampilkan_gambar(gambar_path)

            button_next = tk.Button(self.main_frame, text="Rekomendasi Makanan Lainnya", command=self.next_rekomendasi, bg="#4CAF50", fg="white", font=("Arial", 12), relief="raised", padx=10, pady=5)
            button_next.pack(fill='x', pady=20)

        button_back = tk.Button(self.main_frame, text="Kembali ke Halaman Awal", command=self.halaman_utama, font=self.custom_font, bg="#FF5722", fg="white", relief="raised")
        button_back.pack(pady=10)

        button_exit = tk.Button(self.main_frame, text="Keluar", command=self.keluar_aplikasi, font=self.custom_font, bg="#F44336", fg="white", relief="raised")
        button_exit.pack(pady=10)

    def tampilkan_gambar(self, image_path):
        try:
            img = tk.PhotoImage(file=image_path)
            img_resized = img.subsample(4, 4)  
            label_image = tk.Label(self.main_frame, image=img_resized, bg="#F1F1F1")
            label_image.image = img_resized 
            label_image.pack(pady=20)
        except Exception as e:
            messagebox.showerror("Error", f"Tidak dapat memuat gambar: {str(e)}")

    def next_rekomendasi(self):
        if len(self.rekomendasi_queue) > 1:
            self.rekomendasi_queue.popleft()
            self.halaman_rekomendasi()

    def keluar_aplikasi(self):
        self.running = False
        self.root.destroy()

root = tk.Tk()
app = BMIApp(root)