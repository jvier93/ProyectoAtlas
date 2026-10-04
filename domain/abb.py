class Nodo:
    def __init__(self, clave, dato):
        self.clave = clave
        self.dato = dato
        self.izquierda = None
        self.derecha = None


class Arbol:
    def __init__(self):
        self.__raiz = None

    def insertar(self, clave, dato):
        self.__raiz = self.__insertar_recursivo(self.__raiz, clave, dato)

    def __insertar_recursivo(self, nodo, clave, dato):
        if nodo is None:
            return Nodo(clave, dato)

        if clave < nodo.clave:
            nodo.izquierda = self.__insertar_recursivo(nodo.izquierda, clave, dato)
        elif clave > nodo.clave:
            nodo.derecha = self.__insertar_recursivo(nodo.derecha, clave, dato)

        return nodo

    def buscar(self, clave):
        return self.__buscar_recursivo(self.__raiz, clave)

    def __buscar_recursivo(self, nodo, clave):
        if nodo is None:
            return None
        if clave == nodo.clave:
            return nodo.dato
        if clave < nodo.clave:
            return self.__buscar_recursivo(nodo.izquierda, clave)
        return self.__buscar_recursivo(nodo.derecha, clave)
