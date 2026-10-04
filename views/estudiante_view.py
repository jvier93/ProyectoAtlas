import flet as ft
from domain.services.cursada_service import CursadaService
from domain.services.estudiante_service import EstudianteService
from domain.services.practica_service import PracticaService
from views.layout import ANCHO_TABLA, ESPACIADO_COLUMNAS


def construir_vista_estudiante(
    page: ft.Page,
    estudiante_id: int,
    volver: callable,
    abrir_crear_cursada: callable,
    abrir_crear_practica: callable,
    abrir_practica: callable,
) -> ft.Column:
    """Construye la vista detallada de un estudiante con sus cursadas."""
    servicio_estudiantes = EstudianteService()
    servicio_cursadas = CursadaService()
    servicio_practicas = PracticaService()

    def mostrar_notificacion(mensaje: str, color: str):
        page.show_dialog(
            ft.SnackBar(
                ft.Text(mensaje),
                bgcolor=color,
                show_close_icon=True,
            )
        )
        page.update()

    try:
        estudiante = servicio_estudiantes.obtener_por_id(estudiante_id)
    except Exception:
        estudiante = None
        mostrar_notificacion(
            "Ocurrió un error al cargar el estudiante.",
            ft.Colors.ERROR,
        )

    try:
        cursadas = servicio_cursadas.listar_cursadas_de_estudiante(estudiante_id)
    except Exception:
        cursadas = []
        mostrar_notificacion(
            "Ocurrió un error al cargar las cursadas del estudiante.",
            ft.Colors.ERROR,
        )

    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Curso")),
            ft.DataColumn(ft.Text("Año")),
            ft.DataColumn(ft.Text("Docente de didáctica")),
            ft.DataColumn(ft.Text("Acciones")),
        ],
        rows=[],
        column_spacing=ESPACIADO_COLUMNAS,
        heading_row_color=ft.Colors.SURFACE,
        bgcolor=ft.Colors.SURFACE,
        width=ANCHO_TABLA,
    )

    if estudiante is None:
        return ft.Column(
            [
                ft.Text("Estudiante no encontrado", size=28, weight=ft.FontWeight.BOLD),
                ft.Text(
                    "No se pudo recuperar la información del estudiante solicitado.",
                    color=ft.Colors.SECONDARY,
                ),
                ft.TextButton("Volver a estudiantes", on_click=volver),
            ],
            spacing=18,
        )

    if not cursadas:
        tabla.rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text("No tiene cursadas registradas.")),
                    ft.DataCell(ft.Text("")),
                    ft.DataCell(ft.Text("")),
                    ft.DataCell(ft.Text("")),
                ]
            )
        )
    else:
        for cursada in cursadas:
            curso = getattr(cursada, "curso", None)
            docente = getattr(cursada, "docenteDidactica", None)
            curso_nombre = curso.nombre if curso is not None else "-"
            docente_nombre = docente.nombre if docente is not None else "-"
            practica = servicio_practicas.obtener_por_cursada_id(cursada.id)
            accion = ft.TextButton(
                "Administrar práctica" if practica is not None else "Crear práctica",
                on_click=(
                    lambda e, cursada=cursada, practica=practica: (
                        abrir_crear_practica(cursada)
                        if practica is None
                        else abrir_practica(practica.id, estudiante_id)
                    )
                ),
            )
            tabla.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(curso_nombre)),
                        ft.DataCell(ft.Text(str(cursada.anio))),
                        ft.DataCell(ft.Text(docente_nombre)),
                        ft.DataCell(accion),
                    ]
                )
            )

    return ft.Column(
        [
            ft.Row(
                [
                    ft.Column(
                        [
                            ft.Text("Estudiante", size=28, weight=ft.FontWeight.BOLD),
                            ft.Text(
                                "Detalle del estudiante seleccionado",
                                color=ft.Colors.SECONDARY,
                            ),
                        ],
                        spacing=3,
                        expand=True,
                    ),
                    ft.OutlinedButton(
                        "Volver a estudiantes",
                        icon=ft.Icons.ARROW_BACK,
                        on_click=volver,
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            ft.Divider(),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            "Datos del estudiante",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                        ),
                        ft.Row(
                            [
                                ft.Text("Nombre:"),
                                ft.Text(estudiante.nombre, weight=ft.FontWeight.BOLD),
                            ],
                            spacing=8,
                        ),
                        ft.Row(
                            [
                                ft.Text("Puntuación en lista:"),
                                ft.Text(
                                    str(estudiante.puntuacionEnLista),
                                    weight=ft.FontWeight.BOLD,
                                ),
                            ],
                            spacing=8,
                        ),
                    ],
                    spacing=12,
                ),
                padding=ft.Padding.all(18),
                bgcolor=ft.Colors.SURFACE,
            ),
            ft.Row(
                [
                    ft.Text(
                        "Cursadas",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.FilledButton(
                        "Crear cursada",
                        icon=ft.Icons.ADD,
                        on_click=lambda e: abrir_crear_cursada(estudiante_id),
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
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
