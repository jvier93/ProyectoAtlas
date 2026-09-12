from domain.models.institucion import Institucion
from domain.repositories.institucion_repository import InstitucionRepository
from domain.repositories.grupo_repository import GrupoRepository


class InstitucionService:
    def __init__(self):
        self.__repository = InstitucionRepository()

    def crear(self, nombre, direccion):
        if nombre is None or nombre == "" or not nombre.strip():
            raise ValueError("El nombre de la institución es obligatorio")
        if direccion is None or direccion == "" or not direccion.strip():
            raise ValueError("La dirección de la institución es obligatoria")

        id_nuevo = self.__repository.obtener_proximo_id()
        institucion = Institucion(id_nuevo, nombre, direccion)
        return self.__repository.agregar(institucion)

    def obtener_por_id(self, id):
        return self.__repository.obtener_por_id(id)

    def listar(self):
        #   raise ValueError("El método listar no está implementado en InstitucionService.")

        return self.__repository.listar()

    def actualizar(self, institucion):
        return self.__repository.actualizar(institucion)

    def eliminar(self, id):
        return self.__repository.eliminar(id)

        institucion = self.obtener_por_id(institucion_id)
        if institucion is None:
            raise ValueError("La institucion no existe")

        docentes = self.__docente_adscriptor_service.listar()
        docentes_adscriptores = []
        for docente in docentes:
            grupos_docente = self.obtener_grupos_de_docente(institucion_id, docente.id)
            if grupos_docente:
                docentes_adscriptores.append(docente)
        return docentes_adscriptores
