import os
import json
import shutil
import urllib.request
import urllib.parse

API_KEY        = os.environ["GOOGLE_CREDENTIALS"]
SPREADSHEET_ID = os.environ["SPREADSHEET_ID"]
SHEET_NAME     = "text"
TEXT_PATH  = "src/assets/text"
MANIFEST_PATH  = os.path.join(TEXT_PATH, "manifest.json")

# ============ SHEETS ============
def fetch_texts():
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
    if os.path.exists(TEXT_PATH):
        shutil.rmtree(TEXT_PATH)
        print(f"🗑️  Eliminada carpeta {TEXT_PATH}")
    os.makedirs(TEXT_PATH)
    print(f"📁 Creada carpeta {TEXT_PATH}\n")

    # Leer sheet
    print(f"📊 Leyendo hoja '{SHEET_NAME}'...")
    rows = fetch_texts()
    print(f"   {len(rows)} textos encontrados en la hoja '{SHEET_NAME}'\n")

    manifest = []

    for i, row in enumerate(rows, start=1):
        key  = row.get("KEY", "").strip()
        catalan      = row.get("CAT", "").strip()
        spanish = row.get("CAST", "").strip()
        english   = row.get("ENG", "").strip()

        if not key:
            print(f"[{i}] ⚠️  Fila sin KEY, saltando.")
            continue

        if not any(item["key"] == key for item in manifest):
            manifest.append({
                "key": key,
                "traductions": []
            })

        text_entry = {
            "catalan": catalan,
            "spanish": spanish,
            "english": english
        }

        key_entry = next(item for item in manifest if item["key"] == key)
        key_entry["traductions"].append(text_entry)

    # Guardar manifest
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print(f"✅ Manifest generado: {MANIFEST_PATH} ({len(manifest)} textos)")


if __name__ == "__main__":
    main()