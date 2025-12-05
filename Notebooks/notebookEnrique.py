import pandas as pd
import numpy as np
import random
import re

# --- 1. Cargar el Dataset Original ---
df = pd.read_csv("felicidad.csv")

    
# Crear una copia para la modificación
df_dirty = df.copy()

# ---Introducir Problemas de Calidad de Datos (Dirtying)---

# Configuración de semilla para reproducibilidad
np.random.seed(42) 
random.seed(42)

# Renombrar una columna
df_dirty.rename(columns={'Trust (Government Corruption)': 'Trust'}, inplace=True)
print("-> Cabecera 'Trust (Government Corruption)' renombrada a 'Trust'.")

# 1. Missing Data (Datos Faltantes): 
# a) NaNs en columna numérica
rows_to_null = np.random.choice(df_dirty.index, size=10, replace=False)
df_dirty.loc[rows_to_null, 'Family'] = np.nan
print(f"-> {len(rows_to_null)} valores NaN introducidos en 'Family'.")

# b) Cadenas Vacías en columna numérica (lo convierte a 'object' implícitamente)
rows_to_blank = np.random.choice(df_dirty.index.difference(rows_to_null), size=5, replace=False)
df_dirty.loc[rows_to_blank, 'Generosity'] = '' 
print(f"-> {len(rows_to_blank)} celdas en blanco introducidas en 'Generosity'.")

# 2.Filas Duplicadas:
# a) Duplicados exactos las primeras 2 filas
df_dirty = pd.concat([df_dirty, df_dirty.iloc[[0, 1]]], ignore_index=True)
# b) Duplicados parciales cambiando ligeramente el puntaje
partial_dup = df_dirty.iloc[[2, 3]].copy()
partial_dup['Happiness Score'] = partial_dup['Happiness Score'].astype(float) + 0.001
df_dirty = pd.concat([df_dirty, partial_dup], ignore_index=True)
print("-> 4 filas duplicadas (2 exactas, 2 parciales) añadidas.")

# 3. Outliers Valores Atípicos
# Usamos las nuevas filas duplicadas para los outliers
idx_outliers = df_dirty.index[-2:]
df_dirty.loc[idx_outliers[0], 'Economy (GDP per Capita)'] = 999.0
df_dirty.loc[idx_outliers[1], 'Economy (GDP per Capita)'] = -50.0
print("-> Outliers insertados en 'Economy (GDP per Capita)' (999.0 y -50.0).")

# Inconsistencias de Formato
# Cambiar '.' por ',' y añadir unidad 'pt' en 'Happiness Score'
rows_to_format = df_dirty.index[4:7]
for idx in rows_to_format:
    original_value = str(df_dirty.loc[idx, 'Happiness Score'])
    formatted_value = original_value.replace('.', ',') + ' pt'
    df_dirty.loc[idx, 'Happiness Score'] = formatted_value
print("-> Inconsistencias de formato ('.,' y unidad 'pt') añadidas en 'Happiness Score'.")

# Símbolos Extra
# Añadir '$' a 'Standard Error'
rows_to_symbol = df_dirty.index[7:9]
df_dirty.loc[rows_to_symbol, 'Standard Error'] = '$' + df_dirty.loc[rows_to_symbol, 'Standard Error'].astype(str)
print("-> Símbolos '$' añadidos en 'Standard Error'.")

# 5. Errores Tipográficos
df_dirty.loc[0, 'Region'] = 'Western Eurrope'  # Error de doble 'r'
df_dirty.loc[4, 'Region'] = 'Nort America'     # Omisión de 'h'
print("-> Errores tipográficos introducidos en 'Region'.")

#  Categorías Extrañas
df_dirty.loc[df_dirty.index[5], 'Region'] = 'Antartica (Not a region)'
print("-> Categoría extraña añadida en 'Region'.")


df_dirty['Happiness Rank'] = df_dirty['Happiness Rank'].astype(str)
print("-> Columna 'Happiness Rank' convertida a tipo string (object).")


file_name_dirty = "felicidad_sucia_codigo.csv"
df_dirty.to_csv(file_name_dirty, index=False, encoding='latin-1')
print(f"\n-> ¡Dataset 'ensuciado' guardado como {file_name_dirty} con codificación 'latin-1'!")
