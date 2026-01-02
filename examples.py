"""
Örnek Kullanım ve Çıktılar
==========================
Bu dosya, RSÜ algoritmasının kullanımını gösterir.

Yazar: [İsminizi Yazın]
Tarih: Ocak 2026
"""

from collatz_rsu import (
    CollatzGenerator, 
    FibonacciLFSR, 
    LogisticMap, 
    CollatzChaosRSU,
    encrypt,
    decrypt,
    VonNeumannExtractor
)


def example_collatz():
    """Collatz dizisi örneği."""
    print("\n" + "=" * 60)
    print("📊 ÖRNEK 1: COLLATZ DİZİSİ")
    print("=" * 60)
    
    seeds = [27, 12345, 7]
    
    for seed in seeds:
        collatz = CollatzGenerator(seed)
        sequence = collatz.generate_sequence()
        bits = collatz.get_bits()
        
        print(f"\n🌱 Tohum: {seed}")
        print(f"   Dizi uzunluğu: {len(sequence)} adım")
        print(f"   İlk 15 sayı: {sequence[:15]}")
        print(f"   Bit dizisi (ilk 30): {''.join(map(str, bits[:30]))}")
        print(f"   1 oranı: {sum(bits)/len(bits):.2%}")


def example_lfsr():
    """Fibonacci LFSR örneği."""
    print("\n" + "=" * 60)
    print("📊 ÖRNEK 2: FİBONACCI LFSR")
    print("=" * 60)
    
    seed = 0xACE1
    lfsr = FibonacciLFSR(seed)
    
    print(f"\n🌱 Tohum (hex): 0x{seed:04X}")
    print(f"   Başlangıç durumu (binary): {bin(seed)[2:].zfill(16)}")
    
    bits = lfsr.generate_bits(100)
    print(f"\n   Üretilen bitler (ilk 50):")
    print(f"   {''.join(map(str, bits[:50]))}")
    
    ones = sum(bits)
    print(f"\n   1 sayısı: {ones}/100 ({ones}%)")
    print(f"   0 sayısı: {100-ones}/100 ({100-ones}%)")


def example_logistic():
    """Logistic Map örneği."""
    print("\n" + "=" * 60)
    print("📊 ÖRNEK 3: LOGISTIC MAP")
    print("=" * 60)
    
    x0 = 0.3
    logistic = LogisticMap(x0)
    
    print(f"\n🌱 Başlangıç x₀: {x0}")
    print(f"   Kaotik parametre r: {LogisticMap.R}")
    
    # İlk 10 iterasyon değerleri
    print(f"\n   İlk 10 iterasyon:")
    logistic2 = LogisticMap(x0)
    for i in range(10):
        x = logistic2.step()
        bit = 1 if x >= 0.5 else 0
        print(f"   x{i+1} = {x:.6f} → bit = {bit}")
    
    # 100 bit üret
    logistic3 = LogisticMap(x0)
    bits = logistic3.generate_bits(100)
    print(f"\n   100 bit (ilk 50): {''.join(map(str, bits[:50]))}")
    
    ones = sum(bits)
    print(f"   1 oranı: {ones}%")


def example_von_neumann():
    """Von Neumann düzeltici örneği."""
    print("\n" + "=" * 60)
    print("📊 ÖRNEK 4: VON NEUMANN DÜZELTİCİ")
    print("=" * 60)
    
    # Bias'lı örnek dizi (%70 bir)
    biased = [1,1,0,1,1,1,0,0,1,1,1,0,1,0,1,1,1,1,0,1]
    print(f"\n   Giriş (bias'lı): {''.join(map(str, biased))}")
    print(f"   1 oranı: {sum(biased)/len(biased):.0%}")
    
    balanced = VonNeumannExtractor.extract(biased)
    print(f"\n   Çıkış (dengeli): {''.join(map(str, balanced))}")
    if balanced:
        print(f"   1 oranı: {sum(balanced)/len(balanced):.0%}")
    print(f"   Bit kaybı: {len(biased) - len(balanced)} bit")


