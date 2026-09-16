#!/usr/bin/env python3
from pathlib import Path
from urllib.parse import quote
import json, re, sys

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
DATA_DIR = ROOT / "data"
MEDIA_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".mp4", ".webm", ".mov"}
VIDEO_EXTS = {".mp4", ".webm", ".mov"}

ALIASES = {
    "title":"title", "titulo":"title",
    "label":"label", "etiqueta":"label",
    "summary":"summary", "resumen":"summary",
    "technologies":"technologies", "tecnologias":"technologies",
    "link":"link", "enlace":"link",
    "linktext":"linkText", "textoenlace":"linkText",
    "order":"order", "orden":"order",
    "placeholder":"placeholder",
    "cover":"cover", "portada":"cover",
    "type":"type", "tipo":"type",
    "role":"role", "rol":"role",
    "year":"year", "ano":"year", "año":"year",
    "date":"date", "fecha":"date",
    "datetext":"dateText", "fechatexto":"dateText",
    "authors":"authors", "autores":"authors",
    "source":"source", "fuente":"source",
    "details":"details", "detalles":"details",
    "student":"student", "estudiante":"student",
    "degree":"degree", "titulo_profesional":"degree", "programa":"degree",
    "institution":"institution", "institucion":"institution",
    "guide":"guide", "guia":"guide",
    "coguide":"coGuide", "coguia":"coGuide",
    "status":"status", "estado":"status",
    "platforms":"platforms", "plataformas":"platforms",
    "participants":"participants", "participantes":"participants",
}

def norm_key(key):
    k = key.strip().lower().replace(" ", "").replace("-", "_")
    return ALIASES.get(k, key.strip())

def parse_info(path):
    data = {}
    current = None
    for raw in path.read_text(encoding="utf-8-sig").splitlines():
        line = raw.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        m = re.match(r"^([^:]+):\s*(.*)$", line)
        if m:
            current = norm_key(m.group(1))
            data[current] = m.group(2).strip()
        elif current:
            extra = line.strip()
            data[current] = (str(data.get(current, "")) + " " + extra).strip()
    return data

def media_type(path):
    return "video" if path.suffix.lower() in VIDEO_EXTS else "image"

def web_path(path):
    rel = path.relative_to(ROOT).as_posix()
    return quote(rel, safe="/-_.~")

def collect_media(folder, requested_cover=""):
    files = sorted([p for p in folder.rglob("*") if p.is_file() and p.suffix.lower() in MEDIA_EXTS], key=lambda p: p.as_posix().lower())
    media = [{"src": web_path(p), "type": media_type(p), "name": p.name} for p in files]
    cover = None
    requested_cover = str(requested_cover or "").strip()
    if requested_cover:
        # Exact filename or path relative to folder.
        candidate = folder / requested_cover
        if candidate.exists() and candidate.is_file():
            cover = {"src": web_path(candidate), "type": media_type(candidate), "name": candidate.name}
        else:
            by_name = next((m for m in media if m["name"] == Path(requested_cover).name), None)
            if by_name: cover = by_name
            elif re.match(r"^(https?:|/|\.\.?/)", requested_cover):
                ext = Path(requested_cover.split("?")[0]).suffix.lower()
                cover = {"src": requested_cover, "type": "video" if ext in VIDEO_EXTS else "image", "name": Path(requested_cover).name}
            else:
                print(f"ADVERTENCIA: portada no encontrada: {folder.relative_to(ROOT)}/{requested_cover}", file=sys.stderr)
    if cover is None and media:
        cover = media[0]
    return media, cover

def as_int(value, default=0):
    try: return int(str(value).strip())
    except Exception: return default

def load_collection(name):
    base = CONTENT / name
    items = []
    if not base.exists(): return items
    for folder in sorted([p for p in base.iterdir() if p.is_dir() and not p.name.startswith(('_','.'))]):
        info = folder / "info.txt"
        if not info.exists():
            print(f"ADVERTENCIA: {folder.relative_to(ROOT)} no tiene info.txt; se omite.", file=sys.stderr)
            continue
        d = parse_info(info)
        if not d.get("title"):
            raise SystemExit(f"ERROR: falta Title/Titulo en {info.relative_to(ROOT)}")
        d["folder"] = folder.name
        d["order"] = as_int(d.get("order"), 9999)
        media, cover = collect_media(folder, d.get("cover", ""))
        d["media"] = media
        d["cover"] = cover
        if name == "courses": d["participants"] = max(0, as_int(d.get("participants"), 0))
        if name in {"production", "formation"}:
            d["year"] = str(d.get("year", "")).strip()
            d["date"] = str(d.get("date") or d.get("year") or "").strip()
        items.append(d)
    if name in {"production", "formation"}:
        items.sort(key=lambda x: (x.get("date", ""), -x.get("order",9999)), reverse=True)
    else:
        items.sort(key=lambda x: (x.get("order",9999), x.get("title","").lower()))
    return items

def validate(data):
    allowed_type = {"Publicación", "Proyecto"}
    allowed_prod_role = {"Autor", "Colaborador"}
    allowed_form_role = {"Guía", "Co-guía"}
    for x in data["production"]:
        if x.get("type") and x["type"] not in allowed_type:
            print(f"ADVERTENCIA: Type '{x['type']}' no estándar en production/{x['folder']}", file=sys.stderr)
        if x.get("role") and x["role"] not in allowed_prod_role:
            print(f"ADVERTENCIA: Role '{x['role']}' no estándar en production/{x['folder']}", file=sys.stderr)
    for x in data["formation"]:
        if x.get("role") and x["role"] not in allowed_form_role:
            print(f"ADVERTENCIA: Role '{x['role']}' no estándar en formation/{x['folder']}", file=sys.stderr)

def main():
    data = {
        "projects": load_collection("projects"),
        "production": load_collection("production"),
        "formation": load_collection("formation"),
        "courses": load_collection("courses"),
    }
    validate(data)
    DATA_DIR.mkdir(exist_ok=True)
    json_text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    (DATA_DIR / "site-data.json").write_text(json_text, encoding="utf-8")
    (DATA_DIR / "site-data.js").write_text("window.PORTFOLIO_DATA = " + json_text.rstrip() + ";\n", encoding="utf-8")
    print(f"OK: {len(data['projects'])} proyectos, {len(data['production'])} contribuciones, {len(data['formation'])} formación, {len(data['courses'])} cursos.")

if __name__ == "__main__": main()
