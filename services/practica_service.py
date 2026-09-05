from models.practica import Practica
from models.curso import Curso
from services.asistencia_service import AsistenciaService
from repositories.practica_repository import PracticaRepository
from services.cursada_service import CursadaService
from services.docente_service import DocenteService
from services.institucion_service import InstitucionService
from services.grupo_service import GrupoService
from services.visita_didactica_service import VisitaDidacticaService


class PracticaService:
    def __init__(self):
        self.__practica_repository = PracticaRepository()
        self.__cursada_service = CursadaService()
        self.__docente_service = DocenteService()
        self.__institucion_service = InstitucionService()
        self.__grupo_service = GrupoService()
        self.__asistencia_service = AsistenciaService()
        self.__visita_didactica_service = VisitaDidacticaService()

   
    def crear(
        self,
        cursada_id,
        institucion_id,
        grupo_id=None,
        docente_adscriptor_id=None,
        docente_didactica_id=None,
        observaciones=None,
    ):
        
        #Resolvemos dependencias
        id_nuevo = self.__practica_repository.obtener_proximo_id()
        cursada = self.__cursada_service.obtener_por_id(cursada_id)
        institucion = self.__institucion_service.obtener_por_id(institucion_id)
        
        if cursada is None or institucion is None:
            raise ValueError("La cursada o institución no existe")
        

        grupo = None
        if grupo_id is not None:
            grupo = self.__grupo_service.obtener_por_id(grupo_id)
            if grupo is None:
                raise ValueError("El grupo no existe")
           

        docente_adscriptor = None
        if docente_adscriptor_id is not None:
            docente_adscriptor = self.__docente_service.obtener_por_id(docente_adscriptor_id)
            if docente_adscriptor is None:
                raise ValueError("El docente adscriptor no existe")

        docente_didactica = None
        if docente_didactica_id is not None:
            docente_didactica = self.__docente_service.obtener_por_id(docente_didactica_id)
            if docente_didactica is None:
                raise ValueError("El docente de didáctica no existe")

        practica = Practica(
            id_nuevo,
            cursada,
            institucion,
            grupo,
            docente_adscriptor,
            docente_didactica,
            observaciones=observaciones,
        )
        return self.registrar_practica(practica)

    def __existe_practica_activa(self, estudiante_id):
        practicas = self.__practica_repository.listar()
        for practica in practicas:
            cursada = self.__cursada_service.obtener_por_id(practica.cursada.id)
            cursada = cursada or practica.cursada
            if (
                cursada.estudiante.id == estudiante_id
                and practica.estado != Practica.ESTADO_FINALIZADA
            ):
                return True
        return False
       
  

    def __practica_ya_existe_para_cursada(self, cursada_id):
        practicas = self.__practica_repository.listar()
        for practica in practicas:
            if practica.cursada.id == cursada_id:
                return True
        return False

    def registrar_practica(self, practica):
        docente = practica.docenteAdscriptor
        if docente is not None:
            docente = self.__docente_service.obtener_por_id(docente.id)

        if self.__existe_practica_activa(practica.cursada.estudiante.id):
            raise ValueError("El estudiante ya tiene una práctica activa")
        
        if self.__practica_ya_existe_para_cursada(practica.cursada.id):
            raise ValueError("Ya existe una práctica para esta cursada")

        if practica.cursada.curso.requiere_docente_adscriptor and docente is None:
            raise ValueError("El curso requiere un docente adscriptor")

        if practica.cursada.curso.requiere_grupo and practica.grupo is None:
            raise ValueError("El curso requiere un grupo")

        if not practica.cursada.curso.requiere_docente_adscriptor:
            practica.estado = Practica.ESTADO_EN_CURSO

        elif self.__docente_service.asignar_practica(docente.id, practica.id):
            practica.estado = Practica.ESTADO_EN_CURSO
        else:
            practica.estado = Practica.ESTADO_EN_ESPERA

        return self.__practica_repository.agregar(practica)

    def registrar_asistencia(
        self, practica_id, fecha, estado, observaciones=None
    ):
        practica = self.obtener_por_id(practica_id)
        if practica is None:
            raise ValueError("La practica no existe")

        asistencia = self.__asistencia_service.crear(
            fecha, estado, observaciones
        )
        practica.agregar_asistencia(asistencia)
        self.actualizar(practica)
        return asistencia

    def registrar_visita_didactica(
        self,
        practica_id,
        fecha,
        observaciones,
        nota,
        docente_didactica,
        docente_adscriptor,
        docente_extra=None,
    ):
        practica = self.obtener_por_id(practica_id)
        if practica is None:
            raise ValueError("La practica no existe")

        visita = self.__visita_didactica_service.crear(
            fecha,
            observaciones,
            nota,
            docente_didactica,
            docente_adscriptor,
            docente_extra,
        )
        practica.agregar_visita_didactica(visita)
        self.actualizar(practica)
        return visita

    def finalizar_practica(self, id):
        practica = self.__practica_repository.obtener_por_id(id)
        if practica is None:
            raise ValueError("La practica no existe")
        if practica.estado != Practica.ESTADO_EN_CURSO:
            raise ValueError("Solo se puede finalizar una practica en curso")

        practica.estado = Practica.ESTADO_FINALIZADA
        if practica.docenteAdscriptor is not None:
            practica_promovida_id = self.__docente_service.liberar_practica(
                practica.docenteAdscriptor.id, practica.id
            )
            self.__promocionar_practica_en_espera(practica_promovida_id)
        self.__practica_repository.actualizar(practica)
        return practica

    def _hidratar_relaciones(self, practica):
        if practica is None:
            return None

        practica.cursada = self.__cursada_service.obtener_por_id(practica.cursada.id)
        practica.institucion = self.__institucion_service.obtener_por_id(
            practica.institucion.id
        )
        practica.docenteDidactica = self.__docente_service.obtener_por_id(
            practica.docenteDidactica.id
        )

        if practica.grupo is not None:
            practica.grupo = self.__grupo_service.obtener_por_id(practica.grupo.id)

        if practica.asistencias:
            asistencias_hidratadas = []
            for asistencia in practica.asistencias:
                asistencia_hidratada = self.__asistencia_service.obtener_por_id(
                    asistencia.id
                )
                asistencias_hidratadas.append(asistencia_hidratada)
            practica.asistencias = asistencias_hidratadas
        if practica.visitasDidacticas:
            visitas_hidratadas = []
            for visita in practica.visitasDidacticas:
                visita_hidratada = self.__visita_didactica_service.obtener_por_id(
                    visita.id
                )
                visitas_hidratadas.append(visita_hidratada)
            practica.visitasDidacticas = visitas_hidratadas

        return practica

    def obtener_por_id(self, id):
        practica = self.__practica_repository.obtener_por_id(id)
        if practica is None:
            return None
        return self._hidratar_relaciones(practica)

    def obtener_por_cursada_id(self, cursada_id):
        """
        Retorna la práctica asociada a una cursada específica (si existe).
        
        Args:
            cursada_id: ID de la cursada.
            
        Returns:
            Objeto Practica hidratado o None si no existe práctica para esa cursada.
        """
        practicas = self.__practica_repository.listar()
        for practica in practicas:
            if practica.cursada.id == cursada_id:
                return self._hidratar_relaciones(practica)
        return None

    def listar(self):
        practicas = self.__practica_repository.listar()
        return [self._hidratar_relaciones(p) for p in practicas]

    def actualizar(self, practica):
        return self.__practica_repository.actualizar(practica)

    def eliminar(self, id):
        practica = self.__practica_repository.obtener_por_id(id)
        if practica is None:
            raise ValueError("La practica no existe")
        
        
        if practica.docenteAdscriptor is not None:
            if practica.estado == Practica.ESTADO_EN_CURSO:
                practica_promovida_id = self.__docente_service.liberar_practica(
                    practica.docenteAdscriptor.id, practica.id
                )
                self.__promocionar_practica_en_espera(practica_promovida_id)
            elif practica.estado == Practica.ESTADO_EN_ESPERA:   
                self.__docente_service.quitar_de_lista_espera(
                    practica.docenteAdscriptor.id, practica.id
                )
        
        return self.__practica_repository.eliminar(id)

    def __promocionar_practica_en_espera(self, practica_promovida_id):
        #Promueve una práctica de la cola a activas, le cambia el estado a EN_CURSO y la actualiza.
        if practica_promovida_id is not None:
            practica_promovida = self.__practica_repository.obtener_por_id(
                practica_promovida_id
            )
            practica_promovida.estado = Practica.ESTADO_EN_CURSO
            self.__practica_repository.actualizar(practica_promovida)