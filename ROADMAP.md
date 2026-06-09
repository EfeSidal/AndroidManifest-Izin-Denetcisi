# ROADMAP — AndroidManifest İzin Denetçisi
> BGT210 Tersine Mühendislik · Istinye University · Danışman: Keyvan Arasteh

---

## Faz 0: Yazmadan Önce Anla
- [x] Proje nedir, girdiler/çıktılar neler
- [x] Hangi araçları kullanacağım ve neden (apktool vs androguard)
- [x] APK içindeki manifest'in neden düz metin olmadığını anladım

## Faz 1: Araştırma
- [x] AXML formatı — docs/research/01-axml-format.md
- [x] Android protectionLevel seviyeleri — docs/research/02-android-permission-levels.md
- [x] Kaynaklar — docs/references/references.md

## Faz 2: Ortam Kurulumu
- [x] İzole Docker ortamı
- [x] requirements.txt (androguard, python-dotenv)
- [x] .env.example

## Faz 3: Uygulama

### İzin Veritabanı (permission_db.json)
- [x] Resmi Android kaynağından izin → seviye/grup/ağırlık eşlemesi
- [x] _meta ile ağırlık şeması belgelendi

### Parser (parser.py)
- [x] androguard birincil yol
- [x] apktool çapraz doğrulama
- [x] AXML namespace sorunu çözüldü

### Puanlama (scorer.py)
- [x] Ağırlık tabanlı toplam puan
- [x] Düşük/Orta/Yüksek bantlar
- [x] 6 tehlikeli kombinasyon bayrağı

### Rapor (report.py)
- [x] Markdown raporu (izin tablosu + kombinasyonlar + çapraz doğrulama)
- [x] JSON raporu

### CLI (main.py)
- [x] --apk (dosya veya klasör), --output, --verbose
- [x] Birden fazla APK desteği
- [x] Özet çıktısı

## Faz 4: Test ve Raporlama
- [x] 3 gerçek APK analiz edildi (F-Droid)
- [x] Fossify Clock → Orta (puan: 28)
- [x] Organic Maps  → Orta (puan: 30)
- [x] Element       → Yüksek (puan: 88)
- [x] Raporlar reports/ altında

## Faz 5: Teslim
- [x] Repo temiz ve organize
- [x] README.md eksiksiz
- [x] Docker doğrulandı (docker compose build + run)
- [x] Danışman collaborator olarak eklendi → keyvanarasteh

---

## Öğrendiklerim

> **Öğrenci Notu:** Bu bölümü kendi deneyimlerinize göre doldurunuz. Aşağıdaki sorular size rehberlik etmesi için bırakılmıştır:

- *AXML formatını öğrenmeden önce ne bekliyordun, gerçekte ne buldun?*
(Buraya cevabınızı yazın)

- *En zorlandığın teknik nokta neydi?*
(Buraya cevabınızı yazın)

- *İki araç (androguard vs apktool) karşılaştırmasında seni şaşırtan bir şey var mıydı?*
(Buraya cevabınızı yazın)

- *Bu aracı gerçek bir senaryoda nasıl kullanırdın?*
(Buraya cevabınızı yazın)
