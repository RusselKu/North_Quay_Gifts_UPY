import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
import os

doc = Document()

# Set standard margins (1 inch)
for section in doc.sections:
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>'))

def format_table(table, col_widths=None):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, row in enumerate(table.rows):
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        for j, cell in enumerate(row.cells):
            if col_widths and j < len(col_widths):
                cell.width = Inches(col_widths[j])
            if i == 0:
                set_cell_background(cell, "1F497D")
                for p in cell.paragraphs:
                    p.paragraph_format.space_before = Pt(4)
                    p.paragraph_format.space_after = Pt(4)
                    for r in p.runs:
                        r.font.bold = True
                        r.font.color.rgb = RGBColor(255, 255, 255)
                        r.font.size = Pt(9.5)
            else:
                bg = "F2F2F2" if i % 2 == 1 else "FFFFFF"
                set_cell_background(cell, bg)
                for p in cell.paragraphs:
                    p.paragraph_format.space_before = Pt(3)
                    p.paragraph_format.space_after = Pt(3)
                    for r in p.runs:
                        r.font.size = Pt(9)

# ----------------- COVER / HEADER -----------------
title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
t_run = title.add_run("ACTIVIDAD DE APRENDIZAJE 1\nEntendimiento y Exploración de Datos")
t_run.font.bold = True
t_run.font.size = Pt(18)
t_run.font.color.rgb = RGBColor(31, 73, 125)

subtitle = doc.add_paragraph()
subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
s_run = subtitle.add_run("North Quay Gifts | Online Retail II | Fase CRISP-DM: Data Understanding")
s_run.font.italic = True
s_run.font.size = Pt(11)
s_run.font.color.rgb = RGBColor(89, 89, 89)

doc.add_paragraph()

meta_table = doc.add_table(rows=2, cols=2)
meta_table.rows[0].cells[0].paragraphs[0].add_run("Equipo de Trabajo")
meta_table.rows[0].cells[1].paragraphs[0].add_run("Profesor y Fecha")

team_p = meta_table.rows[1].cells[0].paragraphs[0]
team_p.add_run("• Russel Emmanuel Ku Aguilar (ID: 2309131)\n• Damian Nicolas Sanchez Novelo (ID: 2109134)\n• Jonathan Abisai Velasco Martín (ID: 2309060)\n• Ángel Rivaldo Canché Chuc (ID: 2309030)\n• Bianca Alexandra Acosta Castellanos (ID: 2309001)")

prof_p = meta_table.rows[1].cells[1].paragraphs[0]
prof_p.add_run("Profesor: Didier Omar Gamboa Angulo\nCorreo: didier.gamboa@upy.edu.mx\nInstitución: Universidad Politécnica de Yucatán\nFecha: Octubre 2026")
format_table(meta_table, [3.5, 3.0])

doc.add_paragraph()

# Purpose & Scope
h_prop = doc.add_heading("Propósito y Alcance", level=2)
p_prop = doc.add_paragraph(
    "El presente documento constituye el Reporte Formal de la Fase de Entendimiento de Datos (CRISP-DM Phase 2) sobre el repositorio transaccional online_retail_II.csv de North Quay Gifts. "
    "El análisis se sustenta en cálculos empíricos rigurosos, visualizaciones con denominadores comunes y una libreta de Python (NB2 Exploración de Datos - Online Retail II.ipynb) completamente ejecutada que valida cada hallazgo. "
    "De acuerdo con los límites metodológicos de la actividad, en esta fase no se alteran ni eliminan transacciones, no se imputan valores nulos y no se crean variables derivadas sintéticas."
)
p_prop.paragraph_format.line_spacing = 1.15

# ----------------- SECTION 1 -----------------
doc.add_heading("1. Reconocimiento de los Datos", level=1)

t1 = doc.add_table(rows=5, cols=2)
t1.rows[0].cells[0].paragraphs[0].add_run("Indicador")
t1.rows[0].cells[1].paragraphs[0].add_run("Resultado")
data_t1 = [
    ("Número de líneas y columnas", "1,067,371 filas × 8 columnas"),
    ("Primera y última fecha con hora", "2009-12-01 07:45:00 a 2011-12-09 12:50:00"),
    ("Facturas distintas y clientes identificados distintos", "53,628 facturas distintas | 5,942 clientes identificados distintos (excluye nulos)"),
    ("Unidad representada por una fila", "Línea individual de ítem/producto dentro de una factura comercial")
]
for idx, (ind, res) in enumerate(data_t1, start=1):
    t1.rows[idx].cells[0].paragraphs[0].add_run(ind)
    t1.rows[idx].cells[1].paragraphs[0].add_run(res)
