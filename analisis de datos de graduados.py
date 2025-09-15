# ==== Paso 1: Graduados por año (1989_2024) ====
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import unicodedata, re
import matplotlib.ticker as mticker

# 1) Ruta al CSV (ajusta si tienes otra ubicación)
RUTA = "Registro_Graduados_20250915.csv"
# RUTA = r"C:\Users\semas\OneDrive\Escritorio\UFPS\estadistica\Registro_Graduados_20250915.csv"

# 2) Carga simple con fallback de encoding
try:
    df = pd.read_csv(RUTA, encoding="utf-8-sig")
except UnicodeDecodeError:
    df = pd.read_csv(RUTA, encoding="latin1")

# 3) Normaliza nombres de columnas -> minusculas, sin tildes, con _
def norm_col(c):
    c = c.strip().lower()
    c = re.sub(r"\s+", "_", c)
    c = "".join(ch for ch in unicodedata.normalize("NFKD", c) if not unicodedata.combining(ch))
    c = re.sub(r"[^0-9a-z_]", "", c)
    return c

df.columns = [norm_col(c) for c in df.columns]

# 4) Verifica columna año de grado
if "ano_grado" not in df.columns:
    raise KeyError("No encontré la columna 'ano_grado'. Revisa el nombre en tu CSV.")

# 5) Limpia el año (maneja '2,004' -> 2004) y convierte a numérico
s = df["ano_grado"].astype(str).str.replace(",", "", regex=False)
df["ano_grado"] = pd.to_numeric(s.str.extract(r"(\d{4})")[0], errors="coerce")

# 6) Filtra rango 1989_2024 y agrupa
serie = (df[df["ano_grado"].between(1989, 2024)]
         .groupby("ano_grado")
         .size()
         .rename("graduados")
         .reset_index()
         .sort_values("ano_grado"))


# --- 7) Graficar ---
fig, ax = plt.subplots(figsize=(10, 4.5))
ax.plot(serie["ano_grado"].astype(int), serie["graduados"], marker="o")
ax.set_title("Graduados por año (1989_2024)")
ax.set_xlabel("Año")
ax.set_ylabel("Cantidad de graduados")

# 🔧 Fuerza años enteros en el eje X
ax.xaxis.set_major_locator(mticker.MultipleLocator(base=1))          # cada 1 año
ax.xaxis.set_major_formatter(mticker.FormatStrFormatter('%d'))       # formatea como entero
ax.set_xlim(serie["ano_grado"].min()-0.5, serie["ano_grado"].max()+0.5)

plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("graduados_por_anio.png", dpi=200)
plt.show()

#_________________________________________________________________________________________________________________________________________________________________________
#_________________PREGUNTA 2_____________________________________________________________________________________________________________________________________________
#_________________________________________________________________________________________________________________________________________________________________________

# 1) Librerías y estilo
import pandas as pd
import re, unicodedata
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter
from pathlib import Path

# Estilo/tema robusto
try:
    plt.style.use("seaborn-v0_8")
except Exception:
    pass
try:
    sns.set_theme(style="whitegrid", palette="deep")
except Exception:
    sns.set_style("whitegrid")
    sns.set_palette("deep")

Path("figuras").mkdir(exist_ok=True)
Path("tablas").mkdir(exist_ok=True)

# 2) Helpers
def normalize_colname(c: str) -> str:
    c = c.strip().lower()
    c = re.sub(r"\s+", "_", c)
    c = "".join(ch for ch in unicodedata.normalize("NFKD", c) if not unicodedata.combining(ch))
    c = re.sub(r"[^0-9a-zA-Z_]", "", c)
    return c

def normalize_text(s: pd.Series) -> pd.Series:
    s = s.astype(str).str.strip().str.replace(r"\s+", " ", regex=True).str.lower()
    return s.map(lambda x: "".join(ch for ch in unicodedata.normalize("NFKD", x) if not unicodedata.combining(ch)))

def miles(x, pos):  # 1.234 formateado
    try:
        return f"{int(x):,}".replace(",", ".")
    except:
        return x

# 3) Ruta del CSV
CSV = r"C:\Users\semas\OneDrive\Escritorio\UFPS\estadistica\Registro_Graduados_20250915.csv"
# (Si está junto al .py, podrías usar simplemente: CSV = "Registro_Graduados_20250915.csv")

# 4) Cargar y limpiar
df = pd.read_csv(CSV, encoding="utf-8", low_memory=False)
df.columns = [normalize_colname(c) for c in df.columns]

col_fac     = "facultad"
col_year    = "ano_grado"
col_codigo  = "codigo_estudiantil"  # existe en tu CSV

# Año de grado
s = df[col_year].astype(str).str.replace(",", "", regex=False)
df[col_year] = pd.to_numeric(s.str.extract(r"(\d{4})")[0], errors="coerce").astype("Int64")

