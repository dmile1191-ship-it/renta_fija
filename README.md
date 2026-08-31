# Quantitative Finance Pipeline: Fixed & Variable Income Analytics 📈

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Pandas](https://img.shields.io/badge/pandas-data_manipulation-150458.svg)
![yfinance](https://img.shields.io/badge/yfinance-market_data-00a86b.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

Un pipeline automatizado en Python para el análisis cuantitativo de portafolios de inversión, extracción de datos de mercado y generación de reportes ejecutivos en PDF. 

Este proyecto resuelve requerimientos analíticos para renta fija, renta variable y commodities, abarcando desde la descarga de históricos hasta el cálculo de Betas desapalancados y matrices de covarianza.

## 🚀 Características Principales (Features)

- *ETL de Datos de Mercado:* Extracción concurrente a 5 años para acciones de la BVC (Colombia), NYSE/NASDAQ, Commodities (Futuros) e Índices (^DJI, ^NDX, ICOL) vía yfinance.
- *Análisis Estadístico:* Cálculo de retornos logarítmicos, volatilidad, asimetría (skewness), curtosis y matrices de correlación/covarianza.
- *Valoración de Riesgo Sistemático (Beta):* Estandarización de Betas apalancados y desapalancados utilizando la ecuación de Hamada (ajustada por tasas impositivas de Colombia y EE. UU. y la estructura de capital D/E).
- *Análisis Técnico:* Implementación del oscilador RSI (14 periodos) y visualización de Price Action mediante Velas Japonesas.
- *Reporting Automatizado:* Motor de renderizado vectorial con fpdf2 y seaborn para consolidar el análisis en un reporte PDF de nivel ejecutivo.

## 🛠️ Stack Tecnológico

- *Core Analítico:* pandas, numpy
- *Visualización:* matplotlib, seaborn
- *Generación de Reportes:* fpdf2
- *Data Provider:* yfinance

## ⚙️ Instalación y Uso

1. *Clonar el repositorio:*
   ```bash
   git clone [https://github.com/TU_USUARIO/renta-fija-variable-analytics.git](https://github.com/TU_USUARIO/renta-fija-variable-analytics.git)
   cd renta-fija-variable-analytics
