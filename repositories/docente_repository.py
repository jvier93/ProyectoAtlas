from models.docente import Docente
from repositories.json_repository import JsonStore


class DocenteRepository:
    def __init__(self, filename="data/docentes.json"):
        self.__store = JsonStore(
            filename, self.__serializar, self.__deserializar
        )

    def __serializar(self, docente):
        return {
            "id": docente.id,
            "nombre": docente.nombre,
            "tipo": docente.tipo,
            # Las listas ya contienen solo IDs
            "lista_espera_ids": list(docente.listaEspera),
            "activas_ids": list(docente.activas),
        }

    def __deserializar(self, registro):
        # Soporta desserialización de diferentes tipos de docente
        tipo = registro.get("tipo", "general")
        docente = Docente(
            registro["id"],
            registro["nombre"],
            tipo=tipo,
        )
        
        # Cargar IDs de prácticas en las listas del adscriptor
        if tipo == "adscriptor":
            for practica_id in registro.get("activas_ids", []):
                docente.agregar_activo(practica_id)
            for practica_id in registro.get("lista_espera_ids", []):
                docente.encolar_en_lista_espera(practica_id)
        
        return docente

    def listar_registros(self):
        return self.__store._JsonStore__read_records()

    def obtener_registro_por_id(self, id):
        for registro in self.listar_registros():
            if registro.get("id") == id:
                return registro
        return None

    def agregar(self, entidad):
        return self.__store.agregar(entidad)

    def crear(self, entidad):
        return self.__store.crear(entidad)

    def obtener_por_id(self, id):
        return self.__store.obtener_por_id(id)

    def obtener_proximo_id(self):
        return self.__store.obtener_proximo_id()

    def buscar(self, criterio):
        return self.__store.buscar(criterio)

    def listar(self):
        return self.__store.listar()

    def actualizar(self, entidad):
        return self.__store.actualizar(entidad)

    def eliminar(self, id):
        return self.__store.eliminar(id)