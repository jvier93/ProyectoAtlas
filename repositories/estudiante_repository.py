from models.estudiante import Estudiante
from repositories.json_repository import JsonStore


class EstudianteRepository:
    def __init__(self, filename="data/estudiantes.json"):
        self.__store = JsonStore(
            filename, self.__serializar, self.__deserializar
        )

    def __serializar(self, estudiante):
        return {
            "id": estudiante.id,
            "nombre": estudiante.nombre,
            "puntuacionEnLista": estudiante.puntuacionEnLista,
        }

    def __deserializar(self, registro):
        return Estudiante(
            registro["id"],
            registro["nombre"],
            registro["puntuacionEnLista"],
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