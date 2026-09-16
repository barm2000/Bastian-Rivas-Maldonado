# Contenido automático

Estas cuatro carpetas controlan las secciones dinámicas del portafolio:

- `projects/` → Investigación y desarrollo.
- `production/` → Producción científica y colaboraciones.
- `formation/` → Formación de capital humano.
- `courses/` → Cursos y formación.

## Regla principal

Cada elemento es **una carpeta** y dentro debe existir `info.txt`.

Las carpetas cuyo nombre comienza con `_` se ignoran, por eso `_PLANTILLA` puede permanecer siempre dentro de cada sección.

## Agregar

1. Duplica `_PLANTILLA`.
2. Renombra la copia con un nombre simple, por ejemplo `nuevo-proyecto`.
3. Completa `info.txt`.
4. Agrega imágenes/GIF/videos dentro de la misma carpeta cuando corresponda.
5. Sube los cambios a GitHub en `main`.

La Action reconstruye y publica automáticamente la página. No necesitas ejecutar el script a mano en GitHub.

## Actualizar

Edita `info.txt`, reemplaza una portada, agrega multimedia o cambia cualquier campo y sube el cambio.

## Eliminar

Elimina la carpeta completa del elemento y sube el cambio. En la siguiente ejecución automática desaparecerá de la página.

## Multimedia

Formatos admitidos: JPG, JPEG, PNG, WEBP, GIF, MP4, WEBM y MOV.

- `Cover: archivo.jpg` fuerza una portada específica.
- Si `Cover:` queda vacío, se utiliza el primer archivo multimedia detectado.
- Los archivos se buscan dentro de la carpeta del elemento, incluso en subcarpetas.
- Las rutas se generan automáticamente; no tienes que mover la imagen a `gifs/`.
- En Linux/GitHub conviene respetar exactamente mayúsculas y minúsculas del nombre del archivo.

### Ejemplo

```text
content/projects/01-hydrogeoai-lab/
├── info.txt
└── logo.jpeg
```

```text
Title: HydroGeoAI Lab
Cover: logo.jpeg
```

Al subir ambos archivos, el workflow detecta `logo.jpeg`, reconstruye `data/site-data.js` y vuelve a desplegar GitHub Pages automáticamente.
