class Practica:
    ESTADO_EN_ESPERA = "en espera"
    ESTADO_EN_CURSO = "en curso"
    ESTADO_FINALIZADA = "finalizada"

    def __init__(
        self,
        id,
        cursada,
        institucion,
        grupo=None,
        docenteAdscriptor=None,
        docenteDidactica=None,
        estado=ESTADO_EN_CURSO,
        notaFinal=None,
        observaciones=None,
        
    ):
        self.__id = id
        self.__cursada = cursada
        self.__institucion = institucion
        self.__grupo = grupo
        self.__docenteAdscriptor = docenteAdscriptor
        self.__docenteDidactica = docenteDidactica
        self.__estado = estado
        self.__asistencias = []
        self.__visitasDidacticas = []
        self.__notaFinal = notaFinal
        self.__observaciones = observaciones
      

    def __str__(self):
        return (
            f"Practica(id={self.__id}, "
            f"cursada={self.__cursada.curso.nombre}/{self.__cursada.anio}, "
            f"institucion={self.__institucion.nombre}, "
            # f"grupo={self.__grupo}, "
            # f"docenteAdscriptor={self.__docenteAdscriptor}, "
            # f"docenteDidactica={self.__docenteDidactica}, "
            # f"estado={self.__estado}, "
            # f"notaFinal={self.__notaFinal}, "
            # f"observaciones={self.__observaciones})"
            
        )

    @property
    def id(self):
        return self.__id

    @property
    def cursada(self):
        return self.__cursada

    @cursada.setter
    def cursada(self, cursada):
        self.__cursada = cursada

    @property
    def institucion(self):
        return self.__institucion

    @institucion.setter
    def institucion(self, institucion):
        self.__institucion = institucion

    @property
    def grupo(self):
        return self.__grupo

    @grupo.setter
    def grupo(self, grupo):
        self.__grupo = grupo

    @property
    def docenteAdscriptor(self):
        return self.__docenteAdscriptor

    @docenteAdscriptor.setter
    def docenteAdscriptor(self, docenteAdscriptor):
        self.__docenteAdscriptor = docenteAdscriptor

    @property
    def docenteDidactica(self):
        return self.__docenteDidactica

    @docenteDidactica.setter
    def docenteDidactica(self, docenteDidactica):
        self.__docenteDidactica = docenteDidactica

    @property
    def estado(self):
        return self.__estado

    @estado.setter
    def estado(self, estado):
        self.__estado = estado

    @property
    def asistencias(self):
        return tuple(self.__asistencias)

    @asistencias.setter
    def asistencias(self, asistencias):
        self.__asistencias = list(asistencias or [])

    @property
    def visitasDidacticas(self):
        return tuple(self.__visitasDidacticas)

    @visitasDidacticas.setter
    def visitasDidacticas(self, visitas):
        self.__visitasDidacticas = list(visitas or [])

    @property
    def notaFinal(self):
        return self.__notaFinal

    @property
    def observaciones(self):
        return self.__observaciones

    @observaciones.setter
    def observaciones(self, observaciones):
        self.__observaciones = observaciones

    @notaFinal.setter
    def notaFinal(self, notaFinal):
        self.__notaFinal = notaFinal

    def agregar_asistencia(self, asistencia):
        self.__asistencias.append(asistencia)

    def agregar_visita_didactica(self, visita):
        self.__visitasDidacticas.append(visita)