format_table(t1, [3.2, 3.3])

doc.add_paragraph()

t2 = doc.add_table(rows=9, cols=3)
t2.rows[0].cells[0].paragraphs[0].add_run("Columna")
t2.rows[0].cells[1].paragraphs[0].add_run("Tipo en Pandas")
t2.rows[0].cells[2].paragraphs[0].add_run("Función y Significado Analítico")
data_t2 = [
    ("Invoice", "object", "Nominal / Identificador: Código único alfanumérico por orden. Prefijo 'C' indica transacción de cancelación."),
    ("StockCode", "object", "Nominal / Alfanumérico: Código de catálogo de producto o partida operativa/servicio (e.g. POST, D, M, B)."),
    ("Description", "object", "Cualitativa Textual: Nombre comercial del producto o glosa de notas internas y mermas de almacén."),
    ("Quantity", "int64", "Cuantitativa Discreta: Unidades facturadas. Valores negativos denotan cancelaciones o mermas de inventario."),
    ("InvoiceDate", "datetime64[ns]", "Temporal / Cronológica: Marca temporal exacta (timestamp) de emisión de la transacción."),
    ("Price", "float64", "Cuantitativa Continua (Razón): Precio unitario de venta en Libras Esterlinas (GBP, £)."),
    ("Customer ID", "float64", "Nominal / Identificador: Clave única de cliente registrado. Los nulos representan compras sin tracking."),
    ("Country", "object", "Cualitativa Nominal: País geográfico asociado a la cuenta de facturación o despacho.")
]
for idx, (c, tp, fn) in enumerate(data_t2, start=1):
    t2.rows[idx].cells[0].paragraphs[0].add_run(c)
    t2.rows[idx].cells[1].paragraphs[0].add_run(tp)
    t2.rows[idx].cells[2].paragraphs[0].add_run(fn)
format_table(t2, [1.5, 1.3, 3.7])

doc.add_paragraph()

# Question 1
q1 = doc.add_paragraph()
q1.add_run("1. Factura multi-producto y discrepancia de conteos\n").bold = True
q1.add_run("Respuesta e interpretación: ").bold = True
q1.add_run(
    "Analizamos la factura 489517 (fecha 2009-12-01 11:34:00, Customer ID 16329.0). Esta orden contiene 38 líneas en total, pero únicamente 28 StockCodes distintos. "
    "Los conteos difieren porque varios productos fueron registrados en múltiples filas separadas dentro de la misma transacción (por ejemplo, los StockCodes 21491, 21821 y 21912 aparecen repetidos dos veces cada uno en el mismo minuto exacto). "
    "Esto sucede cuando el cliente agrega artículos en distintas etapas del armado del carrito o cuando la pasarela registra líneas redundantes en vez de consolidar cantidades. "
    "Por consiguiente, el total de filas (1,067,371) no equivale al número de pedidos (53,628). Cada fila representa una partida de mercancía; equiparar filas con pedidos inflaría la frecuencia de compra 19.9 veces."
)

# Question 2
q2 = doc.add_paragraph()
q2.add_run("2. Promedio de identificadores y escalas de medición\n").bold = True
q2.add_run("Respuesta e interpretación: ").bold = True
q2.add_run(
    "Calcular el promedio de Customer ID (15,555.57) o de un código de producto carece de validez metodológica porque ambas variables pertenecen a una escala nominal de medición (taxonomía de Stevens). "
    "Los números funcionan como etiquetas o llaves subrogadas cualitativas para diferenciar clientes, no como magnitudes con propiedades métricas o de distancia. "
    "El promedio resultante es un decimal sin sentido que no corresponde a ningún comprador real ni describe volumen de compra. "
    "Existe una diferencia fundamental entre el tipo de almacenamiento (cómo se asigna en memoria en Pandas, e.g. float64 para admitir valores NaN de clientes anónimos) y el significado analítico (la naturaleza conceptual y operaciones matemáticas legítimas de la variable)."
)

