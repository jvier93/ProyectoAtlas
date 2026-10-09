# Proyecto Atlas

Proyecto para administrar prácticas estudiantiles con una arquitectura pensada en capas y una interfaz desarrollada con Flet.

## Descripción general

La aplicación gestiona instituciones, grupos, docentes, estudiantes y cursos, manteniendo la lógica de negocio separada de la capa de presentación.

Estructura principal:

- `domain/`: modelos y servicios del dominio.
- `views/`: pantallas y formularios de la interfaz Flet.
- `data/`: almacenamiento local de los datos.
- `storage/`: archivos auxiliares de almacenamiento.
- `assets/`: recursos gráficos del proyecto.
- `docs/`: documentación y diagramas del sistema.

Cada repositorio usa un archivo independiente dentro de `data/` y las relaciones entre entidades se almacenan por IDs para reconstruirse al momento de leer la información.

## Requisitos

- Python 3.10 o superior
- pip actualizado
- Entorno virtual recomendado (`.venv`)

## Instalación

1. Clona el repositorio y entra a la carpeta del proyecto:

   ```bash
   git clone https://github.com/jvier93/ProyectoAtlas.git
   cd ProyectoAtlas
   ```

2. Crea y activa un entorno virtual:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

   En Windows PowerShell:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Instala las dependencias del proyecto:

   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

## Ejecución

Para levantar la aplicación:

```bash
python main.py
```

También puedes usar Flet directamente:

```bash
flet run main.py
```

## Documentación

La carpeta de documentación del proyecto es `docs/`.

Dentro de ella se encuentran el diagrama de la app:

- `docs/diagramas/diagrama_clases_actual.mmd`
