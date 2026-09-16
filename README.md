# Bastián Rivas Maldonado — Portafolio automatizado

Esta versión separa por completo **contenido** y **diseño**.

- `index.html`: diseño y funcionamiento. En mantención normal **no se edita**.
- `content/`: toda la información visible del portafolio.
- `scripts/build_data.py`: detecta carpetas, `info.txt`, imágenes, GIF y videos.
- `data/`: datos generados automáticamente.
- `.github/workflows/update-site.yml`: actualiza y publica GitHub Pages automáticamente en cada `push` a `main`.

## Regla principal

Para agregar, actualizar o eliminar información, trabaja dentro de `content/`.

Los nombres de las carpetas (`01-...`, `02-...`) son principalmente para mantener ordenado el repositorio. El contenido de la web lo determina `info.txt`. Para controlar el orden visual usa `Order:`. Las carpetas que comienzan con `_` o `.` se ignoran, por eso `_PLANTILLA` nunca aparece en la web.

## Secciones automatizadas

- `content/site/info.txt` — título del navegador, marca y pie de página.
- `content/profile/info.txt` — nombre, subtítulo, descripción, etiquetas y botones de portada.
- `content/memberships/` — laboratorios, universidades, grupos o centros y sus logos.
- `content/knowledge/` — áreas de conocimiento y palabras clave.
- `content/focus/` — problemas/enfoques que puedes abordar.
- `content/projects/` — proyectos, imágenes, GIF y videos.
- `content/production/` — publicaciones y colaboraciones/proyectos.
- `content/formation/` — guía/co-guía de tesis y trabajos.
- `content/tools/` — software, lenguajes y plataformas.
- `content/courses/` — cursos, portadas y número de participantes.
- `content/contact/` — perfiles/enlaces de contacto y QR.

Cada sección de colección contiene `_PLANTILLA/`. Cópiala para crear un registro nuevo.

## Multimedia

En `memberships`, `projects` y `courses` puedes colocar archivos directamente dentro de la carpeta del registro. Formatos reconocidos:

`JPG · JPEG · PNG · WEBP · GIF · MP4 · WEBM · MOV`

Usa `Cover: archivo.ext` para elegir la portada. Si `Cover:` queda vacío, se usa automáticamente el primer archivo multimedia encontrado.

## Actualización automática

1. Agrega, modifica o elimina contenido en `content/`.
2. Haz commit/push a la rama `main` (incluido subir archivos desde la web de GitHub).
3. GitHub Actions ejecuta `python scripts/build_data.py`.
4. Se regeneran `data/site-data.js` y `data/site-data.json`.
5. GitHub Pages publica automáticamente el sitio actualizado.

En GitHub, configura una sola vez: **Settings → Pages → Source → GitHub Actions**.

## Prueba local

```bash
python scripts/build_data.py
python -m http.server 8000
```

Luego abre `http://localhost:8000`.
