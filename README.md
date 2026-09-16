# Bastián Rivas — Portafolio automatizado

Portafolio académico y profesional mantenible mediante carpetas y archivos `info.txt`.

La parte visual queda en `index.html`, pero las secciones que cambian con el tiempo se administran sin editar manualmente el HTML:

- Proyectos / Investigación y desarrollo.
- Producción científica y colaboraciones.
- Formación de capital humano.
- Cursos y formación.

## Cómo funciona

Cada elemento es una carpeta dentro de `content/`. El archivo `scripts/build_data.py` recorre esas carpetas, lee los `info.txt`, detecta imágenes/GIF/videos y genera automáticamente:

- `data/site-data.js`
- `data/site-data.json`

La web usa esos datos para construir tarjetas, filtros, contadores y carruseles.

## Flujo normal de mantención

1. Entra en `content/` y abre la sección que quieras modificar.
2. Para agregar un elemento, copia la carpeta `_PLANTILLA`.
3. Renombra la copia y completa `info.txt`.
4. Agrega imágenes, GIF o videos dentro de esa misma carpeta si corresponde.
5. Sube los cambios a GitHub.
6. La Action `.github/workflows/update-site.yml` se ejecuta en **cada push a `main`**, regenera los datos y despliega el sitio actualizado en GitHub Pages.

**Actualizar:** edita `info.txt` o reemplaza/agrega multimedia.  
**Eliminar:** elimina la carpeta completa.  
**No necesitas editar `index.html` para estas cuatro secciones.**

## Configuración de GitHub Pages — una sola vez

Para que el despliegue automático funcione con el workflow incluido:

1. En el repositorio abre `Settings`.
2. Entra en `Pages`.
3. En `Build and deployment` → `Source`, selecciona **GitHub Actions**.

Después de eso, cada vez que subas o modifiques archivos en `main`, GitHub reconstruirá y publicará automáticamente el sitio.

## Multimedia en Proyectos y Cursos

Formatos detectados automáticamente:

- JPG / JPEG
- PNG
- WEBP
- GIF
- MP4
- WEBM
- MOV

Ejemplo:

```text
content/projects/01-hydrogeoai-lab/
├── info.txt
└── logo.jpeg
```

Si `info.txt` contiene:

```text
Cover: logo.jpeg
```

esa imagen será la portada. Si `Cover:` está vacío, el generador utiliza automáticamente el primer archivo multimedia disponible.

Con varios archivos:

```text
content/projects/04-reconstruccion-3d/
├── info.txt
├── portada.jpg
├── sfm.gif
├── mvs.gif
└── resultado.mp4
```

puedes seleccionar explícitamente:

```text
Cover: portada.jpg
```

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
│   ├── site-data.js
│   └── site-data.json
├── scripts/
│   └── build_data.py
├── gifs/
│   ├── logo.jpeg
│   ├── biospeq.png
│   └── qr.png
└── .github/
    └── workflows/
        └── update-site.yml
```

Consulta `content/README.md` para los campos de cada sección.

## Ejecutar localmente

El generador no requiere paquetes externos:

```bash
python scripts/build_data.py
```

Después puedes abrir `index.html` mediante un servidor local, por ejemplo:

```bash
python -m http.server 8000
```
