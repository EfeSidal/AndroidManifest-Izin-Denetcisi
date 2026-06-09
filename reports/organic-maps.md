# APK İzin Risk Raporu — Organic Maps

## Uygulama Bilgileri
| Alan | Değer |
|------|-------|
| Paket | `app.organicmaps` |
| Uygulama Adı | Organic Maps |
| Rapor Tarihi | 2026-06-09 12:00 UTC |

## Risk Özeti
| Metrik | Değer |
|--------|-------|
| Toplam Puan | **30** |
| Risk Bandı | 🟡 **Orta** |
| Tehlikeli İzin | 3 |
| Normal İzin | 7 |
| İmza İzni | 0 |
| Bilinmeyen | 1 |

## Tehlikeli Kombinasyonlar
- 🔴 **KONUM_TAKIBI** — Hassas konum surekli takip edilip sunucuya iletilebilir `[YUKSEK]`

## İzin Dökümü
| İzin | Seviye | Grup | Ağırlık |
|------|--------|------|---------|
| `android.permission.ACCESS_FINE_LOCATION` | dangerous | LOCATION | 9 |
| `android.permission.ACCESS_COARSE_LOCATION` | dangerous | LOCATION | 5 |
| `android.permission.POST_NOTIFICATIONS` | dangerous | NOTIFICATIONS | 5 |
| `android.permission.ACCESS_LOCATION_EXTRA_COMMANDS` | unknown | UNKNOWN | 4 |
| `android.permission.INTERNET` | normal | NETWORK | 1 |
| `android.permission.ACCESS_NETWORK_STATE` | normal | NETWORK | 1 |
| `android.permission.WAKE_LOCK` | normal | SYSTEM | 1 |
| `android.permission.FOREGROUND_SERVICE` | normal | SYSTEM | 1 |
| `android.permission.FOREGROUND_SERVICE_LOCATION` | normal | SYSTEM | 1 |
| `android.permission.FOREGROUND_SERVICE_MEDIA_PLAYBACK` | normal | SYSTEM | 1 |
| `android.permission.FOREGROUND_SERVICE_DATA_SYNC` | normal | SYSTEM | 1 |

## Çapraz Doğrulama
> ⚠️ apktool mevcut değil, çapraz doğrulama atlandı.

---
*Bu rapor AndroidManifest İzin Denetçisi tarafından otomatik oluşturulmuştur.*
