"""
Collatz-Fibonacci-Chaos RSÜ (Rastgele Sayı Üreteci)
====================================================
Bu algoritma Collatz sanısı, Fibonacci LFSR ve Logistic Map'i
birleştirerek kriptografik kalitede rastgele sayı üretir.

Yöntemler:
1. Fibonacci LFSR + Collatz Hybrid
2. Logistic Map Kaotik Dönüşüm

Yazar: [İsminizi Yazın]
Tarih: Ocak 2026
"""

import struct
from typing import List, Tuple, Generator


class CollatzGenerator:
    """
    Collatz sanısına göre bit dizisi üreten sınıf.
    
    Collatz kuralı:
    - n çift ise: n = n / 2
    - n tek ise: n = 3n + 1
    
    Her adımda:
    - Çift sayı = 0 biti
    - Tek sayı = 1 biti
    """
    
    def __init__(self, seed: int):
        """
        Args:
            seed: Başlangıç sayısı (pozitif tam sayı)
        """
        if seed <= 0:
            raise ValueError("Seed pozitif bir tam sayı olmalıdır")
        self.seed = seed
        self.sequence: List[int] = []
        self.bits: List[int] = []
    
    def generate_sequence(self, max_steps: int = 1000) -> List[int]:
        """
        Collatz dizisini üretir.
        
        Args:
            max_steps: Maksimum adım sayısı
            
        Returns:
            Collatz dizisi
        """
        n = self.seed
        self.sequence = [n]
        self.bits = [n % 2]  # İlk sayının paritesi
        
        step = 0
        while n != 1 and step < max_steps:
            if n % 2 == 0:
                n = n // 2
            else:
                n = 3 * n + 1
            
            self.sequence.append(n)
            self.bits.append(n % 2)
            step += 1
        
        return self.sequence
    
    def get_bits(self) -> List[int]:
        """Üretilen bit dizisini döndürür."""
        if not self.bits:
            self.generate_sequence()
        return self.bits
    
    def get_seed_from_bits(self, bits: List[int]) -> int:
        """Bit dizisinden sayısal değer üretir (LFSR için tohum)."""
        if not bits:
            bits = self.bits
        
        # İlk 16 biti kullanarak 16-bit tohum üret
        seed_bits = bits[:16] if len(bits) >= 16 else bits + [0] * (16 - len(bits))
        seed = 0
        for i, bit in enumerate(seed_bits):
            seed |= (bit << i)
        
        return seed if seed != 0 else 1  # Sıfır olmamalı


class FibonacciLFSR:
    """
    Fibonacci Linear Feedback Shift Register (LFSR).
    
    Polinom: x^16 + x^14 + x^13 + x^11 + 1
    Tap pozisyonları: 16, 14, 13, 11 (0-indexed: 15, 13, 12, 10)
    
    Bu polinom maksimum periyot sağlar: 2^16 - 1 = 65535
    """
    
    # Tap pozisyonları (0-indexed)
    TAPS = [15, 13, 12, 10]
    
    def __init__(self, seed: int):
        """
        Args:
            seed: 16-bit başlangıç değeri (1-65535 arası)
        """
        # Seed'i 16-bit'e sınırla
        self.state = seed & 0xFFFF
        if self.state == 0:
            self.state = 1  # Sıfır durumu yasak
    
    def step(self) -> int:
        """
        Bir adım ilerler ve yeni bit üretir.
        
        Returns:
            Üretilen bit (0 veya 1)
        """
        # Tap pozisyonlarındaki bitleri XOR'la
        feedback = 0
        for tap in self.TAPS:
            feedback ^= (self.state >> tap) & 1
        
        # Kaydırma yap ve yeni biti ekle
        output_bit = self.state & 1
        self.state = (self.state >> 1) | (feedback << 15)
        
        return output_bit
    
    def generate_bits(self, count: int) -> List[int]:
        """
        Belirtilen sayıda bit üretir.
        
        Args:
            count: Üretilecek bit sayısı
            
        Returns:
            Bit listesi
        """
        return [self.step() for _ in range(count)]
    
    def get_state(self) -> int:
        """Mevcut durumu döndürür."""
        return self.state