# Question 3
q3 = doc.add_paragraph()
q3.add_run("3. Cobertura mensual en los límites temporales\n").bold = True
q3.add_run("Respuesta e interpretación: ").bold = True
q3.add_run(
    "Ninguno de los dos meses extremos está completo: "
    "(1) Diciembre 2009 inicia el 2009-12-01 07:45:00 y corta abruptamente el 2009-12-23 16:58:00 (21 días activos), omitiendo la semana de liquidaciones post-navideñas. "
    "(2) Diciembre 2011 registra actividad únicamente hasta el 2011-12-09 12:50:00 (8 días activos con 25,526 filas, frente a 84,711 de noviembre 2011). "
    "Restricción analítica: Cualquier comparación directa mes a mes o año contra año (e.g. comparar diciembre 2010 completo con diciembre 2009 o 2011) generará un sesgo severo de contracción artificial a menos que se normalicen los ingresos por día hábil o se recorten a ventanas comparables (1 al 9 de diciembre)."
)

# ----------------- SECTION 2 -----------------
doc.add_heading("2. Estadística Descriptiva", level=1)

t3 = doc.add_table(rows=11, cols=3)
t3.rows[0].cells[0].paragraphs[0].add_run("Estadístico")
t3.rows[0].cells[1].paragraphs[0].add_run("Quantity (Unidades)")
t3.rows[0].cells[2].paragraphs[0].add_run("Price (GBP £ / Unidad)")
data_t3 = [
    ("Observaciones no nulas", "1,067,371", "1,067,371"),
    ("Media", "9.9389", "4.6494"),
    ("Mediana", "3.0000", "2.1000"),
    ("Desviación estándar", "172.7058", "123.5531"),
    ("Mínimo", "-80,995", "-53,594.36"),
    ("Primer cuartil (Q1 - 25%)", "1.0000", "1.2500"),
    ("Tercer cuartil (Q3 - 75%)", "10.0000", "4.1500"),
    ("Máximo", "80,995", "38,970.00"),
    ("Asimetría (Skewness)", "3.9961", "-69.1647"),
    ("Curtosis (Fisher Excess Kurtosis)", "155,059.71", "73,751.83")
]
for idx, (st, q, p) in enumerate(data_t3, start=1):
    t3.rows[idx].cells[0].paragraphs[0].add_run(st)
    t3.rows[idx].cells[1].paragraphs[0].add_run(q)
    t3.rows[idx].cells[2].paragraphs[0].add_run(p)
format_table(t3, [2.7, 1.9, 1.9])

doc.add_paragraph()

t4 = doc.add_table(rows=3, cols=4)
t4.rows[0].cells[0].paragraphs[0].add_run("Variable")
t4.rows[0].cells[1].paragraphs[0].add_run("Presentes")
t4.rows[0].cells[2].paragraphs[0].add_run("Distintos")
t4.rows[0].cells[3].paragraphs[0].add_run("Categoría más frecuente y líneas")
data_t4 = [
    ("Country", "1,067,371", "43", "United Kingdom (981,330 líneas, 91.94%)"),
    ("StockCode", "1,067,371", "5,305", "85123A (5,829 líneas, 0.55%)")
]
for idx, (v, pr, dst, mf) in enumerate(data_t4, start=1):
    t4.rows[idx].cells[0].paragraphs[0].add_run(v)
    t4.rows[idx].cells[1].paragraphs[0].add_run(pr)
    t4.rows[idx].cells[2].paragraphs[0].add_run(dst)
    t4.rows[idx].cells[3].paragraphs[0].add_run(mf)
format_table(t4, [1.5, 1.3, 1.1, 2.6])

doc.add_paragraph()

# Question 4
q4 = doc.add_paragraph()
q4.add_run("4. Comparación de Media vs. Mediana y Asimetría\n").bold = True
q4.add_run("Respuesta e interpretación: ").bold = True
q4.add_run(
    "Para Quantity, la media es 9.94 unidades mientras que la mediana es 3.00 unidades (Q1=1, Q3=10). La media es 3.3 veces mayor a la mediana debido a una marcada asimetría positiva (3.996) provocada por pedidos mayoristas atípicos de hasta 80,995 unidades. "
    "Para Price, la media es £4.65 frente a una mediana de £2.10 (Q1=£1.25, Q3=£4.15). La variable presenta asimetría negativa (-69.16) debido a asientos contables negativos extremos (-£53,594.36). "
    "Con curtosis extrema superior a 70,000, la media aritmética no representa una compra típica. La mediana y el rango intercuartílico (IQR) constituyen las únicas medidas robustas: una compra típica minorista consta de 1 a 10 unidades de productos entre £1.25 y £4.15."
)