# Normalizar facultad
df[col_fac] = normalize_text(df[col_fac])

# Filtrar 1989–2024
df = df[df[col_year].between(1989, 2024, inclusive="both")].copy()

# Deduplicar por (codigo, año)
DEDUPLICAR = True
if DEDUPLICAR and col_codigo in df.columns:
    antes = df.shape[0]
    df = df.drop_duplicates(subset=[col_codigo, col_year], keep="first").copy()
    print(f"Deduplicación: {antes - df.shape[0]} filas removidas.")
else:
    df = df.drop_duplicates().copy()

# 5) Agregar por facultad
conteo = df[col_fac].value_counts().sort_values(ascending=False)
conteo.to_frame("graduados").to_csv("tablas/facultades_top.csv", index=True)

# 6) Gráfico de barras
plt.figure(figsize=(12, 6))
ax = sns.barplot(x=[s.title() for s in conteo.index], y=conteo.values)
ax.yaxis.set_major_formatter(FuncFormatter(miles))
plt.title("Facultades con más graduados — 1989–2024")
plt.xlabel("Facultad")
plt.ylabel("Número de graduados")
plt.xticks(rotation=20, ha="right")

total = int(conteo.sum())
for i, v in enumerate(conteo.values):
    pct = v / total * 100
    ax.text(i, v, f"{v:,}\n({pct:.1f}%)".replace(",", "."), ha="center", va="bottom", fontsize=9)

plt.tight_layout()
plt.savefig("figuras/facultades_top_bar.png", dpi=220)
plt.show()

#_________________________________________________________________________________________________________________________________________________________________________
#_________________PREGUNTA 3_____________________________________________________________________________________________________________________________________________
#_________________________________________________________________________________________________________________________________________________________________________

# 1) Librerías y estilo
import pandas as pd
import numpy as np
import re, unicodedata
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter

# Estilo robusto
try:
    plt.style.use("seaborn-v0_8")
except Exception:
    pass
try:
    sns.set_theme(style="whitegrid", palette="deep")
except Exception:
    sns.set_style("whitegrid")
    sns.set_palette("deep")

Path("figuras").mkdir(exist_ok=True)
Path("tablas").mkdir(exist_ok=True)

# 2) Helpers
def normalize_colname(c: str) -> str:
    c = c.strip().lower()
    c = re.sub(r"\s+", "_", c)
    c = "".join(ch for ch in unicodedata.normalize("NFKD", c) if not unicodedata.combining(ch))
    c = re.sub(r"[^0-9a-zA-Z_]", "", c)
    return c

def normalize_text(s: pd.Series) -> pd.Series:
    s = s.astype(str).str.strip().str.replace(r"\s+", " ", regex=True).str.lower()
    return s.map(lambda x: "".join(ch for ch in unicodedata.normalize("NFKD", x) if not unicodedata.combining(ch)))

def to_decimal_year(anio, periodo, default_half=True):
    """Convierte (año, periodo 1/2) a año decimal. Si falta periodo, usa 0.5."""
    base = anio.astype("float")
    per = periodo.astype("float")
    if default_half:
        # p=1 -> +0.0, p=2 -> +0.5, NaN -> +0.5
        add = np.where(per == 1, 0.0, np.where(per == 2, 0.5, 0.5))
    else:
        add = np.where(per == 2, 0.5, 0.0)  # NaN -> 0.0
    return base + add

def miles(x, pos):  # 1.234 formateado
    try:
        return f"{int(x):,}".replace(",", ".")
    except Exception:
        return x

# 3) Ruta del CSV (usa la que tengas; aquí va tu archivo)
CSV = r"C:\Users\semas\OneDrive\Escritorio\UFPS\estadistica\Registro_Graduados_20250915.csv"
# Si el CSV está junto al .py, podrías usar: CSV = "Registro_Graduados_20250915.csv"

# 4) Cargar y preparar
df = pd.read_csv(CSV, encoding="utf-8", low_memory=False)
df.columns = [normalize_colname(c) for c in df.columns]

col = dict(
    ano_ingreso="ano_ingreso",
    periodo_ingreso="periodo_ingreso",
    ano_grado="ano_grado",
    periodo_grado="periodo_grado",
    modalidad="modalidad",
    codigo="codigo_estudiantil",
)

# Convertir años (extrae 4 dígitos por si vienen con comas)
for y in ["ano_ingreso","ano_grado"]:
    s = df[col[y]].astype(str).str.replace(",", "", regex=False)
    df[col[y]] = pd.to_numeric(s.str.extract(r"(\d{4})")[0], errors="coerce").astype("Int64")

# Períodos a numérico (1/2)
for p in ["periodo_ingreso","periodo_grado"]:
    df[col[p]] = pd.to_numeric(df[col[p]], errors="coerce").astype("Int64")

