# Motor Estocástico para Evaluación de Riesgo Financiero (Monte Carlo)

Un simulador financiero avanzado desarrollado en Python que reemplaza las proyecciones estáticas tradicionales en Excel por simulaciones de Monte Carlo. Diseñado para la toma de decisiones corporativas y evaluación de proyectos de inversión bajo condiciones de incertidumbre.

##  El Problema que Resuelve
La evaluación de proyectos tradicional asume un único escenario fijo (Ej: vender exactamente 100 unidades a $50.000). Este motor destruye esa linealidad ejecutando **10.000 iteraciones (realidades alternativas)** utilizando distribuciones triangulares para modelar el caos del mercado real, entregando una probabilidad matemática de éxito o fracaso.

##  Características Técnicas y Funcionales
* **Motor Estadístico (`numpy`):** Genera 10.000 flujos de caja iterativos en segundos.
* **Lógica de Finanzas Corporativas:** Integra cálculo automático de CAPEX, Capital de Trabajo, Escudo Fiscal por depreciación y valor de desecho.
* **Interfaz Gráfica Nativa (`tkinter`):** Interfaz amigable para ingreso rápido de variables críticas sin necesidad de tocar el código.
* **Exportación Gerencial Automatizada:** Genera reportes listos para directorio usando `pandas` (Excel) y `matplotlib` (Gráficos de distribución).

## Visualización de Resultados
El motor genera automáticamente una "Radiografía de Riesgo" que permite a los tomadores de decisiones visualizar el VAN Promedio, los escenarios extremos y la probabilidad exacta de destrucción de valor.

<img width="992" height="665" alt="Campana montecarlo" src="https://github.com/user-attachments/assets/e6ec6265-25af-4e8a-b852-a9ee751ae2d3" />


## 🛠️ Stack Tecnológico
* Python 3.x
* Data Science: `numpy`, `pandas`, `matplotlib`
* UI: `tkinter`
