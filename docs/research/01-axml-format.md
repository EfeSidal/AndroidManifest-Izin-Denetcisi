# Android Binary XML (AXML) Formatı

## AndroidManifest.xml Neden Düz Metin Değildir?

Bir Android uygulamasının kaynak kodunda `AndroidManifest.xml` dosyası okunabilir, düz metin
XML formatındadır. Ancak uygulama derlenip APK haline getirildiğinde bu dosya **Android Binary
XML (AXML)** adı verilen özel bir ikili (binary) formata dönüştürülür. APK içindeki
`AndroidManifest.xml`'i bir metin editörüyle açarsanız anlamsız baytlar görürsünüz; çünkü artık
düz metin değildir.

## AXML Nedir?

AXML, Android'in kaynak dosyalarını (layout XML'leri, string tanımları ve manifest dahil)
paketlemek için kullandığı kompakt, ikili kodlanmış bir XML temsilidir. Bu format Android işletim
sistemi tarafından doğrudan okunabilecek şekilde tasarlanmıştır.

AXML dosyasının temel yapısı şöyledir:

- **String Pool (Dize Havuzu):** Dosyada kullanılan tüm metin dizeleri (etiket adları, öznitelik
  değerleri vb.) tek bir havuzda toplanır ve dosyanın geri kalanında indeks numaralarıyla
  referans verilir.
- **Resource ID Table:** `android:name`, `android:label` gibi özniteliklerin karşılık geldiği
  sayısal kaynak kimliklerini (ör. `0x7f040001`) tutar.
- **XML Ağaç Yapısı:** Etiketlerin açılış/kapanış bilgileri, öznitelikler ve ad alanları ikili
  olarak kodlanır.

## Derleme Sırasında Neden İkili Formata Çevrilir?

Bu dönüşümün üç temel nedeni vardır:

1. **Performans:** Mobil cihazlar sınırlı işlemci ve bellek kaynaklarına sahiptir. Düz metin XML
   parse etmek, karakter karakter okuma ve dize karşılaştırma gerektirdiğinden yavaştır. AXML
   formatı ise önceden dizinlenmiş bir yapıya sahip olduğundan Android çalışma zamanı tarafından
   çok daha hızlı okunur.

2. **Dosya Boyutu:** İkili formatta tekrar eden dizeler tek bir havuzda tutulur ve indekslerle
   referans verilir. Bu, düz metin XML'e kıyasla önemli ölçüde yer tasarrufu sağlar.

3. **Derleme Bütünlüğü:** AAPT2 (Android Asset Packaging Tool 2) derleme sırasında XML
   dosyalarını doğrular, hatalı referansları yakalar ve tüm kaynakları `resources.arsc` tablosu
   ile eşler. Bu süreç APK'nın tutarlılığını garanti altına alır.

AAPT2 bu işlemi iki aşamada yapar:
- **Compile aşaması:** Her kaynak dosyası ayrı ayrı derlenerek `.flat` ara dosyalarına çevrilir.
- **Link aşaması:** Ara dosyalar birleştirilir, `resources.arsc` oluşturulur ve son APK
  paketlenir.

## Düz XML Parser Neden Çalışmaz?

Python'un standart kütüphanesindeki `xml.etree.ElementTree` veya `xml.dom.minidom` gibi
parser'lar **düz metin XML** okumak için tasarlanmıştır. Bir APK'dan çıkarılan ham
`AndroidManifest.xml` dosyası ise ikili formattadır; bu parser'lar dosyayı açmaya çalıştığında
geçerli bir XML başlığı (`<?xml ...?>`) bulamaz, anlamsız baytlarla karşılaşır ve
`ParseError` hatası fırlatır.

Kısaca: **APK içindeki manifest ikili (binary) formattadır, düz metin değildir; bu yüzden
standart XML araçlarıyla okunamaz.**

## İki Çözüm Yolu

### Yol 1: apktool ile Decode Etmek

[apktool](https://apktool.org/) bir APK'yı tam olarak decode edebilen bir komut satırı aracıdır:

```bash
apktool d uygulama.apk -o uygulama_decoded/
```

Bu komut, APK'nın içindeki AXML formatındaki manifest'i ve diğer kaynakları **okunabilir düz
metin XML'e** geri çevirir. Decode işlemi sonrasında `uygulama_decoded/AndroidManifest.xml`
dosyası standart bir XML dosyasıdır ve Python'ın `xml.etree.ElementTree` modülüyle rahatlıkla
parse edilebilir.

**Avantajları:**
- Çıktı standart XML olduğundan herhangi bir XML kütüphanesiyle işlenebilir.
- Manifest dışında tüm kaynaklar (layout, string, drawable vb.) da decode edilir; isteğe bağlı
  ek analiz yapılabilir.
- smali kodu da çıkarılır — gelişmiş analizler için faydalıdır.

**Dezavantajları:**
- Dışarıdan bir sistem aracıdır, pip ile kurulamaz (Java gerektirir).
- Tam decode işlemi yavaş olabilir, özellikle büyük APK'larda.
- Geçici dosyalar oluşturur, disk alanı kullanır.

### Yol 2: androguard ile Doğrudan AXML Çözmek

[androguard](https://github.com/androguard/androguard), Python ile yazılmış bir kütüphanedir ve
APK'yı **decode etmeden**, AXML formatını doğrudan bellekte çözümleyebilir:

```python
from androguard.core.apk import APK

apk = APK("uygulama.apk")
permissions = apk.get_permissions()
manifest_xml = apk.get_android_manifest_axml().get_xml()
```

**Avantajları:**
- Tamamen Python içinde çalışır, `pip install androguard` ile kurulur.
- Geçici dosya oluşturmaz, doğrudan bellekte işlem yapar.
- İzinler, aktiviteler, servisler gibi manifest bilgilerine erişmek için hazır API sunar.

**Dezavantajları:**
- AXML çözücüsü bazı kenar durumlarında (obfuscated veya manipüle edilmiş APK'lar)
  sorun yaşayabilir.
- Smali veya kaynak dosyalarına erişim sağlamaz.

## Bu Projede Neden İkisini Birden Kullanıyoruz?

Bu projede **androguard'ı birincil (ana) yol**, **apktool'u ise çapraz doğrulama aracı** olarak
kullanacağız. Gerekçeler şunlardır:

1. **Güvenilirlik:** Tek bir araca bağımlı kalmak risklidir. Androguard'ın AXML çözücüsü bir
   APK'da hata verirse, apktool ile aynı APK'yı decode edip sonuçları karşılaştırabiliriz.
   Tersi durum da geçerlidir.

2. **Tutarlılık Kontrolü:** İki bağımsız araçtan gelen izin listeleri birbirleriyle
   karşılaştırılarak raporun doğruluğu güvence altına alınır. Eğer iki aracın çıktısı
   uyuşmuyorsa bu, APK'nın manipüle edilmiş olabileceğine dair bir sinyal olabilir.

3. **Esneklik:** Androguard hızlı ve programatik erişim sağlarken, apktool tam decode ile
   daha derin analiz (smali inceleme, kaynak dosyaları okuma) imkânı sunar. Farklı kullanım
   senaryolarında farklı araçlara ihtiyaç duyulabilir.

4. **Savunma Derinliği (Defense in Depth):** Güvenlik analizi araçlarında tek bir veri
   kaynağına güvenmek yerine birden fazla kaynağı çapraz doğrulamak, yanlış negatif ve yanlış
   pozitif oranını azaltır.

---

*Kaynaklar: [references.md](../references/references.md) dosyasına bakınız.*
