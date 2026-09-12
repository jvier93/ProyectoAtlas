class Docente:
  
    
    def __init__(self, id, nombre, tipo="general"):
        
        tiposDocente = ("general", "adscriptor", "didactica")
        if tipo not in tiposDocente:
            raise ValueError("Tipo de docente no válido")
        self.__id = id
        self.__nombre = nombre
        self.__tipo = tipo  # "general", "adscriptor", "didactica"
        
        # Solo para docente de tipo adscriptor.
        self.__activas = []
        self.__listaEspera = []
        self.__cuposMaximo = 3

    @property
    def id(self):
        return self.__id

    @property
    def nombre(self):
        return self.__nombre
    
    @property
    def tipo(self):
        return self.__tipo
    
    
    @property
    def activas(self):
        return tuple(self.__activas)

    @property
    def listaEspera(self):
        return tuple(self.__listaEspera)

    @property
    def cuposMaximo(self):
        return self.__cuposMaximo
    
    
    def agregar_activo(self, practica_id):
        if self.__tipo != "adscriptor":
            return

        if practica_id not in self.__activas:
            self.__activas.append(practica_id)

    def quitar_activo(self, practica_id):
        if self.__tipo != "adscriptor":
            return

        if practica_id in self.__activas:
            self.__activas.remove(practica_id)

    def encolar_en_lista_espera(self, practica_id):
        if self.__tipo != "adscriptor":
            return

        if practica_id not in self.__listaEspera:
            self.__listaEspera.append(practica_id)

  

    def desencolar_siguiente_en_espera(self):
        if self.__tipo != "adscriptor":
            return None

        if not self.__listaEspera:
            return None

        return self.__listaEspera.pop(0)

    def siguiente_de_lista_espera(self):
       
        return self.desencolar_siguiente_en_espera()

    def quitar_de_lista_espera(self, practica_id):
        if self.__tipo != "adscriptor":
            return

        if practica_id in self.__listaEspera:
            self.__listaEspera.remove(practica_id)