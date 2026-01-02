"""
İstatistiksel Testler
=====================
Bu modül, RSÜ algoritmasının rastgelelik kalitesini test eder.

Testler:
1. Ki-kare (Chi-square) testi
2. Runs testi (ardışık bit analizi)
3. Frekans testi (0-1 dağılımı)
4. Monobit testi

Yazar: [İsminizi Yazın]
Tarih: Ocak 2026
"""

import math
from typing import List, Dict, Tuple
from collatz_rsu import CollatzChaosRSU


def frequency_test(bits: List[int]) -> Dict:
    """
    Frekans Testi (Monobit Testi).
    
    0 ve 1 sayılarının eşit dağılıp dağılmadığını kontrol eder.
    
    H0: Bitler rastgele dağılmış (p=0.5)
    H1: Bitler rastgele dağılmamış
    
    Args:
        bits: Test edilecek bit dizisi
        
    Returns:
        Test sonuçları sözlüğü
    """
    n = len(bits)
    if n == 0:
        return {'error': 'Boş bit dizisi'}
    
    # 1'lerin sayısı
    ones = sum(bits)
    zeros = n - ones
    
    # Beklenen değerler (p=0.5 için)
    expected = n / 2
    
    # Ki-kare istatistiği (1 serbestlik derecesi)
    chi_square = ((ones - expected) ** 2 / expected) + ((zeros - expected) ** 2 / expected)
    
    # p-değeri hesaplama (chi-square dağılımı, df=1)
    # Basitleştirilmiş yaklaşım
    p_value = math.exp(-chi_square / 2)
    
    # Karar (α = 0.05)
    is_random = p_value > 0.05
    
    return {
        'test_adı': 'Frekans (Monobit) Testi',
        'toplam_bit': n,
        'birler': ones,
        'sıfırlar': zeros,
        'bir_oranı': ones / n,
        'sıfır_oranı': zeros / n,
        'beklenen': expected,
        'ki_kare': chi_square,
        'p_değeri': p_value,
        'rastgele_mi': is_random,
        'sonuç': '✅ BAŞARILI - Rastgele dağılım' if is_random else '❌ BAŞARISIZ - Rastgele değil'
    }


def runs_test(bits: List[int]) -> Dict:
    """
    Runs Testi.
    
    Ardışık aynı bit dizilerini (runs) analiz eder.
    Rastgele bir dizide belirli sayıda run beklenir.
    
    Args:
        bits: Test edilecek bit dizisi
        
    Returns:
        Test sonuçları sözlüğü
    """
    n = len(bits)
    if n < 2:
        return {'error': 'Yetersiz bit sayısı'}
    
    # Run sayısını hesapla
    runs = 1
    for i in range(1, n):
        if bits[i] != bits[i - 1]:
            runs += 1
    
    # 1'lerin ve 0'ların sayısı
    n1 = sum(bits)
    n0 = n - n1
    
    if n0 == 0 or n1 == 0:
        return {'error': 'Tüm bitler aynı'}
    
    # Beklenen run sayısı ve standart sapma
    expected_runs = (2 * n0 * n1) / n + 1
    variance = (2 * n0 * n1 * (2 * n0 * n1 - n)) / (n * n * (n - 1))
    std_dev = math.sqrt(variance) if variance > 0 else 1
    
    # Z-skoru
    z_score = (runs - expected_runs) / std_dev if std_dev > 0 else 0
    
    # p-değeri (iki kuyruklu test, normal dağılım yaklaşımı)
    p_value = 2 * (1 - normal_cdf(abs(z_score)))
    
    # Karar (α = 0.05)
    is_random = p_value > 0.05
    
    return {
        'test_adı': 'Runs Testi',
        'toplam_bit': n,
        'run_sayısı': runs,
        'beklenen_run': expected_runs,
        'standart_sapma': std_dev,
        'z_skoru': z_score,
        'p_değeri': p_value,
        'rastgele_mi': is_random,
        'sonuç': '✅ BAŞARILI - Rastgele dağılım' if is_random else '❌ BAŞARISIZ - Rastgele değil'
    }


