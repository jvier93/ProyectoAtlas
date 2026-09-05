from models.estudiante import Estudiante
from repositories.estudiante_repository import EstudianteRepository


class EstudianteService:
    def __init__(self):
        self.__repository =EstudianteRepository()

    def crear(self, nombre, puntuacionEnLista):
        id_nuevo = self.__repository.obtener_proximo_id()
        estudiante = Estudiante(id_nuevo, nombre, puntuacionEnLista)
        return self.__repository.agregar(estudiante)

    def obtener_por_id(self, id):
        return self.__repository.obtener_por_id(id)

    def listar(self):
        return self.__repository.listar()

    def buscar(self, criterio):
        return self.__repository.buscar(criterio)

    def actualizar(self, estudiante):
        return self.__repository.actualizar(estudiante)

    def eliminar(self, id):
        return self.__repository.eliminar(id)