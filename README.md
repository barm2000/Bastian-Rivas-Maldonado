# Bastián Rivas — Portafolio automatizado

Portafolio académico y profesional mantenible mediante carpetas y archivos de texto.

La versión visual corresponde a la etapa preliminar final del sitio. A partir de esta versión, **Proyectos, Producción científica y colaboraciones, Formación de capital humano y Cursos** se administran sin editar manualmente `index.html`.

## Flujo normal de mantención

1. Entra a `content/` y a la sección que quieras modificar.
2. Para agregar un elemento, copia la carpeta `_PLANTILLA`.
3. Completa su `info.txt` y agrega imágenes/GIF/videos cuando corresponda.
4. Sube los archivos a GitHub.
5. `.github/workflows/build-data.yml` ejecuta `scripts/build_data.py` y actualiza automáticamente `data/site-data.js` y `data/site-data.json`.
6. GitHub Pages publica el cambio normalmente.

**Para actualizar:** edita la carpeta existente.  
**Para eliminar:** elimina la carpeta completa.  
**No es necesario modificar el HTML para estas cuatro secciones.**

## Estructura

```text
Bastian-Rivas/
├── index.html
├── README.md
├── content/
│   ├── projects/
│   ├── production/
│   ├── formation/
│   └── courses/
├── data/
│   ├── site-data.js        # generado
│   └── site-data.json      # generado
├── scripts/
│   └── build_data.py
├── gifs/
│   └── qr.png
└── .github/
    └── workflows/
        └── build-data.yml
```

Consulta `content/README.md` para instrucciones de uso y las carpetas `_PLANTILLA` para ver los campos disponibles.

## Ejecutar el generador manualmente

```bash
python scripts/build_data.py
```

No usa paquetes externos; solo Python estándar.

## Logos estáticos

Si quieres conservar los logos reales de los laboratorios, agrega tus archivos actuales como:

- `gifs/logo.jpeg` — HydroGeoAI Lab
- `gifs/biospeq.png` — BioSpeQ

La interfaz tiene fallback si alguno aún no está presente.
