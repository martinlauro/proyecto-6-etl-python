# proyecto-6-etl-python
ETL con Python — limpieza y carga de datos en SQL Server


Pipeline ETL completo: extracción de datos sucios, 
transformación y carga en SQL Server.

## Tecnologías
- Python (pandas, pyodbc)
- SQL Server

## Proceso ETL
- **Extract** — Lectura de CSV con datos sucios (fechas inconsistentes, 
  texto en mayúsculas/minúsculas mezcladas)
- **Transform** — Normalización de texto, fechas y eliminación de duplicados
- **Load** — Carga automática en SQL Server

## Archivos
- `etl_ventas.py` — Script principal ETL
- `ventas_sucias.csv` — Datos originales sin limpiar
- `ventas_limpias.csv` — Datos después de la transformación

## Autor
Martin Lauro — [LinkedIn](https://www.linkedin.com/in/martin-lauro/)