# Question 5
q5 = doc.add_paragraph()
q5.add_run("5. Significado de Mínimos y Máximos\n").bold = True
q5.add_run("Respuesta e interpretación: ").bold = True
q5.add_run(
    "Los extremos revelan anomalías operativas de gran impacto: "
    "(1) En Quantity, el mínimo (-80,995) y máximo (+80,995) corresponden exactamente al mismo producto (StockCode 23843, Paper Craft Little Star). Los datos reflejan una anulación simétrica completa de una orden colosal. Hipótesis: venta mayorista cancelada por falta de stock o impago; requiere confirmación con Ventas y Logística. "
    "(2) En Price, el mínimo de -£53,594.36 (factura A506401, 'Adjust bad debt') evidencia que se mezclaron registros no comerciales en la tabla de ventas. Hipótesis: saneamiento contable de cartera vencida por Finanzas; requiere confirmación formal con Contabilidad."
)

# Question 6
q6 = doc.add_paragraph()
q6.add_run("6. Evaluación de Dispersión y Escalas\n").bold = True
q6.add_run("Respuesta e interpretación: ").bold = True
q6.add_run(
    "Dado que Quantity (unidades) y Price (libras £) manejan dimensiones distintas, sus desviaciones estándar no son directamente comparables. Evaluamos la dispersión relativa mediante el Rango Intercuartílico (IQR) respecto a la mediana: "
    "En Quantity, IQR = 9 sobre una mediana de 3 (dispersión relativa del 300%; desviación estándar de 172.71 unidades, 17.4 veces la media). "
    "En Price, IQR = £2.90 sobre una mediana de £2.10 (dispersión relativa del 138%; desviación estándar de £123.55, 26.6 veces la media). "
    "Conclusión: Quantity presenta mayor dispersión operativa real durante la operación habitual, reflejando que North Quay atiende simultáneamente a compradores minoristas (1 a 3 piezas) y mayoristas B2B (cientos de piezas)."
)

# ----------------- SECTION 3 -----------------
doc.add_heading("3. Análisis Univariado", level=1)

# Add Figures 1 & 2
if os.path.exists("A-3-3_DataUnderstanding/figures/fig1_quantity_hist.png"):
    doc.add_paragraph().add_run("Figura 1. Distribución Empírica de Quantity (Full vs. Zoom)").bold = True
    doc.add_picture("A-3-3_DataUnderstanding/figures/fig1_quantity_hist.png", width=Inches(6.2))

if os.path.exists("A-3-3_DataUnderstanding/figures/fig2_price_hist.png"):
    doc.add_paragraph().add_run("Figura 2. Distribución Empírica de Price en GBP (Full vs. Zoom)").bold = True
    doc.add_picture("A-3-3_DataUnderstanding/figures/fig2_price_hist.png", width=Inches(6.2))

# Question 7
q7 = doc.add_paragraph()
q7.add_run("7. Concentración, Asimetría y Valores Extremos en Histogramas\n").bold = True
q7.add_run("Respuesta e interpretación: ").bold = True
q7.add_run(
    "Los histogramas confirman una concentración leptocúrtica extrema en valores positivos bajos: "
    "En Quantity (Figura 1), más del 95.53% de las transacciones se sitúan entre 1 y 50 unidades (mediana = 3, moda = 1). La ventana focalizada [-50, 100] captura el 98.84% del archivo total (solo 1.16% queda fuera). Se observa una cola derecha de pedidos mayoristas y una cola izquierda discreta de devoluciones y mermas. "
    "En Price (Figura 2), el 98.17% de los registros está entre £0.00 y £15.00 GBP, con un pico pronunciado en £1.25–£2.50 (mediana = £2.10). La ventana [£0.00, £25.00] encierra el 99.39% de los datos (0.61% fuera). Los registros negativos corresponden a ajustes de deuda."
)

# Add Figures 3 & 4
if os.path.exists("A-3-3_DataUnderstanding/figures/fig3_country_bar.png"):
    doc.add_paragraph().add_run("Figura 3. Diez Países Más Frecuentes").bold = True
    doc.add_picture("A-3-3_DataUnderstanding/figures/fig3_country_bar.png", width=Inches(6.0))

if os.path.exists("A-3-3_DataUnderstanding/figures/fig4_stockcode_bar.png"):
    doc.add_paragraph().add_run("Figura 4. Diez StockCodes Más Frecuentes").bold = True
    doc.add_picture("A-3-3_DataUnderstanding/figures/fig4_stockcode_bar.png", width=Inches(6.0))

