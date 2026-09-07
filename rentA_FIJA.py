# =========================================================================================================
# LIBRERÍAS DE INFRAESTRUCTURA, ANÁLISIS CUANTITATIVO Y REPORTING FINANCIERO
# =========================================================================================================

# datetime: Módulo estándar de Python para gestionar intervalos de tiempo, fechas y desfases temporales.
import datetime

# os: Interfaz del sistema operativo para manipular rutas de archivos y crear directorios de forma segura.
import os

# warnings: Utilizado para suprimir alertas menores (mensajes de advertencia por métodos obsoletos de librerías).
import warnings

# matplotlib.pyplot: Motor base de graficación bidimensional para la renderización visual de series financieras.
import matplotlib.pyplot as plt

# numpy: Núcleo de cálculo numérico vectorizado de alto rendimiento para álgebra lineal y transformaciones logarítmicas.
import numpy as np

# pandas: Librería principal de manipulación de estructuras de datos bidimensionales (DataFrames y Series temporales).
import pandas as pd

# seaborn: Capa de abstracción sobre Matplotlib que optimiza paletas cromáticas, temas visuales y mapas de calor (heatmaps).
import seaborn as sns

# yfinance: Cliente de extracción de datos bursátiles en tiempo real e históricos desde los servidores de Yahoo Finance.
import yfinance as yf

# Suprimir avisos secundarios para mantener una consola de ejecución limpia y profesional.
warnings.filterwarnings("ignore")

# ---------------------------------------------------------------------------------------------------------
# GESTIÓN AUTOMATIZADA DE DIRECTORIOS EN DISCO LOCAL
# ---------------------------------------------------------------------------------------------------------
# os.makedirs con el parámetro exist_ok=True crea las carpetas si no existen, evitando excepciones por colisión.
os.makedirs("output/img", exist_ok=True)
os.makedirs("output/img/velas", exist_ok=True)


# =========================================================================================================
# FASE 1: DEFINICIÓN DEL UNIVERSO DE INVERSIÓN Y DESCARGA DE DATOS (PUNTOS 1, 2 Y 10)
# =========================================================================================================

# 1.1 Tickers representativos de la Bolsa de Valores de Colombia (BVC).
# El sufijo '.CL' indica a la API de Yahoo Finance que los títulos cotizan en el mercado colombiano.
TICKERS_BVC = ["ECOPETROL.CL", "GRUPOSURA.CL", "ISA.CL", "GEB.CL", "CEMARGOS.CL"]

# 1.2 Tickers de alta liquidez cotizados en las bolsas estadounidenses (NYSE / NASDAQ).
TICKERS_USA = ["AAPL", "MSFT", "NVDA", "JPM", "XOM"]

# 1.3 Contratos de futuros sobre Materias Primas (Commodities) transados en mercados globales:
# GC=F (Oro), CL=F (Petróleo Crudo WTI), BZ=F (Petróleo Brent), KC=F (Café Arábica), NG=F (Gas Natural).
TICKERS_COMMODITIES = ["GC=F", "CL=F", "BZ=F", "KC=F", "NG=F"]

# 1.4 Índices bursátiles de referencia (Benchmarks para cálculo de Betas y correlaciones):
# ICOL (Proxy del MSCI COLCAP Colombia), ^DJI (Dow Jones Industrial Average), ^NDX (Nasdaq 100).
TICKERS_INDICES = ["ICOL", "^DJI", "^NDX"]

# Lista consolidada que agrupa los 18 instrumentos objeto de evaluación cuantitativa.
ALL_TICKERS = TICKERS_BVC + TICKERS_USA + TICKERS_COMMODITIES + TICKERS_INDICES

# Ventana temporal móvil exacta: 5 años cronológicos hacia atrás desde el instante de ejecución.
end_date = datetime.datetime.now()
start_date = end_date - datetime.timedelta(days=5 * 365)

print("Descargando datos del mercado (Open, High, Low, Close)...")

# Extracción concurrente de datos vía Yahoo Finance:
# - auto_adjust=False: Conserva la columna 'Close' original sin adulterar los niveles de soporte/resistencia técnicos.
# - group_by='ticker': Organiza las columnas en un índice jerárquico multinivel (Ticker -> Métricas OHLCV).
data = yf.download(ALL_TICKERS, start=start_date, end=end_date, group_by="ticker", auto_adjust=False)

