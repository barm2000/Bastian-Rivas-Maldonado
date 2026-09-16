# Contenido automático

Estas cuatro carpetas controlan las secciones que cambian con el tiempo:

- `projects/` → Investigación y desarrollo.
- `production/` → Producción científica y colaboraciones.
- `formation/` → Formación de capital humano.
- `courses/` → Cursos y formación.

## Regla principal

Cada elemento es **una carpeta**. Dentro de ella debe existir un archivo `info.txt`. En proyectos y cursos puedes poner además imágenes, GIF o videos en la misma carpeta.

Las carpetas cuyo nombre comienza con `_` se ignoran, por eso `_PLANTILLA` sirve como modelo.

### Agregar
1. Duplica `_PLANTILLA`.
2. Renombra la copia con un nombre simple, idealmente minúsculas y guiones, sin tildes: `nuevo-proyecto`.
3. Completa `info.txt`.
4. Agrega la portada o multimedia si corresponde.
5. Sube los cambios a GitHub. La Action reconstruye los datos automáticamente.

### Actualizar
Edita `info.txt`, reemplaza/agrega multimedia y sube los cambios. No toques `index.html`.

### Eliminar
Borra la carpeta completa del elemento y sube el cambio. Desaparecerá de la página en la próxima reconstrucción.

## Multimedia
Formatos admitidos: JPG, JPEG, PNG, WEBP, GIF, MP4, WEBM y MOV.

- Si escribes `Cover: archivo.jpg`, ese archivo se usa como portada.
- Si `Cover:` no existe, se usa el primer archivo multimedia encontrado.
- Puedes guardar más de un archivo multimedia; el generador los conserva en `data/site-data.json`, aunque la tarjeta principal usa la portada.
