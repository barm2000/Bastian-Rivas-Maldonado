# Cómo mantener el portafolio

Toda la información editable vive aquí. No necesitas editar `index.html` para el mantenimiento normal.

## Archivos únicos

### `site/info.txt`
Configuración general del sitio.

### `profile/info.txt`
Portada: nombre, grado/subtítulo, descripción, etiquetas y botones.

## Secciones con carpetas

`memberships`, `knowledge`, `focus`, `projects`, `production`, `formation`, `tools`, `courses` y `contact` funcionan mediante carpetas.

Para agregar un elemento:
1. copia `_PLANTILLA`;
2. renombra la copia con un nombre simple;
3. completa `info.txt`;
4. agrega imágenes/GIF/videos si corresponde;
5. sube los cambios a GitHub.

Para actualizar: edita `info.txt` o reemplaza multimedia.
Para eliminar: borra la carpeta completa.

## Títulos e introducciones de secciones

Cada sección tiene `section.txt`. Ahí puedes cambiar `Kicker`, `Title` e `Intro` sin tocar HTML.

## Nombres de carpetas

El nombre de la carpeta no es el contenido visible. `01-`, `02-`, etc. sirven para organización humana. El orden mostrado se controla con `Order:`; Producción y Formación se ordenan principalmente por `Date:`/`Year:`.

Las carpetas cuyo nombre comienza con `_` o `.` no se publican.
