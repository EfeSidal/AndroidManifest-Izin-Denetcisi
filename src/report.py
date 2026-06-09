"""
Rapor Üretici (Report)

Bu modül, scorer'dan alınan analiz sonuçlarını okuyarak
kullanıcı dostu Markdown (.md) ve makine okunabilir JSON (.json) formatında
iki adet rapor dosyası üretir.
"""

import datetime
import json
import logging
import os
import re

# ---------------------------------------------------------------------------
# Loglama
# ---------------------------------------------------------------------------
LOG_LEVEL = os.environ.get("LOG_LEVEL", "info").upper()
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("report")


# ---------------------------------------------------------------------------
# Yardımcı Fonksiyonlar
# ---------------------------------------------------------------------------
def _band_emoji(band: str) -> str:
    """Risk bandına uygun emoji döndürür."""
    if band == "Düşük":
        return "🟢"
    elif band == "Orta":
        return "🟡"
    elif band == "Yüksek":
        return "🔴"
    return "⚪"


def _risk_emoji(risk: str) -> str:
    """Kombinasyon risk seviyesine uygun emoji döndürür."""
    if risk == "KRITIK":
        return "🚨"
    elif risk == "YUKSEK":
        return "🔴"
    elif risk == "ORTA_YUKSEK":
        return "🟠"
    return "🟡"


# ---------------------------------------------------------------------------
# Rapor Oluşturma (Markdown ve JSON)
# ---------------------------------------------------------------------------
def render_markdown(analysis: dict) -> str:
    """Analiz sözlüğünden okunabilir Markdown metni üretir.
    
    Args:
        analysis: scorer.analyze() çıktısı olan dict.
        
    Returns:
        Biçimlendirilmiş Markdown metni.
    """
    apk = analysis.get("apk_info", {})
    score = analysis.get("score", {})
    combos = analysis.get("combinations", [])
    cross = analysis.get("cross_check", {})

    app_name = apk.get("app_name", "Unknown")
    package = apk.get("package", "unknown.package")
    sha256 = apk.get("sha256", "N/A")
    now_utc = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    band = score.get("band", "Bilinmiyor")
    emoji = _band_emoji(band)

    md = []
    
    # 1) Başlık
    md.append(f"# APK İzin Risk Raporu — {app_name}\n")

    # 2) Uygulama Bilgileri
    md.append("## Uygulama Bilgileri")
    md.append("| Alan | Değer |")
    md.append("|------|-------|")
    md.append(f"| Paket | `{package}` |")
    md.append(f"| Uygulama Adı | {app_name} |")
    md.append(f"| SHA256 | `{sha256}` |")
    md.append(f"| Rapor Tarihi | {now_utc} |\n")

    # 3) Risk Özeti
    md.append("## Risk Özeti")
    md.append("| Metrik | Değer |")
    md.append("|--------|-------|")
    md.append(f"| Toplam Puan | **{score.get('total_score', 0)}** |")
    md.append(f"| Risk Bandı | {emoji} **{band}** |")
    md.append(f"| Tehlikeli İzin | {score.get('dangerous_count', 0)} |")
    md.append(f"| Normal İzin | {score.get('normal_count', 0)} |")
    md.append(f"| İmza İzni | {score.get('signature_count', 0)} |")
    md.append(f"| Bilinmeyen | {score.get('unknown_count', 0)} |\n")

    # 4) Tehlikeli Kombinasyonlar
    md.append("## Tehlikeli Kombinasyonlar")
    if not combos:
        md.append("> ✅ Bilinen tehlikeli kombinasyon tespit edilmedi.\n")
    else:
        for c in combos:
            r_emoji = _risk_emoji(c.get("risk", ""))
            md.append(f"- {r_emoji} **{c.get('ad', '')}** — {c.get('aciklama', '')} `[{c.get('risk', '')}]`")
        md.append("")

    # 5) İzin Dökümü
    md.append("## İzin Dökümü")
    md.append("| İzin | Seviye | Grup | Ağırlık |")
    md.append("|------|--------|------|---------|")
    
    breakdown = score.get("breakdown", [])
    if breakdown:
        for b in breakdown:
            md.append(f"| `{b.get('permission', '')}` | {b.get('level', '')} | {b.get('group', '')} | {b.get('weight', 0)} |")
    else:
        md.append("| - | - | - | - |")
    md.append("")

    # 6) Çapraz Doğrulama
    md.append("## Çapraz Doğrulama")
    if cross.get("apktool_available"):
        match = cross.get("match")
        if match:
            md.append("> ✅ apktool ile yapılan çapraz doğrulama başarılı: Fark yok.\n")
        else:
            md.append("> ❌ **apktool çapraz doğrulama UYUŞMAZLIĞI!**\n")
            only_andro = cross.get("only_in_androguard", [])
            only_apk = cross.get("only_in_apktool", [])
            
            if only_andro:
                md.append("**Yalnızca androguard'da bulunanlar:**")
                for p in only_andro:
                    md.append(f"- `{p}`")
            if only_apk:
                md.append("**Yalnızca apktool'da bulunanlar:**")
                for p in only_apk:
                    md.append(f"- `{p}`")
            md.append("")
    else:
        md.append("> ⚠️ apktool mevcut değil, çapraz doğrulama atlandı.\n")

    # 7) Footer
    md.append("---")
    md.append("*Bu rapor AndroidManifest İzin Denetçisi tarafından otomatik oluşturulmuştur.*\n")

    return "\n".join(md)


