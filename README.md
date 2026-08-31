# 📈 Quantitative Finance Pipeline: Fixed & Variable Income Analytics

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.2+-150458?style=for-the-badge&logo=pandas&logoColor=white)
![yfinance](https://img.shields.io/badge/yfinance-Market_Data-00a86b?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

Pipeline automatizado para el análisis cuantitativo de portafolios de inversión, extracción de datos de mercado (BVC, NYSE, NASDAQ, Commodities) y generación de reportes ejecutivos en PDF. Diseñado para automatizar flujos de trabajo en finanzas cuantitativas, desde la ingesta de datos hasta el cálculo avanzado de métricas de riesgo sistemático.

---

## 🚀 Core Técnico y Features

- *ETL de Mercado Financiero:* Extracción concurrente de series de tiempo (5 años) vía la API de Yahoo Finance (yfinance).
- *Análisis Estadístico:* Procesamiento vectorizado con numpy y pandas para cálculo de retornos logarítmicos, volatilidad, asimetría (skewness) y curtosis.
- *Riesgo Sistemático y Markowitz:* Matrices de correlación/covarianza y estandarización de Betas (apalancados y desapalancados) mediante la ecuación de Hamada.
- *Análisis Técnico Automatizado:* Cálculo de osciladores (RSI 14) y validación de Price Action vía Velas Japonesas.
- *Reporting en PDF:* Motor de renderizado vectorial con fpdf2 y seaborn para consolidar insights en reportes de nivel ejecutivo.

---

## ⚙️ Instalación y Uso

1. *Clonar el repositorio:*
   bash
   git clone [https://github.com/TU_USUARIO/renta-fija-variable-analytics.git](https://github.com/TU_USUARIO/renta-fija-variable-analytics.git)
   cd renta-fija-variable-analytics
   

2. *Crear entorno virtual e instalar dependencias:*
   bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   

3. *Ejecutar el motor cuantitativo:*
   bash
   python src/pipeline_cuantitativo.py
   
   El PDF y las visualizaciones se exportarán automáticamente al directorio /output/.

---

## 📊 Síntesis de Resultados Cuantitativos

El pipeline evalúa un universo de activos diversificado. A continuación, se presenta el análisis extraído de la última ejecución del modelo:

### 1. Días Hábiles Transados por Año
Se evidencia una asimetría operativa entre bolsas por festivos locales (Ley Emiliani en Colombia vs. feriados federales en EE. UU.). Los futuros operan con máxima liquidez temporal.

| Mercado / Activos | 2021 (Sep-Dic) | 2022 | 2023 | 2024 | 2025 | 2026 (YTD) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| *BVC (Ecopetrol, Sura, ISA)* | 90 | 260 | 258 - 260 | 252 - 253 | 251 | 157 - 158 |
| *USA (AAPL, MSFT, NVDA, JPM)* | 87 | 251 | 250 | 252 | 250 | 164 |
| *Commodities (Oro, WTI, Brent)* | 87 | 251 | 250 - 251 | 252 | 252 | 164 |

### 2. Extremos Históricos y Ciclos Macro (Top 5 Max/Min)
El log de precios capturó dos superciclos estructurales en los últimos 5 años:

*   *Ciclo Energético (ECOPETROL.CL & CL=F):* La crisis energética de 2022 llevó al crudo WTI a máximos de *$123.70 USD* (08-Mar-2022) y a Ecopetrol a *$3,610 COP* (07-Abr-2022). Sus mínimos recientes reflejan normalización de oferta.
*   *Superciclo IA (AAPL & NVDA):* La concentración de capital en semiconductores empujó a Apple a máximos de *$340.08 USD* (Julio 2026) frente a mínimos de $125.02 USD (Enero 2023).

### 3. Perfilamiento Fundamental: Value vs. Growth

| Ticker | Market Cap | P/E Ratio | Dividend Yield | EPS (UPA) | Perfil |
| :--- | :--- | :--- | :--- | :--- | :--- |
| *ECOPETROL* | $108.14 B (COP) | 10.55x | 4.70% | $249.26 | Value / Yield |
| *GRUPOSURA* | $20.16 B (COP) | 9.91x | 3.26% | $6,207.66 | Value |
| *ISA* | $32.16 B (COP) | 12.74x | 5.48% | $2,278.75 | Value / Yield |
| *AAPL* | $4.59 T (USD) | 36.12x | 0.34% | $8.71 | Growth |
| *MSFT* | $3.75 T (USD) | 28.11x | 0.73% | $17.97 | Growth |
| *NVDA* | $5.51 T (USD) | 34.97x | 0.47% | $6.52 | Hyper-Growth |
| *JPM* | $941.58 B (USD) | 15.17x | 1.68% | $23.35 | Value / Core |

> *Insight Estratégico:* La matriz fundamental confirma la dicotomía del portafolio. La BVC ofrece múltiplos atractivos (P/E ~10x) y alto flujo de caja (Yields >4%), ideal para rentas. EE. UU. exige pagar una prima por crecimiento (P/E >34x), sacrificando dividendos por apreciación de capital.

### 4. Estructura de los Índices Benchmark
*   *MSCI COLCAP (Colombia):* Ponderado por free-float. Altamente concentrado: Bancolombia (>30%), Ecopetrol (~13-15%), y Grupo Sura (~10-12%).
*   *Dow Jones (^DJI):* Ponderado por *precio nominal* (Price-Weighted). Otorga mayor influencia matemática a empresas con acciones "caras", ignorando el tamaño real (Market Cap) de la compañía.
*   *Nasdaq 100 (^NDX):* Ponderado por capitalización modificada, actuando como termómetro puro del sector IT y semiconductores.

### 5. Matrices de Covarianza y Cobertura (Hedging)
La matriz de correlación de Pearson ($\rho$) revela dinámicas clave para la diversificación:
*   Alta correlación intra-sectorial en EE. UU.: MSFT y NVDA comparten un $\rho = 0.5678$.
*   *El Escudo Diversificador:* XOM (ExxonMobil) presenta una correlación de apenas *0.1257* frente al Nasdaq. Inyectar XOM en una cartera altamente tecnológica neutraliza la varianza total frente a shocks en semiconductores.

### 6. Descomposición del Riesgo Sistemático (Betas)
Aplicación de la ecuación de Hamada para aislar el riesgo operativo ($\beta_U = \beta_L / [1 + (1 - T)(D/E)]$).

| Ticker | Mercado Base | $\beta_L$ (Apalancado) | D/E Ratio | $\beta_U$ (Desapalancado) |
| :--- | :--- | :--- | :--- | :--- |
| *NVDA* | USA (^DJI) | 1.7750 | 0.0023 | 1.7717 |
| *AAPL* | USA (^DJI) | 1.2048 | 0.0184 | 1.1875 |
| *JPM* | USA (^DJI) | 1.1726 | 1.4266 | 0.5513 |
| *ECOPETROL* | BVC (ICOL) | 0.7149 | 0.9702 | 0.4384 |
| *ISA* | BVC (ICOL) | 0.6055 | 1.0700 | 0.3571 |

> *Nota Metodológica sobre Discrepancias:* Los Betas calculados discrepan intencionalmente de terminales como Bloomberg. Nuestro pipeline computa sobre *varianzas diarias continuas* a 5 años (alta fidelidad microestructural), frente a los retornos *mensuales* a 3 años y el factor de convergencia (Vasicek: $0.67\beta + 0.33$) utilizado por plataformas comerciales.
> 
> Caso Destacado: El $\beta_L$ de JPMorgan es agresivo (1.17) debido a su masivo apalancamiento financiero ($D/E = 1.42$). Sin embargo, su riesgo operativo subyacente ($\beta_U = 0.55$) es eminentemente defensivo.

### 7. Señales Técnicas y Price Action
*   *RSI:* El barrido del oscilador detectó sobrecompra técnica en GRUPOSURA.CL (RSI: 72.46), sugiriendo resistencia al alza de corto plazo. El bloque tecnológico USA neutralizó volatilidad, estabilizándose en la franja 45-55.
*   *Price Action:* Las visualizaciones de velas japonesas validan canales laterales de distribución institucional tras los rallies del verano de 2026.
