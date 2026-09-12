class Institucion:
    def __init__(self, id, nombre, direccion):
        self.__id = id
        self.__nombre = nombre
        self.__direccion = direccion

    @property
    def id(self):
        return self.__id

    @property
    def nombre(self):
        return self.__nombre

    @property
    def direccion(self):
        return self.__direccion