def example_rsu():
    """Ana RSÜ örneği."""
    print("\n" + "=" * 60)
    print("📊 ÖRNEK 5: COLLATZ-CHAOS RSÜ")
    print("=" * 60)
    
    seed = 12345
    rsu = CollatzChaosRSU(seed)
    
    print(f"\n🌱 Ana tohum: {seed}")
    
    # 256 bit üret
    bits = rsu.generate_balanced_bits(256)
    print(f"\n   256 bit üretildi:")
    
    # 4 satırda göster
    for i in range(4):
        start = i * 64
        end = start + 64
        print(f"   [{start:3d}-{end:3d}]: {''.join(map(str, bits[start:end]))}")
    
    # İstatistikler
    stats = rsu.get_statistics()
    print(f"\n   📈 İstatistikler:")
    print(f"      Toplam bit: {stats['total_bits']}")
    print(f"      1'ler: {stats['ones']} ({stats['ones_ratio']:.2%})")
    print(f"      0'lar: {stats['zeros']} ({stats['zeros_ratio']:.2%})")
    print(f"      Denge sapması: {stats['balance']:.4f}")
    
    # Anahtar üret
    key = rsu.generate_key(16)
    print(f"\n   🔑 128-bit Anahtar (hex): {key}")


def example_encryption():
    """Şifreleme/Deşifreleme örneği."""
    print("\n" + "=" * 60)
    print("📊 ÖRNEK 6: ŞİFRELEME / DEŞİFRELEME")
    print("=" * 60)
    
    messages = [
        "Merhaba Dünya!",
        "RSÜ Algoritması",
        "Collatz + Fibonacci + Chaos = Güvenlik",
        "12345"
    ]
    
    seed = 27644437
    
    for msg in messages:
        print(f"\n{'─' * 50}")
        print(f"   📝 Mesaj: {msg}")
        print(f"   🌱 Tohum: {seed}")
        
        # Şifrele
        encrypted, key = encrypt(msg, seed)
        print(f"   🔒 Şifreli: {encrypted[:40]}..." if len(encrypted) > 40 else f"   🔒 Şifreli: {encrypted}")
        
        # Deşifrele
        decrypted = decrypt(encrypted, seed)
        print(f"   🔓 Çözülen: {decrypted}")
        
        # Doğrulama
        if msg == decrypted:
            print(f"   ✅ BAŞARILI!")
        else:
            print(f"   ❌ HATA!")


def example_different_seeds():
    """Farklı tohumlarla karşılaştırma."""
    print("\n" + "=" * 60)
    print("📊 ÖRNEK 7: FARKLI TOHUMLAR")
    print("=" * 60)
    
    seeds = [1, 100, 12345, 999999, 27644437]
    
    print(f"\n   {'Tohum':<12} | {'Collatz Adım':<12} | {'1 Oranı':<10} | {'İlk 32 Bit'}")
    print(f"   {'-'*12}-+-{'-'*12}-+-{'-'*10}-+-{'-'*32}")
    
    for seed in seeds:
        rsu = CollatzChaosRSU(seed)
        bits = rsu.generate_balanced_bits(256)
        
        collatz_steps = len(rsu.collatz.sequence)
        ones_ratio = sum(bits) / len(bits)
        first_bits = ''.join(map(str, bits[:32]))
        
        print(f"   {seed:<12} | {collatz_steps:<12} | {ones_ratio:<10.2%} | {first_bits}")


def example_key_generation():
    """Anahtar üretimi örnekleri."""
    print("\n" + "=" * 60)
    print("📊 ÖRNEK 8: ANAHTAR ÜRETİMİ")
    print("=" * 60)
    
    seed = 12345678
    rsu = CollatzChaosRSU(seed)
    
    print(f"\n🌱 Tohum: {seed}")
    print(f"\n   Farklı uzunluklarda anahtarlar:\n")
    
    lengths = [8, 16, 32, 64]
    names = ["64-bit", "128-bit", "256-bit", "512-bit"]
    
    for length, name in zip(lengths, names):
        # Her seferinde yeni RSÜ (aynı anahtar için)
        rsu = CollatzChaosRSU(seed)
        key = rsu.generate_key(length)
        print(f"   {name:>8}: {key}")


def main():
    """Tüm örnekleri çalıştır."""
    print("\n" + "🎯" * 30)
    print("  COLLATZ-FIBONACCI-CHAOS RSÜ - ÖRNEK ÇIKTILAR")
    print("🎯" * 30)
    
    example_collatz()
    example_lfsr()
    example_logistic()
    example_von_neumann()
    example_rsu()
    example_encryption()
    example_different_seeds()
    example_key_generation()
    
    print("\n\n" + "=" * 60)
    print("✅ Tüm örnekler başarıyla çalıştırıldı!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
