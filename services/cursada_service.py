from models.cursada import Cursada
from repositories.cursada_repository import CursadaRepository
from services.estudiante_service import EstudianteService
from services.curso_service import CursoService
from services.docente_service import DocenteService


class CursadaService:
    def __init__(self):
        self.__repository = CursadaRepository()
        self.__estudiante_service = EstudianteService()
        self.__curso_service = CursoService()
        self.__docente_service = DocenteService()

    def _hidratar_relaciones(self, cursada):
        if cursada is None:
            return None

        cursada.estudiante = self.__estudiante_service.obtener_por_id(cursada.estudiante.id)
        cursada.curso = self.__curso_service.obtener_por_id(cursada.curso.id)
        cursada.docenteDidactica = self.__docente_service.obtener_por_id(cursada.docenteDidactica.id)
        
        return cursada

    def __cursada_ya_existe(self, estudiante_id, curso_id, anio):
       
        cursadas = self.__repository.listar() 
        for cursada in cursadas:
            mismo_estudiante = cursada.estudiante.id == estudiante_id 
            mismo_curso = cursada.curso.id == curso_id
            mismo_anio = cursada.anio == anio
            if mismo_estudiante and mismo_curso and mismo_anio:
                return True
        return False

    def crear(self, estudiante_id, curso_id, anio, docente_didactica_id):
    
        # Resolvemos dependencias
        id_nuevo = self.__repository.obtener_proximo_id()
        estudiante = self.__estudiante_service.obtener_por_id(estudiante_id)
        curso = self.__curso_service.obtener_por_id(curso_id)
        docente_didactica = self.__docente_service.obtener_por_id(docente_didactica_id)
        
        if estudiante is None:
            raise ValueError("El estudiante no existe")
        if curso is None:
            raise ValueError("El curso no existe")
        if docente_didactica is None:
            raise ValueError("El docente de didáctica no existe")
        
        # Validamos que que ya no exista una cursada para este estudiante, curso y año
        if self.__cursada_ya_existe(estudiante_id, curso_id, anio):
            raise ValueError(
                f"Ya existe una cursada para este estudiante, curso y año ({anio})"
            )
        
        cursada = Cursada(id_nuevo, estudiante, curso, anio, docente_didactica)
      
        return  self.__repository.agregar(cursada)

    def obtener_por_id(self, id):
        cursada = self.__repository.obtener_por_id(id)
        return self._hidratar_relaciones(cursada)

    def listar_cursadas_de_estudiante(self, estudiante_id):
    
        cursadas = self.listar()  
        cursadas_estudiante = []
        for cursada in cursadas:
            if cursada.estudiante.id == estudiante_id:
                cursadas_estudiante.append(cursada)
        return cursadas_estudiante

    def listar(self):
        cursadas = self.__repository.listar()
        cursadas_hidratadas = []
        for cursada in cursadas:
            cursadas_hidratadas.append(self._hidratar_relaciones(cursada))
        return cursadas_hidratadas

    def actualizar(self, cursada):
        return self.__repository.actualizar(cursada)

    def eliminar(self, id):
        return self.__repository.eliminar(id)
