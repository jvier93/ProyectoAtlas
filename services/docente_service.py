from models.docente import Docente
from repositories.docente_repository import DocenteRepository


class DocenteService:
    def __init__(self):
        self.__repository = DocenteRepository()

   
    def crear(self, nombre, tipo="general"):
        id_nuevo = self.__repository.obtener_proximo_id()
        docente = Docente(id_nuevo, nombre, tipo=tipo)
        return self.__repository.agregar(docente)

    def obtener_por_id(self, id):
        docente = self.__repository.obtener_por_id(id)
        return docente

    def listar(self):
        docentes = []
        for docente in self.__repository.listar():
            docentes.append(docente)
        return docentes


    def actualizar(self, docente):
        return self.__repository.actualizar(docente)

    def eliminar(self, id):
        return self.__repository.eliminar(id)


    def asignar_practica(self, docente_id, practica_id):
       #Asigna una practica y la agrega a activos, si no hay cupo la pone en espera.
        docente = self.obtener_por_id(docente_id)
        if docente is None or docente.tipo != "adscriptor":
            return None

        if len(docente.activas) < docente.cuposMaximo:
            docente.agregar_activo(practica_id)
            self.actualizar(docente)
            return True

        docente.encolar_en_lista_espera(practica_id)
        self.actualizar(docente)
        return False

#Quita la practica en activos y si hay alguien en lista de espera lo promueve a activos cola (FIFO)
    def liberar_practica(self, docente_id, practica_id):
       
        docente = self.obtener_por_id(docente_id)
        if docente is None or docente.tipo != "adscriptor":
            return None

        docente.quitar_activo(practica_id)
        practica_promovida_id = docente.desencolar_siguiente_en_espera()
        if practica_promovida_id is not None:
            docente.agregar_activo(practica_promovida_id)
        self.actualizar(docente)
        return practica_promovida_id

      
        docente = self.obtener_por_id(docente_id)
        if docente and docente.tipo == "adscriptor":
            docente.encolar_en_lista_espera(practica)
            return self.actualizar(docente)
        return None


    def quitar_de_lista_espera(self, docente_id, practica):
        docente = self.obtener_por_id(docente_id)
        if docente and docente.tipo == "adscriptor":
            docente.quitar_de_lista_espera(practica)
            return self.actualizar(docente)
        return None
