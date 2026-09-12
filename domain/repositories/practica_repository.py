from domain.models.practica import Practica
from domain.repositories.json_repository import JsonStore
from types import SimpleNamespace


class PracticaRepository:
    def __init__(
        self,
        filename="data/practicas.json",
    ):
        self.__store = JsonStore(
            filename, self.__serializar, self.__deserializar
        )

    def __serializar(self, practica):
        return {
            "id": practica.id,
            "cursada_id": practica.cursada.id,
            "institucion_id": practica.institucion.id,
            "grupo_id": practica.grupo.id if practica.grupo else None,
            "docente_adscriptor_id": (
                practica.docenteAdscriptor.id
                if practica.docenteAdscriptor
                else None
            ),
            "docente_didactica_id": (
                practica.docenteDidactica.id
                if practica.docenteDidactica
                else None
            ),
            "estado": practica.estado,
            "asistencias": [
                asistencia.id for asistencia in practica.asistencias
            ],
            "visitas_didacticas": [
                visita.id for visita in practica.visitasDidacticas
            ],
            "nota_final": practica.notaFinal,
            "observaciones": practica.observaciones,
        }

    def __deserializar(self, registro):
        asistencias = [
            SimpleNamespace(id=asistencia_id)
            for asistencia_id in registro.get("asistencias", [])
        ]
        visitas_didacticas = [
            SimpleNamespace(id=visita_id)
            for visita_id in registro.get("visitas_didacticas", [])
        ]

        practica = Practica(
            registro["id"],
            SimpleNamespace(id=registro["cursada_id"]),
            SimpleNamespace(id=registro["institucion_id"]),
            SimpleNamespace(id=registro["grupo_id"])
            if registro.get("grupo_id") is not None
            else None,
            SimpleNamespace(id=registro["docente_adscriptor_id"])
            if registro.get("docente_adscriptor_id") is not None
            else None,
            SimpleNamespace(id=registro["docente_didactica_id"])
            if registro.get("docente_didactica_id") is not None
            else None,
            estado=registro.get("estado", Practica.ESTADO_EN_CURSO),
            notaFinal=registro.get("nota_final"),
            observaciones=registro.get("observaciones"),
        )
        practica.asistencias = asistencias
        practica.visitasDidacticas = visitas_didacticas
        return practica

    def agregar(self, entidad):
        return self.__store.agregar(entidad)

    def crear(self, entidad):
        return self.__store.crear(entidad)

    def obtener_por_id(self, id):
        return self.__store.obtener_por_id(id)

    def listar(self):
        return self.__store.listar()

    def actualizar(self, entidad):
        return self.__store.actualizar(entidad)

    def eliminar(self, id):
        return self.__store.eliminar(id)

    def obtener_proximo_id(self):
        return self.__store.obtener_proximo_id()
