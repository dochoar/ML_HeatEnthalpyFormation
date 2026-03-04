# Proyecto: Predicción de Entalpía de Formación con Machine Learning (ML_HeatEnthalpyFormation)

Este repositorio contiene un proyecto enfocado en la predicción de la **Entalpía de Formación (Heat/Enthalpy of Formation)** de moléculas tanto experimentales como dadas por métodos puramente teóricos.

El proyecto en sí toma datos calculados con múltiples métodos de química cuántica o teórica (referidos comúnmente en el paper local) y los compara con los de métodos de Machine Learning (ML). A partir de la generación y uso de características estructurales o atómicas (como Bag of Bonds, Smooth Overlap of Atomic Positions y Coulomb Matrices), se entrenan modelos de ML para buscar la mayor precisión predictiva frente a los valores experimentales usando el **Error Absoluto Medio (MAE)**.

## Estructura del Repositorio

- **`data/`**: Carpeta principal que maneja los conjuntos de datos.
  - `raw/`: Datos sin procesar iniciales (ej. `SI_data_2020.xlsx`).
  - `structure/`: Estructuras atómicas individuales y globales en formato `.xyz`.
  - `processed/`: Salida de características/descriptores (features) construidos analizando las estructuras de las moléculas.
  - `external/`: Archivos referenciados de manera externa.
- **`src/`**: Carpeta donde se aloja el código fuente del proyecto (`Python`).
  - `ml_analysis.py`: Script y núcleo central que carga los datos limpios, evalúa la precisión (usando la métrica MAE) de los cálculos computacionales previos y entrena distintos modelos de regresión de ML generándose gráficas automáticas según el rendimiento de este ante los experimentales.
  - `split_geometries.py`: Divisor de geometrías moleculares contenidas en un archivo general en archivos individuales `.xyz`.
  - Herramientas de generación de características (features) para los modelos de Inteligencia Artificial:
    - `generate_bob_features.py` (Bag of Bonds).
    - `generate_coulomb_features.py` (Coulomb Matrix).
    - `generate_soap_features.py` (SOAP descriptors).
  - `explore_data.py`: Script para el análisis rápido de la completitud de la base de datos y búsqueda de características faltantes.
- **`analysis_results/`**: Carpeta de resultados de los comparativos de MAE (ej. `mae_comparison.png`, `predicted_vs_experimental.png`, `correlation_matrix.png`).
- **`2007.06436v5.pdf`**: Artículo/Paper de referencia principal (`arXiv:2007.06436`) respecto a "Machine Learning of Heats of Formation".

## Modelos de Machine Learning Implementados
El script `ml_analysis.py` entrena tres principales modelos estadísticos con los datos estructurados previstos:
1. **Regresión Lineal (Linear Regression)**
2. **Bosques Aleatorios (Random Forest Regressor)**
3. **Potenciación del Gradiente (Gradient Boosting Regressor)**

Los resultados de cada uno se imprimen en consola y se agrupan gráfica y numéricamente frente a más de 30 metodologías teóricas para la identificación del algoritmo puntero.

## Cómo Ejecutar el Proyecto
Para entrenar los modelos automáticamente, medir su rendimiento estadístico y visualizar los gráficos de resultados (los cuales se generarán dentro de `analysis_results/`):

```bash
python src/ml_analysis.py
```
> **Nota:** Assegúrate de satisfacer todas las dependencias usadas en `src/` (típicamente `pandas`, `numpy`, `matplotlib`, `seaborn` y `scikit-learn`).
