"""
Script para generar un reporte ejecutivo en PDF a partir del notebook
eda_pole_dance_spain.ipynb
"""
import json
import base64
import os
import tempfile
from fpdf import FPDF


# ── 1. Leer el notebook ────────────────────────────────────────────
NOTEBOOK_PATH = os.path.join(os.path.dirname(__file__), "eda_pole_dance_spain.ipynb")
OUTPUT_PDF = os.path.join(os.path.dirname(__file__), "Reporte_Ejecutivo_Pole_Dance_Spain.pdf")

with open(NOTEBOOK_PATH, "r", encoding="utf-8") as f:
    nb = json.load(f)


# ── 2. Extraer imágenes PNG de los outputs ─────────────────────────
def extract_images_from_cells(nb):
    """
    Recorre las celdas del notebook y extrae todas las imágenes PNG
    embebidas en los outputs, en orden.
    Devuelve una lista de dicts:
      { 'cell_index': int, 'image_data': bytes, 'text_outputs': [str] }
    """
    results = []
    img_counter = 0
    for idx, cell in enumerate(nb["cells"]):
        if cell["cell_type"] != "code":
            continue
        cell_images = []
        text_outputs = []
        for output in cell.get("outputs", []):
            if output["output_type"] == "stream":
                text_outputs.append("".join(output.get("text", [])))
            elif output["output_type"] == "display_data":
                data = output.get("data", {})
                if "image/png" in data:
                    b64 = data["image/png"]
                    img_bytes = base64.b64decode(b64)
                    cell_images.append(img_bytes)
                    img_counter += 1
        if cell_images or text_outputs:
            results.append({
                "cell_index": idx,
                "images": cell_images,
                "text_outputs": text_outputs,
            })
    print(f"Total imágenes extraídas: {img_counter}")
    return results


cell_data = extract_images_from_cells(nb)


# ── 3. Guardar imágenes temporalmente ──────────────────────────────
tmp_dir = tempfile.mkdtemp()
img_paths = []
img_idx = 0
for cd in cell_data:
    for img_bytes in cd["images"]:
        path = os.path.join(tmp_dir, f"img_{img_idx:03d}.png")
        with open(path, "wb") as f:
            f.write(img_bytes)
        img_paths.append(path)
        img_idx += 1


