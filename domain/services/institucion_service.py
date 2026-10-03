from domain.models.institucion import Institucion
from domain.abb import Arbol
from domain.repositories.institucion_repository import InstitucionRepository
from domain.repositories.grupo_repository import GrupoRepository


class InstitucionService:
    def __init__(self):
        self.__repository = InstitucionRepository()
        self.__grupo_repository = GrupoRepository()

    def crear(self, nombre, direccion):
        self.__validar_datos(nombre, direccion)

        id_nuevo = self.__repository.obtener_proximo_id()
        institucion = Institucion(id_nuevo, nombre, direccion)
        return self.__repository.agregar(institucion)

    def __validar_datos(self, nombre, direccion):
        if nombre is None or nombre == "" or not nombre.strip():
            raise ValueError("El nombre de la institución es obligatorio")
        if direccion is None or direccion == "" or not direccion.strip():
            raise ValueError("La dirección de la institución es obligatoria")

    def obtener_por_id(self, id):
        return self.__repository.obtener_por_id(id)

    def listar(self):

        return self.__repository.listar()

    def buscar_por_nombre(self, nombre):
        criterio = nombre.strip().casefold()
        if not criterio:
            return None

        arbol = Arbol()
        for institucion in self.__repository.listar():
            clave = institucion.nombre.strip().casefold()
            arbol.insertar(clave, institucion)

        return arbol.buscar(criterio)

    def actualizar(self, id, nombre, direccion):
        self.__validar_datos(nombre, direccion)
        institucion = Institucion(id, nombre, direccion)
        return self.__repository.actualizar(institucion)

    def eliminar(self, id):
        grupos = self.__grupo_repository.listar()
        if any(str(grupo.institucion.id) == str(id) for grupo in grupos):
            raise ValueError(
                "No se puede eliminar la institución porque tiene grupos asociados"
            )
        return self.__repository.eliminar(id)