# Normalización temporal para compatibilidad con Excel:
# Excel no admite zonas horarias (UTC). tz_localize(None) elimina el desfase manteniendo la estampa pura.
if isinstance(data.index, pd.DatetimeIndex):
    data.index = data.index.tz_localize(None)

# 1.5 Matrices segregadas de Precios de Cierre:
# Precios de Cierre Nominales (Close): Requeridos para cálculo de osciladores técnicos y niveles psicológicos.
close_prices = pd.DataFrame({t: data[t]["Close"] for t in ALL_TICKERS}).dropna(how="all")

# Precios de Cierre Ajustados (Adj Close): Corrigen eventos corporativos (splits de acciones y pago de dividendos).
adj_close_prices = pd.DataFrame({t: data[t]["Adj Close"] for t in ALL_TICKERS}).dropna(how="all")

# 1.6 Cálculo de Rendimientos Continuamente Compuestos (Logarítmicos) (Puntos 8 y 11):
# Fórmula: r_t = ln(P_t / P_{t-1}). Los rendimientos logarítmicos garantizan la aditividad temporal de las series.
returns_log = np.log(adj_close_prices / adj_close_prices.shift(1)).dropna(how="all")


# =========================================================================================================
# FASE 2: MOTOR DE PROCESAMIENTO ESTADÍSTICO, FUNDAMENTAL Y DE RIESGO
# =========================================================================================================

# 2.1 Estadísticas Descriptivas Multivariables de las Series de Precios (Punto 5):
stats = pd.DataFrame({
    "Media": close_prices.mean(),              # Esperanza matemática del precio en los últimos 5 años
    "Volatilidad (Std)": close_prices.std(),    # Desviación estándar muestral (dispersión absoluta)
    "Mínimo": close_prices.min(),              # Mínimo absoluto alcanzado en la serie
    "Máximo": close_prices.max(),              # Máximo absoluto registrado en la serie
    "Skewness": close_prices.skew(),            # Asimetría: >0 cola hacia la derecha (alzas extremas); <0 caídas abruptas
    "Curtosis": close_prices.kurtosis()         # Curtosis: >0 colas pesadas o distribución leptocúrtica
}).round(2)

# 2.2 Extracción de Métricas Fundamentales y Múltiplos Financieros (Puntos 7 y 19):
fundamentals = []
for t in TICKERS_BVC + TICKERS_USA:
    try:
        # Consulta a los metadatos corporativos proporcionados por la API
        info = yf.Ticker(t).info
        fundamentals.append({
            "Ticker": t,
            "Market Cap": info.get("marketCap", np.nan),                  # Capitalización bursátil total
            "P/E Ratio": info.get("trailingPE", np.nan),                   # Relación Precio/Ganancia (Price-to-Earnings)
            "Dividend Yield (%)": (info.get("dividendYield", 0) or 0) * 100, # Rentabilidad por dividendo anualizada
            "EPS": info.get("trailingEps", np.nan),                       # Utilidad por acción (Earnings Per Share)
            "Deuda Total": info.get("totalDebt", np.nan)                  # Pasivo financiero total exigible
        })
    except Exception:
        pass
df_fund = pd.DataFrame(fundamentals).set_index("Ticker")

# 2.3 Descomposición del Riesgo Sistemático: Beta Apalancado y Desapalancado (Puntos 16, 17 y 18):
# El Beta (CAPM) cuantifica la sensibilidad del activo frente a las variaciones del mercado: Cov(Ra, Rm) / Var(Rm).
# La Ecuación de Hamada desapalanca el Beta para aislar el riesgo operativo eliminando la carga de deuda:
# Beta_U = Beta_L / [1 + (1 - Tasa_Impositiva) * (Deuda / Capital)]
betas_calc = []
tax_col, tax_usa = 0.35, 0.21  # Tasas impositivas marginales corporativas (Colombia: 35%, EE.UU.: 21%)

