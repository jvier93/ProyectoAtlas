from models.grupo import Grupo
from repositories.json_repository import JsonStore
from types import SimpleNamespace


class GrupoRepository:
    def __init__(self, filename="data/grupos.json"):
        self.__store = JsonStore(
            filename, self.__serializar, self.__deserializar
        )

    def __serializar(self, grupo):
        return {
            "id": grupo.id,
            "nombre": grupo.nombre,
            "docente_id": grupo.docente.id,
            "institucion_id": grupo.institucion.id,
            "horario": grupo.horario,
        }

    def __deserializar(self, registro):
        return Grupo(
            registro["id"],
            registro["nombre"],
            SimpleNamespace(id=registro["docente_id"]),
            SimpleNamespace(id=registro["institucion_id"]),
            registro["horario"],
        )

    def agregar(self, entidad):
        return self.__store.agregar(entidad)

    def crear(self, entidad):
        return self.__store.crear(entidad)

    def obtener_por_id(self, id):
        return self.__store.obtener_por_id(id)

    def obtener_proximo_id(self):
        return self.__store.obtener_proximo_id()
    
    def listar(self):
        return self.__store.listar()
    
    def buscar(self, criterio):
        return self.__store.buscar(criterio)
    
    def actualizar(self, entidad):
        return self.__store.actualizar(entidad)

    def eliminar(self, id):
        return self.__store.eliminar(id)