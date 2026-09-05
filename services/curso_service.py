from models.curso import Curso
from repositories.curso_repository import CursoRepository


class CursoService:
    def __init__(self):
        self.__repository = CursoRepository()

    def crear(self, nombre, requiere_docente_adscriptor=False, requiere_grupo=False):
        id_nuevo = self.__repository.obtener_proximo_id()
        curso = Curso(id_nuevo, nombre, requiere_docente_adscriptor, requiere_grupo)
        return self.__repository.agregar(curso)

    def obtener_por_id(self, id):
        return self.__repository.obtener_por_id(id)

    def listar(self):
        return self.__repository.listar()

    def buscar(self, criterio):
        return self.__repository.buscar(criterio)

    def actualizar(self, curso):
        return self.__repository.actualizar(curso)

    def eliminar(self, id):
        return self.__repository.eliminar(id)