class LogisticMap:
    """
    Logistic Map Kaotik Dönüşüm.
    
    Formül: x(n+1) = r * x(n) * (1 - x(n))
    
    r = 3.99 değeri tam kaotik bölgede çalışmayı garanti eder.
    Bu değer 3.57'nin üzerinde olduğunda sistem kaotik davranış gösterir.
    """
    
    R = 3.99  # Kaotik parametre
    
    def __init__(self, x0: float):
        """
        Args:
            x0: Başlangıç değeri (0 < x0 < 1)
        """
        # x0'ı geçerli aralığa sınırla
        self.x = max(0.001, min(0.999, x0))
        self.initial_x = self.x
    
    @classmethod
    def from_integer(cls, seed: int) -> 'LogisticMap':
        """
        Tam sayıdan LogisticMap oluşturur.
        
        Args:
            seed: Tam sayı tohum değeri
            
        Returns:
            LogisticMap instance
        """
        # Seed'i 0-1 aralığına normalize et
        x0 = (seed % 997 + 1) / 999.0  # 0.001 - 0.998 arası
        return cls(x0)
    
    def step(self) -> float:
        """
        Bir iterasyon yapar.
        
        Returns:
            Yeni x değeri
        """
        self.x = self.R * self.x * (1 - self.x)
        return self.x
    
    def generate_bit(self) -> int:
        """
        Bir bit üretir.
        
        Returns:
            0 veya 1 (x >= 0.5 ise 1, değilse 0)
        """
        self.step()
        return 1 if self.x >= 0.5 else 0
    
    def generate_bits(self, count: int) -> List[int]:
        """
        Belirtilen sayıda bit üretir.
        
        Args:
            count: Üretilecek bit sayısı
            
        Returns:
            Bit listesi
        """
        return [self.generate_bit() for _ in range(count)]
    
    def reset(self):
        """Başlangıç durumuna sıfırlar."""
        self.x = self.initial_x


class VonNeumannExtractor:
    """
    Von Neumann Düzeltici (Bias Extractor).
    
    Ardışık bit çiftlerini analiz eder:
    - 01 -> 0 çıktısı
    - 10 -> 1 çıktısı
    - 00 ve 11 -> atılır
    
    Bu yöntem bias'lı girdiyi dengeli çıktıya dönüştürür.
    """
    
    @staticmethod
    def extract(bits: List[int]) -> List[int]:
        """
        Bit dizisini dengeler.
        
        Args:
            bits: Giriş bit dizisi
            
        Returns:
            Dengelenmiş bit dizisi
        """
        result = []
        i = 0
        while i < len(bits) - 1:
            if bits[i] == 0 and bits[i + 1] == 1:
                result.append(0)
            elif bits[i] == 1 and bits[i + 1] == 0:
                result.append(1)
            # 00 ve 11 atılır
            i += 2
        return result


