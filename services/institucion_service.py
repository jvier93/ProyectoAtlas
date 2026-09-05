from models.institucion import Institucion
from repositories.institucion_repository import InstitucionRepository
from repositories.grupo_repository import GrupoRepository


class InstitucionService:
    def __init__(self):
        self.__repository = InstitucionRepository()
      

    def crear(self, nombre, direccion):
        id_nuevo = self.__repository.obtener_proximo_id()
        institucion = Institucion(id_nuevo, nombre, direccion)
        return self.__repository.agregar(institucion)

    def obtener_por_id(self, id):
        return self.__repository.obtener_por_id(id)

    def listar(self):
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