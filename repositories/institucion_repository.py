from models.institucion import Institucion
from repositories.json_repository import JsonStore


class InstitucionRepository:
    def __init__(self, filename="data/instituciones.json"):
        self.__store = JsonStore(
            filename, self.__serializar, self.__deserializar
        )

    def __serializar(self, institucion):
        return {
            "id": institucion.id,
            "nombre": institucion.nombre,
            "direccion": institucion.direccion,
        }

    def __deserializar(self, registro):
        return Institucion(
            registro["id"],
            registro["nombre"],
            registro["direccion"],
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

    def obtener_proximo_id(self):
        return self.__store.obtener_proximo_id()

    def eliminar(self, id):
        return self.__store.eliminar(id)