t5 = doc.add_table(rows=3, cols=3)
t5.rows[0].cells[0].paragraphs[0].add_run("Variable")
t5.rows[0].cells[1].paragraphs[0].add_run("Categorías distintas")
t5.rows[0].cells[2].paragraphs[0].add_run("Tres categorías más frecuentes con líneas y porcentaje")
data_t5 = [
    ("Country", "43", "1. United Kingdom: 981,330 (91.94%)\n2. EIRE: 17,866 (1.67%)\n3. Germany: 17,624 (1.65%)"),
    ("StockCode", "5,305", "1. 85123A: 5,829 (0.55%)\n2. 22423: 4,424 (0.41%)\n3. 85099B: 4,216 (0.39%)")
]
for idx, (v, c, m) in enumerate(data_t5, start=1):
    t5.rows[idx].cells[0].paragraphs[0].add_run(v)
    t5.rows[idx].cells[1].paragraphs[0].add_run(c)
    t5.rows[idx].cells[2].paragraphs[0].add_run(m)
format_table(t5, [1.5, 1.3, 3.7])

doc.add_paragraph()

# Question 8
q8 = doc.add_paragraph()
q8.add_run("8. Concentración vs. Diversidad en Frecuencias\n").bold = True
q8.add_run("Respuesta e interpretación: ").bold = True
q8.add_run(
    "Country muestra una concentración geográfica extrema: Reino Unido concentra el 91.94% de las filas y los diez primeros países cubren el 98.46%. En contraste, StockCode exhibe una altísima diversidad de catálogo: el SKU más vendido (85123A) apenas alcanza el 0.55% de las filas y los diez primeros productos abarcan conjuntamente solo el 3.24% de los registros. "
    "El producto o país con más líneas no necesariamente genera más ingresos o unidades: "
    "(1) Un artículo económico de impulso (e.g. llavero de £0.42) puede acumular miles de líneas individuales de 1 pieza, sumando pocos ingresos. "
    "(2) Un artículo costoso (e.g. soporte de pasteles de £12.75) vendido en lotes de 100 unidades genera ingresos drásticamente mayores con muchas menos líneas."
)

# Add Figures 5 & 6
if os.path.exists("A-3-3_DataUnderstanding/figures/fig5_6_boxplots.png"):
    doc.add_paragraph().add_run("Figuras 5 y 6. Diagramas de Caja y Bigotes (Regla Tukey 1.5×IQR)").bold = True
    doc.add_picture("A-3-3_DataUnderstanding/figures/fig5_6_boxplots.png", width=Inches(6.2))

# Question 9
q9 = doc.add_paragraph()
q9.add_run("9. Interpretación de Boxplots y Validación de Atípicos\n").bold = True
q9.add_run("Respuesta e interpretación: ").bold = True
q9.add_run(
    "Los boxplots aplican la regla estándar de Tukey: bigotes hasta 1.5 × IQR desde Q1 y Q3. "
    "En Quantity: Q1=1, Q3=10, IQR=9. El bigote superior corta en 10 + 1.5(9) = 23.5 (~23 unidades); valores mayores son señalados como atípicos. "
    "En Price: Q1=£1.25, Q3=£4.15, IQR=£2.90. El bigote superior corta en £4.15 + 1.5(£2.90) = £8.50. "
    "Un punto atípico no basta para declarar un error: en comercio mayorista B2B es legítimo y habitual que un cliente compre lotes de 50 a 500 unidades en una sola línea. Los errores genuinos se diferencian por el contexto semántico (e.g. precio negativo, ausencia de cliente o glosas de ajuste), no por el mero hecho de rebasar los bigotes."
)

# ----------------- SECTION 4 -----------------
doc.add_heading("4. Diagnóstico de Calidad de Datos", level=1)

t6 = doc.add_table(rows=9, cols=3)
t6.rows[0].cells[0].paragraphs[0].add_run("Columna")
t6.rows[0].cells[1].paragraphs[0].add_run("Nulos")
t6.rows[0].cells[2].paragraphs[0].add_run("Porcentaje sobre el total (N = 1,067,371)")
data_t6 = [
    ("Invoice", "0", "0.0000%"),
    ("StockCode", "0", "0.0000%"),
    ("Description", "4,382", "0.4105%"),
    ("Quantity", "0", "0.0000%"),
    ("InvoiceDate", "0", "0.0000%"),
    ("Price", "0", "0.0000%"),
    ("Customer ID", "243,007", "22.7669%"),
    ("Country", "0", "0.0000%")
]
for idx, (col, nl, pct) in enumerate(data_t6, start=1):
    t6.rows[idx].cells[0].paragraphs[0].add_run(col)
    t6.rows[idx].cells[1].paragraphs[0].add_run(nl)
    t6.rows[idx].cells[2].paragraphs[0].add_run(pct)
