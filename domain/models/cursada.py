class Cursada:


    def __init__(self, id, estudiante, curso, anio, docenteDidactica):
     
        self.__id = id
        self.__estudiante = estudiante
        self.__curso = curso
        self.__anio = anio
        self.__docenteDidactica = docenteDidactica

    @property
    def id(self):
        return self.__id

    @property
    def estudiante(self):
        return self.__estudiante

    @estudiante.setter
    def estudiante(self, estudiante):
        self.__estudiante = estudiante

    @property
    def curso(self):
        return self.__curso

    @curso.setter
    def curso(self, curso):
        self.__curso = curso

    @property
    def anio(self):
        return self.__anio

    @property
    def docenteDidactica(self):
        return self.__docenteDidactica

    @docenteDidactica.setter
    def docenteDidactica(self, docenteDidactica):
        self.__docenteDidactica = docenteDidactica
