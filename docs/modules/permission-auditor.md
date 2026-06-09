# İzin Denetçisi Modülü

## Amaç
APK'dan AndroidManifest.xml'i ayrıştırır, izinleri sınıflandırır
ve risk raporu üretir.

## Nasıl Çalışır
1. androguard ile izinler çıkarılır (birincil)
2. apktool ile çapraz doğrulama yapılır
3. permission_db.json ile her izin seviye/ağırlık alır
4. Toplam puan hesaplanır, bant belirlenir
5. Tehlikeli kombinasyonlar kontrol edilir
6. .md ve .json rapor dosyaları üretilir

## Kullanım
```bash
docker compose run --rm auditor --apk apks/ornek.apk --output reports/
python src/main.py --apk apks/ornek.apk --output reports/
```

## 3 Örnek Uygulama Karşılaştırması
| Uygulama | Paket | Kaynak | Toplam Puan | Bant | Tehlikeli | Normal | Kombinasyon |
|----------|-------|--------|-------------|------|-----------|--------|-------------|
| Fossify Clock | org.fossify.clock | F-Droid | 28 | Orta | 1 | 8 | 0 |
| Organic Maps  | app.organicmaps   | F-Droid | 30 | Orta | 3 | 7 | 1 |
| Element       | im.vector.app     | F-Droid | 88 | Yüksek | 8 | 9 | 4 |

> **Analiz Notu:** Fossify Clock uygulamasının beklendiği gibi "Düşük" bant çıkması umuluyordu; ancak güncel AndroidManifest analizi sonucunda **28 puan** alarak "Orta" banta yerleşmiştir. Bunun nedeni uygulamanın Android 13+ ile zorunlu hale gelen `POST_NOTIFICATIONS` (5 puan) tehlikeli iznini içermesi ve ayrıca veritabanında bilinmeyen olarak değerlendirilen `USE_FULL_SCREEN_INTENT`, `FOREGROUND_SERVICE_SPECIAL_USE`, `DISABLE_KEYGUARD` (toplam 3x4 = 12 puan) gibi izinler talep etmesidir. Düşük eşiğinin (20) aşılması bu yeni gereksinimlerden kaynaklanmaktadır.

## Bilinen Kısıtlamalar
- permission_db.json'da olmayan izinler "unknown" olarak işlenir
- apktool kurulu değilse çapraz doğrulama atlanır
- Yalnızca manifest'teki beyan edilen izinler analiz edilir;
  çalışma zamanında dinamik yüklenen izinler kapsam dışıdır
