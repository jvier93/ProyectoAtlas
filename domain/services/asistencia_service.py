from domain.models.asistencia import Asistencia
from domain.repositories.asistencia_repository import AsistenciaRepository


class AsistenciaService:
    def __init__(self, repository=None):
        self.__repository = repository or AsistenciaRepository()

    def crear(self, fecha, estado, observaciones=None):
        id_nuevo = self.__repository.obtener_proximo_id()
        asistencia = Asistencia(id_nuevo, fecha, estado, observaciones)
        return self.__repository.agregar(asistencia)

    def obtener_por_id(self, id):
        return self.__repository.obtener_por_id(id)

    def listar(self):
        return self.__repository.listar()

    def actualizar(self, asistencia):
        return self.__repository.actualizar(asistencia)

    def eliminar(self, id):
        return self.__repository.eliminar(id)