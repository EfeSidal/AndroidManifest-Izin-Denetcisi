# APK İzin Risk Raporu — Fossify Clock

## Uygulama Bilgileri
| Alan | Değer |
|------|-------|
| Paket | `org.fossify.clock` |
| Uygulama Adı | Fossify Clock |
| Rapor Tarihi | 2026-06-09 12:00 UTC |

## Risk Özeti
| Metrik | Değer |
|--------|-------|
| Toplam Puan | **28** |
| Risk Bandı | 🟡 **Orta** |
| Tehlikeli İzin | 1 |
| Normal İzin | 8 |
| İmza İzni | 1 |
| Bilinmeyen | 3 |

## Tehlikeli Kombinasyonlar
> ✅ Bilinen tehlikeli kombinasyon tespit edilmedi.

## İzin Dökümü
| İzin | Seviye | Grup | Ağırlık |
|------|--------|------|---------|
| `android.permission.POST_NOTIFICATIONS` | dangerous | NOTIFICATIONS | 5 |
| `android.permission.USE_FULL_SCREEN_INTENT` | unknown | UNKNOWN | 4 |
| `android.permission.FOREGROUND_SERVICE_SPECIAL_USE` | unknown | UNKNOWN | 4 |
| `android.permission.DISABLE_KEYGUARD` | unknown | UNKNOWN | 4 |
| `android.permission.SYSTEM_ALERT_WINDOW` | signature | SIGNATURE_SYSTEM | 3 |
| `android.permission.VIBRATE` | normal | SYSTEM | 1 |
| `android.permission.RECEIVE_BOOT_COMPLETED` | normal | SYSTEM | 1 |
| `android.permission.SCHEDULE_EXACT_ALARM` | normal | SYSTEM | 1 |
| `android.permission.USE_EXACT_ALARM` | normal | SYSTEM | 1 |
| `android.permission.FOREGROUND_SERVICE` | normal | SYSTEM | 1 |
| `android.permission.WAKE_LOCK` | normal | SYSTEM | 1 |
| `android.permission.REQUEST_IGNORE_BATTERY_OPTIMIZATIONS` | normal | SYSTEM | 1 |
| `com.android.alarm.permission.SET_ALARM` | normal | SYSTEM | 1 |

## Çapraz Doğrulama
> ⚠️ apktool mevcut değil, çapraz doğrulama atlandı.

---
*Bu rapor AndroidManifest İzin Denetçisi tarafından otomatik oluşturulmuştur.*
