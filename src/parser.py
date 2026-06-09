"""
APK İzin Çıkarıcı (Parser)

Bir APK dosyasından izin listesini iki farklı yöntemle çıkarır:
  1. androguard (birincil) — AXML'i doğrudan bellekte çözer
  2. apktool  (çapraz doğrulama) — APK'yı decode edip XML olarak parse eder

İki yöntemin sonuçları karşılaştırılır; fark varsa rapora eklenir.
"""

import hashlib
import logging
import os
import shutil
import subprocess
import tempfile
import xml.etree.ElementTree as ET

from androguard.core.apk import APK

# ---------------------------------------------------------------------------
# Loglama
# ---------------------------------------------------------------------------
LOG_LEVEL = os.environ.get("LOG_LEVEL", "info").upper()
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("parser")

# Android XML namespace
ANDROID_NS = "http://schemas.android.com/apk/res/android"


# ---------------------------------------------------------------------------
# 1) androguard ile izin çıkarma
# ---------------------------------------------------------------------------
def get_permissions_androguard(apk_path: str) -> set[str]:
    """androguard kullanarak APK'dan izinleri çıkarır.

    Args:
        apk_path: APK dosyasının yolu.

    Returns:
        Bulunan izinlerin kümesi (set).
    """
    logger.info("androguard ile izinler çıkarılıyor: %s", apk_path)
    apk = APK(apk_path)
    permissions = set(apk.get_permissions())
    logger.info("androguard: %d izin bulundu", len(permissions))
    return permissions


# ---------------------------------------------------------------------------
# 2) apktool ile izin çıkarma
# ---------------------------------------------------------------------------
def get_permissions_apktool(apk_path: str) -> set[str] | None:
    """apktool ile APK'yı decode edip AndroidManifest.xml'den izinleri çıkarır.

    apktool kurulu değilse veya hata oluşursa None döndürür (çökmez).

    Args:
        apk_path: APK dosyasının yolu.

    Returns:
        Bulunan izinlerin kümesi veya apktool kullanılamıyorsa None.
    """
    tmp_dir = None
    try:
        tmp_dir = tempfile.mkdtemp(prefix="apktool_")
        logger.info("apktool ile decode ediliyor: %s -> %s", apk_path, tmp_dir)

        result = subprocess.run(
            ["apktool", "d", "-f", apk_path, "-o", tmp_dir],
            capture_output=True,
            text=True,
            timeout=120,
        )

        if result.returncode != 0:
            logger.warning(
                "apktool hata döndürdü (kod %d): %s",
                result.returncode,
                result.stderr.strip(),
            )
            return None

        manifest_path = os.path.join(tmp_dir, "AndroidManifest.xml")
        if not os.path.isfile(manifest_path):
            logger.warning("apktool decode sonrası AndroidManifest.xml bulunamadı")
            return None

        tree = ET.parse(manifest_path)
        root = tree.getroot()

        permissions: set[str] = set()
        for element in root.iter("uses-permission"):
            name = element.get(f"{{{ANDROID_NS}}}name")
            if name:
                permissions.add(name)

        logger.info("apktool: %d izin bulundu", len(permissions))
        return permissions

    except FileNotFoundError:
        logger.warning(
            "apktool bulunamadı (kurulu değil veya PATH'te yok). "
            "Çapraz doğrulama atlanıyor."
        )
        return None
    except subprocess.TimeoutExpired:
        logger.warning("apktool zaman aşımına uğradı (120s). Çapraz doğrulama atlanıyor.")
        return None
    except Exception as exc:
        logger.warning("apktool işlemi sırasında beklenmeyen hata: %s", exc)
        return None
    finally:
        if tmp_dir and os.path.isdir(tmp_dir):
            shutil.rmtree(tmp_dir, ignore_errors=True)
            logger.debug("Geçici klasör temizlendi: %s", tmp_dir)


# ---------------------------------------------------------------------------
# 3) APK bilgileri
# ---------------------------------------------------------------------------
def get_apk_info(apk_path: str) -> dict:
    """APK'nın paket adı, uygulama etiketi ve SHA256 hash'ini döndürür.

    Args:
        apk_path: APK dosyasının yolu.

    Returns:
        {"package": str, "app_name": str, "sha256": str}
    """
    apk = APK(apk_path)

    sha256_hash = hashlib.sha256()
    with open(apk_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256_hash.update(chunk)

    return {
        "package": apk.get_package(),
        "app_name": apk.get_app_name(),
        "sha256": sha256_hash.hexdigest(),
    }


# ---------------------------------------------------------------------------
# 4) Ana fonksiyon — izin çıkarma ve çapraz doğrulama
# ---------------------------------------------------------------------------
def extract_permissions(apk_path: str) -> dict:
    """APK'dan izinleri çıkarır, çapraz doğrulama yapar ve yapısal sonuç döndürür.

    Args:
        apk_path: APK dosyasının yolu.

    Returns:
        {
          "apk_info": {...},
          "permissions": [...],     # sıralı liste (androguard sonucu)
          "cross_check": {
            "apktool_available": bool,
            "match": bool | None,
            "only_in_androguard": [...],
            "only_in_apktool": [...]
          }
        }

    Raises:
        FileNotFoundError: APK dosyası bulunamazsa.
    """
    if not os.path.isfile(apk_path):
        raise FileNotFoundError(f"APK dosyası bulunamadı: {apk_path}")

    # APK bilgileri
    logger.info("APK bilgileri alınıyor: %s", apk_path)
    apk_info = get_apk_info(apk_path)
    logger.info("Paket: %s | Uygulama: %s", apk_info["package"], apk_info["app_name"])

    # Birincil: androguard
    perms_androguard = get_permissions_androguard(apk_path)

    # Çapraz doğrulama: apktool
    perms_apktool = get_permissions_apktool(apk_path)

    # Karşılaştırma
    apktool_available = perms_apktool is not None
    match = None
    only_in_androguard: list[str] = []
    only_in_apktool: list[str] = []

    if apktool_available:
        only_in_androguard = sorted(perms_androguard - perms_apktool)
        only_in_apktool = sorted(perms_apktool - perms_androguard)
        match = len(only_in_androguard) == 0 and len(only_in_apktool) == 0

        if match:
            logger.info("Çapraz doğrulama BAŞARILI: iki araç aynı sonucu verdi.")
        else:
            logger.warning(
                "Çapraz doğrulama UYUŞMAZLIK tespit etti! "
                "Yalnızca androguard'da: %s | Yalnızca apktool'da: %s",
                only_in_androguard,
                only_in_apktool,
            )
    else:
        logger.info("apktool kullanılamadı; çapraz doğrulama atlandı.")

    return {
        "apk_info": apk_info,
        "permissions": sorted(perms_androguard),
        "cross_check": {
            "apktool_available": apktool_available,
            "match": match,
            "only_in_androguard": only_in_androguard,
            "only_in_apktool": only_in_apktool,
        },
    }


# ---------------------------------------------------------------------------
# Smoke test
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import json
    import sys

    if len(sys.argv) < 2:
        print("Kullanım: python src/parser.py <apk_dosyasi>")
        sys.exit(1)

    result = extract_permissions(sys.argv[1])
    print(json.dumps(result, indent=2, ensure_ascii=False))
