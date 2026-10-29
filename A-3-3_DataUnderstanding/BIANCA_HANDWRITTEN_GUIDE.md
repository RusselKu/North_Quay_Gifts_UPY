# Detailed Handwritten Guide for Learning Activity 1: Data Understanding
**Target Audience / Role:** Instructions & exact text for Bianca Alexandra Acosta Castellanos to copy/write down into the physical/editable evaluation deliverable.  
**Course:** Data Mining / Advanced Data Science — Faculty of Data Engineering, Universidad Politécnica de Yucatán (UPY)  
**Project:** North Quay Gifts — CRISP-DM Phase 2: Data Understanding  
**Advisor / Professor:** Didier Omar Gamboa Angulo (`didier.gamboa@upy.edu.mx`)  
**Team Members:**
- Russel Emmanuel Ku Aguilar (ID: 2309131)
- Damian Nicolas Sanchez Novelo (ID: 2109134)
- Jonathan Abisai Velasco Martín (ID: 2309060)
- Ángel Rivaldo Canché Chuc (ID: 2309030)
- Bianca Alexandra Acosta Castellanos (ID: 2309001)

---

## Cover Information (Información de Portada)
- **Equipo o participante:** Russel Ku, Damian Sanchez, Jonathan Velasco, Ángel Canché, Bianca Acosta
- **Fecha de entrega:** October 2026

---

## 1. Data Recognition (Reconocimiento de los Datos)

### Table 1: Dataset Indicators (Indicador / Resultado)
Fill the first table on Page 2 with these exact verified figures:

| Indicator (Indicador) | Result (Resultado) | Notes for Writing |
| :--- | :--- | :--- |
| **Número de líneas y columnas** | `1,067,371 filas × 8 columnas` | Write both rows and columns clearly. |
| **Primera y última fecha con hora** | `2009-12-01 07:45:00` a `2011-12-09 12:50:00` | State exact timestamps from parsed datetime. |
| **Facturas distintas y clientes identificados distintos** | `53,628 facturas distintas` \| `5,942 clientes identificados distintos` | Clarify that missing IDs do not count as a customer. |
| **Unidad representada por una fila** | `Línea individual de producto/ítem dentro de una factura comercial` | It is a transaction item line, NOT a whole order. |

---

### Table 2: Analytical Classification of Variables (Clasificación de Variables)
Fill the second table on Page 2 with the 8 columns:

| Column (Columna) | Type in Pandas (Tipo en Pandas) | Function & Meaning (Función y Significado) |
| :--- | :--- | :--- |
| **Invoice** | `object` / `string` | **Nominal Identifier (Identificador nominal):** Unique transaction alphanumeric code. Prefix 'C' indicates a commercial cancellation/cancellation transaction. |
| **StockCode** | `object` / `string` | **Nominal Alphanumeric (Alfanumérico nominal):** Unique SKU / catalog identifier of an item or service surcharge (e.g. POST, D, M, B). |
| **Description** | `object` / `string` | **Qualitative Textual (Cualitativa textual):** Commercial name of the merchandise, or internal operational memo (e.g. damages, audit checks). |
| **Quantity** | `int64` | **Quantitative Discrete (Cuantitativa discreta):** Number of merchandise units billed. Negative quantities represent transaction cancellations or stock adjustments. |
| **InvoiceDate** | `datetime64[ns]` (or `object`) | **Temporal / Chronological (Temporal / cronológica):** Exact timestamp representing when the transaction was generated. |
| **Price** | `float64` | **Quantitative Continuous (Cuantitativa continua):** Unit product price expressed in British Pounds Sterling (GBP, £). |
| **Customer ID** | `float64` | **Nominal Identifier (Identificador nominal):** Unique client identifier key. Floating-point format due to missing (NaN) values for unregistered/walk-in buyers. |
| **Country** | `object` / `string` | **Qualitative Categorical Nominal (Cualitativa nominal):** Country of the customer's billing or shipping address. |

---

### Question 1 (Pregunta 1)
**Prompt:** *Selecciona una factura con varios productos. Reporta su identificador, número de líneas y número de StockCode distintos. ¿Por qué esos conteos pueden diferir? ¿Por qué el total de filas no equivale al número de pedidos?*

