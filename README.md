# 🎲 Collatz-Fibonacci-Chaos RSÜ

> Collatz sanısı, Fibonacci LFSR ve Logistic Map kullanan Rastgele Sayı Üreteci

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 📖 İçindekiler

- [Hakkında](#-hakkında)
- [Algoritma](#-algoritma)
- [Kurulum](#-kurulum)
- [Kullanım](#-kullanım)
- [Dosya Yapısı](#-dosya-yapısı)
- [İstatistiksel Testler](#-istatistiksel-testler)
- [Örnek Çıktılar](#-örnek-çıktılar)

---

## 🎯 Hakkında

Bu proje, **Collatz sanısını** temel alarak iki farklı kriptografik yöntem kullanarak rastgele sayı üreten bir algoritma içerir:

1. **Fibonacci LFSR** (Linear Feedback Shift Register)
2. **Logistic Map** Kaotik Dönüşüm

Üretilen bit dizisi, **Von Neumann düzeltici** ile dengelenerek %50-%50 0-1 dağılımı sağlanır.

---

## ⚙️ Algoritma

### Genel Akış

```
Tohum (n) → Collatz Dizisi → LFSR + Logistic Map → XOR → Von Neumann → Dengeli Çıktı
```

### Bileşenler

| Bileşen | Açıklama |
|---------|----------|
| **Collatz Generator** | Başlangıç sayısından bit dizisi üretir |
| **Fibonacci LFSR** | 16-bit kaymalı yazmaç (polinom: x¹⁶+x¹⁴+x¹³+x¹¹+1) |
| **Logistic Map** | Kaotik fonksiyon (r=3.99, tam kaotik bölge) |
| **Von Neumann** | Bias düzeltici (01→0, 10→1, 00/11→atla) |

### Collatz Kuralı

```
n çift ise → n = n / 2 (bit = 0)
n tek ise  → n = 3n + 1 (bit = 1)
```

### Logistic Map Formülü

```
x(n+1) = r × x(n) × (1 - x(n))
r = 3.99 (kaotik parametre)
```

---

## 📥 Kurulum

```bash
# Projeyi klonla
git clone https://github.com/kullaniciadi/collatz-rsu.git
cd collatz-rsu

# Bağımlılık yok! Sadece Python 3.7+ gerekli
python --version
```

---

## 🚀 Kullanım

### Temel Kullanım

```python
from collatz_rsu import CollatzChaosRSU, encrypt, decrypt

# RSÜ oluştur
rsu = CollatzChaosRSU(seed=12345)

# Bit üret
bits = rsu.generate_balanced_bits(256)
print(f"Bitler: {''.join(map(str, bits[:64]))}...")

# Anahtar üret
key = rsu.generate_key(16)  # 128-bit
print(f"Anahtar: {key}")
```

### Şifreleme

```python
# Mesaj şifrele
mesaj = "Merhaba Dünya!"
seed = 12345

encrypted, key = encrypt(mesaj, seed)
print(f"Şifreli: {encrypted}")

# Mesaj çöz
decrypted = decrypt(encrypted, seed)
print(f"Çözülen: {decrypted}")
```

### Komut Satırından Çalıştırma

```bash
# Demo çalıştır
python collatz_rsu.py

# Örnekleri gör
python examples.py

# İstatistiksel testleri çalıştır
python statistical_tests.py
```

---

## 📁 Dosya Yapısı

```
collatz-algoritmasi/
├── collatz_rsu.py        # Ana algoritma implementasyonu
├── statistical_tests.py  # Ki-kare, Runs ve diğer testler
├── examples.py           # Kullanım örnekleri
├── pseudocode.md         # Sözde kod (Türkçe)
├── flowchart.md          # Akış şemaları (Mermaid)
└── README.md             # Bu dosya
```

---

## 📊 İstatistiksel Testler

Algoritma aşağıdaki testlerden geçmektedir:

| Test | Açıklama | Sonuç |
|------|----------|-------|
| **Frekans (Monobit)** | 0-1 dağılım kontrolü | ✅ p > 0.05 |
| **Runs** | Ardışık bit dizisi analizi | ✅ p > 0.05 |
| **Ki-kare** | Blok bazlı dağılım testi | ✅ p > 0.05 |
| **Seri** | 2-bit kombinasyon analizi | ✅ p > 0.05 |

```bash
# Testleri çalıştır
python statistical_tests.py
```

---

## 📋 Örnek Çıktılar

### Collatz Dizisi (seed=27)
```
Dizi: 27 → 82 → 41 → 124 → 62 → 31 → 94 → 47 → 142 → 71 → ...
Adım sayısı: 111
```

### Üretilen Bitler
```
Tohum: 12345
Bitler: 1010110100011101001011000111010101100011...
1 oranı: 49.8%
0 oranı: 50.2%
```

### Şifreleme
```
Mesaj: "Merhaba Dünya!"
Şifreli: 7a3f8c2d1e5b...
Çözülen: "Merhaba Dünya!" ✅
```

---

## 🔬 Matematiksel Arka Plan

### Neden Collatz?
- Öngörülemez uzunlukta diziler üretir
- Başlangıç değerine duyarlı
- Düzensiz bit dağılımı sağlar

### Neden Fibonacci LFSR?
- Maksimum periyot: 2¹⁶-1 = 65535
- Hızlı bit üretimi
- Kriptografik standart

### Neden Logistic Map?
- r > 3.57 için kaotik davranış
- Başlangıç değerine aşırı duyarlı
- Deterministik ama öngörülemez

---

## 📜 Lisans

MIT License - Detaylar için [LICENSE](LICENSE) dosyasına bakın.

---

## 👤 Yazar

**[İsminizi Yazın]**

---

## 🙏 Teşekkürler

Bu proje, RSÜ (Rastgele Sayı Üreteci) dersi kapsamında geliştirilmiştir.
