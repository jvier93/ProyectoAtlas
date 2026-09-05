from pathlib import Path

from services.curso_service import CursoService
from services.docente_service import DocenteService
from services.estudiante_service import EstudianteService
from services.grupo_service import GrupoService
from services.institucion_service import InstitucionService
from services.practica_service import PracticaService
from services.cursada_service import CursadaService


DATA_FILES = [
    "asistencias.json",
    "cursadas.json",
    "cursos.json",
    "docentes.json",
    "estudiantes.json",
    "grupos.json",
    "instituciones.json",
    "practicas.json",
    "visitas_didacticas.json",
]


def limpiar_datos():
    data_dir = Path(__file__).resolve().parent / "data"
    for nombre_archivo in DATA_FILES:
        archivo = data_dir / nombre_archivo
        archivo.write_text("[]\n", encoding="utf-8")


estudiante_service = EstudianteService()
curso_service = CursoService()
docente_service = DocenteService()
institucion_service = InstitucionService()
grupo_service = GrupoService()
practica_service = PracticaService()
cursada_service = CursadaService()


if __name__ == "__main__":
    limpiar_datos()

    estudiante = estudiante_service.crear("Mariano", 100)
    docente_didactica = docente_service.crear("Pitico", "didactica")
    docente_adscriptor = docente_service.crear("Nacho", "adscriptor")
    institucion = institucion_service.crear("UTN", "Av. Siempre Viva 123")
    curso = curso_service.crear("Didactica I", True, True)
    grupo = grupo_service.crear(
        "Grupo A",
        docente_didactica.id,
        institucion.id,
        "Lunes 10:00-12:00",
    )
    cursada = cursada_service.crear(estudiante.id, curso.id, 2026, docente_didactica.id)
    cursada2 = cursada_service.crear(estudiante.id, curso.id, 2027, docente_didactica.id)
    cursada3 = cursada_service.crear(estudiante.id, curso.id, 2028, docente_didactica.id)
    cursada4 = cursada_service.crear(estudiante.id, curso.id, 2029, docente_didactica.id)
    practica = practica_service.crear(
        cursada.id,
        institucion.id,
        grupo.id,
        docente_adscriptor.id,
        docente_didactica.id,
        "Observaciones de la práctica",
    )
    print(cursada2.docenteDidactica.nombre)
    practica_service.registrar_asistencia(practica.id, "2026-09-01", "Presente", "Asistencia inicial")
    
    # practica2 = practica_service.crear(
	# 		cursada2.id,
	# 		institucion.id,
	# 		grupo.id,
	# 		docente_adscriptor.id,
	# 		docente_didactica.id,
	# 		"Observaciones de la práctica",
	# 	)
    # practica3 = practica_service.crear(
	# 			cursada3.id,
	# 			institucion.id,
	# 			grupo.id,
	# 			docente_adscriptor.id,
	# 			docente_didactica.id,
	# 			"Observaciones de la práctica",
	# 		)
    # practica4 = practica_service.crear(
	# 			cursada4.id,
	# 			institucion.id,
	# 			grupo.id,
	# 			docente_adscriptor.id,
	# 			docente_didactica.id,
	# 			"Observaciones de la práctica",
	# 		)

    docente_actualizado = docente_service.obtener_por_id(docente_adscriptor.id)
    print(
        f"Prácticas activas de {docente_actualizado.nombre}: "
        f"{list(docente_actualizado.activas)}"
    )
   