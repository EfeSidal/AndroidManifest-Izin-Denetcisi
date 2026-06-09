<div align="center">

  # AndroidManifest İzin Denetçisi

  ![GitHub](https://img.shields.io/badge/GitHub-Private-red?style=flat-square&logo=github)
  ![Language](https://img.shields.io/badge/Language-Python-blue?style=flat-square)
  ![Status](https://img.shields.io/badge/Status-Complete-brightgreen?style=flat-square)
  ![Course](https://img.shields.io/badge/Course-BGT210-purple?style=flat-square)
  ![License](https://img.shields.io/badge/License-Educational-green?style=flat-square)

</div>

---

## 🎓 Danışman
| | |
|---|---|
| **Ad** | Keyvan Arasteh |
| **GitHub** | [@keyvanarasteh](https://github.com/keyvanarasteh) |
| **E-posta** | keyvan.arasteh@istinye.edu.tr |

## 👤 Öğrenci
| | |
|---|---|
| **Ad Soyad** | Efe Sidal |
| **Öğrenci No** | [Öğrenci Numaranız] |

## 📚 Ders Bilgileri
| | |
|---|---|
| **Ders** | Tersine Mühendislik / Reverse Engineering |
| **Kod** | BGT210 |
| **Dönem** | 2025-2026 Bahar |
| **Üniversite** | Istinye University |

---

## 📋 Proje Özeti
Herhangi bir APK dosyasından AndroidManifest.xml'i ayrıştırır,
istenen izinleri normal / tehlikeli / imza olarak sınıflandırır,
şeffaf bir risk puanı hesaplar ve okunabilir Markdown + JSON raporları üretir.

---

## 🗂 Repo Yapısı
```text
.
├── apks/               # İncelenecek örnek APK dosyaları
├── docs/               # Proje ve araştırma dokümantasyonları
│   ├── modules/
│   │   └── permission-auditor.md
│   ├── references/
│   │   └── references.md
│   └── research/
│       ├── 01-axml-format.md
│       └── 02-android-permission-levels.md
├── reports/            # Üretilen Markdown ve JSON raporları
├── src/                # Projenin kaynak kodları
│   ├── main.py         # Ana CLI komutu
│   ├── parser.py       # AXML ve manifest parsing mantığı
│   ├── permission_db.json # Android izinleri veritabanı (ağırlıklar vb.)
│   ├── report.py       # JSON ve Markdown rapor üretici
│   └── scorer.py       # Risk ağırlıklandırma ve kombinasyon analizi
├── Dockerfile          # Python ve Java içeren tam yapılandırılmış ortam
├── docker-compose.yml  # Kolay çalıştırma için composer
├── requirements.txt    # Python bağımlılıkları (androguard, python-dotenv)
├── README.md
└── ROADMAP.md
```

---

## 🚀 Kurulum ve Kullanım

### Docker ile (önerilen)
```bash
git clone https://github.com/EfeSidal/AndroidManifest-Izin-Denetcisi.git
cd AndroidManifest-Izin-Denetcisi
cp .env.example .env
docker compose build
docker compose run --rm auditor --apk apks/ornek.apk --output reports/
```

### Yerel (Docker olmadan)
```bash
pip install -r requirements.txt
# apktool sistem aracı olarak ayrıca kurulmalı
python src/main.py --apk apks/ornek.apk --output reports/
```

---

## 📊 Teslimler
| Teslim | Durum |
|--------|-------|
| İzin denetçisi aracı (parser + scorer + report + CLI) | ✅ |
| Risk puanlaması (ağırlık, bant, kombinasyon bayrakları) | ✅ |
| 3 örnek uygulama analizi | ✅ |

---

## 🔬 3 Örnek Analiz Sonucu
| Uygulama | Paket | Kaynak | Toplam Puan | Bant | Tehlikeli | Normal | Kombinasyon |
|----------|-------|--------|-------------|------|-----------|--------|-------------|
| Fossify Clock | org.fossify.clock | F-Droid | 28 | Orta | 1 | 8 | 0 |
| Organic Maps  | app.organicmaps   | F-Droid | 30 | Orta | 3 | 7 | 1 |
| Element       | im.vector.app     | F-Droid | 88 | Yüksek | 8 | 9 | 4 |

---

## 📚 Belgeler
- Araç detayı → [docs/modules/permission-auditor.md](docs/modules/permission-auditor.md)
- Araştırma notları → [docs/research/](docs/research/)
- Kaynaklar → [docs/references/references.md](docs/references/references.md)

---

## 🔗 Kaynaklar
- Android İzin Referansı: https://developer.android.com/reference/android/Manifest.permission
- apktool: https://apktool.org
- androguard: https://github.com/androguard/androguard
