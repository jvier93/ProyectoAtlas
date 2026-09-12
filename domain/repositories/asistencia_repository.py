from domain.models.asistencia import Asistencia
from domain.repositories.json_repository import JsonStore


class AsistenciaRepository:
    def __init__(self, filename="data/asistencias.json"):
        self.__store = JsonStore(
            filename, self.__serializar, self.__deserializar
        )

    def __serializar(self, asistencia):
        return {
            "id": asistencia.id,
            "fecha": asistencia.fecha,
            "estado": asistencia.estado,
            "observaciones": asistencia.observaciones,
        }

    def __deserializar(self, registro):
        return Asistencia(
            registro["id"],
            registro["fecha"],
            registro["estado"],
            registro.get("observaciones"),
        )

    def agregar(self, entidad):
        return self.__store.agregar(entidad)

    def crear(self, entidad):
        return self.__store.crear(entidad)

    def obtener_por_id(self, id):
        return self.__store.obtener_por_id(id)

    def buscar(self, criterio):
        return self.__store.buscar(criterio)

    def listar(self):
        return self.__store.listar()

    def actualizar(self, entidad):
        return self.__store.actualizar(entidad)

    def eliminar(self, id):
        return self.__store.eliminar(id)

    def obtener_proximo_id(self):
        return self.__store.obtener_proximo_id()