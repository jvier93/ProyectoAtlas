import math
import flet as ft
from domain.models.asistencia import Asistencia
from domain.services.curso_service import CursoService
from domain.services.cursada_service import CursadaService
from domain.services.docente_service import DocenteService
from domain.services.estudiante_service import EstudianteService
from domain.services.grupo_service import GrupoService
from domain.services.institucion_service import InstitucionService
from domain.services.practica_service import PracticaService
from views.cursos_view import construir_vista_cursos
from views.docentes_view import construir_vista_docentes
from views.estudiante_view import construir_vista_estudiante
from views.estudiantes_view import construir_vista_estudiantes
from views.grupos_view import construir_vista_grupos
from views.inicio_view import construir_vista_inicio
from views.instituciones_view import construir_vista_instituciones
from views.practica_view import construir_vista_practica


def main(page: ft.Page):
    page.title = "ProyectoAtlas"
    page.window.icon = "assets/icon.png"
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
    servicio_cursadas = CursadaService()
    servicio_docentes = DocenteService()
    servicio_estudiantes = EstudianteService()
    servicio_grupos = GrupoService()
    servicio_instituciones = InstitucionService()
    servicio_practicas = PracticaService()

    def mostrar_notificacion(mensaje: str, color: str = None):
        page.show_dialog(
            ft.SnackBar(
                ft.Text(mensaje),
                bgcolor=color,
                show_close_icon=True,
            )
        )
        page.update()

    def abrir_formulario_institucion(institucion=None):
        es_edicion = institucion is not None
        nombre = ft.TextField(
            label="Nombre",
            value=institucion.nombre if es_edicion else None,
            autofocus=True,
        )
        direccion = ft.TextField(
            label="Dirección",
            value=institucion.direccion if es_edicion else None,
        )

        def guardar(e):
            try:
                if es_edicion:
                    servicio_instituciones.actualizar(
                        institucion.id,
                        nombre.value,
                        direccion.value,
                    )
                else:
                    servicio_instituciones.crear(nombre.value, direccion.value)
            except ValueError as error:
                mostrar_notificacion(
                    f"No se pudo {'actualizar' if es_edicion else 'crear'} la institución: {error}",
                    ft.Colors.ERROR,
                )
                return
            except Exception:
                mostrar_notificacion(
                    "Ocurrió un error inesperado al guardar la institución.",
                    ft.Colors.ERROR,
                )
                return

            abrir_instituciones()
            mostrar_notificacion(
                (
                    "Institución actualizada correctamente."
                    if es_edicion
                    else "Institución creada correctamente."
                ),
                ft.Colors.GREEN_700,
            )

        contenido.content = ft.Column(
            [
                ft.Text(
                    "Editar institución" if es_edicion else "Crear institución",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Text(
                    (
                        "Modifica los datos de la institución"
                        if es_edicion
                        else "Completa los datos de la institución"
                    ),
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
                            "Guardar cambios" if es_edicion else "Guardar institución",
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

    def abrir_crear_institucion(e=None):
        abrir_formulario_institucion()

    def abrir_editar_institucion(institucion_id):
        try:
            institucion = servicio_instituciones.obtener_por_id(institucion_id)
        except Exception:
            mostrar_notificacion(
                "Ocurrió un error al cargar la institución.",
                ft.Colors.ERROR,
            )
            return

        if institucion is None:
            mostrar_notificacion(
                "No se encontró la institución que quieres editar.",
                ft.Colors.ERROR,
            )
            return

        abrir_formulario_institucion(institucion)

    def abrir_formulario_estudiante(estudiante=None):
        es_edicion = estudiante is not None
        nombre = ft.TextField(
            label="Nombre",
            value=estudiante.nombre if es_edicion else None,
            autofocus=True,
        )
        puntuacion = ft.TextField(
            label="Puntuación en lista",
            value=(str(estudiante.puntuacionEnLista) if es_edicion else None),
        )

        def guardar(evento):
            try:
                if es_edicion:
                    servicio_estudiantes.actualizar(
                        estudiante.id,
                        nombre.value,
                        puntuacion.value,
                    )
                else:
                    servicio_estudiantes.crear(nombre.value, puntuacion.value)
            except ValueError as error:
                mostrar_notificacion(
                    f"No se pudo {'actualizar' if es_edicion else 'crear'} el estudiante: {error}",
                    ft.Colors.ERROR,
                )
                return
            except Exception:
                mostrar_notificacion(
                    "Ocurrió un error inesperado al guardar el estudiante.",
                    ft.Colors.ERROR,
                )
                return

            abrir_estudiantes()
            mostrar_notificacion(
                (
                    "Estudiante actualizado correctamente."
                    if es_edicion
                    else "Estudiante creado correctamente."
                ),
                ft.Colors.GREEN_700,
            )

        contenido.content = ft.Column(
            [
                ft.Text(
                    "Editar estudiante" if es_edicion else "Crear estudiante",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Text(
                    (
                        "Modifica los datos del estudiante"
                        if es_edicion
                        else "Completa los datos del estudiante"
                    ),
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
                            "Guardar cambios" if es_edicion else "Guardar estudiante",
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

    def abrir_crear_estudiante(e=None):
        abrir_formulario_estudiante()

    def abrir_editar_estudiante(estudiante_id):
        try:
            estudiante = servicio_estudiantes.obtener_por_id(estudiante_id)
        except Exception:
            mostrar_notificacion(
                "Ocurrió un error al cargar el estudiante.",
                ft.Colors.ERROR,
            )
            return

        if estudiante is None:
            mostrar_notificacion(
                "No se encontró el estudiante que quieres editar.",
                ft.Colors.ERROR,
            )
            return

        abrir_formulario_estudiante(estudiante)

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
        requiere_grupo = ft.Checkbox(label="Requiere grupo")
        requiere_docente_adscriptor = ft.Checkbox(
            label="Requiere docente adscriptor",
            disabled=True,
        )

        def cambiar_requiere_grupo(evento):
            requiere_docente_adscriptor.disabled = not requiere_grupo.value
            if not requiere_grupo.value:
                requiere_docente_adscriptor.value = False
            page.update()

        requiere_grupo.on_change = cambiar_requiere_grupo

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
                requiere_grupo,
                requiere_docente_adscriptor,
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

    def abrir_crear_cursada(estudiante_id):
        try:
            cursos = servicio_cursos.listar()
            docentes_didactica = [
                docente
                for docente in servicio_docentes.listar()
                if docente.tipo == "didactica"
            ]
        except Exception:
            mostrar_notificacion(
                "Ocurrió un error al cargar los datos de la cursada.",
                ft.Colors.ERROR,
            )
            return

        curso_selector = ft.Dropdown(
            label="Curso",
            options=[
                ft.DropdownOption(key=str(curso.id), text=curso.nombre)
                for curso in cursos
            ],
            value=str(cursos[0].id) if cursos else None,
        )
        anio = ft.TextField(label="Año", autofocus=True)
        docente_selector = ft.Dropdown(
            label="Docente de didáctica",
            options=[
                ft.DropdownOption(key=str(docente.id), text=docente.nombre)
                for docente in docentes_didactica
            ],
            value=(str(docentes_didactica[0].id) if docentes_didactica else None),
        )

        def guardar(evento):
            try:
                servicio_cursadas.crear(
                    estudiante_id,
                    curso_selector.value,
                    anio.value,
                    docente_selector.value,
                )
            except ValueError as error:
                mostrar_notificacion(
                    f"No se pudo crear la cursada: {error}",
                    ft.Colors.ERROR,
                )
                return
            except Exception:
                mostrar_notificacion(
                    "Ocurrió un error inesperado al crear la cursada.",
                    ft.Colors.ERROR,
                )
                return

            abrir_estudiante(estudiante_id)
            mostrar_notificacion(
                "Cursada creada correctamente.",
                ft.Colors.GREEN_700,
            )

        controles = [
            ft.Text("Crear cursada", size=28, weight=ft.FontWeight.BOLD),
            ft.Text(
                "Completa los datos de la cursada",
                color=ft.Colors.SECONDARY,
            ),
            curso_selector,
            anio,
            docente_selector,
        ]

        if not cursos:
            controles.append(
                ft.Text(
                    "No hay cursos disponibles.",
                    color=ft.Colors.ERROR,
                )
            )
        if not docentes_didactica:
            controles.append(
                ft.Text(
                    "No hay docentes de didáctica disponibles.",
                    color=ft.Colors.ERROR,
                )
            )

        controles.append(
            ft.Row(
                [
                    ft.TextButton(
                        "Volver al estudiante",
                        on_click=lambda e: abrir_estudiante(estudiante_id),
                    ),
                    ft.FilledButton(
                        "Guardar cursada",
                        icon=ft.Icons.SAVE_OUTLINED,
                        on_click=guardar,
                        disabled=not cursos or not docentes_didactica,
                    ),
                ],
                spacing=12,
            )
        )

        contenido.content = ft.Column(controles, spacing=18)
        page.update()

    def abrir_crear_grupo(e):
        docentes_adscriptor = [
            docente
            for docente in servicio_docentes.listar()
            if docente.tipo == "adscriptor"
        ]
        instituciones = servicio_instituciones.listar()

        nombre = ft.TextField(label="Nombre", autofocus=True)
        horario = ft.TextField(label="Horario")

        docente_selector = ft.Dropdown(
            label="Docente adscriptor (opcional)",
            options=[
                ft.DropdownOption(key=str(docente.id), text=docente.nombre)
                for docente in docentes_adscriptor
            ],
            value=None,
        )
        institucion_selector = ft.Dropdown(
            label="Institución",
            options=[
                ft.DropdownOption(key=str(institucion.id), text=institucion.nombre)
                for institucion in instituciones
            ],
            value=str(instituciones[0].id) if instituciones else None,
        )

        def guardar(evento):
            try:
                servicio_grupos.crear(
                    nombre.value,
                    docente_selector.value,
                    institucion_selector.value,
                    horario.value,
                )
            except ValueError as error:
                mostrar_notificacion(
                    f"No se pudo crear el grupo: {error}",
                    ft.Colors.ERROR,
                )
                return
            except Exception:
                mostrar_notificacion(
                    "Ocurrió un error inesperado al crear el grupo.",
                    ft.Colors.ERROR,
                )
                return

            abrir_grupos()
            mostrar_notificacion(
                "Grupo creado correctamente.",
                ft.Colors.GREEN_700,
            )

        guardar_button = ft.FilledButton(
            "Guardar grupo",
            icon=ft.Icons.SAVE_OUTLINED,
            on_click=guardar,
            disabled=not instituciones,
        )
        controles = [
            ft.Text("Crear grupo", size=28, weight=ft.FontWeight.BOLD),
            ft.Text(
                "Completa los datos del grupo",
                color=ft.Colors.SECONDARY,
            ),
            nombre,
            docente_selector,
            institucion_selector,
            horario,
        ]
        if not instituciones:
            controles.append(
                ft.Text(
                    "No hay instituciones disponibles.",
                    color=ft.Colors.ERROR,
                )
            )
        controles.append(
            ft.Row(
                [
                    ft.TextButton(
                        "Volver a grupos",
                        on_click=abrir_grupos,
                    ),
                    guardar_button,
                ],
                spacing=12,
            )
        )
        contenido.content = ft.Column(controles, spacing=18)
        page.update()

    def abrir_editar_grupo(grupo_id):
        try:
            grupo = servicio_grupos.obtener_por_id(grupo_id)
        except Exception:
            mostrar_notificacion(
                "Ocurrió un error al cargar el grupo.",
                ft.Colors.ERROR,
            )
            return

        if grupo is None:
            mostrar_notificacion(
                "No se encontró el grupo que quieres editar.",
                ft.Colors.ERROR,
            )
            return

        nombre = ft.TextField(
            label="Nombre",
            value=grupo.nombre,
            disabled=True,
        )
        docente = ft.TextField(
            label="Docente adscriptor",
            value=grupo.docente.nombre if grupo.docente is not None else "-",
            disabled=True,
        )
        institucion = ft.TextField(
            label="Institución",
            value=grupo.institucion.nombre if grupo.institucion is not None else "-",
            disabled=True,
        )
        horario = ft.TextField(
            label="Horario",
            value=grupo.horario,
            autofocus=True,
        )

        def guardar(evento):
            try:
                servicio_grupos.actualizar(grupo.id, horario.value)
            except ValueError as error:
                mostrar_notificacion(
                    f"No se pudo actualizar el grupo: {error}",
                    ft.Colors.ERROR,
                )
                return
            except Exception:
                mostrar_notificacion(
                    "Ocurrió un error inesperado al actualizar el grupo.",
                    ft.Colors.ERROR,
                )
                return

            abrir_grupos()
            mostrar_notificacion(
                "Horario del grupo actualizado correctamente.",
                ft.Colors.GREEN_700,
            )

        contenido.content = ft.Column(
            [
                ft.Text("Editar horario del grupo", size=28, weight=ft.FontWeight.BOLD),
                ft.Text(
                    "Solo se puede modificar el horario del grupo",
                    color=ft.Colors.SECONDARY,
                ),
                nombre,
                docente,
                institucion,
                horario,
                ft.Row(
                    [
                        ft.TextButton("Volver a grupos", on_click=abrir_grupos),
                        ft.FilledButton(
                            "Guardar cambios",
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

    def abrir_crear_practica(cursada):
        estudiante_id = cursada.estudiante.id
        curso_requiere_grupo = cursada.curso.requiere_grupo
        curso_requiere_docente_adscriptor = cursada.curso.requiere_docente_adscriptor

        try:
            instituciones = servicio_instituciones.listar()
        except Exception:
            mostrar_notificacion(
                "Ocurrió un error al cargar las instituciones de la práctica.",
                ft.Colors.ERROR,
            )
            return

        institucion_selector = ft.Dropdown(
            label="Institución",
            options=[
                ft.DropdownOption(key=str(institucion.id), text=institucion.nombre)
                for institucion in instituciones
            ],
            value=None,
        )
        grupo_selector = ft.Dropdown(label="Grupo", options=[], disabled=True)
        curso = ft.TextField(
            label="Curso",
            value=getattr(cursada.curso, "nombre", ""),
            disabled=True,
        )
        docente_didactica = ft.TextField(
            label="Docente de didáctica",
            value=getattr(cursada.docenteDidactica, "nombre", ""),
            disabled=True,
        )
        docente_adscriptor = ft.TextField(
            label="Docente adscriptor",
            disabled=True,
        )
        observaciones = ft.TextField(
            label="Observaciones",
            multiline=True,
            min_lines=3,
            max_lines=5,
        )

        def actualizar_docente(grupo):
            docente_adscriptor.value = (
                grupo.docente.nombre
                if grupo is not None and grupo.docente is not None
                else ""
            )

        def mostrar_aviso_cola(docente, posicion):
            def aceptar(evento):
                page.pop_dialog()

            page.show_dialog(
                ft.AlertDialog(
                    modal=True,
                    title=ft.Text("Práctica en cola"),
                    content=ft.Text(
                        f'El docente "{docente.nombre}" no tiene cupos disponibles. '
                        f"La práctica quedará en cola, en la posición {posicion}."
                    ),
                    actions=[
                        ft.TextButton("Aceptar", on_click=aceptar),
                    ],
                    actions_alignment=ft.MainAxisAlignment.END,
                )
            )
            page.update()

        def evaluar_estado_cola(grupo):
            if (
                not curso_requiere_docente_adscriptor
                or grupo is None
                or grupo.docente is None
            ):
                return

            estado_cola = servicio_docentes.obtener_estado_cola(grupo.docente.id)
            if estado_cola and estado_cola["en_cola"]:
                mostrar_aviso_cola(
                    grupo.docente,
                    estado_cola["posicion"],
                )

        def cargar_grupos(institucion_id):
            if not curso_requiere_grupo:
                return None

            if institucion_id is None:
                grupo_selector.options = []
                grupo_selector.value = None
                grupo_selector.disabled = True
                actualizar_docente(None)
                return False

            try:
                grupos = servicio_grupos.obtener_por_institucion(int(institucion_id))
            except Exception:
                grupo_selector.options = []
                grupo_selector.value = None
                grupo_selector.disabled = True
                actualizar_docente(None)
                mostrar_notificacion(
                    "Ocurrió un error al cargar los grupos de la institución.",
                    ft.Colors.ERROR,
                )
                return False

            grupos = [
                grupo
                for grupo in grupos
                if (grupo.docente is not None) == curso_requiere_docente_adscriptor
            ]
            grupo_selector.options = [
                ft.DropdownOption(key=str(grupo.id), text=grupo.nombre)
                for grupo in grupos
            ]
            grupo_selector.value = None
            grupo_selector.disabled = not grupos
            actualizar_docente(None)
            return None

        def cambiar_institucion(evento):
            grupo = cargar_grupos(evento.control.value)
            evaluar_estado_cola(grupo)
            page.update()

        def cambiar_grupo(evento):
            try:
                grupos = servicio_grupos.obtener_por_institucion(
                    int(institucion_selector.value)
                )
                grupo = next(
                    (
                        grupo
                        for grupo in grupos
                        if str(grupo.id) == grupo_selector.value
                    ),
                    None,
                )
            except Exception:
                grupo = None
            actualizar_docente(grupo)
            evaluar_estado_cola(grupo)
            page.update()

        institucion_selector.on_select = cambiar_institucion
        if curso_requiere_grupo:
            grupo_selector.on_select = cambiar_grupo

        def guardar(evento):
            grupo = None
            if curso_requiere_grupo and grupo_selector.value is not None:
                try:
                    grupo = servicio_grupos.obtener_por_id(int(grupo_selector.value))
                except Exception:
                    grupo = None

            try:
                servicio_practicas.crear(
                    cursada.id,
                    institucion_selector.value,
                    grupo_selector.value if curso_requiere_grupo else None,
                    (
                        grupo.docente.id
                        if curso_requiere_docente_adscriptor
                        and grupo is not None
                        and grupo.docente is not None
                        else None
                    ),
                    getattr(cursada.docenteDidactica, "id", None),
                    observaciones.value,
                )
            except ValueError as error:
                mostrar_notificacion(
                    f"No se pudo crear la práctica: {error}",
                    ft.Colors.ERROR,
                )
                return
            except Exception:
                mostrar_notificacion(
                    "Ocurrió un error inesperado al crear la práctica.",
                    ft.Colors.ERROR,
                )
                return

            abrir_estudiante(estudiante_id)
            mostrar_notificacion(
                "Práctica creada correctamente.",
                ft.Colors.GREEN_700,
            )

        guardar_button = ft.FilledButton(
            "Guardar práctica",
            icon=ft.Icons.SAVE_OUTLINED,
            on_click=guardar,
        )
        cargar_grupos(institucion_selector.value)

        controles = [
            ft.Text("Crear práctica", size=28, weight=ft.FontWeight.BOLD),
            ft.Text(
                "Completa los datos de la práctica",
                color=ft.Colors.SECONDARY,
            ),
            curso,
            docente_didactica,
            institucion_selector,
        ]

        if curso_requiere_grupo:
            controles.append(grupo_selector)
        if curso_requiere_docente_adscriptor:
            controles.append(docente_adscriptor)
        controles.append(observaciones)

        controles.append(
            ft.Row(
                [
                    ft.TextButton(
                        "Volver al estudiante",
                        on_click=lambda e: abrir_estudiante(estudiante_id),
                    ),
                    guardar_button,
                ],
                spacing=12,
            )
        )

        contenido.content = ft.Container(
            content=ft.Column(
                controles,
                expand=True,
                spacing=18,
                scroll=ft.ScrollMode.AUTO,
            ),
            expand=True,
        )
        page.update()

    def abrir_crear_visita(practica_id, estudiante_id):
        try:
            practica = servicio_practicas.obtener_por_id(practica_id)
            docentes = servicio_docentes.listar()
        except Exception:
            mostrar_notificacion(
                "Ocurrió un error al cargar los datos de la visita didáctica.",
                ft.Colors.ERROR,
            )
            return

        if practica is None or practica.docenteDidactica is None:
            mostrar_notificacion(
                "La práctica no tiene un docente de didáctica asignado.",
                ft.Colors.ERROR,
            )
            return

        docentes_por_id = {docente.id: docente for docente in docentes}
        docente_adscriptor_ref = practica.docenteAdscriptor
        docente_adscriptor = (
            docentes_por_id.get(docente_adscriptor_ref.id)
            if docente_adscriptor_ref is not None
            else None
        )

        fecha = ft.TextField(
            label="Fecha",
            hint_text="Selecciona una fecha",
            read_only=True,
        )
        nota = ft.TextField(
            label="Nota",
            keyboard_type=ft.KeyboardType.NUMBER,
            autofocus=True,
        )
        observaciones = ft.TextField(
            label="Observaciones",
            multiline=True,
            min_lines=3,
            max_lines=5,
        )
        docente_didactica_field = ft.TextField(
            label="Docente de didáctica",
            value=practica.docenteDidactica.nombre,
            disabled=True,
        )
        docente_adscriptor_field = ft.TextField(
            label="Docente adscriptor",
            value=(docente_adscriptor.nombre if docente_adscriptor else ""),
            disabled=True,
        )
        docente_extra_selector = ft.Dropdown(
            label="Docente extra (opcional)",
            options=[
                ft.DropdownOption(key=str(docente.id), text=docente.nombre)
                for docente in docentes
            ],
        )

        def seleccionar_fecha(evento):
            if selector_fecha.value is not None:
                fecha.value = selector_fecha.value.strftime("%Y-%m-%d")
                page.update()

        selector_fecha = ft.DatePicker(
            help_text="Selecciona la fecha de la visita didáctica",
            cancel_text="Cancelar",
            confirm_text="Aceptar",
            on_change=seleccionar_fecha,
        )

        def abrir_selector_fecha(evento):
            page.show_dialog(selector_fecha)

        def guardar(evento):
            if not fecha.value or not nota.value or not nota.value.strip():
                mostrar_notificacion(
                    "La fecha y la nota son obligatorias.",
                    ft.Colors.ERROR,
                )
                return

            try:
                nota_numerica = float(nota.value)
                if not math.isfinite(nota_numerica):
                    raise ValueError
            except ValueError:
                mostrar_notificacion(
                    "La nota debe ser un valor numérico.",
                    ft.Colors.ERROR,
                )
                return

            docente_extra = next(
                (
                    docente
                    for docente in docentes
                    if str(docente.id) == docente_extra_selector.value
                ),
                None,
            )

            try:
                servicio_practicas.registrar_visita_didactica(
                    practica_id,
                    fecha.value,
                    observaciones.value,
                    nota_numerica,
                    practica.docenteDidactica,
                    docente_adscriptor,
                    docente_extra,
                )
            except ValueError as error:
                mostrar_notificacion(
                    f"No se pudo crear la visita didáctica: {error}",
                    ft.Colors.ERROR,
                )
                return
            except Exception:
                mostrar_notificacion(
                    "Ocurrió un error inesperado al crear la visita didáctica.",
                    ft.Colors.ERROR,
                )
                return

            abrir_practica(practica_id, estudiante_id)
            mostrar_notificacion(
                "Visita didáctica creada correctamente.",
                ft.Colors.GREEN_700,
            )

        contenido.content = ft.Column(
            [
                ft.Text(
                    "Crear visita didáctica",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Text(
                    "Completa los datos de la visita didáctica",
                    color=ft.Colors.SECONDARY,
                ),
                ft.Row(
                    [
                        fecha,
                        ft.IconButton(
                            icon=ft.Icons.CALENDAR_MONTH,
                            tooltip="Seleccionar fecha",
                            on_click=abrir_selector_fecha,
                        ),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                nota,
                observaciones,
                docente_didactica_field,
                docente_adscriptor_field,
                docente_extra_selector,
                ft.Row(
                    [
                        ft.TextButton(
                            "Volver a la práctica",
                            on_click=lambda e: abrir_practica(
                                practica_id,
                                estudiante_id,
                            ),
                        ),
                        ft.FilledButton(
                            "Guardar visita didáctica",
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

    def abrir_crear_asistencia(practica_id, estudiante_id):
        fecha = ft.TextField(
            label="Fecha",
            hint_text="Selecciona una fecha",
            read_only=True,
        )
        estado = ft.Dropdown(
            label="Estado",
            options=[
                ft.DropdownOption(key=Asistencia.ASISTIO, text=Asistencia.ASISTIO),
                ft.DropdownOption(
                    key=Asistencia.NO_ASISTIO,
                    text=Asistencia.NO_ASISTIO,
                ),
                ft.DropdownOption(
                    key=Asistencia.JUSTIFICADA,
                    text=Asistencia.JUSTIFICADA,
                ),
            ],
        )
        observaciones = ft.TextField(
            label="Observaciones",
            multiline=True,
            min_lines=3,
            max_lines=5,
        )

        def seleccionar_fecha(evento):
            if selector_fecha.value is not None:
                fecha.value = selector_fecha.value.strftime("%Y-%m-%d")
                page.update()

        selector_fecha = ft.DatePicker(
            help_text="Selecciona la fecha de asistencia",
            cancel_text="Cancelar",
            confirm_text="Aceptar",
            on_change=seleccionar_fecha,
        )

        def abrir_selector_fecha(evento):
            page.show_dialog(selector_fecha)

        def guardar(evento):
            if not fecha.value or not estado.value:
                mostrar_notificacion(
                    "La fecha y el estado son obligatorios.",
                    ft.Colors.ERROR,
                )
                return

            try:
                servicio_practicas.registrar_asistencia(
                    practica_id,
                    fecha.value,
                    estado.value,
                    observaciones.value,
                )
            except ValueError as error:
                mostrar_notificacion(
                    f"No se pudo crear la asistencia: {error}",
                    ft.Colors.ERROR,
                )
                return
            except Exception:
                mostrar_notificacion(
                    "Ocurrió un error inesperado al crear la asistencia.",
                    ft.Colors.ERROR,
                )
                return

            abrir_practica(practica_id, estudiante_id)
            mostrar_notificacion(
                "Asistencia creada correctamente.",
                ft.Colors.GREEN_700,
            )

        contenido.content = ft.Column(
            [
                ft.Text("Crear asistencia", size=28, weight=ft.FontWeight.BOLD),
                ft.Text(
                    "Completa los datos de la asistencia",
                    color=ft.Colors.SECONDARY,
                ),
                ft.Row(
                    [
                        fecha,
                        ft.IconButton(
                            icon=ft.Icons.CALENDAR_MONTH,
                            tooltip="Seleccionar fecha",
                            on_click=abrir_selector_fecha,
                        ),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                estado,
                observaciones,
                ft.Row(
                    [
                        ft.TextButton(
                            "Volver a la práctica",
                            on_click=lambda e: abrir_practica(
                                practica_id,
                                estudiante_id,
                            ),
                        ),
                        ft.FilledButton(
                            "Guardar asistencia",
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

    def abrir_finalizar_practica(practica_id, estudiante_id):
        try:
            practica = servicio_practicas.obtener_por_id(practica_id)
        except Exception:
            mostrar_notificacion(
                "Ocurrió un error al cargar la práctica.",
                ft.Colors.ERROR,
            )
            return

        if practica is None:
            mostrar_notificacion(
                "No se encontró la práctica que quieres finalizar.",
                ft.Colors.ERROR,
            )
            return

        nota_final = ft.TextField(
            label="Nota final",
            value=str(practica.notaFinal) if practica.notaFinal is not None else "",
            keyboard_type=ft.KeyboardType.NUMBER,
            autofocus=True,
        )
        observaciones = ft.TextField(
            label="Observaciones",
            value=practica.observaciones or "",
            multiline=True,
            min_lines=3,
            max_lines=5,
        )

        def guardar(evento):
            if not nota_final.value or not nota_final.value.strip():
                mostrar_notificacion(
                    "La nota final es obligatoria.",
                    ft.Colors.ERROR,
                )
                return

            try:
                servicio_practicas.finalizar_practica(
                    practica_id,
                    nota_final.value,
                    observaciones.value,
                )
            except ValueError as error:
                mostrar_notificacion(
                    f"No se pudo finalizar la práctica: {error}",
                    ft.Colors.ERROR,
                )
                return
            except Exception:
                mostrar_notificacion(
                    "Ocurrió un error inesperado al finalizar la práctica.",
                    ft.Colors.ERROR,
                )
                return

            abrir_practica(practica_id, estudiante_id)
            mostrar_notificacion(
                "Práctica finalizada correctamente.",
                ft.Colors.GREEN_700,
            )

        contenido.content = ft.Column(
            [
                ft.Text("Finalizar práctica", size=28, weight=ft.FontWeight.BOLD),
                ft.Text(
                    "Ingresa la nota final y las observaciones",
                    color=ft.Colors.SECONDARY,
                ),
                nota_final,
                observaciones,
                ft.Row(
                    [
                        ft.TextButton(
                            "Cancelar",
                            on_click=lambda evento: abrir_practica(
                                practica_id,
                                estudiante_id,
                            ),
                        ),
                        ft.FilledButton(
                            "Guardar y finalizar",
                            icon=ft.Icons.CHECK,
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
        contenido.content = construir_vista_instituciones(
            page,
            abrir_crear_institucion,
            abrir_editar_institucion,
        )
        page.update()

    def abrir_estudiante(estudiante_id):
        contenido.content = construir_vista_estudiante(
            page,
            estudiante_id,
            abrir_estudiantes,
            abrir_crear_cursada,
            abrir_crear_practica,
            abrir_practica,
        )
        page.update()

    def abrir_practica(practica_id, estudiante_id):
        contenido.content = construir_vista_practica(
            page,
            practica_id,
            lambda e: abrir_estudiante(estudiante_id),
            lambda e: abrir_crear_asistencia(practica_id, estudiante_id),
            lambda e: abrir_crear_visita(practica_id, estudiante_id),
            lambda e: abrir_finalizar_practica(practica_id, estudiante_id),
        )
        page.update()

    def abrir_estudiantes(e=None):
        contenido.content = construir_vista_estudiantes(
            page,
            abrir_crear_estudiante,
            abrir_estudiante,
            abrir_editar_estudiante,
        )
        page.update()

    def abrir_docentes(e=None):
        contenido.content = construir_vista_docentes(page, abrir_crear_docente)
        page.update()

    def abrir_cursos(e=None):
        contenido.content = construir_vista_cursos(page, abrir_crear_curso)
        page.update()

    def abrir_grupos(e=None):
        contenido.content = construir_vista_grupos(
            page,
            abrir_crear_grupo,
            abrir_editar_grupo,
        )
        page.update()

    def abrir_inicio(e=None):
        contenido.content = construir_vista_inicio(
            abrir_instituciones,
            abrir_cursos,
            abrir_docentes,
            abrir_grupos,
            abrir_estudiantes,
        )
        page.update()

    navbar = ft.Container(
        content=ft.Row(
            [
                ft.Text("ProyectoAtlas", size=22, weight=ft.FontWeight.BOLD),
                ft.VerticalDivider(width=1),
                ft.TextButton(
                    "Inicio",
                    icon=ft.Icons.HOME,
                    on_click=abrir_inicio,
                ),
                ft.VerticalDivider(width=1),
                ft.TextButton(
                    "Instituciones",
                    icon=ft.Icons.ACCOUNT_BALANCE,
                    on_click=abrir_instituciones,
                ),
                ft.TextButton(
                    "Grupos",
                    icon=ft.Icons.GROUPS,
                    on_click=abrir_grupos,
                ),
                ft.VerticalDivider(width=1),
                ft.TextButton(
                    "Docentes",
                    icon=ft.Icons.CAST_FOR_EDUCATION,
                    on_click=abrir_docentes,
                ),
                ft.TextButton(
                    "Estudiantes",
                    icon=ft.Icons.SCHOOL,
                    on_click=abrir_estudiantes,
                ),
                ft.TextButton(
                    "Cursos",
                    icon=ft.Icons.MENU_BOOK,
                    on_click=abrir_cursos,
                ),
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
    abrir_inicio()


ft.run(main)