format_table(t6, [2.2, 1.8, 2.5])

doc.add_paragraph()

t7 = doc.add_table(rows=6, cols=3)
t7.rows[0].cells[0].paragraphs[0].add_run("Situación")
t7.rows[0].cells[1].paragraphs[0].add_run("Líneas")
t7.rows[0].cells[2].paragraphs[0].add_run("Porcentaje sobre el total")
data_t7 = [
    ("Duplicados exactos adicionales", "34,335", "3.2168%"),
    ("Quantity < 0", "22,950", "2.1501%"),
    ("Quantity = 0", "0", "0.0000%"),
    ("Price < 0", "5", "0.0005%"),
    ("Price = 0", "6,202", "0.5811%")
]
for idx, (sit, ln, pct) in enumerate(data_t7, start=1):
    t7.rows[idx].cells[0].paragraphs[0].add_run(sit)
    t7.rows[idx].cells[1].paragraphs[0].add_run(ln)
    t7.rows[idx].cells[2].paragraphs[0].add_run(pct)
format_table(t7, [3.0, 1.5, 2.0])

doc.add_paragraph()

# Question 10
q10 = doc.add_paragraph()
q10.add_run("10. Impacto de Nulos en Customer ID vs. Utilidad Comercial\n").bold = True
q10.add_run("Respuesta e interpretación: ").bold = True
q10.add_run(
    "La ausencia de Customer ID en 243,007 filas (22.77%) impide calcular métricas de cliente individual: RFM (Recencia, Frecuencia, Valor Monetario), Valor de Vida del Cliente (CLV), fidelidad y probabilidad de churn. "
    "Sin embargo, estas líneas siguen siendo valiosas para la actividad comercial global: reflejan ventas minoristas reales de clientes no registrados en caja y consumo físico de inventario. "
    "Conservarlas permite pronosticar la demanda agregada de la tienda, planificar el reabastecimiento en almacén y modelar afinidad de productos (market basket) en todo el catálogo."
)

# Question 11
q11 = doc.add_paragraph()
q11.add_run("11. Examen de Casos de Duplicados y Precios No Positivos\n").bold = True
q11.add_run("Respuesta e interpretación: ").bold = True
q11.add_run(
    "(1) Duplicado Exacto: Factura 489517, StockCode 21491 ('MINI PAINT SET VINTAGE'), Quantity 6, Price £0.65, Customer ID 16329.0, Timestamp 2009-12-01 11:34:00. Las filas 379 y 391 contienen los mismos datos al segundo exacto. Evidencia: reintentos de red o doble clic en pasarela web. Información faltante: logs web de clics o albarán de despacho físico para confirmar si se entregaron 6 o 12 piezas. "
    "(2) Precio Negativo: Factura A506401, StockCode B, Quantity 1, Price -£53,594.36, Descripción 'Adjust bad debt', Customer ID NaN. Evidencia: prefijo 'A' y glosa confirman ajustes contables de cartera incobrable. Información faltante: catálogo contable corporativo para validar si fueron auditadas. "
    "Otros hallazgos: partidas no mercantiles como POST (1,983 líneas), D (214), M (939), BANK CHARGES (110); 6,202 registros con Price = £0.00 con notas de auditoría de almacén ('check', 'damages', 'found'); 100% de fechas interpretables."
)

# ----------------- SECTION 5 -----------------
doc.add_heading("5. Investigación de Cancelaciones y Cantidades Negativas", level=1)

t8 = doc.add_table(rows=6, cols=2)
t8.rows[0].cells[0].paragraphs[0].add_run("Indicador")
t8.rows[0].cells[1].paragraphs[0].add_run("Resultado")
data_t8 = [
    ("Líneas con prefijo C", "19,494"),
    ("Facturas C distintas", "8,292"),
    ("Líneas C con Quantity < 0", "19,493"),
    ("Líneas C con Quantity = 0", "0"),
    ("Líneas C con Quantity > 0", "1 (Factura C496350, Manual, Q=+1, £373.57)")
]
for idx, (ind, res) in enumerate(data_t8, start=1):
    t8.rows[idx].cells[0].paragraphs[0].add_run(ind)
    t8.rows[idx].cells[1].paragraphs[0].add_run(res)
format_table(t8, [3.2, 3.3])

doc.add_paragraph()

