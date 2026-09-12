import flet as ft
from domain.services.institucion_service import InstitucionService
from views.layout import ANCHO_TABLA, ESPACIADO_COLUMNAS


def construir_vista_instituciones(page: ft.Page, abrir_crear: callable) -> ft.Column:
    """Construye la vista de instituciones con sus acciones principales."""
    servicio = InstitucionService()

    def mostrar_notificacion(mensaje: str, color: str):
        page.show_dialog(
            ft.SnackBar(
                ft.Text(mensaje),
                bgcolor=color,
                show_close_icon=True,
            )
        )
        page.update()

    def eliminar_institucion(institucion_id: int):
        try:
            servicio.eliminar(institucion_id)
        except ValueError as error:
            mostrar_notificacion(
                f"No se pudo eliminar la institución: {error}",
                ft.Colors.ERROR,
            )
            return
        except Exception:
            mostrar_notificacion(
                "Ocurrió un error inesperado al eliminar la institución.",
                ft.Colors.ERROR,
            )
            return

        cargar_instituciones()
        mostrar_notificacion(
            "Institución eliminada correctamente.",
            ft.Colors.GREEN_700,
        )

    def confirmar_eliminacion(institucion_id: int, nombre: str):
        def cancelar(e):
            page.pop_dialog()

        def confirmar(e):
            page.pop_dialog()
            eliminar_institucion(institucion_id)

        page.show_dialog(
            ft.AlertDialog(
                modal=True,
                title=ft.Text("Eliminar institución"),
                content=ft.Text(
                    f'¿Seguro que deseas eliminar la institución "{nombre}"?'
                ),
                actions=[
                    ft.TextButton("Cancelar", on_click=cancelar),
                    ft.TextButton(
                        "Eliminar",
                        on_click=confirmar,
                        style=ft.ButtonStyle(
                            color=ft.Colors.ERROR,
                        ),
                    ),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
        )

    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Dirección")),
            ft.DataColumn(ft.Text("Acciones")),
        ],
        rows=[],
        column_spacing=ESPACIADO_COLUMNAS,
        heading_row_color=ft.Colors.SURFACE,
        bgcolor=ft.Colors.SURFACE,
        width=ANCHO_TABLA,
    )

    def cargar_instituciones():
        tabla.rows.clear()
        try:
            instituciones = servicio.listar()
        except Exception:
            tabla.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(
                            ft.Text("No se pudieron cargar las instituciones.")
                        ),
                        ft.DataCell(ft.Text("")),
                        ft.DataCell(ft.Text("")),
                    ]
                )
            )
            mostrar_notificacion(
                "Ocurrió un error al cargar las instituciones.",
                ft.Colors.ERROR,
            )
            return

        if not instituciones:
            tabla.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("No hay instituciones cargadas.")),
                        ft.DataCell(ft.Text("")),
                        ft.DataCell(ft.Text("")),
                    ]
                )
            )
            return

        for institucion in instituciones:
            acciones = ft.Row(
                [
                    ft.IconButton(
                        icon=ft.Icons.DELETE_OUTLINE,
                        tooltip="Eliminar institución",
                        icon_color=ft.Colors.ERROR,
                        on_click=lambda e, id=institucion.id, nombre=institucion.nombre: (
                            confirmar_eliminacion(id, nombre)
                        ),
                    ),
                ],
                spacing=0,
            )

            tabla.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(institucion.nombre)),
                        ft.DataCell(ft.Text(institucion.direccion)),
                        ft.DataCell(acciones),
                    ]
                )
            )

    cargar_instituciones()

    return ft.Column(
        [
            ft.Row(
                [
                    ft.Column(
                        [
                            ft.Text(
                                "Instituciones", size=28, weight=ft.FontWeight.BOLD
                            ),
                            ft.Text(
                                "Gestiona las instituciones disponibles",
                                color=ft.Colors.SECONDARY,
                            ),
                        ],
                        spacing=3,
                        expand=True,
                    ),
                    ft.FilledButton(
                        "Crear institución",
                        icon=ft.Icons.ADD,
                        on_click=abrir_crear,
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
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
