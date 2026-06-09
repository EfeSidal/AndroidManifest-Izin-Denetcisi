# Android İzin Seviyeleri ve Tehlikeli İzinler

## `<uses-permission>` Etiketinin Manifest'teki Rolü

Android uygulamaları, cihazın korunan özelliklerine (kamera, konum, rehber vb.) veya diğer
uygulamaların verilerine erişmek için **izin** talep etmek zorundadır. Bu talepler
`AndroidManifest.xml` dosyasında `<uses-permission>` etiketi ile bildirilir:

```xml
<uses-permission android:name="android.permission.CAMERA" />
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
```

Bu etiket, Android işletim sistemine "Bu uygulama çalışabilmek için şu izne ihtiyaç duyuyor"
mesajını verir. Sistem, izin türüne göre (aşağıda açıklanacak) ya otomatik olarak izni verir,
ya da kullanıcıdan açık onay ister.

Android 5.1 (API 22) ve altı sürümlerde tüm izinler **yükleme sırasında** toplu olarak
kabul edilirdi. Android 6.0 (API 23) ve üstünde ise tehlikeli izinler **çalışma zamanında
(runtime)** kullanıcıdan tek tek istenmektedir.

## Protection Level (Koruma Seviyesi)

Her Android izninin bir `protectionLevel` özniteliği vardır. Bu seviye, iznin ne kadar hassas
olduğunu ve sistemin izni nasıl yöneteceğini belirler. Resmi Android dokümantasyonuna göre
temel koruma seviyeleri şunlardır:

### 1. `normal` — Normal İzinler

Kullanıcının gizliliğine veya diğer uygulamaların çalışmasına minimum risk oluşturan izinlerdir.
Sistem bu izinleri **otomatik olarak yükleme sırasında** verir; kullanıcıdan ayrıca onay
istenmez ve kullanıcı bu izinleri iptal edemez.

**Örnekler:**
- `INTERNET` — Ağ soketleri açma
- `ACCESS_NETWORK_STATE` — Ağ bağlantı durumunu sorgulama
- `SET_ALARM` — Alarm kurma
- `VIBRATE` — Cihazı titretme
- `ACCESS_WIFI_STATE` — Wi-Fi bağlantı bilgilerini okuma

### 2. `dangerous` — Tehlikeli İzinler

Kullanıcının özel verilerine erişim sağlayan veya cihaz üzerinde kullanıcıyı doğrudan
etkileyen işlemler için gereken izinlerdir. Bu izinler **çalışma zamanında (runtime)**
kullanıcıdan açıkça istenmek zorundadır. Kullanıcı izni reddedebilir veya daha sonra
Ayarlar'dan iptal edebilir.

**Örnekler:** Aşağıda izin gruplarıyla birlikte detaylandırılmıştır.

### 3. `signature` — İmza İzinleri

Sistem bu izinleri **yalnızca**, izni talep eden uygulama ile izni tanımlayan uygulama (veya
işletim sistemi) **aynı sertifika** ile imzalanmışsa verir. Kullanıcıdan herhangi bir onay
istenmez. Bu mekanizma, aynı geliştirici tarafından yayınlanan uygulamaların birbirleriyle
güvenli biçimde veri paylaşmasını sağlar.

**Örnekler:**
- `BIND_NOTIFICATION_LISTENER_SERVICE` — Bildirim dinleyici servise bağlanma
- `BIND_INPUT_METHOD` — Giriş yöntemi servisine bağlanma

### 4. `signatureOrSystem` (Deprecated) — İmza veya Sistem İzinleri

