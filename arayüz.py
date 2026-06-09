# main.py
import tkinter as tk
from tkinter import ttk, messagebox
import random
from hata_algilama import hamming_kod_hesapla, hata_olustur, hata_duzelt, veri_cikar

class ModernHammingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hamming Single Error Detection")
        self.geometry("1100x700")
        self.configure(bg="#f8f9fa") # Açık modern gri arka plan
        
        # Değişken Tanımlamaları
        self.veri_uzunluk = tk.IntVar(value=8)
        self.random_hata = tk.BooleanVar(value=True)
        self.hata_poz = tk.IntVar(value=0)
        self.kodlanmis_veri = []
        self.hata_enjekte_edildi = False
        self.arayuz_tasarla()
        
    def arayuz_tasarla(self):
        # ------------------ SOL MENÜ (SIDEBAR) ------------------
        sidebar = tk.Frame(self, bg="#2c3e50", width=280, padx=20, pady=20)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)
        
        #  Başlık
        side_title = tk.Label(sidebar, text="SINGLE ERROR\nDETECTION", font=("Helvetica", 14, "bold"), fg="#ecf0f1", bg="#2c3e50")
        side_title.pack(pady=(10, 30))
        
        # Ayarlar Bölümü
        lbl_config = tk.Label(sidebar, text="KONTROL PANELİ", font=("Helvetica", 10, "bold"), fg="#bdc3c7", bg="#2c3e50")
        lbl_config.pack(anchor="w", pady=(10, 5))
        
        # Veri Uzunluğu Seçimi (Radio)
        len_frame = tk.Frame(sidebar, bg="#34495e", padx=10, pady=10, bd=0)
        len_frame.pack(fill=tk.X, pady=5)
        lbl_len = tk.Label(len_frame, text="Veri Uzunluğu Seçin:", font=("Helvetica", 9), fg="#ecf0f1", bg="#34495e")
        lbl_len.pack(anchor="w")
        
        for uzunluk, text in [(8, "8-Bit Modu"), (16, "16-Bit Modu"), (32, "32-Bit Modu")]:
            rb = tk.Radiobutton(len_frame, text=text, variable=self.veri_uzunluk, value=uzunluk,
                                bg="#34495e", fg="#ecf0f1", selectcolor="#2c3e50", activebackground="#34495e", activeforeground="white")
            rb.pack(anchor="w", padx=5, pady=2)
            
        # Hata Enjeksiyon Paneli
        hata_panel = tk.Frame(sidebar, bg="#34495e", padx=10, pady=10)
        hata_panel.pack(fill=tk.X, pady=15)
        lbl_hata_t = tk.Label(hata_panel, text="Hata Enjeksiyon Ayarı:", font=("Helvetica", 9), fg="#ecf0f1", bg="#34495e")
        lbl_hata_t.pack(anchor="w", pady=(0, 5))
        
        cb_rand = tk.Checkbutton(hata_panel, text="Pozisyonu Rastgele Seç", variable=self.random_hata,
                                 bg="#34495e", fg="#ecf0f1", selectcolor="#2c3e50", activebackground="#34495e", activeforeground="white")
        cb_rand.pack(anchor="w")
        
        spin_frame = tk.Frame(hata_panel, bg="#34495e")
        spin_frame.pack(fill=tk.X, pady=5)
        tk.Label(spin_frame, text="Manuel İndeks:", fg="#ecf0f1", bg="#34495e", font=("Helvetica", 9)).pack(side=tk.LEFT)
        self.poz_spinbox = tk.Spinbox(spin_frame, from_=0, to=38, textvariable=self.hata_poz, width=5)
        self.poz_spinbox.pack(side=tk.RIGHT, padx=5)

        # Alt Bilgi Bölümü
        lbl_info = tk.Label(sidebar, text="Mavi: Veri Biti\nYeşil: Hamming Parity\nSarı: Genel Parity\nKırmızı: Hatalı Bit", font=("Helvetica", 8, "italic"), fg="#95a5a6", bg="#2c3e50", justify=tk.LEFT)
        lbl_info.pack(side=tk.BOTTOM, anchor="w")

        # ------------------ SAĞ PANEL (ANA İÇERİK) ------------------
        ana_icerik = tk.Frame(self, bg="#e6f0fa", padx=25, pady=20)
        ana_icerik.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # ÜST KART: Veri Girişi ve Canvas Görselleştirme
        kart_ust = tk.LabelFrame(ana_icerik, text=" 1. Giriş ve Bit Haritası Görselleştirme ", font=("Helvetica", 10, "bold"), bg="white", fg="#2c3e50", bd=1, relief=tk.SOLID, padx=15, pady=15)
        kart_ust.pack(fill=tk.X, pady=(0, 15))
        
        giris_satir = tk.Frame(kart_ust, bg="white")
        giris_satir.pack(fill=tk.X, pady=(0, 10))
        tk.Label(giris_satir, text="Simüle Edilecek İkilik (Binary) Veri:", font=("Helvetica", 10), bg="white", fg="#333").pack(side=tk.LEFT, padx=(0, 10))
        
        self.veri_entry = tk.Entry(giris_satir, font=("Consolas", 12), width=30, bd=1, relief=tk.SOLID)
        self.veri_entry.pack(side=tk.LEFT, padx=5, ipady=3)
        
        btn_rand = tk.Button(giris_satir, text="Rastgele Veri Üret", command=self.random_veri_olustur, bg="#e9ecef", fg="#333", font=("Helvetica", 9), relief=tk.GROOVE, padx=10)
        btn_rand.pack(side=tk.LEFT, padx=10)
        
        # Bit Şeridi Canvas
        self.bit_canvas = tk.Canvas(kart_ust, height=85, bg="#f1f3f5", bd=0, highlightthickness=0)
        self.bit_canvas.pack(fill=tk.X, pady=5)

        # ORTA KART: Eylem Butonları (Yatay ve Düzenli Renklerle)
        kart_orta = tk.LabelFrame(ana_icerik, text=" 2. Simülasyon Adımları ", font=("Helvetica", 10, "bold"), bg="white", fg="#2c3e50", bd=1, relief=tk.SOLID, padx=15, pady=15)
        kart_orta.pack(fill=tk.X, pady=(0, 15))
        
        btn_calc = tk.Button(kart_orta, text="Hamming Kodunu Hesapla", command=self.hamming_hesapla, bg="#0d6efd", fg="white", font=("Helvetica", 10, "bold"), width=24, pady=6, relief=tk.FLAT)
        btn_calc.pack(side=tk.LEFT, padx=10, expand=True)
        
        btn_err = tk.Button(kart_orta, text="Kanala Hata Enjekte Et", command=self.hata_olustur, bg="#dc3545", fg="white", font=("Helvetica", 10, "bold"), width=24, pady=6, relief=tk.FLAT)
        btn_err.pack(side=tk.LEFT, padx=10, expand=True)
        
        btn_fix = tk.Button(kart_orta, text="Hata Tespit Et ve Onar", command=self.hata_tespit, bg="#198754", fg="white", font=("Helvetica", 10, "bold"), width=24, pady=6, relief=tk.FLAT)
        btn_fix.pack(side=tk.LEFT, padx=10, expand=True)

        # ALT KART: Çıktı Tablosu
        kart_alt = tk.LabelFrame(ana_icerik, text=" 3. Analiz Raporu ve Çıktılar ", font=("Helvetica", 10, "bold"), bg="white", fg="#2c3e50", bd=1, relief=tk.SOLID, padx=15, pady=15)
        kart_alt.pack(fill=tk.BOTH, expand=True)
        
        grid_container = tk.Frame(kart_alt, bg="white")
        grid_container.pack(fill=tk.BOTH, expand=True)
        
        etiketler = ["Orijinal Veri:", "Hamming Kodu:", "Hatalı Veri:", "Sendrom Değeri:", "Düzeltilmiş Veri:", "Saptanan Hata İndeksi:"]
        self.sonuc_kutulari = {}
        
        for i, etiket in enumerate(etiketler):
            tk.Label(grid_container, text=etiket, font=("Helvetica", 9, "bold"), bg="white", fg="#495057", anchor="w").grid(row=i, column=0, padx=10, pady=6, sticky="w")
            entry = tk.Entry(grid_container, font=("Consolas", 11), bg="#f8f9fa", fg="#212529", bd=1, relief=tk.SOLID)
            entry.grid(row=i, column=1, padx=10, pady=6, sticky="ew")
            self.sonuc_kutulari[etiket] = entry
            
        grid_container.columnconfigure(1, weight=1)
        
        # Durum Çubuğu
        self.status_bar = tk.Label(self, text="Sistem Hazır - Veri girişi bekleniyor.", bd=0, anchor=tk.W, bg="#e9ecef", fg="#495057", padx=15, pady=5, font=("Helvetica", 9))
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    # ------------------ MANTIKSAL KÖPRÜ FONKSİYONLARI ------------------
    def random_veri_olustur(self):
        uzunluk = self.veri_uzunluk.get()
        veri = ''.join(str(random.randint(0, 1)) for _ in range(uzunluk))
        self.veri_entry.delete(0, tk.END)
        self.veri_entry.insert(0, veri)
        self.status_bar.config(text=f"Bilgi: {uzunluk} bit uzunluğunda rastgele veri üretildi.")
        
    def hamming_hesapla(self):
        veri_str = self.veri_entry.get().strip()
        uzunluk = self.veri_uzunluk.get()
        
        if not veri_str or not all(bit in '01' for bit in veri_str) or len(veri_str) != uzunluk:
            messagebox.showerror("Giriş Hatası", f"Lütfen seçilen mod ile uyumlu ({uzunluk} bit) sadece 0 ve 1'lerden oluşan veri girin!")
            return
            
        self.kodlanmis_veri = hamming_kod_hesapla(veri_str, uzunluk)
        self.hata_enjekte_edildi = False
        self.bitleri_goster(self.kodlanmis_veri)
        
        for k in self.sonuc_kutulari.values(): k.delete(0, tk.END)
        
        self.sonuc_kutulari["Orijinal Veri:"].insert(0, veri_str)
        self.sonuc_kutulari["Hamming Kodu:"].insert(0, ''.join(map(str, self.kodlanmis_veri)))
        self.status_bar.config(text=f"İşlem: Hamming kodu başarıyla hesaplandı. Paket boyutu: {len(self.kodlanmis_veri)} bit.")

    def hata_olustur(self):
        if not self.kodlanmis_veri:
            messagebox.showerror("Sıralama Hatası", "Önce Hamming kodunu hesaplamalısınız!")
            return
            
        # ÇOKLU HATA ENGELLEME KONTROLÜ
        if self.hata_enjekte_edildi:
            messagebox.showwarning("Simülasyon Sınırı", "Zaten 1 bit hata enjekte edildi!\nBu simülatörün doğru çalışması için sadece tek bit kontrolü yapabilirsiniz.")
            return
            
        if self.random_hata.get():
            hata_poz = random.randint(0, len(self.kodlanmis_veri)-1)
            self.hata_poz.set(hata_poz)
        else:
            hata_poz = self.hata_poz.get()
            if hata_poz >= len(self.kodlanmis_veri):
                messagebox.showerror("Sınır Hatası", f"Hata indeksi 0 ile {len(self.kodlanmis_veri)-1} arasında olmalıdır!")
                return
                
        self.kodlanmis_veri = hata_olustur(self.kodlanmis_veri, hata_poz)
        self.hata_enjekte_edildi = True 
        self.bitleri_goster(self.kodlanmis_veri, hata_poz)
        
        self.sonuc_kutulari["Hatalı Veri:"].delete(0, tk.END)
        self.sonuc_kutulari["Hatalı Veri:"].insert(0, ''.join(map(str, self.kodlanmis_veri)))
        self.sonuc_kutulari["Saptanan Hata İndeksi:"].delete(0, tk.END)
        self.sonuc_kutulari["Saptanan Hata İndeksi:"].insert(0, f"{hata_poz}. İndeks Değiştirildi")
        self.status_bar.config(text=f"Simülasyon: {hata_poz}. indeksteki bit kasıtlı olarak bozuldu.")
    def hata_tespit(self):
        if not self.kodlanmis_veri:
            messagebox.showerror("Sıralama Hatası", "Analiz edilecek veri bulunamadı!")
            return
            
        duzeltilmis, mesaj, sendrom, hata_biti = hata_duzelt(self.kodlanmis_veri)
        self.kodlanmis_veri = duzeltilmis
        self.bitleri_goster(self.kodlanmis_veri, hata_biti)
        
        orijinal_veri = veri_cikar(duzeltilmis, self.veri_uzunluk.get())
        
        self.sonuc_kutulari["Sendrom Değeri:"].delete(0, tk.END)
        self.sonuc_kutulari["Sendrom Değeri:"].insert(0, f"Binary: {bin(sendrom)} (Desimal: {sendrom})")
        self.sonuc_kutulari["Düzeltilmiş Veri:"].delete(0, tk.END)
        self.sonuc_kutulari["Düzeltilmiş Veri:"].insert(0, ''.join(map(str, orijinal_veri)))
        self.status_bar.config(text=mesaj)

    def bitleri_goster(self, bits, highlight_pos=-1):
        self.bit_canvas.delete("all")
        if not bits: return
        
        bit_count = len(bits)
        canvas_width = self.bit_canvas.winfo_width()
        if canvas_width < 100: canvas_width = 750
        
        box_width = min(28, canvas_width // bit_count)
        box_height = 32
        start_x = (canvas_width - (box_width * bit_count)) // 2
        
        for i, bit in enumerate(bits):
            x1 = start_x + (i * box_width)
            y1 = 15
            x2 = x1 + box_width
            y2 = y1 + box_height
            
            # Renk Şeması Ataması (Modern Tonlar)
            if i == highlight_pos:
                color = "#dc3545"  # Hatalı/Düzeltilen Bit (Kırmızı)
            elif i == len(bits) - 1:
                color = "#ffc107"  # Genel Parity (Sarı)
            elif (i+1) & i == 0:
                color = "#198754"  # Hamming Parity (Yeşil)
            else:
                color = "#0d6efd"  # Veri Biti (Mavi)
                
            # Dikdörtgen Hücreler ve Yazılar
            self.bit_canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#ffffff", width=1)
            self.bit_canvas.create_text((x1+x2)//2, (y1+y2)//2, text=str(bit), font=("Helvetica", 10, "bold"), fill="white")
            self.bit_canvas.create_text((x1+x2)//2, y2 + 12, text=f"i:{i}", font=("Helvetica", 7), fill="#6c757d")

if __name__ == "__main__":
    app = ModernHammingApp()
    app.mainloop()