# Filtrar rango de años de grado
df = df[df[col["ano_grado"]].between(1989, 2024, inclusive="both")].copy()

# Deduplicar por (codigo, año_grado) para evitar doble conteo
if col["codigo"] in df.columns:
    antes = df.shape[0]
    df = df.drop_duplicates(subset=[col["codigo"], col["ano_grado"]], keep="first").copy()
    print(f"Deduplicación: {antes - df.shape[0]} filas removidas.")

# 5) Calcular tiempo hasta el grado (años decimales)
grad_decimal = to_decimal_year(df[col["ano_grado"]], df[col["periodo_grado"]], default_half=True)
ing_decimal  = to_decimal_year(df[col["ano_ingreso"]], df[col["periodo_ingreso"]], default_half=True)
df["tiempo_grado_anios"] = (grad_decimal - ing_decimal)

# Mantener valores plausibles (evita negativos o extremos)
MIN_YRS, MAX_YRS = 0, 20
df_t = df[df["tiempo_grado_anios"].between(MIN_YRS, MAX_YRS)].copy()

# 6) Resumen estadístico (general y por modalidad)
resumen = {
    "n": int(df_t.shape[0]),
    "media": round(df_t["tiempo_grado_anios"].mean(), 2),
    "mediana": round(df_t["tiempo_grado_anios"].median(), 2),
    "p25": round(df_t["tiempo_grado_anios"].quantile(0.25), 2),
    "p75": round(df_t["tiempo_grado_anios"].quantile(0.75), 2),
}
print("=== Tiempo a grado (años) — Resumen general ===")
print(resumen)

if col["modalidad"] in df_t.columns:
    mod_stats = (df_t.assign(mod=lambda d: normalize_text(d[col["modalidad"]]))
                   .groupby("mod")["tiempo_grado_anios"]
                   .agg(["count","median","mean","std","min","max"])
                   .round(2)
                   .sort_values("median"))
    mod_stats.to_csv("tablas/tiempo_grado_por_modalidad.csv")
    print("\n=== Tiempo a grado por modalidad ===")
    print(mod_stats)

# 7) Gráfico principal: Histograma + KDE con media y mediana
bins = np.arange(MIN_YRS, MAX_YRS + 0.5, 0.5)  # bins de 0.5 años
plt.figure(figsize=(10, 5))
sns.histplot(df_t["tiempo_grado_anios"], bins=bins, kde=True, stat="count", color="#4C72B0")
plt.axvline(resumen["media"],   color="#DD8452", linestyle="--", linewidth=2, label=f"Media: {resumen['media']} a")
plt.axvline(resumen["mediana"], color="#55A868", linestyle="-.", linewidth=2, label=f"Mediana: {resumen['mediana']} a")
plt.title("¿Cuánto tardan en graduarse? — Distribución del tiempo a grado")
plt.xlabel("Años hasta el grado")
plt.ylabel("Estudiantes")
plt.legend()
plt.tight_layout()
plt.savefig("figuras/tiempo_grado_hist_kde.png", dpi=220)
plt.show()

# 8) Gráfico auxiliar: Boxplot por modalidad (si existe)
if col["modalidad"] in df_t.columns:
    df_t["mod_plot"] = normalize_text(df_t[col["modalidad"]]).str.title()
    plt.figure(figsize=(9, 5))
    sns.boxplot(data=df_t, x="mod_plot", y="tiempo_grado_anios")
    plt.title("Tiempo a grado por nivel académico (modalidad)")
    plt.xlabel("Modalidad")
    plt.ylabel("Años hasta el grado")
    plt.tight_layout()
    plt.savefig("figuras/tiempo_grado_box_modalidad.png", dpi=220)
    plt.show()

# 9) (Opcional) Tendencia de la mediana por año de grado
trend = (df_t.groupby(col["ano_grado"])["tiempo_grado_anios"]
           .median().reset_index(name="mediana"))
trend.to_csv("tablas/tiempo_grado_mediana_por_anio.csv", index=False)

plt.figure(figsize=(10, 4))
sns.lineplot(data=trend, x=col["ano_grado"], y="mediana", marker="o")
plt.title("Mediana del tiempo a grado por cohorte de graduación")
plt.xlabel("Año de grado")
plt.ylabel("Mediana (años)")
plt.tight_layout()
plt.savefig("figuras/tiempo_grado_mediana_por_anio.png", dpi=220)
plt.show()

# 10) Mensaje corto para tu infografía (imprime una línea amigable)
print(f"\nPara infografía → Tiempo típico hasta el grado: mediana {resumen['mediana']} años "
      f"(media {resumen['media']}; IQR {resumen['p25']}–{resumen['p75']}), "
      f"n={resumen['n']} observaciones (filtrado {MIN_YRS}-{MAX_YRS} años).")
