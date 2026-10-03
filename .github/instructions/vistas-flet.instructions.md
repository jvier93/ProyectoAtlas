---
applyTo: "views/*_view.py,main.py"
description: "Guía para crear y modificar vistas Flet y formularios de creación en ProyectoAtlas, siguiendo la separación entre interfaz, servicios de dominio y navegación."
---

# Vistas y formularios Flet de ProyectoAtlas

Usa estas pautas al crear o modificar pantallas y formularios. Mantén el estilo y las decisiones del código vecino; antes de asumir nombres de atributos o firmas, consulta el servicio y el modelo actuales.

## Responsabilidades y flujo

- Una vista presenta información y conecta controles con acciones. No implementes reglas de negocio ni accedas directamente a repositorios o archivos JSON desde la vista.
- Usa el servicio del dominio correspondiente para cargar, actualizar o eliminar entidades. Deja las validaciones y reglas de negocio en los servicios.
- Mantén la navegación fuera de la vista: recibe las acciones necesarias como callbacks desde `main.py` y asígnalas a los controles. No importes `main.py` ni dupliques su lógica de navegación.
- En el patrón actual, `main.py` coordina navegación y formularios generales; las vistas de listado y detalle construyen la pantalla y pueden gestionar acciones propias de esa pantalla, como confirmar una eliminación y refrescar la tabla.
- Las relaciones pueden ser opcionales. Comprueba valores `None` antes de leer atributos y usa las relaciones hidratadas que exponga el servicio; verifica su implementación si no está claro qué devuelve.

## Formularios de creación en `main.py`

- Sigue el patrón actual: una función `abrir_crear_<entidad>` prepara controles, define una función local `guardar` y reemplaza `contenido.content` por el formulario. Mantén la navegación y el envío coordinados desde `main.py`; no los muevas a una vista aparte salvo que la tarea lo pida.
- Usa los controles adecuados al dato: `ft.TextField` para texto o números, `ft.Dropdown` para opciones y `ft.Checkbox` para valores booleanos. Configura etiquetas claras y usa `autofocus=True` en el primer campo cuando encaje con el flujo existente.
- Para opciones, consulta los servicios correspondientes antes de construir el formulario y convierte los registros en `ft.DropdownOption(key=str(entidad.id), text=entidad.nombre)`. Verifica las firmas y atributos actuales en lugar de suponerlos.
- Si un selector depende de otro, carga y reemplaza sus opciones al cambiar el selector padre, limpia la selección anterior y deshabilita el selector dependiente cuando no haya una selección válida u opciones disponibles. Actualiza los campos derivados, como el docente asociado al grupo, y llama `page.update()` tras los cambios.
- Si faltan catálogos requeridos, informa cuáles no están disponibles y deshabilita el botón de guardar para evitar envíos incompletos. No des por válida una selección solo porque exista un primer elemento: el formulario debe reflejar el requisito real del servicio.
- En `guardar`, invoca el servicio con los valores de los controles. Captura `ValueError` para errores de validación conocidos y `Exception` para errores inesperados; muestra el error y conserva el formulario para corregir o reintentar.
- Solo después de guardar correctamente, navega mediante la función `abrir_<entidad>` correspondiente, muestra confirmación con `mostrar_notificacion` y usa colores semánticos. Mantén consistentes los callbacks de volver y guardar con las funciones de navegación existentes.
- En formularios con campos informativos no editables, usa controles deshabilitados y deriva sus valores de la entidad ya disponible; evita duplicar esos datos como entrada editable.
- Para eventos Flet, conserva las convenciones vigentes del proyecto (`on_click` para acciones y `on_select` en los desplegables existentes) y actualiza la página cuando cambie el estado visible de los controles.

## Estructura de la vista

- Expón una función `construir_vista_<entidad>(...)` que reciba `page` y solo los datos o callbacks que la pantalla necesita, y retorne el control raíz usado por las vistas vecinas (`ft.Column`). Conserva las firmas y convenciones existentes salvo que el nuevo flujo requiera un cambio.
- Importa `flet as ft`, el servicio usado y las constantes compartidas de `views.layout` cuando la pantalla tenga tablas.
- Para una pantalla de listado, sigue la jerarquía habitual: encabezado con título y descripción, acción principal, divisor y contenido. Para una pantalla de detalle, conserva el patrón de encabezado con acción para volver y secciones con la información relacionada.
- Usa `expand=True`, `spacing` y `ft.ScrollMode.AUTO` donde corresponda para que el contenido extenso pueda desplazarse dentro de la ventana existente.
- Mantén los textos y nombres de acciones en español, de acuerdo con las vistas actuales.

## Datos, estados y errores

- Carga los datos mediante el servicio al construir la vista. Si se puede recargar después de una acción, encapsula la carga en una función local que limpie y vuelva a poblar los controles.
- Maneja errores de carga y de acciones. Captura `ValueError` para comunicar errores de validación conocidos y usa un mensaje genérico para errores inesperados; no ocultes fallos mostrando datos parciales como si fueran correctos.
- Informa al usuario mediante `ft.SnackBar` con `page.show_dialog(...)` y luego actualiza la página, siguiendo el patrón existente. Usa colores semánticos como `ft.Colors.ERROR` y `ft.Colors.GREEN_700`.
- Representa explícitamente listas vacías y errores de carga en la interfaz. En una `ft.DataTable`, la fila informativa debe tener la misma cantidad de celdas que las columnas.
- Protege el acceso a relaciones opcionales con `getattr` o comprobaciones explícitas y muestra un valor de reemplazo comprensible cuando no exista el dato.
- Tras crear, actualizar o eliminar correctamente, refresca la vista o invoca el callback de navegación adecuado y muestra una confirmación. Si la operación falla, conserva la pantalla para que la persona pueda corregir o reintentar.

## Tablas y acciones

- Construye las columnas y filas de `ft.DataTable` en el mismo orden, reutilizando `ANCHO_TABLA` y `ESPACIADO_COLUMNAS` de `views.layout` cuando aplique.
- Conserva los colores de superficie usados por las tablas existentes (`ft.Colors.SURFACE`) y permite desplazamiento horizontal envolviendo la tabla en una columna con `scroll=ft.ScrollMode.AUTO`.
- Si una fila tiene acciones, usa controles Flet apropiados. Los botones de icono deben tener `tooltip` descriptivo.
- Al crear callbacks dentro de un bucle, captura los valores de esa fila como argumentos por defecto de `lambda` para evitar que todas las acciones usen el último registro.
- Antes de una acción destructiva, solicita confirmación con un diálogo modal; al cancelar o confirmar, cierra el diálogo. Después de confirmar y completar la operación, recarga los datos.

## Comprobación

- Antes de terminar, comprueba que los atributos y métodos llamados existan en los modelos y servicios actuales, que los callbacks coincidan con la forma en que `main.py` los invoca y que las filas informativas tengan el número correcto de celdas.
- Ejecuta una comprobación enfocada de sintaxis o diagnósticos para los módulos modificados. No cambies servicios, modelos ni navegación como parte de una vista salvo que el flujo lo requiera explícitamente.
