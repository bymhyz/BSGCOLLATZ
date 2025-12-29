import java.util.Scanner;

public class Collatz {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.println("--- Collatz Algoritması Hesaplayıcı ---");

        while (true) {
            System.out.print("\nLütfen bir sayı giriniz (Çıkmak için 'q' basın): ");
            String giris = scanner.next();

            if (giris.equalsIgnoreCase("q")) {
                System.out.println("Sistemden çıkış yapılıyor. İyi günler!");
                break; 
            }

            try {
                long sayi = Long.parseLong(giris);

                if (sayi <= 0) {
                    System.out.println("HATA: Lütfen pozitif bir tam sayı giriniz!");
                } 
                else {
                    System.out.print("Sonuç: " + sayi);
                    
                    while (sayi > 1) {
                        if (sayi % 2 == 0) {
                            sayi = sayi / 2;
                        } else {
                            sayi = (3 * sayi) + 1;
                        }
                        System.out.print(" -> " + sayi);
                    }
                    System.out.println(); 
                }

            } catch (NumberFormatException e) {
                System.out.println("HATA: Lütfen geçerli bir sayı giriniz veya 'q' ile çıkınız.");
            }
        }
        
        scanner.close();
    }
}