def save_reports(analysis: dict, output_dir: str) -> dict:
    """Hem MD hem de JSON formatında raporları kaydeder.
    
    Args:
        analysis: scorer.analyze() çıktısı.
        output_dir: Kayıt dizini (yoksa oluşturulur).
        
    Returns:
        {"md": "/tam/yol.md", "json": "/tam/yol.json"}
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        logger.info("Çıktı klasörü oluşturuldu: %s", output_dir)

    package = analysis.get("apk_info", {}).get("package", "unknown")
    # Dosya adında paket ismindeki geçersiz/noktalı karakterleri alt çizgiye çevir
    safe_pkg = re.sub(r'[^a-zA-Z0-9]', '_', package).strip('_')
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    base_name = f"{safe_pkg}_{timestamp}"
    
    md_path = os.path.join(output_dir, f"{base_name}.md")
    json_path = os.path.join(output_dir, f"{base_name}.json")

    # MD Kaydet
    md_content = render_markdown(analysis)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    logger.info("Markdown raporu kaydedildi: %s", md_path)

    # JSON Kaydet
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)
    logger.info("JSON raporu kaydedildi: %s", json_path)

    return {"md": md_path, "json": json_path}


def generate_report(analysis: dict, output_dir: str = "./reports") -> dict:
    """save_reports() çağrısını sarar, hata yakalar.
    
    Args:
        analysis: scorer.analyze() çıktısı.
        output_dir: Rapor dizini (varsayılan: ./reports).
        
    Returns:
        Oluşturulan dosya yollarının sözlüğü.
        
    Raises:
        Exception: Dosya yazma sırasında hata oluşursa.
    """
    try:
        paths = save_reports(analysis, output_dir)
        return paths
    except Exception as e:
        logger.error("Rapor üretilirken hata oluştu: %s", e)
        raise


# ---------------------------------------------------------------------------
# Smoke test
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import sys
    
    try:
        from parser import extract_permissions
        from scorer import analyze
    except ImportError:
        print("Uyarı: parser/scorer modülleri bulunamadı, import atlanıyor.")
        
    if len(sys.argv) < 2:
        print("Kullanım: python src/report.py <apk_dosyasi> [cikti_klasoru]")
        sys.exit(1)

    apk_path   = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "./reports"

    try:
        # Dummy test: Eğer extract_permissions vs import edildiyse kullan, 
        # aksi halde kod yapısı import edilmiş ve test edilmiş olur.
        result = generate_report(analyze(extract_permissions(apk_path)), output_dir)
        print("Rapor oluşturuldu:")
        print("  MD :", result["md"])
        print("  JSON:", result["json"])
    except Exception as e:
        print("Çalıştırma hatası:", e)
        sys.exit(1)
