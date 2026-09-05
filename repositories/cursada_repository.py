from models.cursada import Cursada
from repositories.json_repository import JsonStore
from types import SimpleNamespace


class CursadaRepository:
    def __init__(self, filename="data/cursadas.json"):
        self.__store = JsonStore(
            filename, self.__serializar, self.__deserializar
        )

    def __serializar(self, cursada):
        return {
            "id": cursada.id,
            "estudiante_id": cursada.estudiante.id,
            "curso_id": cursada.curso.id,
            "anio": cursada.anio,
            "docente_didactica_id": cursada.docenteDidactica.id if cursada.docenteDidactica else None,
        }

    def __deserializar(self, registro):
        return Cursada(
            registro["id"],
            SimpleNamespace(id=registro["estudiante_id"]),
            SimpleNamespace(id=registro["curso_id"]),
            registro["anio"],
            SimpleNamespace(id=registro["docente_didactica_id"])
            if registro.get("docente_didactica_id")
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
