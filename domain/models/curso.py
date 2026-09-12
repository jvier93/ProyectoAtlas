class Curso:

    def __init__(
        self,
        id,
        nombre,
        requiere_docente_adscriptor=False,
        requiere_grupo=False
    ):
        self.__id = id
        self.__nombre = nombre
        self.__requiere_docente_adscriptor = requiere_docente_adscriptor
        self.__requiere_grupo = requiere_grupo

    @property
    def id(self):
        return self.__id

    @property
    def nombre(self):
        return self.__nombre

    @property
    def requiere_docente_adscriptor(self):
        return self.__requiere_docente_adscriptor

    @property
    def requiere_grupo(self):
        return self.__requiere_grupo