**Exact Text to Write (Respuesta e interpretación):**
> "We analyzed invoice **489517** (dated 2009-12-01 11:34:00, Customer ID 16329.0). This single invoice contains **38 total lines** but only **28 distinct StockCodes**. 
> The counts differ because identical products were registered across multiple separate rows within the same transaction (e.g., StockCodes `21491`, `21821`, and `21912` each appear twice at the exact same minute). This occurs when customers add items at different stages of basket building or when e-commerce systems record duplicate line items rather than aggregating quantities into a single record.
> Consequently, the total row count (1,067,371) does not equal the number of orders (53,628). Each row represents an individual line item of merchandise, not an entire order entity. Equating rows to orders would catastrophically inflate order frequency by a factor of 19.9×."

---

### Question 2 (Pregunta 2)
**Prompt:** *Explica por qué el promedio de Customer ID o de un código de producto no describe el comportamiento de compra. ¿Qué diferencia existe entre el tipo de almacenamiento y el significado de una columna?*

**Exact Text to Write (Respuesta e interpretación):**
> "Calculating the mean of `Customer ID` (e.g., 15555.57) or a numeric product code is methodologically invalid because these variables possess **strictly nominal measurement scales**. Numbers here act purely as qualitative surrogate keys to differentiate entities, not as quantities expressing scale, magnitude, or distance. Averaging customer IDs produces a nonsensical number that corresponds to no real individual and conveys zero behavioral information.
> This demonstrates the critical distinction between **storage type** (how the data is physically allocated in memory, such as `float64` or `int64`) and **analytical meaning** (the semantic interpretation and allowable mathematical operations under Stevens' scales of measurement). Storing an ID as a float allows fast vector indexing and NaN handling, but does not grant mathematical legitimacy to arithmetic operations."

---

### Question 3 (Pregunta 3)
**Prompt:** *¿El primer y el último mes están completos? Explica qué restricción introduce la cobertura observada al comparar periodos.*

**Exact Text to Write (Respuesta e interpretación):**
> "Neither the first nor the final month contains complete chronological coverage:
> 1. **First month (December 2009):** Data begins on 2009-12-01 at 07:45:00 and terminates on 2009-12-23 at 16:58:00 (covering 21 active days), truncating the peak post-Christmas and boxing-day shopping week.
> 2. **Final month (December 2011):** Data terminates abruptly on 2011-12-09 at 12:50:00 (covering only 8 active days; 25,526 lines compared to 84,711 in November 2011).
> **Analytical Restriction:** Direct period-to-period or year-over-year comparisons (such as comparing total December 2010 with December 2009 or 2011) will introduce severe artificial contraction bias unless metrics are normalized by active trading days, annualized, or truncated to identical date windows (e.g., Dec 1–Dec 9)."

---

## 2. Descriptive Statistics (Estadística Descriptiva)

### Table 3: Summary of Quantitative Measures (Quantity & Price)
Fill the numerical table on Page 3 with these exact empirical values:

| Statistic (Estadístico) | Quantity (unidades) | Price (GBP £ por unidad) |
| :--- | :--- | :--- |
| **Observaciones no nulas** | `1,067,371` | `1,067,371` |
| **Media** | `9.9389` | `4.6494` |
| **Mediana** | `3.0000` | `2.1000` |
| **Desviación estándar** | `172.7058` | `123.5531` |
| **Mínimo** | `-80,995` | `-53,594.36` |
| **Primer cuartil (Q1 - 25%)** | `1.0000` | `1.2500` |
| **Tercer cuartil (Q3 - 75%)** | `10.0000` | `4.1500` |
| **Máximo** | `80,995` | `38,970.00` |
| **Asimetría (Skewness)** | `3.9961` | `-69.1647` |
| **Curtosis (Fisher Excess)** | `155,059.71` | `73,751.83` |

*Note for Bianca:* State explicitly that kurtosis uses **Fisher's definition (excess kurtosis relative to normal distribution = 0)**.

---

### Table 4: Summary of Categorical Variables (Country & StockCode)
Fill the categorical table on Page 3:

| Variable | Presentes | Distintos | Categoría más frecuente y líneas |
| :--- | :--- | :--- | :--- |
| **Country** | `1,067,371` | `43` | `United Kingdom (981,330 líneas, 91.94%)` |
| **StockCode** | `1,067,371` | `5,305` | `85123A (5,829 líneas, 0.55%)` |

*Note on Nulls:* Neither variable contains nulls in raw storage (`0` nulls).

---

### Question 4 (Pregunta 4)
**Prompt:** *Compara media y mediana de cada medida. Relaciona las diferencias con la asimetría y con los extremos observados; evita afirmar que una media representa una compra típica sin justificarlo.*

**Exact Text to Write (Respuesta e interpretación):**
> "For `Quantity`, the mean is **9.94 units**, whereas the median is **3.00 units** (Q1=1, Q3=10). The mean is 3.3× larger than the median, driven by positive skewness (3.996) and massive wholesale batch purchases of up to +80,995 units.
> For `Price`, the mean is **£4.65**, whereas the median is **£2.10** (Q1=£1.25, Q3=£4.15). The price exhibits negative skewness (-69.16) primarily due to extreme negative accounting write-offs (-£53,594.36).
> Under such heavy skewness and astronomical excess kurtosis (>70,000), the arithmetic mean **does not represent a typical purchase**. The mean is heavily distorted by extreme outliers. The median and interquartile range (IQR) provide the only robust measure of central tendency: a typical retail transaction line consists of 1 to 10 units of an item priced between £1.25 and £4.15."

---

### Question 5 (Pregunta 5)
**Prompt:** *¿Qué sugieren los mínimos y máximos de Quantity y Price? Distingue lo que muestran los datos de una explicación que necesitaría confirmación empresarial.*

**Exact Text to Write (Respuesta e interpretación):**
> "The extremes reveal massive operational anomalies:
> 1. `Quantity`: Min is **-80,995** and Max is **+80,995** (StockCode `23843`, Paper Craft Little Star). The data shows an exact symmetrical cancellation canceling out an enormous order. Hypotheses: Wholesale bulk order canceled due to stockout or credit failure. Requires confirmation with Sales & Warehouse logistics.
> 2. `Price`: Min is **-£53,594.36** (Invoice `A506401`, StockCode `B`, 'Adjust bad debt') and Max is **£38,970.00** (manual fee). The data reveals that non-merchandise bookkeeping adjustments are injected into the sales table. Hypothesis: Corporate accountants manually wrote off uncollectible debt. This requires formal confirmation with the Finance department."

---

### Question 6 (Pregunta 6)
**Prompt:** *¿Dónde observas mayor dispersión? Sustenta tu respuesta con cuartiles y desviación estándar dentro de cada variable. Quantity y Price tienen unidades distintas: no compares sus desviaciones como si midieran lo mismo. ¿Cómo pueden los extremos afectar sus promedios?*

**Exact Text to Write (Respuesta e interpretación):**
> "Because `Quantity` (units) and `Price` (GBP £) use different scales, comparing standard deviations directly is invalid. Instead, we evaluate dispersion using the **Interquartile Range (IQR)** and the non-parametric dispersion relative to the median:
> - For `Quantity`: Median = 3, IQR = 9 (Q1=1, Q3=10). Relative IQR dispersion = 9 / 3 = **300%**. Standard deviation is 172.71 units (17.4× the mean).
> - For `Price`: Median = £2.10, IQR = £2.90 (Q1=£1.25, Q3=£4.15). Relative IQR dispersion = 2.90 / 2.10 = **138%**. Standard deviation is £123.55 (26.6× the mean).
> **Conclusion:** `Quantity` exhibits substantially wider relative dispersion across normal trading, reflecting North Quay's dual customer base of individual gift shoppers (1–3 units) alongside bulk wholesalers purchasing hundreds of items. Extreme values distort the sample means by pulling them far away from 75% of the observed population."

---

## 3. Univariate Analysis (Análisis Univariado)

### Visualizations Insertion Notes (Figuras 1 a 6)
- **Figuras 1 y 2:** Insert plots from `figures/fig1_quantity_hist.png` and `figures/fig2_price_hist.png`.
- **Figuras 3 y 4:** Insert plots from `figures/fig3_country_bar.png` and `figures/fig4_stockcode_bar.png`.
- **Figuras 5 y 6:** Insert boxplots from `figures/fig5_quantity_boxplot.png` and `figures/fig6_price_boxplot.png`.

---

### Question 7 (Pregunta 7)
**Prompt:** *Describe dónde se concentra cada distribución, su asimetría y la presencia de valores negativos o extremos. Cita al menos un estadístico que respalde la lectura de cada histograma.*

**Exact Text to Write (Respuesta e interpretación):**
> "The histograms demonstrate extreme leptokurtic concentration around low positive values:
> - **Quantity (Figure 1):** Over **95.53%** of all transactions fall between 1 and 50 units (median = 3, mode = 1). The zoomed window `[-50, 100]` contains **98.84%** of the entire dataset (only 1.16% lies outside). The distribution displays a heavy right-hand tail of wholesale volumes and a discrete negative tail representing cancellations and warehouse stock-outs.
> - **Price (Figure 2):** Over **98.17%** of records fall between £0.00 and £15.00 GBP, with a sharp spike at £1.25–£2.50 (median = £2.10). The zoomed window `[£0.00, £25.00]` encloses **99.39%** of observations (only 0.61% outside). Extreme spikes at negative values correspond to isolated accounting adjustments (`Adjust bad debt`)."

---

### Table 5: Three Most Frequent Categories (Country & StockCode)
Fill the table on Page 4:

| Variable | Distinct Categories (Categorías distintas) | Three Most Frequent with Lines and Percentage (Tres categorías con líneas y porcentaje) |
| :--- | :--- | :--- |
| **Country** | `43` | 1. **United Kingdom:** 981,330 lines (`91.94%`)<br>2. **EIRE (Ireland):** 17,866 lines (`1.67%`)<br>3. **Germany:** 17,624 lines (`1.65%`) |
| **StockCode** | `5,305` | 1. **85123A** (White Hanging Heart T-Light Holder): 5,829 lines (`0.55%`)<br>2. **22423** (Regency Cakestand 3 Tier): 4,424 lines (`0.41%`)<br>3. **85099B** (Jumbo Bag Red Retrospot): 4,216 lines (`0.39%`) |

*Coverage of Top 10:*
- Country Top 10 covers `1,050,946 lines` (**98.46%**).
- StockCode Top 10 covers `34,610 lines` (**3.24%**).

---

### Question 8 (Pregunta 8)
**Prompt:** *¿Qué concentración o diversidad muestran las frecuencias? ¿Por qué el país o producto con más líneas no necesariamente tiene más pedidos, unidades o ingresos?*

**Exact Text to Write (Respuesta e interpretación):**
> "`Country` exhibits **extreme geographic concentration**, with the UK capturing 91.94% of all lines, followed distantly by EIRE (1.67%) and Germany (1.65%). In contrast, `StockCode` shows **high catalog diversity**: the most popular SKU (`85123A`) accounts for only 0.55% of lines, and the entire top 10 products represent just 3.24% of records.
> A higher line count does not directly imply greater revenue, units, or orders because:
> 1. A low-cost impulse novelty item (e.g., £0.42 keychains) can appear on thousands of invoices with 1 unit each, yielding low total revenue.
> 2. Conversely, a high-value item (e.g., £12.75 cakestands) sold in wholesale lots of 100 units generates vastly superior gross revenue despite having fewer transaction lines."

---

### Question 9 (Pregunta 9)
**Prompt:** *Interpreta mediana, rango intercuartílico y puntos fuera de los bigotes. Indica la regla usada por tu gráfico. Explica por qué un punto atípico no basta para declarar un registro erróneo y relaciona tus conclusiones con los histogramas.*

**Exact Text to Write (Respuesta e interpretación):**
> "The boxplots employ **Tukey's standard rule**: whiskers extend to $1.5 \times \text{IQR}$ beyond $Q_1$ and $Q_3$:
> - For `Quantity`: $Q_1 = 1$, $Q_3 = 10$, $\text{IQR} = 9$. Upper whisker ends at $10 + 1.5(9) = 23.5 \approx 23$ units. All values $> 23$ or $< -12$ are flagged as outliers.
> - For `Price`: $Q_1 = £1.25$, $Q_3 = £4.15$, $\text{IQR} = £2.90$. Upper whisker ends at $£4.15 + 1.5(£2.90) = £8.50$.
> A mathematical outlier **is not automatically an error**. In B2B retail, legitimate wholesale buyers routinely purchase 100–500 units in bulk, which are genuine, valid commercial sales. True errors or accounting entries are distinguished not by outlier status alone, but by contextual semantic anomalies (e.g., missing Customer ID, negative price, 'Adjust bad debt' description)."

---

## 4. Data Quality Diagnostics (Diagnóstico de Calidad de Datos)

### Table 6: Missing Values per Column (Valores Nulos)
Fill the nulls table on Page 5. **Denominator for all 8 columns: 1,067,371 lines**:

| Column (Columna) | Nulls (Nulos) | Percentage of Total (Porcentaje sobre el total) |
| :--- | :--- | :--- |
| **Invoice** | `0` | `0.0000%` |
| **StockCode** | `0` | `0.0000%` |
| **Description** | `4,382` | `0.4105%` |
| **Quantity** | `0` | `0.0000%` |
| **InvoiceDate** | `0` | `0.0000%` |
| **Price** | `0` | `0.0000%` |
| **Customer ID** | `243,007` | `22.7669%` |
| **Country** | `0` | `0.0000%` |

---

### Table 7: Anomalous Situations (Situaciones Anómalas)
Fill the situations table on Page 5:

| Situation (Situación) | Lines (Líneas) | Percentage of Total (Porcentaje sobre el total) |
| :--- | :--- | :--- |
| **Duplicados exactos adicionales** | `34,335` | `3.2168%` |
| **Quantity < 0** | `22,950` | `2.1501%` |
| **Quantity = 0** | `0` | `0.0000%` |
| **Price < 0** | `5` | `0.0005%` |
| **Price = 0** | `6,202` | `0.5811%` |

---

### Question 10 (Pregunta 10)
**Prompt:** *¿Qué análisis de clientes se limitan por la falta de Customer ID? ¿Por qué esas mismas líneas todavía podrían ser útiles para estudiar actividad comercial global?*

**Exact Text to Write (Respuesta e interpretación):**
> "The absence of `Customer ID` in **243,007 lines (22.77%)** directly prevents:
> 1. Calculating customer-level behavioral metrics: Recency, Frequency, Monetary Value (RFM), Customer Lifetime Value (CLV), churn prediction, and repeat purchase loyalty.
> 2. Developing individualized customer return rate models.
> However, these records **remain highly valuable for macro-commercial analysis**:
> They reflect genuine retail revenue and inventory turnover. Retaining them enables store-wide demand forecasting, warehouse replenishment planning, seasonal velocity analysis, and product affinity (market basket) modeling across the entire business catalog."

---

### Question 11 (Pregunta 11)
**Prompt:** *Examina al menos dos ejemplos de duplicados o de precios no positivos. Registra Invoice, StockCode, Quantity, Price y Description en la libreta. ¿Qué evidencia permite describirlos y qué información faltaría para decidir si deben excluirse?*

**Exact Text to Write (Respuesta e interpretación):**
> "We inspected specific cases in the notebook:
> 1. **Exact Duplicate Example:** Invoice `489517`, StockCode `21491` ('MINI PAINT SET VINTAGE'), Quantity `6`, Price `£0.65`, Customer ID `16329.0`, Timestamp `2009-12-01 11:34:00`. The identical item, price, quantity, and customer are duplicated in row 379 and row 391. Evidence: identical timestamps indicate redundant network clicks. Missing info: e-commerce session logs or warehouse fulfillment receipts to confirm whether 6 or 12 physical units were shipped.
> 2. **Negative Price Example:** Invoice `A506401`, StockCode `B`, Quantity `1`, Price **-£53,594.36**, Description 'Adjust bad debt', Customer ID `NaN`. Evidence: Prefix 'A' and description denote non-merchandise bookkeeping write-offs. Missing info: corporate chart of accounts to confirm if these were audited by external finance."

---

### Other Findings (Otros Hallazgos con Evidencia)
**Text to Write:**
> - Non-product administrative codes: `POST` (postage fees, 1,983 lines), `D` (discount, 214 lines), `M` (manual fees, 939 lines), `BANK CHARGES` (110 lines).
> - Records with Price = £0.00 (6,202 lines): 98.8% lack Customer ID and contain warehouse audit descriptions such as `'check'` (162 lines), `'damages'` (84 lines), `'damaged'` (81 lines), `'found'` (28 lines).
> - Date parsing: 100% of dates parsed successfully with zero invalid timestamp formats.

---

## 5. Investigation of Cancellations & Negative Quantities

### 5.A: Invoices with Prefix 'C' (Facturas con Prefijo C)
Fill Table 5.A on Page 6:

| Indicator (Indicador) | Result (Resultado) |
| :--- | :--- |
| **Líneas con prefijo C** | `19,494` |
| **Facturas C distintas** | `8,292` |
| **Líneas C con Quantity < 0** | `19,493` |
| **Líneas C con Quantity = 0** | `0` |
| **Líneas C con Quantity > 0** | `1` |

*Note on the anomaly:* Invoice `C496350`, StockCode `M`, Description `'Manual'`, Quantity `+1`, Price `£373.57`.

---

### 5.B: Negative Quantities Without Prefix 'C' (Cantidades Negativas sin Prefijo C)
Fill Table 5.B on Page 6:

| Negative Lines without C (Líneas negativas sin C) | Distinct Invoices (Facturas distintas) | Findings in Prices & Customers (Hallazgos en precios y clientes) |
| :--- | :--- | :--- |
| `3,457` | `3,393` | **100% have Price = £0.00 (3,457 lines). 100% have Customer ID = NaN (0 customers).** Descriptions are internal notes: *check* (123), *damages* (84), *?* (83), *damaged* (78), *missing* (27), *sold as set on dotcom* (20), *smashed* (9), *thrown away* (9). |

---

### Question 12 (Pregunta 12)
**Prompt:** *¿Qué explicaciones son compatibles con las descripciones observadas, como ajustes, daños o devoluciones? Distingue esas hipótesis de una causa confirmada. ¿Se puede interpretar cualquier negativo como una devolución de venta?*

**Exact Text to Write (Respuesta e interpretación):**
> "The evidence reveals two completely separate operational phenomena:
> 1. **Prefix 'C' (19,494 lines):** These are genuine commercial order cancellations or customer product returns. They contain active prices and valid Customer IDs.
> 2. **Negative Quantities without 'C' (3,457 lines):** These represent **internal warehouse inventory adjustments and write-offs** (breakage, defective units, lost inventory, cycle-count reconciliations). Every single one has Price = 0 and no customer.
> **Definitive Conclusion:** Negative quantities **cannot** be universally treated as customer sales returns. Treating warehouse breakage as customer churn would severely bias reverse logistics rates and falsely distort customer cancellation behavior."

---

### 5.C: Set Comparison: Contingency Matrix (Comparación de Conjuntos)
Fill the 2×3 table on Page 6. **Grand Total must equal 1,067,371 lines**:

| Invoice Prefix (Prefijo) | Quantity < 0 | Quantity = 0 | Quantity > 0 | Total Row (Total Fila) |
| :--- | :--- | :--- | :--- | :--- |
| **Con C (With C)** | `19,493` | `0` | `1` | `19,494` |
| **Sin C (Without C)** | `3,457` | `0` | `1,044,420` | `1,047,877` |
| **Total Column (Total Columna)** | `22,950` | `0` | `1,044,421` | **`1,067,371`** |

---

### Question 13 (Pregunta 13)
**Prompt:** *¿Coinciden exactamente las líneas C con las cantidades negativas? Sustenta la respuesta con las celdas de la tabla. Si encuentras líneas C con cantidad positiva o cero, inspecciónalas en la libreta y explica por qué requieren revisión específica.*

**Exact Text to Write (Respuesta e interpretación):**
> "Lines with prefix 'C' **do not match** negative quantities exactly:
> - Of 22,950 total negative rows, 19,493 have prefix 'C' and 3,457 do not.
> - Furthermore, exactly **1 row** has prefix 'C' but a **positive quantity**: Invoice `C496350`, StockCode `M` ('Manual'), Quantity `+1`, Price `£373.57`, Customer ID `NaN`.
> This outlier requires specific intervention: it appears to be a manual debit correction or administrative fee billed under a cancellation invoice header. It must not be inverted into a sale nor counted as a negative refund."

---

## 6. Action Plan & Evaluation (Plan de Acción y Evaluación)

### Table 8: Strategic Action Plan Matrix (Plan de Acción)
Fill the comprehensive table on Page 7:

| Identified Problem (Problema) | Evidence (Evidencia) | Potential Business Impact (Impacto empresarial) | Proposed Treatment (Tratamiento propuesto) |
| :--- | :--- | :--- | :--- |
| **Missing Customer IDs** | 243,007 lines (22.77% of dataset). Example: Invoice 489435. | Cannot model CLV or retention for anonymous buyers; losing them drops 22.8% of volume. | **Segment analytical pipelines:** Filter out missing IDs for customer CLV/churn modeling; retain in an independent aggregate baseline for inventory forecasting. |
| **Exact Duplicate Rows** | 34,335 additional lines (3.22%). Example: Invoice 489517 duplicates items 21491, 21821. | Artificial inflation of billed revenue, merchandise volume, and transaction frequency. | Deduplicate using `df.drop_duplicates(keep='first')`. Request IT gateway audit to verify checkout double-clicks. |
| **Negative Quantities without 'C'** | 3,457 lines (0.32%), 100% have Price=0 and Customer ID=NaN (damages, check, thrown away). | Conflating inventory shrinkage with customer returns distorts return rate models. | Segregate entirely from sales tables into an internal Warehouse Shrinkage / Operational Loss dataset. |
| **Non-Positive Prices (Price <= 0)** | 5 lines with Price < 0 (StockCode 'B', 'Adjust bad debt', -£53,594.36); 6,202 lines with Price = 0. | Catastrophic distortion of gross margin and revenue; negative bad debts erase millions. | Exclude bad debt rows ('A' invoices) permanently from commercial sales. Audit zero-price lines for promotional gifts vs data omissions. |
| **Commercial Cancellations ('C')** | 19,494 lines (1.83%), 19,493 with Quantity < 0 and 1 with Quantity > 0 (C496350). | Skews gross revenue calculation if returns are not matched to original purchases. | Conciliate cancellation lines with original sales invoices to construct net customer spend and historical return rates. |

---

### Question 14 (Pregunta 14) — Priority and Justification (100–150 words)
**Prompt:** *¿Qué decisión de preparación atenderías primero y por qué? Responde en 100 a 150 palabras, con referencia a los conteos y casos del reporte. Explica qué riesgo persistiría aun después del tratamiento propuesto.*

**Exact Text to Write (Prioridad y justificación - 138 words):**
> "The most urgent data preparation priority is the **bifurcation and handling of missing Customer IDs (243,007 lines, 22.77%) alongside non-positive prices (6,207 lines)**. Attempting to train customer lifetime value (CLV) or churn models on anonymous purchases would fatally corrupt customer profile aggregation, while bad-debt write-offs (-£53,594.36 in Invoice A506401) distort revenue scaling. We must split the data pipeline: isolate complete customer histories for CRM modeling while preserving anonymous lines as baseline demand for inventory replenishment.
> 
> However, even after filtering, a major **residual risk persists**: unobserved B2B wholesale transaction dynamics. The remaining data contains wholesale buyers purchasing thousands of units whose irregular ordering cycles can overwhelm retail predictions. Without contractual margins or customer demographic metadata, models remain vulnerable to sudden wholesale order swings."

---

## References (Referencias)
- Chen, D. (2012). *Online Retail II* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5CG6D
- North Quay Gifts Case Study. UPY Course Material.
- ResearchGate (2025). *Forecasting Customer Lifetime Value: A Data-Driven Approach*.
- ResearchGate (2015). *Predicting Product Returns in E-Commerce*.
