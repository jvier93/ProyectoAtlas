import flet as ft
from domain.services.estudiante_service import EstudianteService
from views.layout import ANCHO_TABLA, ESPACIADO_COLUMNAS


def construir_vista_estudiantes(
    page: ft.Page,
    abrir_crear: callable,
    abrir_administrar: callable = None,
    abrir_editar: callable = None,
) -> ft.Column:
    """Construye la vista principal de estudiantes con acciones."""
    servicio = EstudianteService()

    def mostrar_notificacion(mensaje: str, color: str):
        page.show_dialog(
            ft.SnackBar(
                ft.Text(mensaje),
                bgcolor=color,
                show_close_icon=True,
            )
        )
        page.update()

    def eliminar_estudiante(estudiante_id: int):
        try:
            servicio.eliminar(estudiante_id)
        except ValueError as error:
            mostrar_notificacion(
                f"No se pudo eliminar el estudiante: {error}",
                ft.Colors.ERROR,
            )
            return
        except Exception:
            mostrar_notificacion(
                "Ocurrió un error inesperado al eliminar el estudiante.",
                ft.Colors.ERROR,
            )
            return

        cargar_estudiantes()
        mostrar_notificacion(
            "Estudiante y sus datos asociados eliminados correctamente.",
            ft.Colors.GREEN_700,
        )

    def confirmar_eliminacion(estudiante_id: int, nombre: str):
        def cancelar(evento):
            page.pop_dialog()

        def confirmar(evento):
            page.pop_dialog()
            eliminar_estudiante(estudiante_id)

        page.show_dialog(
            ft.AlertDialog(
                modal=True,
                title=ft.Text("Eliminar estudiante"),
                content=ft.Text(
                    f'¿Seguro que deseas eliminar al estudiante "{nombre}"? '
                    "También se eliminarán sus cursadas, prácticas, asistencias "
                    "y visitas didácticas asociadas."
                ),
                actions=[
                    ft.TextButton("Cancelar", on_click=cancelar),
                    ft.TextButton(
                        "Eliminar",
                        on_click=confirmar,
                        style=ft.ButtonStyle(color=ft.Colors.ERROR),
                    ),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
        )

    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Puntuación en lista")),
            ft.DataColumn(ft.Text("Acciones")),
        ],
        rows=[],
        column_spacing=ESPACIADO_COLUMNAS,
        heading_row_color=ft.Colors.SURFACE,
        bgcolor=ft.Colors.SURFACE,
        width=ANCHO_TABLA,
    )
    busqueda = ft.TextField(
        label="Buscar por nombre",
        hint_text="Nombre del estudiante",
        expand=True,
    )

    def cargar_estudiantes():
        tabla.rows.clear()
        try:
            criterio = (busqueda.value or "").strip().casefold()
            if criterio:
                estudiantes = servicio.buscar(
                    lambda estudiante: estudiante.nombre.strip().casefold() == criterio
                )
            else:
                estudiantes = servicio.listar()
        except Exception:
            tabla.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("No se pudieron cargar los estudiantes.")),
                        ft.DataCell(ft.Text("")),
                        ft.DataCell(ft.Text("")),
                    ]
                )
            )
            mostrar_notificacion(
                "Ocurrió un error al cargar los estudiantes.",
                ft.Colors.ERROR,
            )
            return

        if not estudiantes:
            mensaje = (
                "No se encontraron estudiantes con ese nombre."
                if busqueda.value and busqueda.value.strip()
                else "No hay estudiantes cargados."
            )
            tabla.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(mensaje)),
                        ft.DataCell(ft.Text("")),
                        ft.DataCell(ft.Text("")),
                    ]
                )
            )
            return

        for estudiante in estudiantes:
            controles_accion = []
            if abrir_editar:
                controles_accion.append(
                    ft.IconButton(
                        icon=ft.Icons.EDIT_OUTLINED,
                        tooltip="Editar estudiante",
                        on_click=lambda e, id_estudiante=estudiante.id: abrir_editar(
                            id_estudiante
                        ),
                    )
                )
            controles_accion.extend(
                [
                    ft.TextButton(
                        "Administrar",
                        on_click=lambda e, id_estudiante=estudiante.id: (
                            abrir_administrar(id_estudiante)
                            if abrir_administrar
                            else None
                        ),
                    ),
                    ft.IconButton(
                        icon=ft.Icons.DELETE_OUTLINE,
                        tooltip="Eliminar estudiante",
                        icon_color=ft.Colors.ERROR,
                        on_click=lambda e, id_estudiante=estudiante.id, nombre=estudiante.nombre: (
                            confirmar_eliminacion(id_estudiante, nombre)
                        ),
                    ),
                ]
            )
            acciones = ft.Row(controles_accion, spacing=0)
            tabla.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(estudiante.nombre)),
                        ft.DataCell(ft.Text(str(estudiante.puntuacionEnLista))),
                        ft.DataCell(acciones),
                    ]
                )
            )

    cargar_estudiantes()

    def buscar_estudiantes(evento):
        cargar_estudiantes()

    return ft.Column(
        [
            ft.Row(
                [
                    ft.Column(
                        [
                            ft.Text("Estudiantes", size=28, weight=ft.FontWeight.BOLD),
                            ft.Text(
                                "Gestiona los estudiantes disponibles",
                                color=ft.Colors.SECONDARY,
                            ),
                        ],
                        spacing=3,
                        expand=True,
                    ),
                    ft.FilledButton(
                        "Crear estudiante",
                        icon=ft.Icons.ADD,
                        on_click=abrir_crear,
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            ft.Row(
                [
                    busqueda,
                    ft.TextButton(
                        "Buscar",
                        icon=ft.Icons.SEARCH,
                        on_click=buscar_estudiantes,
                    ),
                ],
                spacing=8,
            ),
            ft.Divider(),
            ft.Container(
                content=ft.Column(
                    [tabla],
                    expand=True,
                    scroll=ft.ScrollMode.AUTO,
                ),
                expand=True,
                bgcolor=ft.Colors.SURFACE,
            ),
        ],
        expand=True,
        spacing=18,
    )
