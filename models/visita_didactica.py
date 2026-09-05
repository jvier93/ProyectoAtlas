class VisitaDidactica:
    def __init__(
        self,
        id,
        fecha,
        observaciones,
        nota,
        docenteDidactica,
        docenteAdscriptor,
        docenteExtra=None,
    ):
        self.__id = id
        self.__fecha = fecha
        self.__observaciones = observaciones
        self.__nota = nota
        self.__docenteDidactica = docenteDidactica
        self.__docenteAdscriptor = docenteAdscriptor
        self.__docenteExtra = docenteExtra

    @property
    def id(self):
        return self.__id

    @property
    def fecha(self):
        return self.__fecha

    @property
    def observaciones(self):
        return self.__observaciones

    @property
    def nota(self):
        return self.__nota

    @property
    def docenteDidactica(self):
        return self.__docenteDidactica

    @docenteDidactica.setter
    def docenteDidactica(self, docente):
        self.__docenteDidactica = docente

    @property
    def docenteAdscriptor(self):
        return self.__docenteAdscriptor

    @docenteAdscriptor.setter
    def docenteAdscriptor(self, docente):
        self.__docenteAdscriptor = docente

    @property
    def docenteExtra(self):
        return self.__docenteExtra

    @docenteExtra.setter
    def docenteExtra(self, docente):
        self.__docenteExtra = docente