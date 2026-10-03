import flet as ft
from domain.services.grupo_service import GrupoService
from views.layout import ANCHO_TABLA, ESPACIADO_COLUMNAS


def construir_vista_grupos(
    page: ft.Page,
    abrir_crear: callable,
    abrir_editar: callable = None,
) -> ft.Column:
    """Construye la vista de grupos con sus acciones principales."""
    servicio = GrupoService()

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
            ft.DataColumn(ft.Text("Docente")),
            ft.DataColumn(ft.Text("Institución")),
            ft.DataColumn(ft.Text("Horario")),
            ft.DataColumn(ft.Text("Acciones")),
        ],
        rows=[],
        column_spacing=ESPACIADO_COLUMNAS,
        heading_row_color=ft.Colors.SURFACE,
        bgcolor=ft.Colors.SURFACE,
        width=ANCHO_TABLA,
    )

    def cargar_grupos():
        tabla.rows.clear()
        try:
            grupos = servicio.listar()
        except Exception:
            tabla.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("No se pudieron cargar los grupos.")),
                        ft.DataCell(ft.Text("")),
                        ft.DataCell(ft.Text("")),
                        ft.DataCell(ft.Text("")),
                        ft.DataCell(ft.Text("")),
                    ]
                )
            )
            mostrar_notificacion(
                "Ocurrió un error al cargar los grupos.",
                ft.Colors.ERROR,
            )
            return

        if not grupos:
            tabla.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("No hay grupos cargados.")),
                        ft.DataCell(ft.Text("")),
                        ft.DataCell(ft.Text("")),
                        ft.DataCell(ft.Text("")),
                        ft.DataCell(ft.Text("")),
                    ]
                )
            )
            return

        for grupo in grupos:
            docente_nombre = (
                grupo.docente.nombre if getattr(grupo, "docente", None) else "-"
            )
            institucion_nombre = (
                grupo.institucion.nombre if getattr(grupo, "institucion", None) else "-"
            )
            acciones = (
                ft.IconButton(
                    icon=ft.Icons.EDIT_OUTLINED,
                    tooltip="Editar horario del grupo",
                    on_click=lambda e, id_grupo=grupo.id: abrir_editar(id_grupo),
                )
                if abrir_editar
                else ft.Text("")
            )
            tabla.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(grupo.nombre)),
                        ft.DataCell(ft.Text(docente_nombre)),
                        ft.DataCell(ft.Text(institucion_nombre)),
                        ft.DataCell(ft.Text(grupo.horario)),
                        ft.DataCell(acciones),
                    ]
                )
            )

    cargar_grupos()

    return ft.Column(
        [
            ft.Row(
                [
                    ft.Column(
                        [
                            ft.Text("Grupos", size=28, weight=ft.FontWeight.BOLD),
                            ft.Text(
                                "Gestiona los grupos disponibles",
                                color=ft.Colors.SECONDARY,
                            ),
                        ],
                        spacing=3,
                        expand=True,
                    ),
                    ft.FilledButton(
                        "Crear grupo",
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
