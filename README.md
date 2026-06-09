# 🛠️ Hamming SEC (Single Error Correction) Simülatörü

Bu proje, veri iletimi sırasında oluşabilecek hataları tespit etmek ve onarmak için kullanılan klasik **Hamming Kodu** algoritmasını modern bir grafik arayüz (Tkinter) ile görselleştiren interaktif bir simülasyon aracıdır. 

Uygulama, veriye eklenen matematiksel kontrol bitleri sayesinde **tek bit hatalarını nokta atışı bulup düzeltebilir (SEC)** ve **çift bit hatalarını algılayarak (DED)** veri bütünlüğünü korur.

---

## 🎨 Ekran Görüntüleri & Arayüz Renk Şeması

Uygulamanın sağ paneli, modern ve gözü yormayan **Buz Mavisi (`#e6f0fa`)** temasına sahiptir. Bit şeridindeki her bir kutu, projedeki görevine göre özel olarak renklendirilmiştir:

* 🔵 **Mavi (Veri Biti):** Kullanıcının simüle etmek için girdiği orijinal binary verinin bitleridir.
* 🟢 **Yeşil (Hamming Parity Biti):** Belirli ritimlerle kendi sorumluluk alanlarındaki veri bitlerini izleyen koruma ajanlarıdır.
* 🟡 **Sarı (Genel Parity Biti):** Paketin en sonunda yer alır ve tüm şeritteki (mavi + yeşil) toplam `1` sayısını çift yapacak şekilde kendini ayarlar. Çift bit hatalarını yakalamayı sağlar.
* 🔴 **Kırmızı (Hatalı / Düzeltilen Bit):** Kanala enjekte edilen hatanın yerini veya sistem tarafından başarıyla onarılan biti temsil eder.

---

## 🧮 Algoritma Nasıl Çalışır?

### 1. Yeşil Bitlerin Görevi (Sendrom Analizi)
Her yeşil bit, ikilik sistemdeki basamak ağırlıklarına göre (1, 2, 4, 8...) belirli indeksleri kontrol eder:
* **P1 (İndeks 0):** 1 bit kontrol eder, 1 bit atlar (0, 2, 4, 6, 8...).
* **P2 (İndeks 1):** 2 bit kontrol eder, 2 bit atlar (1, 2, 5, 6, 9...).
* **P4 (İndeks 3):** 4 bit kontrol eder, 4 bit atlar (3, 4, 5, 6, 11...).
* **P8 (İndeks 7):** 8 bit kontrol eder, 8 bit atlar (7, 8, 9, 10...).

Hata durumunda dengesi bozulan yeşil bitler birer **Alarm (1)** üretir. Bu alarmlar büyükten küçüğe yan yana dizilerek **Sendrom Değeri**'ni (örn. `0b110` -> Desimal: 6) oluşturur. Bulunan bu değerden 1 çıkarılarak ($6 - 1 = 5$) hatalı indeks nokta atışı tespit edilir.

### 2. Sarı Bitin Görevi (Kritik Çift Hata Yakalama)
* **1 Bit Bozulursa:** Toplam `1` dengesi bozulur; sarı bit alarm verir, yeşil bitler hatanın yerini gösterir -> **Hata Düzeltilir.**
* **2 Bit Bozulursa:** Toplam `1` dengesi bozulmaz (çift kalır); sarı bit sakin kalır ancak yeşil bitler alarm üretir. Bu çelişki sayesinde sistem veri kaybını önler -> **Çift Bit Hatası Algılandı Bildirimi Verilir.**

---

## 🚀 Proje Yapısı

Proje modüler iki ana dosyadan oluşmaktadır:
1. `main.py` (veya `arayüz.py`): Tkinter tabanlı modern arayüz bileşenlerini, bit haritası çizim kanvasını ve buton tetikleyicilerini içerir.
2. `hamming_core.py`: Hamming kodunun hesaplanması, kanal gürültüsü/hata enjeksiyonu ve sendrom analizi gibi tüm matematiksel çekirdek mantığı yürütür.

---

## 🛠️ Kurulum ve Çalıştırma

Projenin çalışması için bilgisayarınızda **Python 3.x** kurulu olması yeterlidir. Herhangi bir harici kütüphaneye (pip) ihtiyaç duymaz, standart Python kütüphanelerini kullanır.

1. Depoyu klonlayın veya dosyaları bilgisayarınıza indirin.
2. Aynı dizinde bir terminal/komut satırı açın.
3. Uygulamayı başlatmak için şu komutu çalıştırın:

```bash
python main.py
