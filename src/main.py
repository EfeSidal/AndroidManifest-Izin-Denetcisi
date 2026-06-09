"""
AndroidManifest İzin Denetçisi - Ana Giriş Noktası (CLI)

Bu script, bir veya birden fazla APK dosyasını işleyerek
Parser -> Scorer -> Report zincirini çalıştırır.
"""

import argparse
import logging
import os
import sys
from pathlib import Path

# python-dotenv yüklemeyi dene
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Modül importları main içinde yapılacak (hızlı help için)

# ---------------------------------------------------------------------------
# CLI Yapılandırması
# ---------------------------------------------------------------------------
def parse_arguments():
    """Komut satırı argümanlarını ayrıştırır."""
    parser = argparse.ArgumentParser(
        description="AndroidManifest İzin Denetçisi - APK'ların izinlerini analiz edip risk raporu üretir."
    )
    
    parser.add_argument(
        "--apk",
        action="append",
        required=True,
        help="İncelenecek APK dosyası veya klasörü (birden çok kez kullanılabilir)."
    )
    
    # Varsayılan output dizinini .env'den al
    default_out = os.environ.get("OUTPUT_DIR", "./reports")
    
    parser.add_argument(
        "--output",
        default=default_out,
        help=f"Raporların kaydedileceği klasör (Varsayılan: {default_out})"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Ayrıntılı (debug) log seviyesini etkinleştirir."
    )
    
    return parser.parse_args()


# ---------------------------------------------------------------------------
# APK Toplayıcı
# ---------------------------------------------------------------------------
def collect_apks(paths: list[str]) -> list[str]:
    """Verilen dosya/klasör yollarından APK'ları toplar."""
    apk_files = []
    
    for p in paths:
        path_obj = Path(p)
        if not path_obj.exists():
            logging.warning(f"Belirtilen yol bulunamadı: {p}")
            continue
            
        if path_obj.is_file() and path_obj.suffix.lower() == ".apk":
            apk_files.append(str(path_obj))
        elif path_obj.is_dir():
            for apk_path in path_obj.rglob("*.apk"):
                apk_files.append(str(apk_path))
        else:
            logging.warning(f"Geçersiz yol (APK değil): {p}")
            
    return apk_files


# ---------------------------------------------------------------------------
# Ana İşlem
# ---------------------------------------------------------------------------
def main():
    args = parse_arguments()
    
    # Loglama yapılandırması
    log_level = logging.DEBUG if args.verbose else getattr(logging, os.environ.get("LOG_LEVEL", "INFO").upper(), logging.INFO)
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    logger = logging.getLogger("main")
    
    # APK'ları topla
    apks_to_process = collect_apks(args.apk)
    
    if not apks_to_process:
        logger.error("İşlenecek hiçbir APK dosyası bulunamadı!")
        sys.exit(1)
        
    logger.info("Toplam %d APK işlenecek. Çıktı klasörü: %s", len(apks_to_process), args.output)
    
    results_summary = []
    error_count = 0
    
    # APK'ları sırayla işle
    for apk_path in apks_to_process:
        filename = os.path.basename(apk_path)
        logger.info("--- İşleniyor: %s ---", filename)
        
        try:
            from parser import extract_permissions
            from scorer import analyze
            from report import generate_report
            
            # 1. Aşama: Parser (Çıkarım)
            parsed_data = extract_permissions(apk_path)
            
            # 2. Aşama: Scorer (Analiz)
            analysis_data = analyze(parsed_data)
            
            # 3. Aşama: Report (Raporlama)
            report_paths = generate_report(analysis_data, args.output)
            
            package_name = analysis_data.get("apk_info", {}).get("package", filename)
            score = analysis_data.get("score", {})
            band = score.get("band", "Bilinmiyor")
            total = score.get("total_score", 0)
            
            logger.info("Başarılı! Raporlar: %s, %s", report_paths.get("md"), report_paths.get("json"))
            
            results_summary.append({
                "status": "success",
                "package": package_name,
                "band": band,
                "score": total
            })
            
        except Exception as e:
            logger.error("HATA: %s işlenirken bir sorun oluştu: %s", filename, str(e))
            if args.verbose:
                logger.exception(e)
            
            results_summary.append({
                "status": "error",
                "package": filename,
                "error_msg": str(e)
            })
            error_count += 1
            
    # -----------------------------------------------------------------------
    # ÖZET ÇIKTISI
    # -----------------------------------------------------------------------
    print("\n" + "─" * 32)
    print(f" SONUÇ: {len(apks_to_process)} APK işlendi, {error_count} hata")
    print("─" * 32)
    
    for res in results_summary:
        if res["status"] == "success":
            print(f"  \u2714 {res['package']:<20} →  {res['band']:<8} (puan: {res['score']})")
        else:
            print(f"  \u2718 {res['package']:<20} →  HATA: {res['error_msg']}")


if __name__ == "__main__":
    main()
