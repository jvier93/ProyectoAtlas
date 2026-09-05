class Estudiante:
    def __init__(self, id, nombre, puntuacionEnLista):
        self.__id = id
        self.__nombre = nombre
        self.__puntuacionEnLista = puntuacionEnLista

    @property
    def id(self):
        return self.__id

    @property
    def nombre(self):
        return self.__nombre

    @property
    def puntuacionEnLista(self):
        return self.__puntuacionEnLista