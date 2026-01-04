# Quantitative Risk Engine

![Java](https://img.shields.io/badge/Java-21%2B-007396?style=flat-square&logo=openjdk&logoColor=white)
![Concurrency](https://img.shields.io/badge/Concurrency-Virtual_Threads-E34F26?style=flat-square)
![Python](https://img.shields.io/badge/Analysis-Python_3.10-3776AB?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![Status](https://img.shields.io/badge/Status-Production_Ready-success?style=flat-square)

## Descripción Ejecutiva

El sistema Quantitative Risk Engine es una solución de computación de alto rendimiento diseñada para la valoración de activos financieros y medición de riesgo bajo incertidumbre. Su propósito fundamental es resolver el problema de latencia en la simulación de escenarios masivos (Montecarlo), permitiendo a las instituciones financieras calcular el Valor en Riesgo (VaR) y la exposición de capital con precisión matemática.

La arquitectura híbrida combina la robustez y concurrencia de Java 21 para el procesamiento numérico intensivo (backend) con la capacidad analítica y visualización de datos de Python (frontend), logrando procesar más de un millón de trayectorias estocásticas en segundos.

## Objetivos Técnicos

1.  **Paralelismo Masivo:** Implementación de Virtual Threads (Project Loom) para gestionar la concurrencia de alta densidad sin penalización en la memoria del sistema.
2.  **Inmutabilidad del Dominio:** Uso estricto de Java Records para garantizar la seguridad de hilos (thread-safety) y la integridad de los datos financieros durante la ejecución paralela.
3.  **Interoperabilidad Agnóstica:** Diseño de un pipeline de datos desacoplado mediante persistencia CSV, permitiendo la auditoría externa de los resultados.
4.  **Modelado Estocástico:** Implementación optimizada del Movimiento Browniano Geométrico (GBM) para la proyección de precios futuros.

## Arquitectura del Sistema

El flujo de información sigue un diseño lineal de tubería (pipeline), separando estrictamente la computación intensiva de la capa de presentación.

```mermaid
graph LR
    A[Configuración de Simulación] -->|Input| B(Motor de Riesgo Java)
    B -->|Procesamiento Paralelo| C{Cálculo Montecarlo}
    C -->|Agregación| D[Persistencia CSV]
    D -->|Ingesta de Datos| E(Analítica Python)
    E -->|Visualización| F[Dashboard Ejecutivo]
