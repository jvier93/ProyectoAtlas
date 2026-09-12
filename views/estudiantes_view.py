import flet as ft
from domain.services.estudiante_service import EstudianteService
from views.layout import ANCHO_TABLA, ESPACIADO_COLUMNAS


def construir_vista_estudiantes(page: ft.Page, abrir_crear: callable) -> ft.Column:
    """Construye la vista de estudiantes con sus acciones principales."""
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

    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Puntuación en lista")),
        ],
        rows=[],
        column_spacing=ESPACIADO_COLUMNAS,
        heading_row_color=ft.Colors.SURFACE,
        bgcolor=ft.Colors.SURFACE,
        width=ANCHO_TABLA,
    )

    def cargar_estudiantes():
        tabla.rows.clear()
        try:
            estudiantes = servicio.listar()
        except Exception:
            tabla.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("No se pudieron cargar los estudiantes.")),
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
            tabla.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("No hay estudiantes cargados.")),
                        ft.DataCell(ft.Text("")),
                    ]
                )
            )
            return

        for estudiante in estudiantes:
            tabla.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(estudiante.nombre)),
                        ft.DataCell(ft.Text(str(estudiante.puntuacionEnLista))),
                    ]
                )
            )

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
