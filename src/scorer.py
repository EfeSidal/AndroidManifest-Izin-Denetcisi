"""
Risk Puanlama Motoru (Scorer)

Bu modül, parser'dan alınan APK izin listesini veritabanı (permission_db.json)
ile eşleştirerek risk puanını hesaplar ve tehlikeli kombinasyonları tespit eder.
"""

import json
import logging
import os

# ---------------------------------------------------------------------------
# PUANLAMA SABİTLERİ
# ---------------------------------------------------------------------------
BAND_LOW_MAX = 20    # Bu eşiğe kadar Düşük risk
BAND_MED_MAX = 50    # Bu eşiğe kadar Orta risk; üstü Yüksek

# Ağırlıklar permission_db.json'dan gelir (_meta.agirlik_semasi'na bak)
# Bilinmeyen (unknown) izin ağırlığı: normal ile dangerous_taban arasında ihtiyatlı değer
UNKNOWN_WEIGHT = 4


# ---------------------------------------------------------------------------
# Loglama
# ---------------------------------------------------------------------------
LOG_LEVEL = os.environ.get("LOG_LEVEL", "info").upper()
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("scorer")


def load_permission_db() -> dict:
    """src/permission_db.json dosyasını okur ve salt izin eşlemesini döndürür.
    
    Returns:
        _meta anahtarı çıkarılmış izin sözlüğü.
        
    Raises:
        FileNotFoundError: Veritabanı dosyası bulunamazsa.
    """
    db_path = os.path.join(os.path.dirname(__file__), "permission_db.json")
    if not os.path.isfile(db_path):
        raise FileNotFoundError(f"İzin veritabanı bulunamadı: {db_path}")

    with open(db_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # _meta anahtarını çıkar
    data.pop("_meta", None)
    return data


def score_permissions(permissions: list[str]) -> dict:
    """İzin listesini puanlar ve istatistikleri çıkarır.
    
    Args:
        permissions: APK'dan çıkarılmış izin listesi.
        
    Returns:
        total_score, band, sayımlar ve detaylı izin dökümünü içeren sözlük.
    """
    db = load_permission_db()
    
    total_score = 0
    dangerous_count = 0
    normal_count = 0
    signature_count = 0
    unknown_count = 0
    
    breakdown = []
    
    for perm in permissions:
        if perm in db:
            entry = db[perm]
            level = entry.get("level", "unknown")
            group = entry.get("group", "UNKNOWN")
            weight = entry.get("weight", UNKNOWN_WEIGHT)
        else:
            level = "unknown"
            group = "UNKNOWN"
            weight = UNKNOWN_WEIGHT
            
        total_score += weight
        
        if level == "dangerous":
            dangerous_count += 1
        elif level == "normal":
            normal_count += 1
        elif level == "signature":
            signature_count += 1
        else:
            unknown_count += 1
            
        breakdown.append({
            "permission": perm,
            "level": level,
            "group": group,
            "weight": weight
        })

    # Ağırlığa göre azalan sırada sırala
    breakdown.sort(key=lambda x: x["weight"], reverse=True)
    
    # Band belirleme
    if total_score <= BAND_LOW_MAX:
        band = "Düşük"
    elif total_score <= BAND_MED_MAX:
        band = "Orta"
    else:
        band = "Yüksek"
        
    logger.info("Puan: %d, Band: %s", total_score, band)
    
    return {
        "total_score": total_score,
        "band": band,
        "dangerous_count": dangerous_count,
        "normal_count": normal_count,
        "signature_count": signature_count,
        "unknown_count": unknown_count,
        "breakdown": breakdown
    }


def check_combinations(permissions: list[str]) -> list[dict]:
    """İzinler arasında bilinen tehlikeli kombinasyonları kontrol eder.
    
    Args:
        permissions: APK'dan çıkarılmış izin listesi.
        
    Returns:
        Tetiklenen kombinasyonların listesi. Her biri: {"ad", "aciklama", "risk"}
    """
    perms_set = set(permissions)
    triggered = []
    
    has_internet = "android.permission.INTERNET" in perms_set
    has_read_sms = "android.permission.READ_SMS" in perms_set
    has_receive_sms = "android.permission.RECEIVE_SMS" in perms_set
    has_send_sms = "android.permission.SEND_SMS" in perms_set
    has_fine_location = "android.permission.ACCESS_FINE_LOCATION" in perms_set
    has_record_audio = "android.permission.RECORD_AUDIO" in perms_set
    has_read_contacts = "android.permission.READ_CONTACTS" in perms_set
    has_camera = "android.permission.CAMERA" in perms_set

    # COMBO_1: SMS_SIZINTISI
    if has_internet and (has_read_sms or has_receive_sms):
        triggered.append({
            "ad": "SMS_SIZINTISI",
            "aciklama": "SMS okunup uzak sunucuya gonderilebilir (2FA kod calintisi)",
            "risk": "YUKSEK"
        })

    # COMBO_2: KONUM_TAKIBI
    if has_internet and has_fine_location:
        triggered.append({
            "ad": "KONUM_TAKIBI",
            "aciklama": "Hassas konum surekli takip edilip sunucuya iletilebilir",
            "risk": "YUKSEK"
        })

    # COMBO_3: SES_SIZINTISI
    if has_internet and has_record_audio:
        triggered.append({
            "ad": "SES_SIZINTISI",
            "aciklama": "Mikrofon kaydi uzak sunucuya gonderilebilir",
            "risk": "YUKSEK"
        })

    # COMBO_4: REHBER_SIZINTISI
    if has_internet and has_read_contacts:
        triggered.append({
            "ad": "REHBER_SIZINTISI",
            "aciklama": "Kisiler listesi disariya sizdirilabilir",
            "risk": "ORTA_YUKSEK"
        })

    # COMBO_5: GIZLI_KAYIT_VE_SIZINTI
    if has_internet and has_record_audio and has_camera:
        triggered.append({
            "ad": "GIZLI_KAYIT_VE_SIZINTI",
            "aciklama": "Kamera + mikrofon kaydi ve internet ile tam gozetim profili",
            "risk": "KRITIK"
        })

    # COMBO_6: SMS_DOLANDIRICILIK
    if has_send_sms and has_read_sms:
        triggered.append({
            "ad": "SMS_DOLANDIRICILIK",
            "aciklama": "Gelen SMS okunur ve yeni SMS gonderilir",
            "risk": "YUKSEK"
        })
        
    logger.info("Toplam %d tehlikeli kombinasyon tespit edildi", len(triggered))
    return triggered


def analyze(parser_result: dict) -> dict:
    """Faz 3'ün extract_permissions() çıktısını alır ve puanlama yapar.
    
    Args:
        parser_result: extract_permissions() fonksiyonundan dönen sözlük.
        
    Returns:
        apk_info, cross_check, score ve combinations bilgilerini içeren detaylı analiz.
    """
    perms = parser_result.get("permissions", [])
    
    return {
        "apk_info": parser_result.get("apk_info", {}),
        "cross_check": parser_result.get("cross_check", {}),
        "score": score_permissions(perms),
        "combinations": check_combinations(perms)
    }


# ---------------------------------------------------------------------------
# Smoke test
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import sys
    from parser import extract_permissions

    if len(sys.argv) < 2:
        print("Kullanım: python src/scorer.py <apk_dosyasi>")
        sys.exit(1)

    try:
        # extract_permissions ile parser'dan verileri al ve analyze ile analiz et
        parsed_data = extract_permissions(sys.argv[1])
        analysis_result = analyze(parsed_data)
        print(json.dumps(analysis_result, indent=2, ensure_ascii=False))
    except Exception as e:
        logger.error("Hata oluştu: %s", e)
        sys.exit(1)