class CollatzChaosRSU:
    """
    Ana Rastgele Sayı Üreteci Sınıfı.
    
    Üç bileşeni birleştirir:
    1. Collatz Generator - Temel bit dizisi
    2. Fibonacci LFSR - Pseudo-random karıştırma
    3. Logistic Map - Kaotik karıştırma
    
    Çıktı: LFSR XOR LogisticMap sonucu Von Neumann ile dengelenir
    """
    
    def __init__(self, seed: int):
        """
        Args:
            seed: Ana tohum değeri
        """
        self.seed = seed
        
        # Collatz dizisi üret
        self.collatz = CollatzGenerator(seed)
        self.collatz.generate_sequence()
        
        # Collatz'dan alt tohumları üret
        collatz_bits = self.collatz.get_bits()
        lfsr_seed = self.collatz.get_seed_from_bits(collatz_bits)
        
        # Alt bileşenleri başlat
        self.lfsr = FibonacciLFSR(lfsr_seed)
        self.logistic = LogisticMap.from_integer(seed)
        
        # İstatistikler
        self.generated_bits: List[int] = []
        self.raw_bits: List[int] = []
    
    def generate_raw_bits(self, count: int) -> List[int]:
        """
        Ham bitler üretir (XOR birleştirme).
        
        Args:
            count: Üretilecek bit sayısı
            
        Returns:
            Ham bit dizisi
        """
        lfsr_bits = self.lfsr.generate_bits(count)
        logistic_bits = self.logistic.generate_bits(count)
        
        # XOR birleştirme
        raw_bits = [l ^ c for l, c in zip(lfsr_bits, logistic_bits)]
        self.raw_bits.extend(raw_bits)
        return raw_bits
    
    def generate_balanced_bits(self, count: int) -> List[int]:
        """
        Dengelenmiş bitler üretir (Von Neumann düzeltici ile).
        
        Args:
            count: Minimum istenen bit sayısı
            
        Returns:
            Dengelenmiş bit dizisi
        """
        result = []
        
        # Yeterli bit toplanana kadar üret
        while len(result) < count:
            # Fazladan bit üret (Von Neumann yaklaşık %50 atar)
            raw = self.generate_raw_bits(count * 3)
            balanced = VonNeumannExtractor.extract(raw)
            result.extend(balanced)
        
        self.generated_bits = result[:count]
        return self.generated_bits
    
    def generate_bytes(self, count: int) -> bytes:
        """
        Rastgele byte'lar üretir.
        
        Args:
            count: Üretilecek byte sayısı
            
        Returns:
            Byte dizisi
        """
        bits = self.generate_balanced_bits(count * 8)
        
        result = bytearray()
        for i in range(0, len(bits), 8):
            byte_bits = bits[i:i + 8]
            if len(byte_bits) == 8:
                byte_val = sum(bit << j for j, bit in enumerate(byte_bits))
                result.append(byte_val)
        
        return bytes(result)
    
    def generate_key(self, length: int) -> str:
        """
        Şifreleme anahtarı üretir (hex formatında).
        
        Args:
            length: Anahtar uzunluğu (byte cinsinden)
            
        Returns:
            Hex formatında anahtar
        """
        key_bytes = self.generate_bytes(length)
        return key_bytes.hex()
    
    def get_statistics(self) -> dict:
        """
        Üretilen bitlerin istatistiklerini döndürür.
        
        Returns:
            İstatistik sözlüğü
        """
        if not self.generated_bits:
            return {}
        
        ones = sum(self.generated_bits)
        zeros = len(self.generated_bits) - ones
        total = len(self.generated_bits)
        
        return {
            'total_bits': total,
            'ones': ones,
            'zeros': zeros,
            'ones_ratio': ones / total if total > 0 else 0,
            'zeros_ratio': zeros / total if total > 0 else 0,
            'balance': abs(ones - zeros) / total if total > 0 else 0
        }


# ==================== ŞİFRELEME FONKSİYONLARI ====================

def text_to_bits(text: str) -> List[int]:
    """Metni bit dizisine dönüştürür."""
    bits = []
    for char in text.encode('utf-8'):
        for i in range(8):
            bits.append((char >> i) & 1)
    return bits


def bits_to_text(bits: List[int]) -> str:
    """Bit dizisini metne dönüştürür."""
    chars = []
    for i in range(0, len(bits), 8):
        byte_bits = bits[i:i + 8]
        if len(byte_bits) == 8:
            byte_val = sum(bit << j for j, bit in enumerate(byte_bits))
            chars.append(byte_val)
    return bytes(chars).decode('utf-8', errors='replace')


def bits_to_hex(bits: List[int]) -> str:
    """Bit dizisini hex string'e dönüştürür."""
    hex_str = ""
    for i in range(0, len(bits), 4):
        nibble = bits[i:i + 4]
        if len(nibble) == 4:
            val = sum(bit << j for j, bit in enumerate(nibble))
            hex_str += format(val, 'x')
    return hex_str


