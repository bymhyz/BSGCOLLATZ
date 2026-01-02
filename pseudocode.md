# Sözde Kod (Pseudocode)

## Collatz-Fibonacci-Chaos RSÜ Algoritması

Bu belge, algoritmanın her modülü için Türkçe sözde kod içerir.

---

## 1. Collatz Dizisi Üreteci

```
FONKSİYON CollatzDizisiÜret(başlangıç_sayısı):
    n ← başlangıç_sayısı
    dizi ← [n]
    bitler ← [n MOD 2]
    
    WHILE n ≠ 1 DO:
        IF n çift ise THEN:
            n ← n / 2
        ELSE:
            n ← 3 × n + 1
        ENDIF
        
        dizi'ye n ekle
        bitler'e (n MOD 2) ekle
    ENDWHILE
    
    RETURN (dizi, bitler)
END FONKSİYON
```

---

## 2. Fibonacci LFSR (Doğrusal Geri Beslemeli Kaydırmalı Yazmaç)

```
FONKSİYON FibonacciLFSR_Başlat(tohum):
    // Polinom: x^16 + x^14 + x^13 + x^11 + 1
    // Tap pozisyonları: 15, 13, 12, 10 (0-indexed)
    
    durum ← tohum AND 0xFFFF    // 16-bit'e sınırla
    IF durum = 0 THEN:
        durum ← 1               // Sıfır durumu yasak
    ENDIF
    
    RETURN durum
END FONKSİYON

FONKSİYON LFSR_Adım(durum):
    // Tap pozisyonlarındaki bitleri XOR'la
    geri_besleme ← 0
    geri_besleme ← geri_besleme XOR (durum >> 15) AND 1
    geri_besleme ← geri_besleme XOR (durum >> 13) AND 1
    geri_besleme ← geri_besleme XOR (durum >> 12) AND 1
    geri_besleme ← geri_besleme XOR (durum >> 10) AND 1
    
    // Çıkış biti (en sağdaki bit)
    çıkış_biti ← durum AND 1
    
    // Kaydırma ve yeni bit ekleme
    yeni_durum ← (durum >> 1) OR (geri_besleme << 15)
    
    RETURN (yeni_durum, çıkış_biti)
END FONKSİYON

FONKSİYON LFSR_BitÜret(durum, adet):
    bitler ← []
    mevcut_durum ← durum
    
    FOR i ← 1 TO adet DO:
        (mevcut_durum, bit) ← LFSR_Adım(mevcut_durum)
        bitler'e bit ekle
    ENDFOR
    
    RETURN bitler
END FONKSİYON
```

---

## 3. Logistic Map (Lojistik Harita)

```
SABİT r ← 3.99    // Kaotik parametre

FONKSİYON LogisticMap_Başlat(tohum):
    // Tohumu 0-1 aralığına normalize et
    x0 ← ((tohum MOD 997) + 1) / 999.0
    
    // Sınır kontrolü
    IF x0 < 0.001 THEN x0 ← 0.001
    IF x0 > 0.999 THEN x0 ← 0.999
    
    RETURN x0
END FONKSİYON

FONKSİYON LogisticMap_Adım(x):
    // Lojistik harita formülü
    x_yeni ← r × x × (1 - x)
    RETURN x_yeni
END FONKSİYON

FONKSİYON LogisticMap_BitÜret(x, adet):
    bitler ← []
    mevcut_x ← x
    
    FOR i ← 1 TO adet DO:
        mevcut_x ← LogisticMap_Adım(mevcut_x)
        
        IF mevcut_x ≥ 0.5 THEN:
            bitler'e 1 ekle
        ELSE:
            bitler'e 0 ekle
        ENDIF
    ENDFOR
    
    RETURN bitler
END FONKSİYON
```

---

## 4. Von Neumann Düzeltici

```
FONKSİYON VonNeumann_Düzelt(bitler):
    // Ardışık bit çiftlerini analiz et
    // 01 → 0, 10 → 1, 00 ve 11 atılır
    
    sonuç ← []
    i ← 0
    
    WHILE i < UZUNLUK(bitler) - 1 DO:
        IF bitler[i] = 0 AND bitler[i+1] = 1 THEN:
            sonuç'a 0 ekle
        ELSE IF bitler[i] = 1 AND bitler[i+1] = 0 THEN:
            sonuç'a 1 ekle
        ENDIF
        // 00 ve 11 durumları atlanır
        
        i ← i + 2
    ENDWHILE
    
    RETURN sonuç
END FONKSİYON
```

---

## 5. Ana RSÜ Algoritması

