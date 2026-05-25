import pandas as pd
import numpy as np
from scipy.stats import qmc

def generar_diseno_32_3muestrasiguales_ordenado():
    
    # 1. Generar el diseño LHS (d=2: PEGDA y LAP)
    sampler = qmc.LatinHypercube(d=2, optimization="random-cd")
    muestra = sampler.random(n=96)
    
    # 2. Escalar a tus rangos: PEGDA (10-30%) e Iniciador (0.05-0.2%)
    l_bounds = [10, 0.05]
    u_bounds = [30, 0.2]
    tabla = qmc.scale(muestra, l_bounds, u_bounds)
    
    # 3. Crear el DataFrame inicial con las 32 condiciones únicas
    df_unico = pd.DataFrame(tabla, columns=['%_PEGDA', '%_Iniciador_LAP'])
    
    # 4. Ordenamos por la columna del LAP de forma ascendente antes de triplicar
    # Esto facilita la preparación de las mezclas en el laboratorio
    df_ordenado = df_unico.sort_values(by='%_Iniciador_LAP', ascending=True)
    
    # 5. Triplicar cada fila (3 réplicas por condición)
    # repeat(3) repite cada fila tres veces seguidas (1,1,1, 2,2,2...)
    df_triplicado = pd.DataFrame(np.repeat(df_ordenado.values, 3, axis=0), 
                                 columns=df_ordenado.columns)
    
    # 6. Guardar el Excel con las 96 filas totales
    df_triplicado.to_excel("diseno_experimental_96_ORDENADO_TRIPLICADO.xlsx", index=False) 

    print(f"Diseño generado con {len(df_triplicado)} filas.")
    return df_triplicado

generar_diseno_32_3muestrasiguales_ordenado()