def chi_square_test(bits: List[int], block_size: int = 8) -> Dict:
    """
    Ki-kare Testi (Blok bazlı).
    
    Bit dizisini bloklara böler ve her bloğun frekansını analiz eder.
    
    Args:
        bits: Test edilecek bit dizisi
        block_size: Blok boyutu
        
    Returns:
        Test sonuçları sözlüğü
    """
    n = len(bits)
    if n < block_size:
        return {'error': 'Yetersiz bit sayısı'}
    
    # Blokları oluştur
    num_blocks = n // block_size
    blocks = []
    for i in range(num_blocks):
        block = bits[i * block_size:(i + 1) * block_size]
        blocks.append(sum(block))  # Her bloktaki 1 sayısı
    
    # Frekans dağılımı (0'dan block_size'a kadar)
    freq = [0] * (block_size + 1)
    for count in blocks:
        freq[count] += 1
    
    # Beklenen frekanslar (binom dağılımı)
    expected_freq = []
    for k in range(block_size + 1):
        # P(X=k) = C(n,k) * 0.5^n
        prob = math.comb(block_size, k) * (0.5 ** block_size)
        expected_freq.append(prob * num_blocks)
    
    # Ki-kare istatistiği
    chi_square = 0
    for observed, expected in zip(freq, expected_freq):
        if expected > 0:
            chi_square += ((observed - expected) ** 2) / expected
    
    # Serbestlik derecesi
    df = block_size  # block_size + 1 - 1
    
    # p-değeri (basitleştirilmiş)
    p_value = chi_square_p_value(chi_square, df)
    
    # Karar (α = 0.05)
    is_random = p_value > 0.05
    
    return {
        'test_adı': 'Ki-kare Testi (Blok)',
        'toplam_bit': n,
        'blok_boyutu': block_size,
        'blok_sayısı': num_blocks,
        'ki_kare': chi_square,
        'serbestlik_derecesi': df,
        'p_değeri': p_value,
        'rastgele_mi': is_random,
        'sonuç': '✅ BAŞARILI - Rastgele dağılım' if is_random else '❌ BAŞARISIZ - Rastgele değil'
    }


def serial_test(bits: List[int]) -> Dict:
    """
    Seri (Serial) Testi.
    
    2-bit kombinasyonların frekansını analiz eder: 00, 01, 10, 11
    
    Args:
        bits: Test edilecek bit dizisi
        
    Returns:
        Test sonuçları sözlüğü
    """
    n = len(bits)
    if n < 2:
        return {'error': 'Yetersiz bit sayısı'}
    
    # 2-bit kombinasyon sayıları
    pairs = {'00': 0, '01': 0, '10': 0, '11': 0}
    
    for i in range(n - 1):
        pair = str(bits[i]) + str(bits[i + 1])
        pairs[pair] += 1
    
    # Toplam çift sayısı
    total_pairs = n - 1
    
    # Beklenen değer (her biri eşit olasılıklı)
    expected = total_pairs / 4
    
    # Ki-kare istatistiği
    chi_square = sum(((count - expected) ** 2) / expected for count in pairs.values())
    
    # p-değeri (df = 3)
    p_value = chi_square_p_value(chi_square, 3)
    
    # Karar (α = 0.05)
    is_random = p_value > 0.05
    
    return {
        'test_adı': 'Seri (Serial) Testi',
        'toplam_bit': n,
        'çift_sayısı': total_pairs,
        'dağılım': pairs,
        'beklenen': expected,
        'ki_kare': chi_square,
        'p_değeri': p_value,
        'rastgele_mi': is_random,
        'sonuç': '✅ BAŞARILI - Rastgele dağılım' if is_random else '❌ BAŞARISIZ - Rastgele değil'
    }


