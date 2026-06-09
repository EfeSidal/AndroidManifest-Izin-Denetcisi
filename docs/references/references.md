# Kaynaklar (References)

## Android Resmi Dokümantasyonu

1. **Permissions on Android — Overview**
   https://developer.android.com/guide/topics/permissions/overview
   → İzin türlerini (install-time, runtime, special), koruma seviyelerini ve izin iş akışının
   genel mantığını öğrendim. Normal, tehlikeli ve imza izinlerinin nasıl yönetildiğini bu
   kaynaktan doğruladım.

2. **`<uses-permission>` Manifest Elementi**
   https://developer.android.com/guide/topics/manifest/uses-permission-element
   → `<uses-permission>` etiketinin manifest'teki sözdizimini, `android:name` ve
   `android:maxSdkVersion` özniteliklerini ve sistem davranışını bu referanstan teyit ettim.

3. **Manifest.permission — Tüm İzinlerin API Referansı**
   https://developer.android.com/reference/android/Manifest.permission
   → Her bir iznin sabit adını, hangi API seviyesinde eklendiğini ve koruma seviyesini bu
   sayfadan kontrol ettim. Tehlikeli izin gruplarının örnek izinlerini buradan doğruladım.

4. **R.attr#protectionLevel — Koruma Seviyesi Tanımı**
   https://developer.android.com/reference/android/R.attr#protectionLevel
   → `protectionLevel` özniteliğinin alabileceği değerleri (normal, dangerous, signature,
   signatureOrSystem) ve bunların tam tanımlarını bu referanstan aldım.

## apktool

5. **apktool Resmi Sayfası**
   https://apktool.org/
   → apktool'un APK decode/rebuild sürecini, kurulum gereksinimlerini (Java bağımlılığı) ve
   temel kullanım komutlarını (`apktool d`, `apktool b`) bu kaynaktan öğrendim.

6. **apktool GitHub Deposu**
   https://github.com/iBotPeaches/Apktool
   → Aracın açık kaynak kodunu, sürüm notlarını ve bilinen sorunları bu repodan inceledim.
   AXML decode mekanizmasının güvenilirliğini değerlendirmek için issue'ları taradım.

## androguard

7. **androguard GitHub Deposu**
   https://github.com/androguard/androguard
   → Kütüphanenin Python API'sini (`APK`, `get_permissions()`, `get_android_manifest_axml()`),
   kurulum yöntemini (`pip install androguard`) ve desteklediği Python sürümlerini bu repodan
   öğrendim.

8. **androguard Dokümantasyonu (Read the Docs)**
   https://androguard.readthedocs.io/en/latest/
   → Androguard'ın AXML çözücüsünün (AXMLPrinter) iç yapısını, kaynak tablosu (resources.arsc)
   parse etme yeteneğini ve sertifika analizi fonksiyonlarını bu dokümantasyondan inceledim.

## AXML Formatı Hakkında Ek Kaynaklar

9. **AAPT2 — Android Asset Packaging Tool 2**
   https://developer.android.com/tools/aapt2
   → Android build sistemi sırasında XML dosyalarının nasıl AXML'e derlendiğini, compile ve link
   aşamalarının detaylarını bu resmi araç dokümantasyonundan öğrendim.

---

*Son güncelleme: 2026-06-09*
