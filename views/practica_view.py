import flet as ft
from domain.models.practica import Practica
from domain.services.practica_service import PracticaService
from views.layout import ANCHO_TABLA, ESPACIADO_COLUMNAS


def construir_vista_practica(
    page: ft.Page,
    practica_id: int,
    volver: callable,
    crear_asistencia: callable,
    crear_visita: callable,
    finalizar_practica: callable,
) -> ft.Column:
    """Construye la vista detallada de una práctica."""
    servicio = PracticaService()

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
        practica = servicio.obtener_por_id(practica_id)
    except Exception:
        practica = None
        mostrar_notificacion(
            "Ocurrió un error al cargar la práctica.",
            ft.Colors.ERROR,
        )

    if practica is None:
        return ft.Column(
            [
                ft.Text("Práctica no encontrada", size=28, weight=ft.FontWeight.BOLD),
                ft.Text(
                    "No se pudo recuperar la información de la práctica solicitada.",
                    color=ft.Colors.SECONDARY,
                ),
                ft.TextButton("Volver al estudiante", on_click=volver),
            ],
            spacing=18,
        )

    cursada = getattr(practica, "cursada", None)
    curso = getattr(cursada, "curso", None)
    institucion = getattr(practica, "institucion", None)
    grupo = getattr(practica, "grupo", None)
    docente_didactica = getattr(practica, "docenteDidactica", None)
    docente_adscriptor = getattr(practica, "docenteAdscriptor", None)

    def nombre(entidad):
        return getattr(entidad, "nombre", "-") if entidad is not None else "-"

    def valor(valor_actual):
        return (
            "-"
            if valor_actual is None or str(valor_actual).strip() == ""
            else str(valor_actual)
        )

    tabla_asistencias = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Fecha")),
            ft.DataColumn(ft.Text("Estado")),
            ft.DataColumn(ft.Text("Observaciones")),
        ],
        rows=[],
        column_spacing=ESPACIADO_COLUMNAS,
        heading_row_color=ft.Colors.SURFACE,
        bgcolor=ft.Colors.SURFACE,
        width=ANCHO_TABLA,
    )

    asistencias = practica.asistencias
    if not asistencias:
        tabla_asistencias.rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text("No hay asistencias registradas.")),
                    ft.DataCell(ft.Text("")),
                    ft.DataCell(ft.Text("")),
                ]
            )
        )
    else:
        for asistencia in asistencias:
            tabla_asistencias.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(valor(asistencia.fecha))),
                        ft.DataCell(ft.Text(valor(asistencia.estado))),
                        ft.DataCell(ft.Text(valor(asistencia.observaciones))),
                    ]
                )
            )

    tabla_visitas = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Fecha")),
            ft.DataColumn(ft.Text("Nota")),
            ft.DataColumn(ft.Text("Docente extra")),
            ft.DataColumn(ft.Text("Observaciones")),
        ],
        rows=[],
        column_spacing=ESPACIADO_COLUMNAS,
        heading_row_color=ft.Colors.SURFACE,
        bgcolor=ft.Colors.SURFACE,
        width=ANCHO_TABLA,
    )

    visitas = practica.visitasDidacticas
    if not visitas:
        tabla_visitas.rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text("No hay visitas registradas.")),
                    ft.DataCell(ft.Text("")),
                    ft.DataCell(ft.Text("")),
                    ft.DataCell(ft.Text("")),
                ]
            )
        )
    else:
        for visita in visitas:
            tabla_visitas.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(valor(visita.fecha))),
                        ft.DataCell(ft.Text(valor(visita.nota))),
                        ft.DataCell(ft.Text(nombre(visita.docenteExtra))),
                        ft.DataCell(ft.Text(valor(visita.observaciones))),
                    ]
                )
            )

    datos_practica = ft.Container(
        content=ft.Column(
            [
                ft.Text("Datos de la práctica", size=18, weight=ft.FontWeight.BOLD),
                ft.Row(
                    [
                        ft.Text("Curso:"),
                        ft.Text(nombre(curso), weight=ft.FontWeight.BOLD),
                        ft.Text("Año:"),
                        ft.Text(
                            valor(getattr(cursada, "anio", None)),
                            weight=ft.FontWeight.BOLD,
                        ),
                    ],
                    spacing=8,
                ),
                ft.Row(
                    [
                        ft.Text("Institución:"),
                        ft.Text(nombre(institucion), weight=ft.FontWeight.BOLD),
                        ft.Text("Grupo:"),
                        ft.Text(nombre(grupo), weight=ft.FontWeight.BOLD),
                    ],
                    spacing=8,
                ),
                ft.Row(
                    [
                        ft.Text("Docente de didáctica:"),
                        ft.Text(nombre(docente_didactica), weight=ft.FontWeight.BOLD),
                        ft.Text("Docente adscriptor:"),
                        ft.Text(nombre(docente_adscriptor), weight=ft.FontWeight.BOLD),
                    ],
                    spacing=8,
                ),
                ft.Row(
                    [
                        ft.Text("Estado:"),
                        ft.Text(valor(practica.estado), weight=ft.FontWeight.BOLD),
                        ft.Text("Nota final:"),
                        ft.Text(valor(practica.notaFinal), weight=ft.FontWeight.BOLD),
                    ],
                    spacing=8,
                ),
                ft.Row(
                    [
                        ft.Text("Observaciones:"),
                        ft.Text(
                            valor(practica.observaciones), weight=ft.FontWeight.BOLD
                        ),
                    ],
                    spacing=8,
                ),
            ],
            spacing=12,
        ),
        padding=ft.Padding.all(18),
        bgcolor=ft.Colors.SURFACE,
    )

    botones_encabezado = [
        ft.OutlinedButton(
            "Volver al estudiante",
            icon=ft.Icons.ARROW_BACK,
            on_click=volver,
        )
    ]
    if practica.estado == Practica.ESTADO_EN_CURSO:
        botones_encabezado.append(
            ft.FilledButton(
                "Finalizar práctica",
                icon=ft.Icons.CHECK,
                on_click=finalizar_practica,
            )
        )

    return ft.Column(
        [
            ft.Row(
                [
                    ft.Column(
                        [
                            ft.Text(
                                "Administrar práctica",
                                size=28,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Text(
                                "Consulta los datos y el seguimiento de la práctica",
                                color=ft.Colors.SECONDARY,
                            ),
                        ],
                        spacing=3,
                        expand=True,
                    ),
                    *botones_encabezado,
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            ft.Divider(),
            datos_practica,
            ft.Row(
                [
                    ft.Text("Asistencias", size=20, weight=ft.FontWeight.BOLD),
                    ft.FilledButton(
                        "Crear asistencia",
                        icon=ft.Icons.ADD,
                        on_click=crear_asistencia,
                        disabled=practica.estado == Practica.ESTADO_FINALIZADA,
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            ft.Container(
                content=ft.Column(
                    [tabla_asistencias],
                    scroll=ft.ScrollMode.AUTO,
                ),
                bgcolor=ft.Colors.SURFACE,
            ),
            ft.Row(
                [
                    ft.Text("Visitas didácticas", size=20, weight=ft.FontWeight.BOLD),
                    ft.FilledButton(
                        "Crear visita didáctica",
                        icon=ft.Icons.ADD,
                        on_click=crear_visita,
                        disabled=(
                            practica.estado == Practica.ESTADO_FINALIZADA
                            or not getattr(curso, "requiere_grupo", False)
                        ),
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            ft.Container(
                content=ft.Column(
                    [tabla_visitas],
                    scroll=ft.ScrollMode.AUTO,
                ),
                bgcolor=ft.Colors.SURFACE,
            ),
        ],
        expand=True,
        spacing=18,
        scroll=ft.ScrollMode.AUTO,
    )
