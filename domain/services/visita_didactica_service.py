from domain.models.visita_didactica import VisitaDidactica
from domain.services.docente_service import DocenteService
from domain.repositories.visita_didactica_repository import VisitaDidacticaRepository


class VisitaDidacticaService:
    def __init__(self, repository=None, docente_service=None):
        self.__repository = repository or VisitaDidacticaRepository()
        self.__docente_service = docente_service or DocenteService()

    def crear(
        self,
        fecha,
        observaciones,
        nota,
        docenteDidactica,
        docenteAdscriptor,
        docenteExtra=None,
    ):
        id_nuevo = self.__repository.obtener_proximo_id()
        visita = VisitaDidactica(
            id_nuevo,
            fecha,
            observaciones,
            nota,
            docenteDidactica,
            docenteAdscriptor,
            docenteExtra,
        )
        return self.__repository.agregar(visita)

    def obtener_por_id(self, id):
        visita = self.__repository.obtener_por_id(id)
        if visita is None:
            return None
        return self._hidratar_relaciones(visita)

    def listar(self):
        visitas = self.__repository.listar()
        return [self._hidratar_relaciones(visita) for visita in visitas]

    def buscar(self, criterio):
        visitas = self.__repository.buscar(criterio)
        return [self._hidratar_relaciones(visita) for visita in visitas]

    def actualizar(self, visita):
        return self.__repository.actualizar(visita)

    def eliminar(self, id):
        return self.__repository.eliminar(id)

    def _hidratar_relaciones(self, visita):
        if visita is None:
            return None

        visita.docenteDidactica = self.__docente_service.obtener_por_id(
            visita.docenteDidactica.id
        )
        visita.docenteAdscriptor = self.__docente_service.obtener_por_id(
            visita.docenteAdscriptor.id
        )

        if visita.docenteExtra is not None:
            visita.docenteExtra = self.__docente_service.obtener_por_id(
                visita.docenteExtra.id
            )

        return visita