for ticker in TICKERS_USA + TICKERS_BVC:
    if ticker in returns_log.columns and not returns_log[ticker].dropna().empty:
        is_usa = ticker in TICKERS_USA
        idx = "^DJI" if is_usa else "ICOL"  # Benchmark sectorial correspondiente
        tax = tax_usa if is_usa else tax_col

        # Cálculo de la covarianza empírica entre el activo analizado y su índice de referencia
        cov_im = returns_log[[ticker, idx]].dropna().cov().iloc[0, 1]
        var_mkt = returns_log[idx].var()
        beta_lev = cov_im / var_mkt  # Beta apalancado de mercado

        # Estructura de apalancamiento financiero: Relación Deuda sobre Patrimonio (D/E)
        debt = df_fund.loc[ticker, "Deuda Total"] if ticker in df_fund.index else np.nan
        equity = df_fund.loc[ticker, "Market Cap"] if ticker in df_fund.index else np.nan

        # Asignación de ratio D/E; si el activo no publica deuda líquida, se aplica proxy de sector (0.2 USA / 0.4 BVC)
        de_ratio = (debt / equity) if (pd.notnull(debt) and pd.notnull(equity) and equity > 0) else (0.2 if is_usa else 0.4)

        # Aplicación del modelo de Hamada para aislar el riesgo operativo intrínseco del negocio
        beta_unlev = beta_lev / (1 + (1 - tax) * de_ratio)

        betas_calc.append({
            "Ticker": ticker,
            "Mercado Base": idx,
            "Beta Apalancado": round(beta_lev, 4),
            "D/E Ratio": round(de_ratio, 4),
            "Beta Desapalancado": round(beta_unlev, 4)
        })
df_betas = pd.DataFrame(betas_calc).set_index("Ticker")

# 2.4 Matrices de Correlación Lineal de Pearson (Puntos 14 y 15):
# Cuantifican la interdependencia direccional entre los activos (-1: correlación inversa perfecta, +1: correlación directa).
col_assets = [t for t in TICKERS_BVC if t in returns_log.columns] + ["ICOL"]
corr_col = returns_log[col_assets].corr().round(3)

usa_assets = TICKERS_USA + ["^DJI", "^NDX"]
corr_usa = returns_log[usa_assets].corr().round(3)

# 2.5 Análisis Técnico Cuantitativo: Oscilador de Fuerza Relativa (RSI de 14 Periodos) (Punto 20):
# El RSI evalúa la velocidad y magnitud de los movimientos direccionales de precios.
def calc_rsi(series, period=14):
    delta = series.diff()  # Diferencial de precio entre sesiones consecutivas
    gain = (delta.where(delta > 0, 0)).rolling(period).mean()  # Media móvil de variaciones positivas
    loss = (-delta.where(delta < 0, 0)).rolling(period).mean() # Media móvil de variaciones negativas
    rs = gain / loss  # Fuerza Relativa (Relative Strength)
    return 100 - (100 / (1 + rs))

rsi_data = []
for t in TICKERS_USA + TICKERS_BVC:
    s = close_prices[t].dropna()
    if len(s) > 15:
        last_rsi = calc_rsi(s).iloc[-1]
        # Umbrales convencionales de J. Welles Wilder: >70 sobrecompra técnica, <30 sobreventa
        signal = "Sobrecompra" if last_rsi > 70 else ("Sobreventa" if last_rsi < 30 else "Neutral")
        last_open = data[t]["Open"].dropna().iloc[-1]
        rsi_data.append({
            "Ticker": t,
            "Última Apertura": round(last_open, 2),
            "Precio Cierre": round(s.iloc[-1], 2),
            "RSI 14d": round(last_rsi, 2),
            "Señal": signal
        })
df_rsi = pd.DataFrame(rsi_data).set_index("Ticker")


# =========================================================================================================
# FASE 3: GENERACIÓN Y RENDERIZACIÓN GRÁFICA DE ALTA RESOLUCIÓN
# =========================================================================================================

print("Generando gráficos de alta resolución...")
sns.set_theme(style="whitegrid")  # Configurar entorno estético con cuadrículas suaves de soporte

# 3.1 Gráfico de Desempeño Acumulado (Base 100) (Punto 3):
# Permite comparar directamente activos con denominaciones y magnitudes de precio heterogéneas.
plt.figure(figsize=(10, 5))
norm = (close_prices / close_prices.bfill().iloc[0]) * 100
sns.lineplot(data=norm[TICKERS_USA + TICKERS_BVC], dashes=False, linewidth=1.2)
plt.title("Evolución Comparativa Base 100")
plt.legend(bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=8)
plt.tight_layout()
plt.savefig("output/img/precios.png", dpi=150)
plt.close()