```
FONKSİYON RSÜ_Oluştur(ana_tohum):
    // Collatz dizisini üret
    (collatz_dizi, collatz_bitler) ← CollatzDizisiÜret(ana_tohum)
    
    // LFSR için tohum çıkar
    lfsr_tohum ← 0
    FOR i ← 0 TO MIN(15, UZUNLUK(collatz_bitler)-1) DO:
        lfsr_tohum ← lfsr_tohum OR (collatz_bitler[i] << i)
    ENDFOR
    
    // Bileşenleri başlat
    lfsr_durum ← FibonacciLFSR_Başlat(lfsr_tohum)
    logistic_x ← LogisticMap_Başlat(ana_tohum)
    
    RETURN (lfsr_durum, logistic_x)
END FONKSİYON

FONKSİYON DengeliBitÜret(lfsr_durum, logistic_x, adet):
    sonuç ← []
    
    WHILE UZUNLUK(sonuç) < adet DO:
        // Her iki kaynaktan bit üret
        lfsr_bitler ← LFSR_BitÜret(lfsr_durum, adet × 3)
        logistic_bitler ← LogisticMap_BitÜret(logistic_x, adet × 3)
        
        // XOR birleştirme
        ham_bitler ← []
        FOR i ← 0 TO UZUNLUK(lfsr_bitler)-1 DO:
            ham_bitler'e (lfsr_bitler[i] XOR logistic_bitler[i]) ekle
        ENDFOR
        
        // Von Neumann düzeltme
        dengeli_bitler ← VonNeumann_Düzelt(ham_bitler)
        sonuç ← sonuç + dengeli_bitler
    ENDWHILE
    
    RETURN sonuç[0:adet]
END FONKSİYON
```

---

## 6. Şifreleme Algoritması

```
FONKSİYON Şifrele(mesaj, tohum):
    // RSÜ oluştur
    (lfsr, logistic) ← RSÜ_Oluştur(tohum)
    
    // Mesajı bitlere dönüştür
    mesaj_bitler ← []
    FOR her karakter c IN mesaj DO:
        byte_değer ← ASCII(c)
        FOR i ← 0 TO 7 DO:
            mesaj_bitler'e ((byte_değer >> i) AND 1) ekle
        ENDFOR
    ENDFOR
    
    // Anahtar üret
    anahtar_bitler ← DengeliBitÜret(lfsr, logistic, UZUNLUK(mesaj_bitler))
    
    // XOR şifreleme
    şifreli_bitler ← []
    FOR i ← 0 TO UZUNLUK(mesaj_bitler)-1 DO:
        şifreli_bitler'e (mesaj_bitler[i] XOR anahtar_bitler[i]) ekle
    ENDFOR
    
    // Hex formatına dönüştür
    şifreli_hex ← BitleriHexeDönüştür(şifreli_bitler)
    
    RETURN şifreli_hex
END FONKSİYON
```

---

## 7. Deşifreleme Algoritması

```
FONKSİYON Deşifrele(şifreli_hex, tohum):
    // RSÜ oluştur (aynı tohum)
    (lfsr, logistic) ← RSÜ_Oluştur(tohum)
    
    // Hex'i bitlere dönüştür
    şifreli_bitler ← HexiBitlereDönüştür(şifreli_hex)
    
    // Aynı anahtarı üret
    anahtar_bitler ← DengeliBitÜret(lfsr, logistic, UZUNLUK(şifreli_bitler))
    
    // XOR deşifreleme (XOR kendi tersi)
    çözülmüş_bitler ← []
    FOR i ← 0 TO UZUNLUK(şifreli_bitler)-1 DO:
        çözülmüş_bitler'e (şifreli_bitler[i] XOR anahtar_bitler[i]) ekle
    ENDFOR
    
    // Bitleri metne dönüştür
    mesaj ← BitleriMetineDönüştür(çözülmüş_bitler)
    
    RETURN mesaj
END FONKSİYON
```

---

## 8. Anahtar Üreteci

```
FONKSİYON AnahtarÜret(tohum, uzunluk):
    // uzunluk: byte cinsinden
    
    // RSÜ oluştur
    (lfsr, logistic) ← RSÜ_Oluştur(tohum)
    
    // Bit üret
    bitler ← DengeliBitÜret(lfsr, logistic, uzunluk × 8)
    
    // Byte'lara dönüştür
    anahtar ← []
    FOR i ← 0 TO uzunluk-1 STEP 8 DO:
        byte_değer ← 0
        FOR j ← 0 TO 7 DO:
            byte_değer ← byte_değer OR (bitler[i×8+j] << j)
        ENDFOR
        anahtar'a byte_değer ekle
    ENDFOR
    
    RETURN anahtar
END FONKSİYON
```
