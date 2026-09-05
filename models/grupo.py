class Grupo:
    def __init__(self, id, nombre, docente, institucion, horario):
        self.__id = id
        self.__nombre = nombre
        self.__docente = docente
        self.__institucion = institucion
        self.__horario = horario

    @property
    def id(self):
        return self.__id

    @property
    def nombre(self):
        return self.__nombre

    @property
    def docente(self):
        return self.__docente
    
    @docente.setter
    def docente(self, docente):
        self.__docente = docente

    @property
    def institucion(self):
        return self.__institucion
    
    @institucion.setter
    def institucion(self, institucion):
        self.__institucion = institucion

    @property
    def horario(self):
        return self.__horario