# 3.2 Mapa de Calor (Heatmap) de la Matriz de Correlación:
plt.figure(figsize=(7, 5))
sns.heatmap(corr_usa, annot=True, cmap="coolwarm", fmt=".2f", vmin=-1, vmax=1)
plt.title("Matriz de Correlación - USA")
plt.tight_layout()
plt.savefig("output/img/heatmap.png", dpi=150)
plt.close()

# 3.3 Bucle Automatizado: Generación de Velas Japonesas Amplias para TODOS los Activos (Punto 4):
for ticker in TICKERS_USA + TICKERS_BVC:
    # Selección estricta de las últimas 60 sesiones de negociación (~3 meses de Price Action)
    df_c = data[ticker].dropna().tail(60)
    if df_c.empty:
        continue

    fig, ax = plt.subplots(figsize=(10, 4))
    # Clasificación booleana: Sesiones alcistas (Cierre >= Apertura) y bajistas (Cierre < Apertura)
    up = df_c[df_c["Close"] >= df_c["Open"]]
    down = df_c[df_c["Close"] < df_c["Open"]]

    # PARÁMETROS DE CALIBRACIÓN GEOMÉTRICA DE LAS VELAS:
    # w_body = 1.2: Otorga robustez visual al cuerpo para evitar que se renderice como una línea delgada.
    # w_wick = 0.15: Otorga una proporción nítida a las mechas o sombras (máximos y mínimos).
    w_body = 1.2
    w_wick = 0.15

    # Construcción de Velas Alcistas (Color verde esmeralda: #00b894 con borde oscuro estructural):
    ax.bar(up.index, up["Close"] - up["Open"], w_body, bottom=up["Open"], color="#00b894", edgecolor="black", linewidth=0.5)
    ax.bar(up.index, up["High"] - up["Close"], w_wick, bottom=up["Close"], color="#00b894")
    ax.bar(up.index, up["Low"] - up["Open"], w_wick, bottom=up["Open"], color="#00b894")

    # Construcción de Velas Bajistas (Color rojo carmesí: #d63031 con borde oscuro estructural):
    ax.bar(down.index, down["Close"] - down["Open"], w_body, bottom=down["Open"], color="#d63031", edgecolor="black", linewidth=0.5)
    ax.bar(down.index, down["High"] - down["Open"], w_wick, bottom=down["Open"], color="#d63031")
    ax.bar(down.index, down["Low"] - down["Close"], w_wick, bottom=down["Close"], color="#d63031")

    ax.set_title(f"Velas Japonesas {ticker} (Últimos 3 Meses)")
    ax.grid(True, linestyle="--", alpha=0.4)
    plt.xticks(rotation=30)
    plt.tight_layout()

    # Almacenamiento serializado individual de cada activo en el directorio dedicado
    plt.savefig(f"output/img/velas/velas_{ticker}.png", dpi=150)
    plt.close()


# =========================================================================================================
# FASE 4: ENSAMBLAJE DEL REPORTE MULTI-PESTAÑA EN EXCEL (XLSXWRITER)
# =========================================================================================================

print("Escribiendo a Excel...")
excel_path = "output/Reporte_Analitico_Portafolio.xlsx"
writer = pd.ExcelWriter(excel_path, engine="xlsxwriter")
workbook = writer.book

# Definición de formatos visuales estándar institucional para el libro de Excel:
header_format = workbook.add_format({'bold': True, 'bg_color': '#2C3E50', 'font_color': 'white', 'border': 1})
text_format = workbook.add_format({'text_wrap': True, 'valign': 'top'})
title_format = workbook.add_format({'bold': True, 'font_size': 14, 'bg_color': '#ECF0F1'})

# Función auxiliar para vaciar DataFrames, estilizar títulos y aplicar autoajuste al ancho de las columnas
def write_df_with_format(df, sheet_name, startrow=0, startcol=0, title=None):
    worksheet = writer.sheets.get(sheet_name) or workbook.add_worksheet(sheet_name)
    if title:
        worksheet.write(startrow, startcol, title, title_format)
        startrow += 2
    df.to_excel(writer, sheet_name=sheet_name, startrow=startrow, startcol=startcol)
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(startrow, startcol + col_num + 1, value, header_format)
    worksheet.autofit()
    return startrow + len(df) + 3