t9 = doc.add_table(rows=2, cols=3)
t9.rows[0].cells[0].paragraphs[0].add_run("Líneas negativas sin C")
t9.rows[0].cells[1].paragraphs[0].add_run("Facturas distintas")
t9.rows[0].cells[2].paragraphs[0].add_run("Hallazgos en precios y clientes")
t9.rows[1].cells[0].paragraphs[0].add_run("3,457")
t9.rows[1].cells[1].paragraphs[0].add_run("3,393")
t9.rows[1].cells[2].paragraphs[0].add_run("100% tienen Price = £0.00 y Customer ID nulo. Descripciones corresponden a merma: check (123), damages (84), ? (83), damaged (78), missing (27), smashed (9), thrown away (9).")
format_table(t9, [1.8, 1.5, 3.2])

doc.add_paragraph()

# Question 12
q12 = doc.add_paragraph()
q12.add_run("12. Hipótesis sobre Cantidades Negativas vs. Causa Confirmada\n").bold = True
q12.add_run("Respuesta e interpretación: ").bold = True
q12.add_run(
    "La evidencia cuantitativa demuestra dos fenómenos operativos completamente distintos: "
    "(1) Prefijo 'C' (19,494 líneas): Devoluciones o cancelaciones comerciales legítimas de clientes, con precios vigentes y clientes identificados. "
    "(2) Negativos sin 'C' (3,457 líneas): Mermas internas de almacén, productos dañados, extravíos y desajustes de conteo físico. El 100% tiene precio cero y cliente nulo. "
    "Conclusión definitiva: No todo registro negativo puede interpretarse como una devolución de venta. Tratar las mermas como cancelaciones comerciales contaminaría gravemente las tasas de devolución y los modelos de retención de clientes."
)

doc.add_paragraph()

# 5.C Contingency Matrix
t10 = doc.add_table(rows=4, cols=5)
t10.rows[0].cells[0].paragraphs[0].add_run("Prefijo de Invoice")
t10.rows[0].cells[1].paragraphs[0].add_run("Quantity < 0")
t10.rows[0].cells[2].paragraphs[0].add_run("Quantity = 0")
t10.rows[0].cells[3].paragraphs[0].add_run("Quantity > 0")
t10.rows[0].cells[4].paragraphs[0].add_run("Total Fila")
data_t10 = [
    ("Con C", "19,493", "0", "1", "19,494"),
    ("Sin C", "3,457", "0", "1,044,420", "1,047,877"),
    ("Total Columna", "22,950", "0", "1,044,421", "1,067,371")
]
for idx, (pref, qn, qz, qp, tot) in enumerate(data_t10, start=1):
    t10.rows[idx].cells[0].paragraphs[0].add_run(pref)
    t10.rows[idx].cells[1].paragraphs[0].add_run(qn)
    t10.rows[idx].cells[2].paragraphs[0].add_run(qz)
    t10.rows[idx].cells[3].paragraphs[0].add_run(qp)
    t10.rows[idx].cells[4].paragraphs[0].add_run(tot)
format_table(t10, [1.5, 1.2, 1.2, 1.3, 1.3])

doc.add_paragraph()

# Question 13
q13 = doc.add_paragraph()
q13.add_run("13. Cruce de Conjuntos: Prefijo C vs. Signo de Quantity\n").bold = True
q13.add_run("Respuesta e interpretación: ").bold = True
q13.add_run(
    "Las líneas con prefijo C no coinciden exactamente con las cantidades negativas: de 22,950 líneas negativas, 19,493 tienen C y 3,457 no la tienen (15.06% de los negativos ocurren fuera de la serie C). "
    "Además, existe exactamente 1 línea con prefijo C y cantidad positiva: Factura C496350, StockCode 'M' ('Manual'), Quantity +1, Price £373.57, Customer ID NaN. "
    "Esta anomalía requiere tratamiento específico: parece ser un cobro manual o cargo administrativo registrado bajo una serie de cancelación. No debe invertirse a venta ni restarse como reembolso."
)

# ----------------- SECTION 6 -----------------
doc.add_heading("6. Plan de Acción y Evaluación", level=1)

