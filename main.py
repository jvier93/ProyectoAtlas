import flet as ft
from domain.services.curso_service import CursoService
from domain.services.docente_service import DocenteService
from domain.services.estudiante_service import EstudianteService
from domain.services.institucion_service import InstitucionService
from views.cursos_view import construir_vista_cursos
from views.docentes_view import construir_vista_docentes
from views.estudiantes_view import construir_vista_estudiantes
from views.instituciones_view import construir_vista_instituciones


def main(page: ft.Page):
    page.title = "ProyectoAtlas"
    page.padding = 0
    page.bgcolor = ft.Colors.SURFACE
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.window.width = 1100
    page.window.height = 700
    page.window.min_width = 1100
    page.window.max_width = 1100
    page.window.min_height = 700
    page.window.max_height = 700
    page.window.resizable = False
    page.window.maximizable = False

    contenido = ft.Container(expand=True, padding=ft.Padding.all(28))
    servicio_cursos = CursoService()
    servicio_docentes = DocenteService()
    servicio_estudiantes = EstudianteService()
    servicio_instituciones = InstitucionService()

    def mostrar_notificacion(mensaje: str, color: str = None):
        page.show_dialog(
            ft.SnackBar(
                ft.Text(mensaje),
                bgcolor=color,
                show_close_icon=True,
            )
        )
        page.update()

    def mostrar_pendiente(e):
        page.show_dialog(
            ft.SnackBar(ft.Text("Esta vista estará disponible próximamente"))
        )
        page.update()

    def abrir_crear_institucion(e):
        nombre = ft.TextField(label="Nombre", autofocus=True)
        direccion = ft.TextField(label="Dirección")

        def guardar(e):
            try:
                servicio_instituciones.crear(nombre.value, direccion.value)
            except ValueError as error:
                mostrar_notificacion(
                    f"No se pudo crear la institución: {error}",
                    ft.Colors.ERROR,
                )
                return
            except Exception:
                mostrar_notificacion(
                    "Ocurrió un error inesperado al crear la institución.",
                    ft.Colors.ERROR,
                )
                return

            abrir_instituciones()
            mostrar_notificacion(
                "Institución creada correctamente.",
                ft.Colors.GREEN_700,
            )

        contenido.content = ft.Column(
            [
                ft.Text("Crear institución", size=28, weight=ft.FontWeight.BOLD),
                ft.Text(
                    "Completa los datos de la institución",
                    color=ft.Colors.SECONDARY,
                ),
                nombre,
                direccion,
                ft.Row(
                    [
                        ft.TextButton(
                            "Volver a instituciones",
                            on_click=abrir_instituciones,
                        ),
                        ft.FilledButton(
                            "Guardar institución",
                            icon=ft.Icons.SAVE_OUTLINED,
                            on_click=guardar,
                        ),
                    ],
                    spacing=12,
                ),
            ],
            spacing=18,
        )
        page.update()

    def abrir_crear_estudiante(e):
        nombre = ft.TextField(label="Nombre", autofocus=True)
        puntuacion = ft.TextField(label="Puntuación en lista")

        def guardar(evento):
            try:
                servicio_estudiantes.crear(nombre.value, puntuacion.value)
            except ValueError as error:
                mostrar_notificacion(
                    f"No se pudo crear el estudiante: {error}",
                    ft.Colors.ERROR,
                )
                return
            except Exception:
                mostrar_notificacion(
                    "Ocurrió un error inesperado al crear el estudiante.",
                    ft.Colors.ERROR,
                )
                return

            abrir_estudiantes()
            mostrar_notificacion(
                "Estudiante creado correctamente.",
                ft.Colors.GREEN_700,
            )

        contenido.content = ft.Column(
            [
                ft.Text("Crear estudiante", size=28, weight=ft.FontWeight.BOLD),
                ft.Text(
                    "Completa los datos del estudiante",
                    color=ft.Colors.SECONDARY,
                ),
                nombre,
                puntuacion,
                ft.Row(
                    [
                        ft.TextButton(
                            "Volver a estudiantes",
                            on_click=abrir_estudiantes,
                        ),
                        ft.FilledButton(
                            "Guardar estudiante",
                            icon=ft.Icons.SAVE_OUTLINED,
                            on_click=guardar,
                        ),
                    ],
                    spacing=12,
                ),
            ],
            spacing=18,
        )
        page.update()

    def abrir_crear_docente(e):
        nombre = ft.TextField(label="Nombre", autofocus=True)
        tipo = ft.Dropdown(
            label="Tipo de docente",
            options=[
                ft.DropdownOption(key="general", text="general"),
                ft.DropdownOption(key="adscriptor", text="adscriptor"),
                ft.DropdownOption(key="didactica", text="didactica"),
            ],
            value="general",
        )

        def guardar(evento):
            try:
                servicio_docentes.crear(nombre.value, tipo.value)
            except ValueError as error:
                mostrar_notificacion(
                    f"No se pudo crear el docente: {error}",
                    ft.Colors.ERROR,
                )
                return
            except Exception:
                mostrar_notificacion(
                    "Ocurrió un error inesperado al crear el docente.",
                    ft.Colors.ERROR,
                )
                return

            abrir_docentes()
            mostrar_notificacion(
                "Docente creado correctamente.",
                ft.Colors.GREEN_700,
            )

        contenido.content = ft.Column(
            [
                ft.Text("Crear docente", size=28, weight=ft.FontWeight.BOLD),
                ft.Text(
                    "Completa los datos del docente",
                    color=ft.Colors.SECONDARY,
                ),
                nombre,
                tipo,
                ft.Row(
                    [
                        ft.TextButton(
                            "Volver a docentes",
                            on_click=abrir_docentes,
                        ),
                        ft.FilledButton(
                            "Guardar docente",
                            icon=ft.Icons.SAVE_OUTLINED,
                            on_click=guardar,
                        ),
                    ],
                    spacing=12,
                ),
            ],
            spacing=18,
        )
        page.update()

    def abrir_crear_curso(e):
        nombre = ft.TextField(label="Nombre", autofocus=True)
        requiere_docente_adscriptor = ft.Checkbox(label="Requiere docente adscriptor")
        requiere_grupo = ft.Checkbox(label="Requiere grupo")

        def guardar(evento):
            try:
                servicio_cursos.crear(
                    nombre.value,
                    requiere_docente_adscriptor.value,
                    requiere_grupo.value,
                )
            except ValueError as error:
                mostrar_notificacion(
                    f"No se pudo crear el curso: {error}",
                    ft.Colors.ERROR,
                )
                return
            except Exception:
                mostrar_notificacion(
                    "Ocurrió un error inesperado al crear el curso.",
                    ft.Colors.ERROR,
                )
                return

            abrir_cursos()
            mostrar_notificacion(
                "Curso creado correctamente.",
                ft.Colors.GREEN_700,
            )

        contenido.content = ft.Column(
            [
                ft.Text("Crear curso", size=28, weight=ft.FontWeight.BOLD),
                ft.Text(
                    "Completa los datos del curso",
                    color=ft.Colors.SECONDARY,
                ),
                nombre,
                requiere_docente_adscriptor,
                requiere_grupo,
                ft.Row(
                    [
                        ft.TextButton(
                            "Volver a cursos",
                            on_click=abrir_cursos,
                        ),
                        ft.FilledButton(
                            "Guardar curso",
                            icon=ft.Icons.SAVE_OUTLINED,
                            on_click=guardar,
                        ),
                    ],
                    spacing=12,
                ),
            ],
            spacing=18,
        )
        page.update()

    def abrir_instituciones(e=None):
        contenido.content = construir_vista_instituciones(page, abrir_crear_institucion)
        page.update()

    def abrir_estudiantes(e=None):
        contenido.content = construir_vista_estudiantes(page, abrir_crear_estudiante)
        page.update()

    def abrir_docentes(e=None):
        contenido.content = construir_vista_docentes(page, abrir_crear_docente)
        page.update()

    def abrir_cursos(e=None):
        contenido.content = construir_vista_cursos(page, abrir_crear_curso)
        page.update()

    navbar = ft.Container(
        content=ft.Row(
            [
                ft.Text("ProyectoAtlas", size=22, weight=ft.FontWeight.BOLD),
                ft.VerticalDivider(width=1),
                ft.TextButton("Instituciones", on_click=abrir_instituciones),
                ft.TextButton("Cursos", on_click=abrir_cursos),
                ft.TextButton("Docentes", on_click=abrir_docentes),
                ft.TextButton("Estudiantes", on_click=abrir_estudiantes),
            ],
            spacing=8,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.Padding.symmetric(horizontal=24, vertical=14),
        bgcolor=ft.Colors.SURFACE,
        border=ft.Border.only(bottom=ft.BorderSide(1, ft.Colors.OUTLINE)),
    )
    page.add(
        ft.Column(
            [navbar, contenido],
            expand=True,
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        )
    )
    abrir_instituciones()


ft.run(main)
