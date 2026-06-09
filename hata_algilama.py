# hamming_core.py

def hamming_kod_hesapla(veri_str, veri_uzunlugu):
    veri = [int(bit) for bit in veri_str]
    
    r = 0
    while 2**r < veri_uzunlugu + r + 1:
        r += 1
    
    kodlanmis_uzunluk = veri_uzunlugu + r + 1
    kodlanmis = [0] * kodlanmis_uzunluk
    
    veri_idx = 0
    for i in range(1, kodlanmis_uzunluk):
        if not (i & (i-1) == 0):
            if veri_idx < len(veri):
                kodlanmis[i-1] = veri[veri_idx]
                veri_idx += 1
    
    for i in range(r):
        parity_poz = 2**i - 1
        parity = 0
        for j in range(kodlanmis_uzunluk):
            if (j+1) & (2**i) and j != kodlanmis_uzunluk-1:
                parity ^= kodlanmis[j]
        kodlanmis[parity_poz] = parity
    
    genel_parity = 0
    for i in range(kodlanmis_uzunluk-1):
        genel_parity ^= kodlanmis[i]
    kodlanmis[kodlanmis_uzunluk-1] = genel_parity
    
    return kodlanmis

def hata_olustur(kodlanmis, pozisyon):
    if 0 <= pozisyon < len(kodlanmis):
        hatali_veri = kodlanmis.copy()
        hatali_veri[pozisyon] = 1 - hatali_veri[pozisyon]
        return hatali_veri
    return kodlanmis

def sendrom_hesapla(kodlanmis):
    uzunluk = len(kodlanmis)
    r = 0
    while 2**r < uzunluk:
        r += 1
    
    genel_parity_check = 0
    for bit in kodlanmis:
        genel_parity_check ^= bit
    
    sendrom = 0
   
    for i in range(r): 
        parity_check = 0
        for j in range(uzunluk-1):
            if (j+1) & (2**i):
                parity_check ^= kodlanmis[j]
        if parity_check != 0:
            sendrom += 2**i
    
    return sendrom, genel_parity_check != 0

def hata_duzelt(kodlanmis):
    sendrom, genel_parity_hatasi = sendrom_hesapla(kodlanmis)
    duzeltilmis = kodlanmis.copy()
    hata_biti = -1
    
    if sendrom == 0 and not genel_parity_hatasi:
        hata_mesaji = "Başarılı: Sistemde herhangi bir hata tespit edilmedi."
    elif sendrom != 0 and genel_parity_hatasi:
        hata_biti = sendrom - 1
        if 0 <= hata_biti < len(duzeltilmis):
            duzeltilmis[hata_biti] = 1 - duzeltilmis[hata_biti]
            hata_mesaji = f"Tek Bit Hatası Düzenlendi: {hata_biti}. indeksteki hata başarıyla düzeltildi."
        else:
            hata_mesaji = "Hata: Geçersiz hata pozisyonu algılandı."
    elif sendrom == 0 and genel_parity_hatasi:
        hata_mesaji = "Genel Parity Hatası: Sadece genel koruma bitinde bozulma var, düzeltildi."
        hata_biti = len(duzeltilmis) - 1
        duzeltilmis[-1] = 1 - duzeltilmis[-1]
    else:
        hata_mesaji = "Kritik Çift Bit Hatası: Aynı anda 2 bit bozulmuş! (Sistem bunu düzeltemez)."
    
    return duzeltilmis, hata_mesaji, sendrom, hata_biti

def veri_cikar(kodlanmis, veri_uzunlugu):
    veri = []
    veri_idx = 0
    for i in range(1, len(kodlanmis)):
        if not (i & (i-1) == 0):
            if veri_idx < veri_uzunlugu:
                veri.append(kodlanmis[i-1])
                veri_idx += 1
    return veri[:veri_uzunlugu]