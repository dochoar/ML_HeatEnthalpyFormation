# Código del Proyecto - ML_HeatEnthalpyFormation

Esta carpeta contiene los scripts de Python utilizados para el procesamiento de datos, análisis estadístico y entrenamiento de modelos de Machine Learning.

## Scripts Disponibles

### 1. `split_geometries.py`
**Propósito:** Divide un archivo `.xyz` con múltiples geometrías en archivos individuales.
- **Funcionamiento:** 
    - Lee el archivo maestro de geometrías.
    - Identifica cada bloque de molécula basado en el número de átomos.
    - Sanitiza el nombre de la molécula para usarlo como nombre de archivo.
    - Guarda cada geometría con el formato `0000_Nombre_Molecula.xyz`.
- **Uso:** Se utiliza para preparar los datos estructurales para cálculos individuales o visualización.

### 2. `explore_data.py`
**Propósito:** Realiza una exploración rápida (EDA) del archivo de datos Excel.
- **Funcionamiento:**
    - Carga todas las hojas del archivo `SI_data_2020.xlsx`.
    - Imprime los nombres de las columnas, la forma del dataset (filas/columnas) y las primeras filas.
    - Identifica valores nulos o faltantes.
- **Uso:** Útil para verificar la integridad de los datos antes de realizar análisis complejos.

### 3. `ml_analysis.py`
**Propósito:** Análisis comparativo de métodos computacionales y entrenamiento de modelos de Machine Learning.
- **Funcionamiento:**
    - **Limpieza:** Filtra filas que contienen errores (como la cadena 'failed') y las convierte a numérico.
    - **Benchmark:** Calcula el Error Absoluto Medio (MAE) de los 30 métodos químicos existentes frente a los valores experimentales.
    - **Modelado ML:** Entrena y evalúa tres modelos:
        - Regresión Lineal (Mejor resultado).
        - Random Forest (Bosque Aleatorio).
        - Gradient Boosting (Potenciación de Gradiente).
    - **Visualización:** Genera gráficos de comparación de errores, correlación y precisión de predicción en la carpeta `analysis_results/`.
- **Uso:** Es el núcleo del análisis para predecir Entalpías de Formación con mayor precisión que los métodos teóricos puros.

---

## Estructura de Salida
Los scripts están configurados para generar resultados en:
- `data/structure/individual_geometries/` (Geometrías separadas)
- `analysis_results/` (Gráficos y métricas de ML)
