import pandas as pd
import pyodbc
from datetime import datetime

# ================================================
# EXTRACT — Crear CSV con datos sucios (simulando fuente real)
# ================================================

data_sucia = {
    'fecha':          ['2026-01-05','2026-01-12','01/18/2026','2026-01-25','2026-01-30',
                       '2026-02-03','2026-02-08','02-14-2026','2026-02-20','2026-02-25',
                       '2026-03-02','2026-03-07','2026-03-11','2026-03-15','2026-03-20'],
    'cliente':        ['Tech SA','comercial norte','TECH SA','Juan Perez','juan perez',
                       'Comercial Norte','tech sa','Barcelona SL','JUAN PEREZ','Tech SA',
                       'COMERCIAL NORTE','Barcelona SL','Tech SA','juan perez','Comercial Norte'],
    'producto':       ['Notebook','Monitor','notebook','Teclado','TECLADO',
                       'Monitor','Notebook','Silla','teclado','NOTEBOOK',
                       'monitor','Silla','Teclado','Notebook','MONITOR'],
    'cantidad':       [1, 2, 1, 3, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 3],
    'precio':         [220000, 120000, 220000, 28000, 28000,
                       120000, 220000, 75000, 28000, 220000,
                       120000, 75000, 28000, 220000, 120000],
    'pais':           ['Argentina','Argentina','argentina','Argentina','ARGENTINA',
                       'argentina','Argentina','España','ARGENTINA','Argentina',
                       'Argentina','españa','Argentina','argentina','Argentina']
}

# Guardar CSV sucio
df_sucio = pd.DataFrame(data_sucia)
df_sucio.to_csv('ventas_sucias.csv', index=False)
print(f"CSV creado con {len(df_sucio)} registros")
print("\n=== DATOS SUCIOS (primeras 5 filas) ===")
print(df_sucio.head())

# ================================================
# TRANSFORM — Limpiar y normalizar
# ================================================

df = pd.read_csv('ventas_sucias.csv')

print(f"\n=== ANTES DE LIMPIAR ===")
print(f"Registros: {len(df)}")
print(f"Duplicados: {df.duplicated().sum()}")

# 1. Normalizar texto
df['cliente']  = df['cliente'].str.strip().str.title()
df['producto'] = df['producto'].str.strip().str.title()
df['pais']     = df['pais'].str.strip().str.title()

# 2. Normalizar fechas
df['fecha'] = pd.to_datetime(df['fecha'], dayfirst=False, format='mixed')

# 3. Eliminar duplicados
df = df.drop_duplicates()

# 4. Agregar columnas calculadas
df['total']      = df['cantidad'] * df['precio']
df['mes']        = df['fecha'].dt.month
df['anio']       = df['fecha'].dt.year
df['cargado_en'] = datetime.now()

print(f"\n=== DESPUÉS DE LIMPIAR ===")
print(f"Registros: {len(df)}")
print(f"Duplicados: {df.duplicated().sum()}")
print("\n=== DATOS LIMPIOS (primeras 5 filas) ===")
print(df.head())

# Guardar CSV limpio
df.to_csv('ventas_limpias.csv', index=False)
print("\nCSV limpio guardado: ventas_limpias.csv")

# ================================================
# LOAD — Cargar en SQL Server
# ================================================

conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=localhost;'
    'DATABASE=retail_analytics;'
    'Trusted_Connection=yes;'
)
cursor = conn.cursor()

# Crear tabla si no existe
cursor.execute("""
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'etl_ventas')
    CREATE TABLE etl_ventas (
        id          INT PRIMARY KEY IDENTITY(1,1),
        fecha       DATE,
        cliente     VARCHAR(100),
        producto    VARCHAR(100),
        cantidad    INT,
        precio      DECIMAL(10,2),
        total       DECIMAL(10,2),
        pais        VARCHAR(50),
        mes         INT,
        anio        INT,
        cargado_en  DATETIME
    )
""")

# Insertar registros
registros_cargados = 0
for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO etl_ventas (fecha, cliente, producto, cantidad, precio, total, pais, mes, anio, cargado_en)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, row['fecha'], row['cliente'], row['producto'],
         row['cantidad'], row['precio'], row['total'],
         row['pais'], row['mes'], row['anio'], row['cargado_en'])
    registros_cargados += 1

conn.commit()
conn.close()

print(f"\n=== CARGA COMPLETADA ===")
print(f"Registros cargados en SQL Server: {registros_cargados}")
print("Tabla: retail_analytics.dbo.etl_ventas")