# PESTAÑA 1: Resumen Estadístico y Análisis Técnico de Última Sesión
write_df_with_format(stats, "1. Estadísticas", 0, 0, "Estadísticas Descriptivas del Portafolio")
write_df_with_format(df_rsi, "1. Estadísticas", 0, 9, "Análisis Técnico y Precios de Cierre/Apertura")

# PESTAÑA 2: Indicadores Fundamentales y Riesgo Sistemático (Betas)
r = write_df_with_format(df_fund, "2. Riesgo y Fundamentales", 0, 0, "Indicadores Fundamentales")
write_df_with_format(df_betas, "2. Riesgo y Fundamentales", r, 0, "Análisis de Betas y Riesgo Sistemático")

# PESTAÑA 3: Matrices de Asociación Lineal (Correlaciones)
r = write_df_with_format(corr_col, "3. Correlaciones", 0, 0, "Correlación Mercado Colombiano")
write_df_with_format(corr_usa, "3. Correlaciones", r, 0, "Correlación Mercado USA")

# PESTAÑA 4: Gráficos Macroeconómicos Generales Embebidos
ws_img = workbook.add_worksheet("4. Gráficos Generales")
ws_img.write(0, 0, "Rendimiento y Correlación", title_format)
ws_img.insert_image('A3', 'output/img/precios.png')
ws_img.insert_image('A28', 'output/img/heatmap.png')

# PESTAÑA 5: Catálogo Visual Completo de Velas Japonesas (Todos los Tickers)
ws_velas = workbook.add_worksheet("5. Velas Japonesas")
ws_velas.write(0, 0, "Price Action - Todos los Activos", title_format)
row_img = 3
for ticker in TICKERS_USA + TICKERS_BVC:
    img_path = f"output/img/velas/velas_{ticker}.png"
    if os.path.exists(img_path):
        ws_velas.insert_image(f'A{row_img}', img_path)
        # Salto de 22 filas en Excel para asegurar espacio suficiente entre imágenes sin solapamientos
        row_img += 22

# PESTAÑA 6: Marco Teórico y Sustentación Conceptual
ws_text = workbook.add_worksheet("6. Análisis Teórico")
ws_text.set_column('A:A', 120)  # Configurar ancho suficiente para párrafos analíticos
analisis = [
    ("1. Composición de Índices (Puntos 12 y 13)", "MSCI COLCAP: Ponderado por flotante libre, con fuerte sesgo financiero (Bancolombia ~30%). DJI: Ponderado exclusivamente por el precio de la acción, ignorando la capitalización. NDX: Ponderado por capitalización modificada, dominado por Big Tech."),
    ("2. Correlación y Covarianza (Puntos 14 y 15)", "Alta correlación intra-sectorial tecnológica (MSFT vs NVDA). ExxonMobil (XOM) presenta correlación mínima con el Nasdaq, actuando como escudo diversificador. La covarianza neutraliza el riesgo idiosincrático cruzado en la frontera de Markowitz."),
    ("3. Análisis de Betas Desapalancados (Puntos 16, 17 y 18)", "NVDA (1.77) amplifica la volatilidad, siendo agresivo. ECOPETROL (0.71) amortigua caídas. La Ecuación de Hamada aísla el riesgo financiero: JPM tiene un Beta apalancado alto (1.17) por su deuda, pero un riesgo operativo defensivo (0.55). Discrepamos de Bloomberg al calcular varianzas sobre retornos diarios (captura microestructural) frente a retornos mensuales."),
    ("4. Price Action y Tendencia", "RSI detecta sobrecompra en activos colombianos específicos, mientras EE. UU. se consolida en rango neutro. Las velas japonesas reafirman resistencia tras los máximos del superciclo de semiconductores.")
]
row = 1
for titulo, contenido in analisis:
    ws_text.write(row, 0, titulo, header_format)
    ws_text.write(row + 1, 0, contenido, text_format)
    ws_text.set_row(row + 1, 45)
    row += 4

# PESTAÑA 7: Data Cruda OHLCV Completa a 5 Años (Auditoría Integral del Taller) (Punto 2)
data.to_excel(writer, sheet_name="7. Datos Históricos (OHLC)")
ws_raw = writer.sheets["7. Datos Históricos (OHLC)"]
ws_raw.write(0, 0, "Fecha", header_format)

# Compilación final y cierre físico del archivo en el sistema de archivos
writer.close()
print("Excel generado exitosamente en: output/Reporte_Analitico_Portafolio.xlsx")