# ── 4. Definir el contenido del reporte ────────────────────────────
# Estructura: secciones con título, hallazgos e índice de imagen
REPORT_SECTIONS = [
    {
        "title": "1. Carga y Limpieza de Datos",
        "img_indices": [],  # Sección sin gráfico propio
        "findings": (
            "Se partió de un dataset original de 3,626 registros obtenidos a través de la "
            "API de Google Places, referentes a búsquedas de escuelas de Pole Dance en España. "
            "Tras eliminar duplicados por place_id, negocios cerrados permanentemente y "
            "aplicar filtros de negocio (black list y white list), el dataset final quedó "
            "conformado por 319 escuelas de Pole Dance operativas, distribuidas en 47 "
            "provincias.\n\n"
            "La valoración media del dataset limpio es de 4.836 estrellas, lo que indica "
            "una satisfacción general muy alta del sector. Se enriqueció el dataset con "
            "variables calculadas: ciudad extraída de la dirección, comunidad autónoma, "
            "presencia digital (web, teléfono, horario) y parseo de horarios."
        ),
    },
    {
        "title": "2. Distribución Geográfica",
        "img_indices": [0, 1, 2, 3],
        "findings": (
            "Las escuelas de Pole Dance en España se concentran de forma desigual:\n\n"
            "- Madrid y Barcelona lideran en número absoluto de escuelas, seguidas por "
            "Valencia y otras grandes ciudades costeras.\n"
            "- Cuando se ajusta por población (densidad por 100k hab.), ciudades como "
            "Valencia, Las Palmas y Santa Cruz de Tenerife muestran una mayor penetración "
            "relativa del mercado.\n"
            "- La mayoría de ciudades tienen entre 1 y 3 escuelas, lo que indica un "
            "mercado fragmentado donde predominan las localidades pequeñas con presencia "
            "reducida.\n"
            "- Existe una oportunidad clara en provincias de alta población pero baja "
            "densidad de escuelas."
        ),
    },
    {
        "title": "3. Valoraciones y Reputación",
        "img_indices": [4, 5, 6],
        "findings": (
            "La valoración media de las escuelas de Pole Dance en España es extremadamente "
            "alta (≈4.84 sobre 5), con más del 92.9% de escuelas superando las 4.5 "
            "estrellas. Esto refleja un sector con un nivel de satisfacción del cliente "
            "muy elevado.\n\n"
            "Las escuelas más populares (con más reseñas) tienden a mantener valoraciones "
            "altas. La correlación no es perfecta: algunas escuelas con pocas reseñas "
            "alcanzan puntuaciones de 5.0, mientras que escuelas muy populares pueden "
            "tener ratings ligeramente menores (4.6-4.7). No obstante, la tendencia "
            "general es positiva: a mayor número de interacciones, la valoración se "
            "mantiene en niveles altos."
        ),
    },
    {
        "title": "4. Competencia del Mercado",
        "img_indices": [7, 8],
        "findings": (
            "El análisis de competencia revela que la mayoría de ciudades españolas tienen "
            "entre 1 y 3 escuelas de Pole Dance, lo que indica un mercado poco saturado a "
            "nivel local. Solo unas pocas ciudades (Madrid, Barcelona, Valencia, Sevilla) "
            "concentran una competencia significativa.\n\n"
            "La distribución muestra una estructura de cola larga: muchas localidades con "
            "presencia mínima y muy pocas con alta concentración. Esto sugiere que el "
            "mercado está lejos de estar saturado en la mayoría del territorio nacional, "
            "y que existe espacio para nuevos centros tanto en ciudades medianas como en "
            "barrios específicos de grandes urbes."
        ),
    },
    {
        "title": "5. Popularidad",
        "img_indices": [9, 10],
        "findings": (
            "La popularidad de las escuelas (medida por número de reseñas) está fuertemente "
            "influenciada por el tamaño de la ciudad y la actividad turística.\n\n"
            "El Top 20 de escuelas más populares incluye centros de grandes capitales y "
            "también de ciudades turísticas como Las Palmas y Santa Cruz de Tenerife. "
            "Esto indica que la demanda de Pole Dance no solo depende del tamaño de la "
            "población, sino también del turismo y la apertura cultural de cada zona.\n\n"
            "Barcelona, Madrid y Valencia lideran en interacción total de usuarios."
        ),
    },
    {
        "title": "6. Horarios y Operación",
        "img_indices": [11, 12],
        "findings": (
            "La mayoría de escuelas de Pole Dance operan de lunes a viernes, con una "
            "notable reducción de oferta los sábados y una caída drástica los domingos.\n\n"
            "El horario de cierre más frecuente se sitúa entre las 21:00 y las 22:00, lo "
            "que indica que el negocio se orienta principalmente a la clientela que acude "
            "después del horario laboral.\n\n"
            "Esta información es relevante para identificar oportunidades de diferenciación: "
            "escuelas que ofrezcan horarios extendidos, domingos o turnos de mañana podrían "
            "capturar un segmento de mercado infraatendido."
        ),
    },
    {
        "title": "7. Presencia Digital",
        "img_indices": [13, 14],
        "findings": (
            "La presencia digital de las escuelas de Pole Dance es relativamente alta: "
            "aproximadamente el 78.4% cuenta con página web y más del 89% publica su "
            "horario en Google.\n\n"
            "El análisis revela que tener página web no se asocia necesariamente a "
            "valoraciones ni reseñas significativamente mayores. Esto sugiere que la "
            "presencia digital, si bien es necesaria, no es un diferenciador competitivo "
            "por sí sola.\n\n"
            "Las escuelas deberían invertir no solo en tener presencia online, sino en "
            "gestionar activamente sus reseñas y contenido para convertir la visibilidad "
            "en reputación."
        ),
    },
    {
        "title": "8. Análisis Espacial (Clusters)",
        "img_indices": [15, 16],
        "findings": (
            "El algoritmo DBSCAN identifica 10 clusters geográficos en las principales "
            "áreas metropolitanas: Madrid, Barcelona, Valencia, Sevilla, Málaga, Bilbao, "
            "entre otras.\n\n"
            "La gran mayoría de escuelas (253 de 319) permanecen como puntos aislados "
            "fuera de estos clusters, lo que confirma la distribución dispersa del mercado.\n\n"
            "Madrid y Barcelona concentran la mayor cantidad de escuelas, pero el gráfico "
            "revela oportunidades en ciudades intermedias con baja densidad. El mercado "
            "presenta un patrón de nucleación urbana: las escuelas se agrupan en zonas "
            "específicas de las grandes ciudades, dejando amplias áreas geográficas sin "
            "cobertura."
        ),
    },
    {
        "title": "9. Oportunidades de Negocio",
        "img_indices": [17, 18],
        "findings": (
            "El análisis de oportunidades combina población y densidad de escuelas para "
            "identificar provincias con mayor potencial:\n\n"
            "- Madrid, Barcelona y Valencia aparecen como los mercados más atractivos por "
            "su alta población, aunque ya cuentan con oferta significativa.\n"
            "- Provincias como Sevilla, Málaga, Murcia, Bilbao y A Coruña representan "
            "oportunidades intermedias: alta población con densidad de escuelas moderada.\n"
            "- El ranking de oportunidades sugiere que el mayor potencial de crecimiento "
            "se encuentra en provincias de nivel medio-alto donde la demanda demográfica "
            "aún no está completamente cubierta por la oferta actual.\n\n"
            "Provincias con mayor índice de oportunidad: Madrid (0.37/100k), Sevilla "
            "(0.36/100k), Bilbao (0.26/100k), A Coruña (0.36/100k) y Granada (0.22/100k)."
        ),
    },
    {
        "title": "10. Resumen Ejecutivo",
        "img_indices": [],
        "findings": (
            "INDICADORES CLAVE:\n\n"
            "- Total de escuelas analizadas: 319\n"
            "- Provincias cubiertas: 47 de 50\n"
            "- Valoración media: 4.836 estrellas\n"
            "- % con rating ≥ 4.5: 92.9%\n"
            "- % con página web: 78.4%\n"
            "- % con horario registrado: 89.0%\n"
            "- Nº de clusters espaciales: 10\n"
            "- Top provincia por escuelas: Madrid (25)\n"
            "- Top ciudad por reseñas: Barcelona (1,984 reseñas)\n\n"
            "CONCLUSIONES:\n\n"
            "El mercado de escuelas de Pole Dance en España presenta un panorama "
            "fragmentado con oportunidades claras de expansión. La alta satisfacción "
            "del cliente (rating medio ≈4.84) y la baja saturación en la mayoría de "
            "provincias sugieren que el sector tiene potencial de crecimiento. Las "
            "mejores oportunidades se encuentran en provincias de alta población y "
            "baja densidad de escuelas, como Sevilla, Málaga, Murcia y Bilbao. "
            "Además, los horarios concentrados en la tarde-noche y la baja presencia "
            "de ofertas los domingos representan nichos de diferenciación para nuevos "
            "emprendimientos."
        ),
    },
]


