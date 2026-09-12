from domain.models.grupo import Grupo
from domain.repositories.grupo_repository import GrupoRepository
from domain.services.docente_service import DocenteService
from domain.services.institucion_service import InstitucionService


class GrupoService:
    def __init__(self):
        self.__repository = GrupoRepository()
        self.__docente_service = DocenteService()
        self.__institucion_service = InstitucionService()

    def crear(self, nombre, docente_id, institucion_id, horario):
      
        #Resolvemos dependencias
        docente = self.__docente_service.obtener_por_id(docente_id)
        institucion = self.__institucion_service.obtener_por_id(institucion_id)
        
        if docente is None or institucion is None:
            raise ValueError("Docente o institución no existe")
        
        id_nuevo = self.__repository.obtener_proximo_id()
        grupo = Grupo(id_nuevo, nombre, docente, institucion, horario)
        return self.__repository.agregar(grupo)

    def obtener_por_id(self, id):
        grupo = self.__repository.obtener_por_id(id)
        if grupo is None:
            return None
        return self.__hidratar_grupo(grupo)
    
    def obtener_por_institucion(self, institucion_id):
        grupos = self.__repository.listar()
        grupos_institucion = []
        for grupo in grupos:
            if grupo.institucion.id == institucion_id:
                grupos_institucion.append(grupo)
        
        grupos_hidratados = []
        for grupo in grupos_institucion:
            grupos_hidratados.append(self.__hidratar_grupo(grupo))
        return grupos_hidratados
    
    def listar(self):
        grupos = self.__repository.listar()
        grupos_hidratados = []
        for grupo in grupos:
            grupos_hidratados.append(self.__hidratar_grupo(grupo))
        return grupos_hidratados
    
    def __hidratar_grupo(self, grupo):
        if grupo is None:
            return None
        
        docente = self.__docente_service.obtener_por_id(grupo.docente.id)
        institucion = self.__institucion_service.obtener_por_id(grupo.institucion.id)
     
        grupo.docente = docente
        grupo.institucion = institucion
        return grupo

    def actualizar(self, grupo):
        return self.__repository.actualizar(grupo)

    def eliminar(self, id):
        return self.__repository.eliminar(id)