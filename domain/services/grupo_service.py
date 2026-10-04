from domain.models.grupo import Grupo
from domain.repositories.grupo_repository import GrupoRepository
from domain.services.docente_service import DocenteService
from domain.services.institucion_service import InstitucionService


class GrupoService:
    def __init__(self):
        self.__repository = GrupoRepository()
        self.__docente_service = DocenteService()
        self.__institucion_service = InstitucionService()

    def crear(self, nombre, docente_id, institucion_id, horario):
        if nombre is None or nombre == "" or not str(nombre).strip():
            raise ValueError("El nombre del grupo es obligatorio")

        if institucion_id is None or str(institucion_id).strip() == "":
            raise ValueError("Debe seleccionar una institución")

        if horario is None or horario == "" or not str(horario).strip():
            raise ValueError("El horario del grupo es obligatorio")

        try:
            institucion_id = int(institucion_id)
            if docente_id is not None and str(docente_id).strip() != "":
                docente_id = int(docente_id)
            else:
                docente_id = None
        except (TypeError, ValueError):
            raise ValueError("Los datos del docente y la institución no son válidos")

        docente = (
            self.__docente_service.obtener_por_id(docente_id)
            if docente_id is not None
            else None
        )
        institucion = self.__institucion_service.obtener_por_id(institucion_id)

        if docente_id is not None and docente is None:
            raise ValueError("El docente no existe")
        if institucion is None:
            raise ValueError("La institución no existe")
        if docente is not None and docente.tipo != "adscriptor":
            raise ValueError("El docente seleccionado no es adscriptor")

        id_nuevo = self.__repository.obtener_proximo_id()
        grupo = Grupo(
            id_nuevo,
            str(nombre).strip(),
            docente,
            institucion,
            str(horario).strip(),
        )
        return self.__repository.agregar(grupo)

    def obtener_por_id(self, id):
        grupo = self.__repository.obtener_por_id(id)
        if grupo is None:
            return None
        return self.__hidratar_grupo(grupo)

    def obtener_por_institucion(self, institucion_id):
        grupos = self.__repository.listar()
        grupos_institucion = []
        for grupo in grupos:
            if grupo.institucion.id == institucion_id:
                grupos_institucion.append(grupo)

        grupos_hidratados = []
        for grupo in grupos_institucion:
            grupos_hidratados.append(self.__hidratar_grupo(grupo))
        return grupos_hidratados

    def listar(self):
        grupos = self.__repository.listar()
        grupos_hidratados = []
        for grupo in grupos:
            grupos_hidratados.append(self.__hidratar_grupo(grupo))
        return grupos_hidratados

    def __hidratar_grupo(self, grupo):
        if grupo is None:
            return None

        docente = (
            self.__docente_service.obtener_por_id(grupo.docente.id)
            if grupo.docente is not None
            else None
        )
        institucion = self.__institucion_service.obtener_por_id(grupo.institucion.id)

        grupo.docente = docente
        grupo.institucion = institucion
        return grupo

    def actualizar(self, id, horario):
        if horario is None or horario == "" or not str(horario).strip():
            raise ValueError("El horario del grupo es obligatorio")

        grupo_actual = self.__repository.obtener_por_id(id)
        if grupo_actual is None:
            raise ValueError("El grupo no existe")

        grupo_actualizado = Grupo(
            grupo_actual.id,
            grupo_actual.nombre,
            grupo_actual.docente,
            grupo_actual.institucion,
            str(horario).strip(),
        )
        return self.__repository.actualizar(grupo_actualizado)

    def eliminar(self, id):
        return self.__repository.eliminar(id)