t11 = doc.add_table(rows=6, cols=4)
t11.rows[0].cells[0].paragraphs[0].add_run("Problema identificado")
t11.rows[0].cells[1].paragraphs[0].add_run("Evidencia")
t11.rows[0].cells[2].paragraphs[0].add_run("Posible impacto empresarial")
t11.rows[0].cells[3].paragraphs[0].add_run("Tratamiento propuesto")
data_t11 = [
    ("Valores nulos en Customer ID", "243,007 líneas (22.77% del archivo). Ejemplo: Invoice 489435.", "Sesgo en CLV y segmentación; perderlas descarta 22.8% del flujo transaccional.", "Bifurcación de pipeline: aislar cuentas completas para CLV/churn; retener compras anónimas como demanda base agregada para inventario."),
    ("Duplicados exactos adicionales", "34,335 líneas adicionales (3.22%). Ejemplo: Factura 489517 duplica 21491 a las 11:34:00.", "Sobrestimación artificial de ingresos (£), unidades vendidas y frecuencia de compra.", "Deduplicar con drop_duplicates(keep='first'). Auditar reintentos de pago HTTP en pasarela web."),
    ("Cantidades negativas sin prefijo C", "3,457 líneas (0.32%), 100% Price=0 y Customer ID nulo ('damages', 'check').", "Confusión entre merma física de bodega y cancelaciones de clientes.", "Segregación operativa: canalizar a un módulo de merma de almacén; excluir del historial de ventas a clientes."),
    ("Precios no positivos (Price <= 0)", "5 líneas con Price < 0 ('Adjust bad debt', hasta -£53,594.36); 6,202 con Price = 0.", "Distorsión masiva de ingresos y margen bruto por asientos de deuda incobrable.", "Excluir asientos contables (prefijo 'A') de ventas retail. Auditar registros en cero para muestras promocionales."),
    ("Cancelaciones comerciales (Prefijo C)", "19,494 líneas (1.83%), 19,493 con Quantity < 0 y 1 con Quantity > 0 (C496350).", "Cálculo erróneo de ingresos brutos si no se concilian con la venta original.", "Conciliar cancelaciones con facturas de venta originales para calcular ingresos netos y tasa de devolución individual.")
]
for idx, (p, ev, imp, tr) in enumerate(data_t11, start=1):
    t11.rows[idx].cells[0].paragraphs[0].add_run(p)
    t11.rows[idx].cells[1].paragraphs[0].add_run(ev)
    t11.rows[idx].cells[2].paragraphs[0].add_run(imp)
    t11.rows[idx].cells[3].paragraphs[0].add_run(tr)
format_table(t11, [1.6, 1.6, 1.6, 1.7])

doc.add_paragraph()

# Question 14
q14 = doc.add_paragraph()
q14.add_run("14. Prioridad de Preparación y Riesgo Residual (100 a 150 palabras)\n").bold = True
q14.add_run("Prioridad y justificación: ").bold = True
q14.add_run(
    "La prioridad inmediata es la bifurcación del pipeline respecto a los valores nulos en Customer ID (243,007 líneas, 22.77%) y la exclusión de precios no positivos (6,207 líneas). "
    "Intentar entrenar modelos de Valor de Vida del Cliente (CLV) o riesgo de cancelación sobre registros anónimos corrompería fatalmente la agregación por cliente, mientras que las partidas contables de deuda incobrable (-£53,594.36 en A506401) distorsionan la escala monetaria. "
    "Debemos separar la ingeniería de datos: clientes con ID completo alimentarán los algoritmos de CRM, mientras que las ventas anónimas se preservan como demanda base para reabastecimiento de inventario. "
    "Riesgo residual persistente: la presencia de compradores mayoristas B2B en la cohorte identificada. Sus patrones masivos e irregulares de compra pueden sesgar los modelos de clientes minoristas, y sin datos de márgenes o costos de envío, las predicciones quedan expuestas a variaciones bruscas de pedidos al por mayor."
)

doc.add_heading("Referencias", level=1)
doc.add_paragraph(
    "• Chen, D. (2012). Online Retail II [Conjunto de datos]. UCI Machine Learning Repository. https://doi.org/10.24432/C5CG6D\n"
    "• Caso de Estudio North Quay Gifts. Material docente UPY.\n"
    "• ResearchGate (2025). Forecasting Customer Lifetime Value: A Data-Driven Approach to Optimizing Marketing Budget Allocation.\n"
    "• ResearchGate (2015). Predicting Product Returns in E-Commerce: The Contribution of Mahalanobis Feature Extraction.\n"
    "• Tukey, J. W. (1977). Exploratory Data Analysis. Addison-Wesley."
)

out_path = "A-3-3_DataUnderstanding/Actividad 1. Entendimiento y Exploración de Datos.docx"
doc.save(out_path)
print(f"Document successfully created at {out_path} ({os.path.getsize(out_path):,} bytes).")