Bu seviye Android'in eski sürümlerinde kullanılıyordu. İzin, ya aynı sertifikayla imzalanmış
uygulamalara ya da `/system` bölümündeki (ROM'a gömülü) uygulamalara verilirdi. Android'in
güncel sürümlerinde bu seviye **kullanımdan kaldırılmıştır (deprecated)** ve yerine
`signature|privileged` bayrağı kullanılmaktadır.

**Örnekler:**
- `INSTALL_PACKAGES` — Uygulama paketleri kurma
- `DELETE_PACKAGES` — Uygulama paketleri silme

## Tehlikeli İzin Grupları

Tehlikeli izinler, mantıksal olarak **gruplara** ayrılmıştır. Bu gruplandırma, Android'in izin
yönetim arayüzünde kullanıcıya anlamlı kategoriler sunmasını sağlar. Aşağıda her grup ve
içerdiği başlıca izinler listelenmiştir:

### 📍 LOCATION (Konum)
| İzin | Açıklama |
|------|----------|
| `ACCESS_FINE_LOCATION` | GPS ile hassas konum erişimi |
| `ACCESS_COARSE_LOCATION` | Wi-Fi/baz istasyonu ile yaklaşık konum |
| `ACCESS_BACKGROUND_LOCATION` | Arka planda konum erişimi (API 29+) |

### 📷 CAMERA (Kamera)
| İzin | Açıklama |
|------|----------|
| `CAMERA` | Kamera donanımına erişim |

### 🎤 MICROPHONE (Mikrofon)
| İzin | Açıklama |
|------|----------|
| `RECORD_AUDIO` | Ses kaydı yapma |

### 👤 CONTACTS (Rehber)
| İzin | Açıklama |
|------|----------|
| `READ_CONTACTS` | Kişi listesini okuma |
| `WRITE_CONTACTS` | Kişi listesine yazma |
| `GET_ACCOUNTS` | Cihazdaki hesap listesini okuma |

### 📞 PHONE (Telefon)
| İzin | Açıklama |
|------|----------|
| `READ_PHONE_STATE` | Telefon durumu ve kimlik bilgilerini okuma |
| `CALL_PHONE` | Doğrudan telefon araması yapma |
| `READ_CALL_LOG` | Arama kaydını okuma |
| `WRITE_CALL_LOG` | Arama kaydına yazma |
| `ADD_VOICEMAIL` | Sesli mesaj ekleme |

### 💬 SMS
| İzin | Açıklama |
|------|----------|
| `SEND_SMS` | SMS gönderme |
| `RECEIVE_SMS` | Gelen SMS'leri okuma |
| `READ_SMS` | Kayıtlı SMS'leri okuma |
| `RECEIVE_WAP_PUSH` | WAP push mesajı alma |
| `RECEIVE_MMS` | MMS mesajı alma |

### 📋 CALL_LOG (Arama Kaydı)
| İzin | Açıklama |
|------|----------|
| `READ_CALL_LOG` | Arama geçmişini okuma |
| `WRITE_CALL_LOG` | Arama geçmişine yazma |
| `PROCESS_OUTGOING_CALLS` | Giden aramaları izleme |

### 📁 STORAGE (Depolama)
| İzin | Açıklama |
|------|----------|
| `READ_EXTERNAL_STORAGE` | Harici depolamayı okuma |
| `WRITE_EXTERNAL_STORAGE` | Harici depolamaya yazma |
| `READ_MEDIA_IMAGES` | Medya görsellerine erişim (API 33+) |
| `READ_MEDIA_VIDEO` | Medya videolarına erişim (API 33+) |
| `READ_MEDIA_AUDIO` | Medya ses dosyalarına erişim (API 33+) |

> **Not:** Android 10 (API 29) ile gelen Scoped Storage modeli ve Android 13 (API 33) ile
> gelen granüler medya izinleri, depolama izinlerinin kapsamını önemli ölçüde değiştirmiştir.

### 📅 CALENDAR (Takvim)
| İzin | Açıklama |
|------|----------|
| `READ_CALENDAR` | Takvim etkinliklerini okuma |
| `WRITE_CALENDAR` | Takvim etkinlikleri oluşturma/düzenleme |

### 🏃 SENSORS (Sensörler)
| İzin | Açıklama |
|------|----------|
| `BODY_SENSORS` | Kalp atış hızı gibi vücut sensörlerine erişim |
| `ACTIVITY_RECOGNITION` | Fiziksel aktivite tanıma (API 29+) |

## İzinleri Sadece Saymak Neden Yeterli Değildir?

Bir güvenlik denetim aracının izinleri yalnızca listelemesi veya sayması **yetersizdir**. İzinler
tek tek masum görünebilir, ancak **birlikte kullanıldıklarında** ciddi gizlilik ve güvenlik
riskleri oluşturabilir. İşte bu yüzden izinlerin **risk açısından sınıflandırılması** ve
**kombinasyon analizi** yapılması gerekir:

### Tek Başına Risk Değerlendirmesi

Her izin kendi başına bir risk seviyesi taşır:
- `INTERNET` tek başına normal bir izindir, pek çok uygulama buna ihtiyaç duyar.
- `READ_SMS` tek başına tehlikeli bir izindir, kullanıcının kişisel mesajlarına erişim sağlar.
- `CAMERA` tek başına tehlikeli bir izindir, ancak bir kamera uygulaması için beklenen bir
  izindir.

### Kombinasyon Analizi

İzinler birlikte değerlendirildiğinde ortaya bambaşka bir tablo çıkabilir:

| Kombinasyon | Risk | Olası Senaryo |
|-------------|------|---------------|
| `INTERNET` + `READ_SMS` | 🔴 Yüksek | SMS'leri okuyup uzak sunucuya gönderebilir — 2FA kodları çalınabilir |
| `INTERNET` + `ACCESS_FINE_LOCATION` | 🔴 Yüksek | Kullanıcının hassas konumunu sürekli takip edip sunucuya iletebilir |
| `CAMERA` + `RECORD_AUDIO` + `INTERNET` | 🔴 Çok Yüksek | Kamera ve mikrofon ile gizlice kayıt yapıp uzak sunucuya gönderebilir |
| `READ_CONTACTS` + `INTERNET` | 🟠 Orta-Yüksek | Rehber bilgilerini dışarıya sızdırabilir |
| `SEND_SMS` + `READ_SMS` | 🔴 Yüksek | SMS tabanlı dolandırıcılık veya premium SMS gönderimi yapabilir |
| `READ_CALL_LOG` + `READ_PHONE_STATE` | 🟠 Orta-Yüksek | Arama geçmişi ve cihaz kimliğiyle kullanıcı profili çıkarılabilir |

### Bağlam Duyarlılığı

Bir el feneri uygulamasının `CAMERA` izni istemesi normaldir (flaş ışığı için), ancak aynı
uygulamanın `READ_CONTACTS`, `SEND_SMS` ve `INTERNET` izinlerini birlikte istemesi **şüpheli**
bir durumdur. Dolayısıyla etkili bir denetim aracı şunları yapmalıdır:

1. Her iznin koruma seviyesini belirlemeli (normal / dangerous / signature)
2. Tehlikeli izinleri gruplarına göre sınıflandırmalı
3. Riskli izin kombinasyonlarını tespit etmeli
4. Uygulamanın türüne göre bağlamsal değerlendirme yapabilmeli
5. Sonuçları anlaşılır bir risk raporu olarak sunmalı

---

*Kaynaklar: [references.md](../references/references.md) dosyasına bakınız.*
