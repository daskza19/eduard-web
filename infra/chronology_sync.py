import os
import json
import shutil
import urllib.request
import urllib.parse

API_KEY        = os.environ["GOOGLE_CREDENTIALS"]
SPREADSHEET_ID = os.environ["SPREADSHEET_ID"]
SHEET_NAME     = "cronologia"
CHRONOLOGY_PATH  = "src/assets/chronology"
MANIFEST_PATH  = os.path.join(CHRONOLOGY_PATH, "manifest.json")

# ============ SHEETS ============
def fetch_events():
    url = (
        f"https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}"
        f"/values/{urllib.parse.quote(SHEET_NAME)}?key={API_KEY}"
    )
    with urllib.request.urlopen(url) as r:
        data = json.loads(r.read())
    rows   = data.get("values", [])
    if not rows:
        return []
    header = rows[0]
    return [dict(zip(header, row)) for row in rows[1:] if any(cell.strip() for cell in row)]


# ============ MAIN ============
def main():
    # Limpiar y recrear carpeta base
    if os.path.exists(CHRONOLOGY_PATH):
        shutil.rmtree(CHRONOLOGY_PATH)
        print(f"🗑️  Eliminada carpeta {CHRONOLOGY_PATH}")
    os.makedirs(CHRONOLOGY_PATH)
    print(f"📁 Creada carpeta {CHRONOLOGY_PATH}\n")

    # Leer sheet
    print(f"📊 Leyendo hoja '{SHEET_NAME}'...")
    rows = fetch_events()
    print(f"   {len(rows)} eventos encontrados en la cronologia\n")

    manifest = []

    for i, row in enumerate(rows, start=1):
        year  = row.get("ANY", "").strip()
        data      = row.get("DATA", "").strip()
        rol1 = row.get("ROL1", "").strip()
        rol2   = row.get("ROL2", "").strip()
        text       = row.get("TEXT", "").strip()
        sub_text = row.get("SUBTÍTOL", "").strip()
        color = row.get("COLOR", "").strip()
        link   = row.get("LINK", "").strip()

        if not year:
            print(f"[{i}] ⚠️  Fila sin ANY, saltando.")
            continue

        if not any(item["year"] == year for item in manifest):
            manifest.append({
                "year": year,
                "events": []
            })

        event_entry = {
            "data": data,
            "rol1": rol1,
            "rol2": rol2,
            "text": text,
            "sub_text": sub_text,
            "color": color,
            "link": link
        }

        year_entry = next(item for item in manifest if item["year"] == year)
        year_entry["events"].append(event_entry)

    # Guardar manifest
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print(f"✅ Manifest generado: {MANIFEST_PATH} ({len(manifest)} eventos)")


if __name__ == "__main__":
    main()