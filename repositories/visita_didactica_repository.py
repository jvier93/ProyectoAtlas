from models.visita_didactica import VisitaDidactica
from repositories.json_repository import JsonStore
from types import SimpleNamespace


class VisitaDidacticaRepository:
    def __init__(self, filename="data/visitas_didacticas.json"):
        self.__store = JsonStore(
            filename, self.__serializar, self.__deserializar
        )

    def __serializar(self, visita):
        return {
            "id": visita.id,
            "fecha": visita.fecha,
            "observaciones": visita.observaciones,
            "nota": visita.nota,
            "docente_didactica_id": visita.docenteDidactica.id,
            "docente_adscriptor_id": visita.docenteAdscriptor.id,
            "docente_extra_id": (
                visita.docenteExtra.id if visita.docenteExtra else None
            ),
        }

    def __deserializar(self, registro):
        return VisitaDidactica(
            registro["id"],
            registro["fecha"],
            registro["observaciones"],
            registro["nota"],
            SimpleNamespace(id=registro["docente_didactica_id"]),
            SimpleNamespace(id=registro["docente_adscriptor_id"]),
            SimpleNamespace(id=registro["docente_extra_id"])
            if registro.get("docente_extra_id") is not None
            else None,
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