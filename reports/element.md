# APK İzin Risk Raporu — Element

## Uygulama Bilgileri
| Alan | Değer |
|------|-------|
| Paket | `im.vector.app` |
| Uygulama Adı | Element |
| Rapor Tarihi | 2026-06-09 12:00 UTC |

## Risk Özeti
| Metrik | Değer |
|--------|-------|
| Toplam Puan | **88** |
| Risk Bandı | 🔴 **Yüksek** |
| Tehlikeli İzin | 8 |
| Normal İzin | 9 |
| İmza İzni | 1 |
| Bilinmeyen | 5 |

## Tehlikeli Kombinasyonlar
- 🔴 **KONUM_TAKIBI** — Hassas konum surekli takip edilip sunucuya iletilebilir `[YUKSEK]`
- 🔴 **SES_SIZINTISI** — Mikrofon kaydi uzak sunucuya gonderilebilir `[YUKSEK]`
- 🟠 **REHBER_SIZINTISI** — Kisiler listesi disariya sizdirilabilir `[ORTA_YUKSEK]`
- 🚨 **GIZLI_KAYIT_VE_SIZINTI** — Kamera + mikrofon kaydi ve internet ile tam gozetim profili `[KRITIK]`

## İzin Dökümü
| İzin | Seviye | Grup | Ağırlık |
|------|--------|------|---------|
| `android.permission.ACCESS_FINE_LOCATION` | dangerous | LOCATION | 9 |
| `android.permission.READ_CONTACTS` | dangerous | CONTACTS | 9 |
| `android.permission.CAMERA` | dangerous | CAMERA | 9 |
| `android.permission.RECORD_AUDIO` | dangerous | MICROPHONE | 9 |
| `android.permission.ACCESS_COARSE_LOCATION` | dangerous | LOCATION | 5 |
| `android.permission.POST_NOTIFICATIONS` | dangerous | NOTIFICATIONS | 5 |
| `android.permission.BLUETOOTH_CONNECT` | dangerous | NEARBY_DEVICES | 5 |
| `android.permission.READ_EXTERNAL_STORAGE` | dangerous | STORAGE | 5 |
| `android.permission.MANAGE_OWN_CALLS` | unknown | UNKNOWN | 4 |
| `android.permission.MODIFY_AUDIO_SETTINGS` | unknown | UNKNOWN | 4 |
| `android.permission.USE_FULL_SCREEN_INTENT` | unknown | UNKNOWN | 4 |
| `android.permission.FOREGROUND_SERVICE_PHONE_CALL` | unknown | UNKNOWN | 4 |
| `android.permission.FOREGROUND_SERVICE_MEDIA_PROJECTION` | unknown | UNKNOWN | 4 |
| `android.permission.SYSTEM_ALERT_WINDOW` | signature | SIGNATURE_SYSTEM | 3 |
| `android.permission.INTERNET` | normal | NETWORK | 1 |
| `android.permission.ACCESS_NETWORK_STATE` | normal | NETWORK | 1 |
| `android.permission.WAKE_LOCK` | normal | SYSTEM | 1 |
| `android.permission.FOREGROUND_SERVICE` | normal | SYSTEM | 1 |
| `android.permission.FOREGROUND_SERVICE_LOCATION` | normal | SYSTEM | 1 |
| `android.permission.FOREGROUND_SERVICE_DATA_SYNC` | normal | SYSTEM | 1 |
| `android.permission.FOREGROUND_SERVICE_MICROPHONE` | normal | SYSTEM | 1 |
| `android.permission.VIBRATE` | normal | SYSTEM | 1 |
| `android.permission.REQUEST_INSTALL_PACKAGES` | normal | DIGER | 1 |

## Çapraz Doğrulama
> ⚠️ apktool mevcut değil, çapraz doğrulama atlandı.

---
*Bu rapor AndroidManifest İzin Denetçisi tarafından otomatik oluşturulmuştur.*
