class Asistencia:
    ASISTIO = "Asistio"
    NO_ASISTIO = "No asistio"
    JUSTIFICADA = "Justificada"

    def __init__(self, id, fecha, estado, observaciones=None):
        self.__id = id
        self.__fecha = fecha
        self.__estado = estado
        self.__observaciones = observaciones

    @property
    def id(self):
        return self.__id

    @property
    def fecha(self):
        return self.__fecha

    @property
    def estado(self):
        return self.__estado

    @property
    def observaciones(self):
        return self.__observaciones