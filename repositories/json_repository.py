import json
import os
from pathlib import Path


class JsonStore:
    def __init__(self, filename, serializer, deserializer):
        self.__path = Path(filename)
        self.__serializer = serializer
        self.__deserializer = deserializer

    def __read_records(self):
        if not self.__path.exists():
            return []
        with self.__path.open("r", encoding="utf-8") as archivo:
            contenido = archivo.read().strip()
        if not contenido:
            return []
        registros = json.loads(contenido)
        if not isinstance(registros, list):
            raise ValueError(f"El archivo {self.__path} debe contener una lista JSON")
        return registros

    def __write_records(self, registros):
        self.__path.parent.mkdir(parents=True, exist_ok=True)
        temporal = self.__path.with_suffix(self.__path.suffix + ".tmp")
        with temporal.open("w", encoding="utf-8") as archivo:
            json.dump(registros, archivo, ensure_ascii=False, indent=2)
            archivo.write("\n")
        os.replace(temporal, self.__path)

    def agregar(self, entidad):
        registros = self.__read_records()
        if any(registro.get("id") == entidad.id for registro in registros):
            raise ValueError("Ya existe una entidad con ese id")
        registros.append(self.__serializer(entidad))
        self.__write_records(registros)
        return entidad

    def crear(self, entidad):
        return self.agregar(entidad)

    def obtener_por_id(self, id):
        for registro in self.__read_records():
            if registro.get("id") == id:
                return self.__deserializer(registro)
        return None

    def buscar(self, criterio):
        return [
            entidad
            for entidad in self.listar()
            if criterio(entidad)
        ]

    def listar(self):
        return [
            self.__deserializer(registro)
            for registro in self.__read_records()
        ]

    def actualizar(self, entidad):
        registros = self.__read_records()
        for indice, registro in enumerate(registros):
            if registro.get("id") == entidad.id:
                registros[indice] = self.__serializer(entidad)
                self.__write_records(registros)
                return entidad
        raise ValueError("La entidad no existe")

    def eliminar(self, id):
        registros = self.__read_records()
        for indice, registro in enumerate(registros):
            if registro.get("id") == id:
                entidad = self.__deserializer(registro)
                del registros[indice]
                self.__write_records(registros)
                return entidad
        return None

    def obtener_proximo_id(self):
        """Devuelve el próximo ID disponible (máximo + 1)"""
        registros = self.__read_records()
        if not registros:
            return 1
        return max(int(registro.get("id", 0)) for registro in registros) + 1