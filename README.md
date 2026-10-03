# Proyecto Atlas

Base de dominio para administrar prácticas estudiantiles. El proyecto usa una arquitectura tradicional en capas:

- `models/`: entidades anémicas y referencias entre objetos.
- `services/`: acciones y reglas de negocio.
- `repositories/`: persistencia local en archivos JSON, sin cachear entidades entre operaciones.

Cada repository utiliza siempre un archivo independiente dentro de `data/`. Las
referencias entre entidades se guardan mediante IDs y se reconstruyen al leer.

## Apunte - Flujo para select dependientes

- Insitucion se listan con institucion_service
- Grupos se obtienen con grupo_service, se tiene diponible una funcion obtener_por_institucion(institucion id) para poder obtener los grupos de una institucion
- El docente de un grupo es opcional. Al obtener los grupos de una institución, las relaciones existentes vienen hidratadas.
