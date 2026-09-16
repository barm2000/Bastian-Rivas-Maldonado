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
    "title":"title", "titulo":"title", "name":"title", "nombre":"title",
    "label":"label", "etiqueta":"label",
    "summary":"summary", "resumen":"summary",
    "description":"description", "descripcion":"description",
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
    "kicker":"kicker", "intro":"intro",
    "keywords":"keywords", "palabrasclave":"keywords",
    "color":"color", "category":"category", "categoria":"category",
    "short":"short", "sigla":"short",
    "showinnavbar":"showInNavbar", "mostrarennavbar":"showInNavbar",
    "brand":"brand", "marca":"brand",
    "browsertitle":"browserTitle", "titulonavegador":"browserTitle",
    "metadescription":"metaDescription", "descripcionmeta":"metaDescription",
    "footername":"footerName", "nombrefinal":"footerName",
    "footertext":"footerText", "textofinal":"footerText",
    "eyebrow":"eyebrow",
    "nameline1":"nameLine1", "nombrelinea1":"nameLine1",
    "nameline2":"nameLine2", "nombrelinea2":"nameLine2",
    "subtitle":"subtitle", "subtitulo":"subtitle",
    "tags":"tags", "etiquetas":"tags",
    "primarytext":"primaryText", "textoprimario":"primaryText",
    "primarylink":"primaryLink", "enlaceprimario":"primaryLink",
    "secondarytext":"secondaryText", "textosecundario":"secondaryText",
    "secondarylink":"secondaryLink", "enlacesecundario":"secondaryLink",
    "qrimage":"qrImage", "imagenqr":"qrImage",
    "qrtitle":"qrTitle", "tituloqr":"qrTitle",
    "qrtext":"qrText", "textoqr":"qrText",
    "navknowledge":"navKnowledge",
    "navfocus":"navFocus",
    "navprojects":"navProjects",
    "navproduction":"navProduction",
    "navformation":"navFormation",
    "navtools":"navTools",
    "navcourses":"navCourses",
    "navcontact":"navContact",
}

def norm_key(key):
    k = key.strip().lower().replace(" ", "").replace("-", "_")
    return ALIASES.get(k, key.strip())

def parse_info(path):
    data = {}
    current = None
    if not path.exists():
        return data
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

def split_list(value):
    return [x.strip() for x in str(value or "").split(";") if x.strip()]

def as_bool(value, default=True):
    if value is None or str(value).strip() == "": return default
    return str(value).strip().lower() not in {"0","false","no","off","n"}

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

def resolve_media_ref(base, value):
    raw = str(value or "").strip()
    if not raw: return None
    candidate = base / raw
    if candidate.exists() and candidate.is_file():
        return {"src": web_path(candidate), "type": media_type(candidate), "name": candidate.name}
    if re.match(r"^(https?:|/|\.\.?/)", raw):
        ext = Path(raw.split("?")[0]).suffix.lower()
        return {"src": raw, "type": "video" if ext in VIDEO_EXTS else "image", "name": Path(raw).name}
    print(f"ADVERTENCIA: archivo multimedia no encontrado: {base.relative_to(ROOT)}/{raw}", file=sys.stderr)
    return None

def as_int(value, default=0):
    try: return int(str(value).strip())
    except Exception: return default

def load_singleton(name):
    d = parse_info(CONTENT / name / "info.txt")
    if name == "profile":
        d["tags"] = split_list(d.get("tags"))
    return d

def load_section(name):
    d = parse_info(CONTENT / name / "section.txt")
    if name == "contact" and d.get("qrImage"):
        d["qr"] = resolve_media_ref(CONTENT / name, d.get("qrImage"))
    return d

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
        if name == "knowledge": d["keywords"] = split_list(d.get("keywords"))
        if name == "memberships": d["showInNavbar"] = as_bool(d.get("showInNavbar"), True)
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
    collections = ["memberships","knowledge","focus","projects","production","formation","tools","courses","contact"]
    section_names = ["memberships","knowledge","focus","projects","production","formation","tools","courses","contact"]
    data = {
        "site": load_singleton("site"),
        "profile": load_singleton("profile"),
        "sections": {name: load_section(name) for name in section_names},
    }
    for name in collections:
        data[name] = load_collection(name)
    validate(data)
    DATA_DIR.mkdir(exist_ok=True)
    json_text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    (DATA_DIR / "site-data.json").write_text(json_text, encoding="utf-8")
    (DATA_DIR / "site-data.js").write_text("window.PORTFOLIO_DATA = " + json_text.rstrip() + ";\n", encoding="utf-8")
    print(
        "OK: "
        f"{len(data['memberships'])} membresías, {len(data['knowledge'])} áreas, {len(data['focus'])} enfoques, "
        f"{len(data['projects'])} proyectos, {len(data['production'])} contribuciones, {len(data['formation'])} formación, "
        f"{len(data['tools'])} herramientas, {len(data['courses'])} cursos, {len(data['contact'])} enlaces de contacto."
    )

if __name__ == "__main__": main()
