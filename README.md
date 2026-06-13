# 📊 Exploración y Visualización de Escuelas de Pole Dance en España (EDA)

---

## Objetivo del Análisis

El propósito de este Análisis Exploratorio de Datos (EDA) es comprender la distribución actual del mercado de escuelas de Pole Dance en España utilizando datos obtenidos a través de la API de Google Places. Se busca identificar patrones geográficos, niveles de competencia, tendencias de popularidad y oportunidades de negocio para la apertura de nuevos centros.

**Pregunta principal del análisis:**
> ¿Cómo está distribuido el mercado de escuelas de Pole Dance en España y en dónde existen oportunidades para la apertura de nuevos centros?

---

## Reporte Ejecutivo del Proyecto
Puedes descargar y visualizar el informe completo en formato PDF haciendo clic aquí: 
👉 **[Descargar Reporte Ejecutivo](https://raw.githubusercontent.com/Bootcamp-IA-MAD-P7/proyecto3-johans-salas/main/Reporte_Ejecutivo_Pole_Dance_Spain.pdf)**

---

## Estructura del Proyecto

```
proyecto3-eda-js/
├── dataset/
│   ├── pole_dance_spain_raw.csv           # Dataset original sin procesar
│   ├── pole_dance_spain_enriched.csv      # Dataset enriquecido y limpio
│   ├── google_places_pole_spain.py        # Script de recolección de datos (v1)
│   └── google_places_pole_spain2.py       # Script de recolección de datos (v2)
├── eda_pole_dance_spain.ipynb             # Notebook principal con el EDA completo
├── requirements.txt                       # Dependencias del proyecto
├── .env                                   # Variables de entorno (API keys)
└── README.md                              # Este archivo
```

---

## Secciones del Análisis

El notebook `eda_pole_dance_spain.ipynb` contiene 10 secciones de análisis:

| # | Sección | Descripción |
|---|---------|-------------|
| 1 | Carga y limpieza de datos | Carga del CSV, eliminación de duplicados, filtrado por relevancia, extracción de ciudades y mapeo de comunidades autónomas |
| 2 | Distribución geográfica | Escuelas por provincia, por comunidad autónoma, densidad por 100k habitantes y distribución por tamaño de ciudad |
| 3 | Valoraciones y reputación | Distribución de ratings, rating por provincia y relación entre popularidad (reseñas) y puntuación |
| 4 | Competencia del mercado | Ciudades con mayor competencia y segmentación de mercados por nivel de saturación |
| 5 | Popularidad | Top 20 escuelas más populares y ciudades con mayor interacción de usuarios |
| 6 | Horarios y operación | Días de apertura por semana y horarios de cierre más frecuentes |
| 7 | Presencia digital | Porcentaje de escuelas con página web, teléfono y horario online; impacto en métricas |
| 8 | Análisis espacial (clusters) | Clustering geográfico con DBSCAN y concentración Madrid/Barcelona vs resto |
| 9 | Oportunidades de negocio | Identificación de provincias con alto potencial (alta población + baja densidad de escuelas) |
| 10 | Resumen ejecutivo | Tabla consolidada de hallazgos clave |

---

## Datos

- **Fuente:** Google Places API
- **Registro temporal:** 2025
- **Dataset enriquecido:** 319 escuelas de Pole Dance en 47 provincias de España tras limpieza
- **Variables principales:** nombre, dirección, valoración, número de reseñas, coordenadas, horarios, presencia digital, comunidad autónoma

---

## Tecnologías Utilizadas

- **Python 3.13**
- **Pandas** - Manipulación y análisis de datos
- **NumPy** - Operaciones numéricas
- **Matplotlib / Seaborn** - Visualización gráfica
- **Scikit-learn** - Clustering (DBSCAN) y escalado
- **SciPy** - Análisis estadístico (regresión lineal)
- **Google Places API** - Obtención de datos
- **Requests** - Obtención de datos

---

## Hallazgos Clave

- **Concentración geográfica:** Madrid y Barcelona concentran la mayor cantidad de escuelas, pero ciudades como Valencia, Las Palmas y Santa Cruz de Tenerife muestran mayor penetración relativa por habitante.
- **Altas valoraciones:** La valoración media es ≈4.84/5, con más del 90% de escuelas por encima de 4.5 estrellas.
- **Mercado poco saturado:** La mayoría de ciudades tienen entre 1 y 3 escuelas, indicando oportunidades de crecimiento.
- **Presencia digital:** ~75% de escuelas tienen página web y >80% publican horarios en Google.
- **Horarios concentrados:** La oferta se centra en horarios vespertinos (cierre habitual entre 21:00-22:00), con poca disponibilidad fines de semana.
- **Oportunidades:** Provincias como Sevilla, Málaga, Murcia y Bilbao combinan alta población con densidad moderada de escuelas.

---

## Ejecución

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar el notebook
jupyter notebook eda_pole_dance_spain.ipynb
```

---