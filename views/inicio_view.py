import flet as ft


def construir_vista_inicio(
    abrir_instituciones: callable,
    abrir_cursos: callable,
    abrir_docentes: callable,
    abrir_grupos: callable,
    abrir_estudiantes: callable,
) -> ft.Column:
    """Construye la guía inicial y accesos directos de ProyectoAtlas."""

    def paso(numero: int, titulo: str, descripcion: str) -> ft.Row:
        return ft.Row(
            [
                ft.Text(
                    f"{numero:02}",
                    width=38,
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.PRIMARY,
                ),
                ft.Column(
                    [
                        ft.Text(titulo, weight=ft.FontWeight.BOLD),
                        ft.Text(descripcion, color=ft.Colors.SECONDARY),
                    ],
                    spacing=3,
                    expand=True,
                ),
            ],
            vertical_alignment=ft.CrossAxisAlignment.START,
        )

    accesos = ft.Row(
        [
            ft.TextButton(
                "Instituciones",
                icon=ft.Icons.ACCOUNT_BALANCE,
                on_click=abrir_instituciones,
            ),
            ft.TextButton(
                "Cursos",
                icon=ft.Icons.MENU_BOOK,
                on_click=abrir_cursos,
            ),
            ft.TextButton(
                "Docentes",
                icon=ft.Icons.CAST_FOR_EDUCATION,
                on_click=abrir_docentes,
            ),
            ft.TextButton(
                "Grupos",
                icon=ft.Icons.GROUPS,
                on_click=abrir_grupos,
            ),
            ft.TextButton(
                "Estudiantes",
                icon=ft.Icons.SCHOOL,
                on_click=abrir_estudiantes,
            ),
        ],
        spacing=8,
        run_spacing=4,
        wrap=True,
    )

    return ft.Column(
        [
            ft.Text("Bienvenido a ProyectoAtlas", size=28, weight=ft.FontWeight.BOLD),
            ft.Text(
                "Guía rápida para organizar cursadas y dar seguimiento a las prácticas.",
                color=ft.Colors.SECONDARY,
            ),
            ft.Divider(),
            ft.Text("Accesos directos", size=18, weight=ft.FontWeight.BOLD),
            accesos,
            ft.Divider(),
            ft.Text("Flujo de trabajo", size=20, weight=ft.FontWeight.BOLD),
            paso(
                1,
                "Prepara los catálogos",
                "Registra instituciones, cursos y docentes. Crea grupos asociados a una "
                "institución y asigna un docente adscriptor cuando corresponda.",
            ),
            paso(
                2,
                "Registra al estudiante",
                "Crea el estudiante con su puntuación en lista y abre su ficha para "
                "gestionar sus cursadas.",
            ),
            paso(
                3,
                "Agrega una cursada",
                "En la ficha del estudiante, registra el curso, el año y el docente "
                "de didáctica.",
            ),
            paso(
                4,
                "Crea la práctica",
                "Desde la cursada, selecciona una institución y, si el curso lo requiere, "
                "un grupo. Cuando también requiera docente adscriptor, el grupo debe tener "
                "uno. Si no tiene cupo, la práctica queda en espera.",
            ),
            paso(
                5,
                "Haz el seguimiento",
                "Registra asistencias y, para cursos que requieren grupo, visitas "
                "didácticas. Al terminar, finaliza la práctica con su nota final.",
            ),
        ],
        expand=True,
        spacing=14,
        scroll=ft.ScrollMode.AUTO,
    )