def normal_cdf(x: float) -> float:
    """Normal dağılım kümülatif fonksiyonu (yaklaşık)."""
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def chi_square_p_value(chi_sq: float, df: int) -> float:
    """
    Ki-kare p-değeri hesaplama (basitleştirilmiş).
    Gamma fonksiyonu kullanarak yaklaşık değer.
    """
    if chi_sq <= 0:
        return 1.0
    
    # Basit yaklaşım: üstel azalma
    # Gerçek uygulamada scipy.stats.chi2.sf kullanılmalı
    try:
        k = df / 2
        x = chi_sq / 2
        
        # Incomplete gamma function yaklaşımı
        if x < k + 1:
            # Seri açılımı
            sum_val = 0
            term = 1 / k
            for n in range(1, 100):
                term *= x / (k + n)
                sum_val += term
                if term < 1e-10:
                    break
            p = math.exp(-x + k * math.log(x) - math.lgamma(k + 1)) * (1 + sum_val)
            return 1 - p
        else:
            # Büyük x için yaklaşım
            return math.exp(-chi_sq / (2 * df)) if df > 0 else 0
    except:
        return 0.5


def run_all_tests(bits: List[int]) -> Dict:
    """
    Tüm testleri çalıştırır.
    
    Args:
        bits: Test edilecek bit dizisi
        
    Returns:
        Tüm test sonuçları
    """
    results = {
        'frekans': frequency_test(bits),
        'runs': runs_test(bits),
        'ki_kare': chi_square_test(bits),
        'seri': serial_test(bits)
    }
    
    # Genel değerlendirme
    passed = sum(1 for r in results.values() if r.get('rastgele_mi', False))
    total = len(results)
    
    results['özet'] = {
        'geçen_test': passed,
        'toplam_test': total,
        'başarı_oranı': passed / total,
        'genel_sonuç': '✅ BAŞARILI' if passed >= 3 else '⚠️ KISMEN BAŞARILI' if passed >= 2 else '❌ BAŞARISIZ'
    }
    
    return results


def print_results(results: Dict):
    """Test sonuçlarını güzel formatla yazdırır."""
    print("\n" + "=" * 70)
    print("📊 İSTATİSTİKSEL TEST SONUÇLARI")
    print("=" * 70)
    
    for test_name, test_result in results.items():
        if test_name == 'özet':
            continue
            
        print(f"\n📌 {test_result.get('test_adı', test_name)}")
        print("-" * 50)
        
        for key, value in test_result.items():
            if key in ['test_adı', 'sonuç']:
                continue
            if isinstance(value, float):
                print(f"   {key}: {value:.6f}")
            else:
                print(f"   {key}: {value}")
        
        print(f"\n   → {test_result.get('sonuç', 'N/A')}")
    
    # Özet
    ozet = results.get('özet', {})
    print("\n" + "=" * 70)
    print("📋 GENEL ÖZET")
    print("=" * 70)
    print(f"   Geçen test sayısı: {ozet.get('geçen_test', 0)}/{ozet.get('toplam_test', 0)}")
    print(f"   Başarı oranı: {ozet.get('başarı_oranı', 0):.1%}")
    print(f"\n   {ozet.get('genel_sonuç', 'N/A')}")
    print("=" * 70)


def main():
    """Ana test fonksiyonu."""
    print("\n🔬 Collatz-Fibonacci-Chaos RSÜ İstatistiksel Test")
    print("=" * 70)
    
    # Farklı tohumlarla test
    seeds = [12345, 27644437, 100000007, 999999937]
    bit_count = 10000
    
    for seed in seeds:
        print(f"\n\n{'*' * 70}")
        print(f"🌱 TOHUM: {seed}")
        print(f"{'*' * 70}")
        
        # RSÜ oluştur ve bit üret
        rsu = CollatzChaosRSU(seed)
        bits = rsu.generate_balanced_bits(bit_count)
        
        print(f"   Üretilen bit sayısı: {len(bits)}")
        
        # Testleri çalıştır
        results = run_all_tests(bits)
        print_results(results)
    
    print("\n\n✅ Tüm testler tamamlandı!")


if __name__ == "__main__":
    main()
