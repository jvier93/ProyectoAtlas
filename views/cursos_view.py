import flet as ft
from domain.services.curso_service import CursoService
from views.layout import ANCHO_TABLA, ESPACIADO_COLUMNAS


def construir_vista_cursos(page: ft.Page, abrir_crear: callable) -> ft.Column:
    """Construye la vista de cursos con sus acciones principales."""
    servicio = CursoService()

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
            ft.DataColumn(ft.Text("Requiere docente adscriptor")),
            ft.DataColumn(ft.Text("Requiere grupo")),
        ],
        rows=[],
        column_spacing=ESPACIADO_COLUMNAS,
        heading_row_color=ft.Colors.SURFACE,
        bgcolor=ft.Colors.SURFACE,
        width=ANCHO_TABLA,
    )

    def cargar_cursos():
        tabla.rows.clear()
        try:
            cursos = servicio.listar()
        except Exception:
            tabla.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("No se pudieron cargar los cursos.")),
                        ft.DataCell(ft.Text("")),
                        ft.DataCell(ft.Text("")),
                    ]
                )
            )
            mostrar_notificacion(
                "Ocurrió un error al cargar los cursos.",
                ft.Colors.ERROR,
            )
            return

        if not cursos:
            tabla.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("No hay cursos cargados.")),
                        ft.DataCell(ft.Text("")),
                        ft.DataCell(ft.Text("")),
                    ]
                )
            )
            return

        for curso in cursos:
            tabla.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(curso.nombre)),
                        ft.DataCell(
                            ft.Text("Sí" if curso.requiere_docente_adscriptor else "No")
                        ),
                        ft.DataCell(ft.Text("Sí" if curso.requiere_grupo else "No")),
                    ]
                )
            )

    cargar_cursos()

    return ft.Column(
        [
            ft.Row(
                [
                    ft.Column(
                        [
                            ft.Text("Cursos", size=28, weight=ft.FontWeight.BOLD),
                            ft.Text(
                                "Gestiona los cursos disponibles",
                                color=ft.Colors.SECONDARY,
                            ),
                        ],
                        spacing=3,
                        expand=True,
                    ),
                    ft.FilledButton(
                        "Crear curso",
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
