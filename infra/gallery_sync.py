import os
import json
import shutil
import urllib.request
import urllib.parse

API_KEY        = "AIzaSyAizMM5euwtLB9omhblTn3q7RSs_P0RUiA"  # os.environ["GOOGLE_CREDENTIALS"]
SPREADSHEET_ID = "1cEgsddgE9c729t-3AG4TizCH80BeLgwxjkHYfLH7fn0"  # os.environ["SPREADSHEET_ID"]
SHEET_NAME     = "projectes"
PROJECTS_PATH  = "src/assets/projects"
MANIFEST_PATH  = os.path.join(PROJECTS_PATH, "manifest.json")

# ============ SHEETS ============
def fetch_projects():
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


# ============ DRIVE HELPERS ============
def extract_file_id(url_or_id):
    """Extrae el file ID de una URL de Google Drive o lo devuelve tal cual."""
    if not url_or_id:
        return None
    if "drive.google.com" in url_or_id:
        if "/file/d/" in url_or_id:
            return url_or_id.split("/file/d/")[1].split("/")[0].split("?")[0]
        if "id=" in url_or_id:
            return url_or_id.split("id=")[1].split("&")[0]
    if "folders/" in url_or_id:
        return url_or_id.split("folders/")[1].split("?")[0]
    return url_or_id.strip()


def get_file_metadata(file_id):
    """Obtiene nombre y mimeType de un archivo de Drive."""
    url = (
        f"https://www.googleapis.com/drive/v3/files/{file_id}"
        f"?fields=name,mimeType&key={API_KEY}"
    )
    try:
        with urllib.request.urlopen(url) as r:
            return json.loads(r.read())
    except Exception as e:
        print(f"        ❌ Error obteniendo metadata de {file_id}: {e}")
        return {}


def get_extension(metadata):
    """Devuelve la extensión a partir del mimeType o nombre del archivo."""
    MIME_TO_EXT = {
        "image/jpeg":      ".jpg",
        "image/png":       ".png",
        "image/webp":      ".webp",
        "image/gif":       ".gif",
        "video/mp4":       ".mp4",
        "video/quicktime": ".mov",
        "video/x-msvideo": ".avi",
        "video/webm":      ".webm",
    }
    mime = metadata.get("mimeType", "")
    if mime in MIME_TO_EXT:
        return MIME_TO_EXT[mime]
    name = metadata.get("name", "")
    if "." in name:
        return "." + name.rsplit(".", 1)[-1].lower()
    return ""


def download_file(file_id, dest_path):
    """Descarga un archivo público de Drive."""
    url = f"https://www.googleapis.com/drive/v3/files/{file_id}?alt=media&key={API_KEY}"
    try:
        with urllib.request.urlopen(url) as r:
            with open(dest_path, "wb") as f:
                f.write(r.read())
        return True
    except Exception as e:
        print(f"        ❌ Error descargando {file_id}: {e}")
        return False


def list_folder_files(folder_id):
    """Lista todos los archivos de imagen/vídeo dentro de una carpeta de Drive."""
    ALLOWED_MIMES = [
        "image/jpeg", "image/png", "image/webp", "image/gif",
        "video/mp4", "video/quicktime", "video/x-msvideo", "video/webm",
    ]
    mime_filter = " or ".join([f"mimeType='{m}'" for m in ALLOWED_MIMES])
    query = f"'{folder_id}' in parents and ({mime_filter}) and trashed=false"
    url = (
        f"https://www.googleapis.com/drive/v3/files"
        f"?q={urllib.parse.quote(query)}"
        f"&fields=files(id,name,mimeType)"
        f"&pageSize=200"
        f"&key={API_KEY}"
    )
    try:
        with urllib.request.urlopen(url) as r:
            data = json.loads(r.read())
        return data.get("files", [])
    except Exception as e:
        print(f"        ❌ Error listando carpeta {folder_id}: {e}")
        return []


