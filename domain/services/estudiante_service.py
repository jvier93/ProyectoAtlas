from domain.models.estudiante import Estudiante
from domain.repositories.estudiante_repository import EstudianteRepository


class EstudianteService:
    def __init__(self):
        self.__repository = EstudianteRepository()

    def crear(self, nombre, puntuacionEnLista):
        self.__validar_datos(nombre, puntuacionEnLista)

        id_nuevo = self.__repository.obtener_proximo_id()
        estudiante = Estudiante(id_nuevo, nombre, puntuacionEnLista)
        return self.__repository.agregar(estudiante)

    def __validar_datos(self, nombre, puntuacionEnLista):
        if nombre is None or nombre == "" or not nombre.strip():
            raise ValueError("El nombre del estudiante es obligatorio")
        if (
            puntuacionEnLista is None
            or puntuacionEnLista == ""
            or not str(puntuacionEnLista).strip()
        ):
            raise ValueError("La puntuación en lista del estudiante es obligatoria")

    def obtener_por_id(self, id):
        return self.__repository.obtener_por_id(id)

    def listar(self):
        return self.__repository.listar()

    def buscar(self, criterio):
        return self.__repository.buscar(criterio)

    def actualizar(self, id, nombre, puntuacionEnLista):
        self.__validar_datos(nombre, puntuacionEnLista)
        estudiante = Estudiante(id, nombre, puntuacionEnLista)
        return self.__repository.actualizar(estudiante)

    def eliminar(self, id):
        from domain.services.cursada_service import CursadaService
        from domain.services.practica_service import PracticaService

        cursada_service = CursadaService()
        practica_service = PracticaService()
        cursadas = cursada_service.listar_cursadas_de_estudiante(id)

        for cursada in cursadas:
            practica = practica_service.obtener_por_cursada_id(cursada.id)
            if practica is not None:
                practica_service.eliminar(practica.id)
            cursada_service.eliminar(cursada.id)

        return self.__repository.eliminar(id)