# ── 5. Construir el PDF ────────────────────────────────────────────
def sanitize(text: str) -> str:
    """Reemplaza caracteres Unicode no soportados por Helvetica."""
    replacements = {
        "\u2248": "~",   # ≈
        "\u2013": "-",   # –
        "\u2014": "-",   # —
        "\u2018": "'",   # '
        "\u2019": "'",   # '
        "\u201c": '"',   # "
        "\u201d": '"',   # "
        "\u2026": "...", # …
        "\u2192": "->",  # →
        "\u2190": "<-",  # ←
        "\u2022": "*",   # •
        "\u2605": "*",   # ★
        "\u2713": "x",   # ✓
        "\u2717": "x",   # ✗
        "\u00b0": " deg", # °
        "\u00ba": "o",    # º
        "\u00aa": "a",    # ª
        "\u00e9": "e",    # é
        "\u00e1": "a",    # á
        "\u00ed": "i",    # í
        "\u00f3": "o",    # ó
        "\u00fa": "u",    # ú
        "\u00f1": "n",    # ñ
        "\u00fc": "u",    # ü
        "\u00c9": "E",    # É
        "\u00c1": "A",    # Á
        "\u00cd": "I",    # Í
        "\u00d3": "O",    # Ó
        "\u00da": "U",    # Ú
        "\u00d1": "N",    # Ñ
        "\u00dc": "U",    # Ü
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    # Fallback: replace any remaining non-latin1 characters
    result = []
    for ch in text:
        try:
            ch.encode("latin-1")
            result.append(ch)
        except UnicodeEncodeError:
            result.append("?")
    return "".join(result)


class ReportPDF(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(100, 100, 100)
            self.cell(0, 8, "Reporte Ejecutivo - Escuelas de Pole Dance en España", align="C")
            self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Página {self.page_no()}/{{nb}}", align="C")

    def chapter_title(self, title):
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(0, 59, 103)  # DARK blue
        self.cell(0, 12, sanitize(title), new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(0, 119, 182)  # BLUE
        self.set_line_width(0.8)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(6)

    def section_text(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(50, 50, 50)
        self.multi_cell(0, 6, sanitize(text))
        self.ln(4)

    def findings_block(self, title, text):
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(0, 180, 216)  # TEAL
        self.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "", 10)
        self.set_text_color(50, 50, 50)
        self.multi_cell(0, 6, sanitize(text))
        self.ln(4)

    def add_image_full_width(self, img_path, max_w=180, max_h=120):
        """Añade una imagen centrada, escalada para caber en la página."""
        from PIL import Image as PILImage
        with PILImage.open(img_path) as im:
            iw, ih = im.size
        aspect = iw / ih
        w = min(max_w, max_h * aspect)
        h = w / aspect
        if h > max_h:
            h = max_h
            w = h * aspect
        x = (210 - w) / 2
        self.image(img_path, x=x, w=w)
        self.ln(4)


pdf = ReportPDF()
pdf.alias_nb_pages()
pdf.set_auto_page_break(auto=True, margin=20)

# ── Portada ────────────────────────────────────────────────────────
pdf.add_page()
pdf.ln(50)
pdf.set_font("Helvetica", "B", 28)
pdf.set_text_color(0, 59, 103)
pdf.multi_cell(0, 14, "REPORTE EJECUTIVO", align="C")
pdf.ln(4)
pdf.set_font("Helvetica", "", 18)
pdf.set_text_color(0, 180, 216)
pdf.multi_cell(0, 10, "Exploración y Visualización de\nEscuelas de Pole Dance en España", align="C")
pdf.ln(6)
pdf.set_font("Helvetica", "I", 12)
pdf.set_text_color(100, 100, 100)
pdf.multi_cell(0, 8, "Análisis Exploratorio de Datos (EDA)\nmediante Google Places API", align="C")
pdf.ln(20)
pdf.set_draw_color(0, 119, 182)
pdf.set_line_width(1)
pdf.line(60, pdf.get_y(), 150, pdf.get_y())
pdf.ln(15)
pdf.set_font("Helvetica", "", 12)
pdf.set_text_color(50, 50, 50)
pdf.cell(0, 8, "Elaborado por:", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Helvetica", "B", 16)
pdf.set_text_color(0, 59, 103)
pdf.cell(0, 12, "Johans Enrique Salas Rodríguez", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.ln(30)
pdf.set_font("Helvetica", "", 10)
pdf.set_text_color(128, 128, 128)
pdf.cell(0, 8, "Junio 2026", align="C", new_x="LMARGIN", new_y="NEXT")

# ── Índice ─────────────────────────────────────────────────────────
pdf.add_page()
pdf.set_font("Helvetica", "B", 20)
pdf.set_text_color(0, 59, 103)
pdf.cell(0, 12, "ÍNDICE", new_x="LMARGIN", new_y="NEXT")
pdf.ln(4)
toc_items = [s["title"] for s in REPORT_SECTIONS]
pdf.set_font("Helvetica", "", 12)
pdf.set_text_color(50, 50, 50)
for i, item in enumerate(toc_items, 1):
    pdf.cell(0, 10, f"  {item}", new_x="LMARGIN", new_y="NEXT")

# ── Pregunta principal ─────────────────────────────────────────────
pdf.add_page()
pdf.set_font("Helvetica", "B", 14)
pdf.set_text_color(0, 59, 103)
pdf.cell(0, 10, "Pregunta Principal del Análisis", new_x="LMARGIN", new_y="NEXT")
pdf.ln(4)
pdf.set_font("Helvetica", "I", 13)
pdf.set_text_color(0, 180, 216)
pdf.multi_cell(0, 8,
    "¿Cómo está distribuido el mercado de escuelas de Pole Dance en España "
    "y en dónde existen oportunidades para la apertura de nuevos centros?",
    align="C"
)
pdf.ln(8)
pdf.set_font("Helvetica", "", 10)
pdf.set_text_color(80, 80, 80)
pdf.multi_cell(0, 6,
    "Este reporte presenta los resultados de un Análisis Exploratorio de Datos (EDA) "
    "realizado sobre un dataset de escuelas de Pole Dance en España, obtenido a través "
    "de la API de Google Places. El análisis cubre distribución geográfica, valoraciones, "
    "competencia, popularidad, horarios, presencia digital, clusters espaciales y "
    "oportunidades de negocio."
)

# ── Secciones del reporte ──────────────────────────────────────────
img_counter = 0
for section in REPORT_SECTIONS:
    pdf.add_page()
    pdf.chapter_title(section["title"])

    # Imágenes de la sección
    for local_idx in section["img_indices"]:
        if img_counter + local_idx < len(img_paths):
            pdf.add_image_full_width(img_paths[img_counter + local_idx])

    img_counter += len(section["img_indices"])

    # Hallazgos
    pdf.findings_block("Hallazgos:", section["findings"])

# ── Guardar PDF ────────────────────────────────────────────────────
pdf.output(OUTPUT_PDF)
print(f"\nPDF generado exitosamente: {OUTPUT_PDF}")

# Limpiar archivos temporales
for p in img_paths:
    os.remove(p)
os.rmdir(tmp_dir)
