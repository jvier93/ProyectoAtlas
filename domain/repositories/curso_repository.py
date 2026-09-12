from domain.models.curso import Curso
from domain.repositories.json_repository import JsonStore


class CursoRepository:
    def __init__(
        self,
        filename="data/cursos.json",
    ):
        self.__store = JsonStore(
            filename, self.__serializar, self.__deserializar
        )

    def __serializar(self, curso):
        return {
            "id": curso.id,
            "nombre": curso.nombre,
            "requiere_docente_adscriptor": curso.requiere_docente_adscriptor,
            "requiere_grupo": curso.requiere_grupo,
        }

    def __deserializar(self, registro):
        return Curso(
            registro["id"],
            registro["nombre"],
            registro.get("requiere_docente_adscriptor", False),
            registro.get("requiere_grupo", False),
        )

    def __obtener(self, repository, id, nombre):
        entidad = repository.obtener_por_id(id)
        if entidad is None:
            raise ValueError(f"La {nombre} referenciada no existe")
        return entidad

    def agregar(self, entidad):
        return self.__store.agregar(entidad)

    def crear(self, entidad):
        return self.__store.crear(entidad)

    def obtener_por_id(self, id):
        return self.__store.obtener_por_id(id)

    def obtener_proximo_id(self):
        return self.__store.obtener_proximo_id()

    def buscar(self, criterio):
        return self.__store.buscar(criterio)

    def listar(self):
        return self.__store.listar()

    def actualizar(self, entidad):
        return self.__store.actualizar(entidad)

    def eliminar(self, id):
        return self.__store.eliminar(id)