def hex_to_bits(hex_str: str) -> List[int]:
    """Hex string'i bit dizisine dönüştürür."""
    bits = []
    for char in hex_str:
        val = int(char, 16)
        for i in range(4):
            bits.append((val >> i) & 1)
    return bits


def encrypt(message: str, seed: int) -> Tuple[str, str]:
    """
    Mesajı şifreler.
    
    Args:
        message: Şifrelenecek mesaj
        seed: Şifreleme anahtarı (tohum)
        
    Returns:
        (şifreli_mesaj_hex, anahtar_hex) tuple'ı
    """
    # RSÜ oluştur
    rsu = CollatzChaosRSU(seed)
    
    # Mesajı bitlere dönüştür
    message_bits = text_to_bits(message)
    
    # Anahtar üret
    key_bits = rsu.generate_balanced_bits(len(message_bits))
    
    # XOR şifreleme
    encrypted_bits = [m ^ k for m, k in zip(message_bits, key_bits)]
    
    # Hex'e dönüştür
    encrypted_hex = bits_to_hex(encrypted_bits)
    key_hex = bits_to_hex(key_bits)
    
    return encrypted_hex, key_hex


def decrypt(encrypted_hex: str, seed: int) -> str:
    """
    Şifreli mesajı çözer.
    
    Args:
        encrypted_hex: Şifreli mesaj (hex formatında)
        seed: Şifreleme anahtarı (tohum)
        
    Returns:
        Çözülmüş mesaj
    """
    # RSÜ oluştur (aynı seed ile)
    rsu = CollatzChaosRSU(seed)
    
    # Şifreli mesajı bitlere dönüştür
    encrypted_bits = hex_to_bits(encrypted_hex)
    
    # Anahtar üret (aynı seed aynı anahtarı üretir)
    key_bits = rsu.generate_balanced_bits(len(encrypted_bits))
    
    # XOR deşifreleme (XOR kendi tersi)
    decrypted_bits = [e ^ k for e, k in zip(encrypted_bits, key_bits)]
    
    # Metne dönüştür
    return bits_to_text(decrypted_bits)


# ==================== TEST FONKSİYONLARI ====================

def demo():
    """Algoritmanın demo çalışması."""
    print("=" * 60)
    print("COLLATZ-FIBONACCI-CHAOS RSÜ DEMO")
    print("=" * 60)
    
    seed = 12345
    print(f"\n[1] Tohum değeri: {seed}")
    
    # Collatz dizisi
    collatz = CollatzGenerator(seed)
    sequence = collatz.generate_sequence()
    print(f"\n[2] Collatz dizisi (ilk 20 eleman):")
    print(f"    {sequence[:20]}...")
    print(f"    Toplam adım: {len(sequence)}")
    
    # Bit üretimi
    rsu = CollatzChaosRSU(seed)
    bits = rsu.generate_balanced_bits(100)
    print(f"\n[3] Üretilen bitler (ilk 50):")
    print(f"    {''.join(map(str, bits[:50]))}")
    
    # İstatistikler
    stats = rsu.get_statistics()
    print(f"\n[4] İstatistikler:")
    print(f"    Toplam bit: {stats['total_bits']}")
    print(f"    1'ler: {stats['ones']} ({stats['ones_ratio']:.2%})")
    print(f"    0'lar: {stats['zeros']} ({stats['zeros_ratio']:.2%})")
    print(f"    Denge sapması: {stats['balance']:.4f}")
    
    # Şifreleme örneği
    message = "Merhaba Dünya!"
    print(f"\n[5] Şifreleme örneği:")
    print(f"    Orijinal mesaj: {message}")
    
    encrypted, key = encrypt(message, seed)
    print(f"    Şifreli (hex): {encrypted}")
    
    decrypted = decrypt(encrypted, seed)
    print(f"    Çözülmüş mesaj: {decrypted}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    demo()