# ============ MAIN ============
def main():
    # Limpiar y recrear carpeta base
    if os.path.exists(PROJECTS_PATH):
        shutil.rmtree(PROJECTS_PATH)
        print(f"🗑️  Eliminada carpeta {PROJECTS_PATH}")
    os.makedirs(PROJECTS_PATH)
    print(f"📁 Creada carpeta {PROJECTS_PATH}\n")

    # Leer sheet
    print(f"📊 Leyendo hoja '{SHEET_NAME}'...")
    rows = fetch_projects()
    print(f"   {len(rows)} proyectos encontrados\n")

    manifest = []

    for i, row in enumerate(rows, start=1):
        categoria  = row.get("CATEGORIA", "").strip()
        titol      = row.get("TITOL", "").strip()
        tipografia = row.get("TIPOGRAFÍA TÍTOL", "").strip()
        subtitol   = row.get("SUBTITOL", "").strip()
        data       = row.get("DATA", "").strip()
        productora = row.get("PRODUCTORA", "").strip()
        rol        = row.get("ROL", "").strip()
        img_header = row.get("IMATGE CAPÇALERA (FORA)", "").strip()
        img_main   = row.get("IMATGE GRAN (DINS)", "").strip()
        video_type  = row.get("TIPO VIDEO", "").strip()
        video_url  = row.get("VIDEO", "").strip()
        carpeta    = row.get("LINK CARPETA AMB FOTOS", "").strip()

        if not titol:
            print(f"[{i}] ⚠️  Fila sin TITOL, saltando.")
            continue

        print(f"[{i}] 📂 {titol}")

        # Crear carpeta del proyecto y subcarpeta assets
        project_path = os.path.join(PROJECTS_PATH, titol)
        assets_path  = os.path.join(project_path, "assets")
        os.makedirs(assets_path, exist_ok=True)

        project_entry = {
            "categoria":  categoria  or None,
            "titol":      titol,
            "tipografia": tipografia or None,
            "subtitol":   subtitol   or None,
            "data":       data       or None,
            "productora": productora or None,
            "rol":        rol        or None,
            "header":     None,
            "main":       None,
            "video":      None,
            "assets":     [],
        }

        # Descargar imagen header
        header_id = extract_file_id(img_header)
        if header_id:
            meta = get_file_metadata(header_id)
            ext  = get_extension(meta)
            dest = os.path.join(project_path, f"header{ext}")
            if download_file(header_id, dest):
                project_entry["header"] = f"header{ext}"
                print(f"     🖼️  header{ext} descargada")
        else:
            print(f"     ⏭️  Sin imagen header")

        # Descargar imagen main
        main_id = extract_file_id(img_main)
        if main_id:
            meta = get_file_metadata(main_id)
            ext  = get_extension(meta)
            dest = os.path.join(project_path, f"main{ext}")
            if download_file(main_id, dest):
                project_entry["main"] = f"main{ext}"
                print(f"     🖼️  main{ext} descargada")
        else:
            print(f"     ⏭️  Sin imagen main")

        # Descargar vídeo
        project_entry["video_type"] = video_type
        if(video_type == "Intern"):
            video_id = extract_file_id(video_url)
            if video_id:
                meta = get_file_metadata(video_id)
                ext  = get_extension(meta)
                dest = os.path.join(project_path, f"video{ext}")
                if download_file(video_id, dest):
                    project_entry["video"] = f"video{ext}"
                    print(f"     🎬  video{ext} descargado")
            else:
                print(f"     ⏭️  Sin vídeo")
        else:
            project_entry["video"] = video_url
            print(f"     🎬  vídeo externo: {video_url}")

        # Descargar archivos de la carpeta assets
        folder_id = extract_file_id(carpeta)
        if folder_id:
            files = list_folder_files(folder_id)
            print(f"     📷 {len(files)} archivos en carpeta assets")
            for file in files:
                dest = os.path.join(assets_path, file["name"])
                if download_file(file["id"], dest):
                    project_entry["assets"].append(file["name"])
                    print(f"        ✅ {file['name']}")
        else:
            print(f"     ⏭️  Sin carpeta de assets")

        manifest.append(project_entry)
        print()

    # Guardar manifest
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print(f"✅ Manifest generado: {MANIFEST_PATH} ({len(manifest)} proyectos)")


if __name__ == "__main__":
    main()