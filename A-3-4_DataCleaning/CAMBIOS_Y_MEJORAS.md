# Fase A-3-4: Preparación y Procesamiento de Datos (Data Cleaning & Processing)
## Registro de Actualizaciones, Conciliación Bidireccional de Abonos y Bifurcación del Pipeline

**Proyecto:** North Quay Gifts — CRISP-DM Fase 3: Data Preparation (`A-3-4_DataCleaning`)  
**Dataset Original:** `online_retail_II.csv` (`1,067,371` filas × `8` columnas)  
**Base Común Deduplicada:** `1,033,036` líneas únicas (`34,335` duplicados exactos adicionales excluidos)  
**Fecha de Actualización:** Noviembre 2026  
**Equipo:**
- Russel Emmanuel Ku Aguilar (ID: 2309131)
- Damian Nicolas Sanchez Novelo (ID: 2109134)
- Jonathan Abisai Velasco Martín (ID: 2309060)
- Ángel Rivaldo Canché Chuc (ID: 2309030)
- Bianca Alexandra Acosta Castellanos (ID: 2309001)

**Docente Asesor:** Didier Omar Gamboa Angulo (`didier.gamboa@upy.edu.mx`)  

---

### 1. Resumen Ejecutivo de la Intervención
En esta revisión integral de la **Fase A-3-4 (Data Preparation and Processing)** se elevó el rigor técnico y metodológico del cuaderno oficial `NB3 Data Preparation and Processing - Online Retail II.ipynb`, subsanando las limitaciones del algoritmo de conciliación previo e integrando los dos hallazgos críticos descubiertos en la fase `A-3-3`:
1. **Conciliación Temporal Bidireccional de Abonos (`'C'`) y Netting de Re-facturaciones ("Salía la verdadera después"):** Se demostró y corrigió el sesgo del algoritmo unidireccional hacia atrás (`compra < abono`), el cual clasificaba falsamente `2,060` líneas como *"Unreconciled: No earlier purchase of the product by the customer"*. Al incorporar la búsqueda hacia adelante (`abono <= compra_posterior`), se identificó que **586 de esas 2,060 líneas (28.45%)** corresponden a re-facturaciones donde la factura positiva definitiva se emitió *después* de la anulación (`168` en `< 24` horas), mientras que **1,474 líneas** en la base deduplicada (**1,484 líneas** en el archivo bruto antes de eliminar `10` duplicados exactos) son devoluciones huérfanas legítimas por censura a la izquierda (compras previas al 1 de diciembre de 2009 o devoluciones de mostrador). En toda la población de `18,390` abonos `'C'` con cliente de la Ruta B (`16,916` apareados con compras), **7,151 líneas (42.27%)** (`7,062` líneas / `41.96%` en el análisis bruto de A-3-3) presentan una compra positiva posterior, incluyendo **1,499 líneas (`1,397` en base bruta) de correcciones en caliente en `< 24` horas** (`1,181` en $\le 60$ minutos).
2. **Aislamiento Contable, Bifurcación del Pipeline y Proxies de Atribución de Marketing:** Se aislaron formalmente las **3,457 líneas brutas (`3,393` deduplicadas)** de merma física de almacén (`Quantity < 0` sin prefijo `'C'`, `100% Price = £0.00` y `CustomerID = <NA>`) y los **6 asientos contables de deuda incobrable serie `'A'`** (`5` con precio negativo hasta `-£53,594.36` en `A506401`, excluidos por `Price <= 0`, y `1` asiento compensatorio `A563185` de `+£11,062.06` marcado como no mercantil). Asimismo, para mitigar la ceguera de atribución de marketing (`0` variables UTM), se bifurcó la Ruta B (`1,027,016` líneas) en el **Repositorio CRM de Clientes Identificados** (`797,815` líneas) y el **Repositorio de Demanda Anónima Web/Mostrador** (`229,201` líneas, de las cuales el **90.10% [`206,506` líneas]** pertenecen a facturas con `StockCode == 'DOT'` de la tienda online *Dotcom*), construyendo las variables proxy `CohortMonth`, `IsUK`, `DOTCOM_OrderFlag`, `AMAZON_OrderFlag` y `DISCOUNT_UserFlag`.

---

### 2. Control de Trazabilidad e Integridad: Del Archivo Original a la Base Común

Cada registro recibe una clave inmutable `SourceRow` (`1` a `1,067,371`, equivalente al índice `0` a `1,067,370`) antes de aplicar cualquier filtro, garantizando trazabilidad total y reconstrucción exacta:

| Etapa de Control Inicial | Filas / Registros | % del Original | Tratamiento Técnico Aplicado |
| :--- | ---: | ---: | :--- |
| **Archivo Original (`online_retail_II.csv`)** | `1,067,371` | `100.00%` | Lectura íntegra con `Invoice` y `StockCode` como texto; asignación de `SourceRow`. |
| **Copias Duplicadas Exactas Adicionales** | `-34,335` | `-3.22%` | `df.duplicated(subset=KEY8, keep='first')`: se retiene `1` fila por cada uno de los `32,907` grupos duplicados (`67,242` filas involucradas; ej. factura `489517`). |
| **Exclusiones Técnicas Comunes (Fechas/Tipos)** | `0` | `0.00%` | `0` fechas inválidas, `0` cantidades/precios no numéricos, `0` identificadores nulos. |
| **Base Común Trazable (`N_BASE`)** | **`1,033,036`** | **`96.78%`** | Punto de partida idéntico y auditable para las Rutas A y B (`235,151` líneas sin `CustomerID` conservadas sin imputación artificial). |

---

### 3. Contraste Formal de Estrategias: Ruta A vs. Ruta B

Sobre la base común de `1,033,036` líneas se ejecutaron y contrastaron las dos estrategias de procesamiento:

| Indicador de Control y Balance | Ruta A (Exclusión Pura) | Ruta B (Reconocimiento de Abonos `'C'`) | Diferencia ($\Delta = B - A$) | Impacto Relativo ($\Delta\%$ sobre A) |
| :--- | ---: | ---: | ---: | ---: |
| **Líneas Conservadas en el Dataset** | `1,007,913` | `1,027,016` | `+19,103` | `+1.90%` |
| **Líneas Excluidas de la Base Común** | `25,123` | `6,020` | `-19,103` | `-76.04%` |
| • *Compras válidas (`!IsC`, `Q > 0`, `P > 0`)* | `1,007,913` | `1,007,913` | `0` | `0.00%` |
| • *Abonos `'C'` reconocidos (`IsC`, `Q < 0`, `P > 0`)* | `0` *(excluidos)* | `19,103` *(en `8,291` facturas)* | `+19,103` | — |
| • *Excepción `'C'` con `Q > 0` (`C496350`, Manual, `Q=1`, `£373.57`)* | `1` *(excluida)* | `1` *(excluida)* | `0` | `0.00%` |
| • *Mermas de almacén sin `'C'` (`Q < 0`, `P = £0.00`, sin cliente)* | `3,393` *(excluidas)* | `3,393` *(excluidas)* | `0` | `0.00%` |
| • *Precios no positivos sin `'C'` (`Q > 0`, `P <= 0`: muestras y deuda `'A'`)* | `2,626` *(excluidas)* | `2,626` *(excluidas)* | `0` | `0.00%` |
| **Días Observados con Actividad Comercial** | `604 días` | `604 días` | `0 días` | `0.00%` |
| **Órdenes Diarias Sumadas (`TotalOrders`)** | `40,077` | `40,077` | `0` | `0.00%` |
| **Unidades Físicas Totales (`TotalUnits`)** | `11,205,148` | `10,728,328` | **`-476,820`** | **`-4.26%`** |
| **Ingresos Netos Acumulados (`Revenue GBP`)** | `£20,476,260.45` | `£19,013,836.27` | **`-£1,462,424.18`** | **`-7.14%`** |

#### Tres días de mayor divergencia monetaria ($\Delta = B - A$):
1. **`2011-12-09` ($\Delta = -\pounds 168,789.07$, `-84.01%` sobre A):** Explicado en un `99.81%` por la anulación `C581484` (`-80,995` unidades de `23843` *PAPER CRAFT , LITTLE BIRDIE* a `£2.08` = `-£168,469.60`, Cliente `16446` a las `09:27`), que reversa exactamente la compra `581483` realizada `12` minutos antes (`09:15`). En la Ruta A se inflaría falsamente el último día del archivo en `+£168,469.60`.
2. **`2011-01-18` ($\Delta = -\pounds 77,297.25$, `-80.56%` sobre A):** Explicado en un `99.85%` por la anulación `C541433` (`-74,215` unidades de `23166` *MEDIUM CERAMIC TOP STORAGE JAR* a `£1.04` = `-£77,183.60`, Cliente `12346` a las `10:17`), que cancela la factura `541431` emitida `16` minutos antes (`10:01`).
3. **`2010-12-07` ($\Delta = -\pounds 54,559.15$, `-54.80%` sobre A):** Originado por `6` cargos administrativos de plataforma `AMAZONFEE` sin cliente (`C537651`, `C537630`, `C537644`, etc., sumando `-£52,784.41`).

---

### 4. Mejora Clave 1: Conciliación Bidireccional de Abonos ("Salía la verdadera después")

#### 4.1. Diagnóstico del Sesgo Unidireccional (Etapa 1) vs. Conciliación Bidireccional (Etapa 2)
En la **Etapa 1 (Conciliación Conservadora Hacia Atrás)** se exige misma clave `(CustomerID, StockCode, Price)` y `invoice_close < credit InvoiceDate`:
- **Reconciled (Hacia atrás):** `9,827` líneas (`51.44%`, `-£588,174.90`), de las cuales `5,577` son devoluciones parciales.
- **Ambiguous (Múltiples facturas candidatas previas):** `5,393` líneas (`28.23%`, `-£132,723.50`).
- **Unreconciled (Sin enlace previo unívoco):** `3,883` líneas (`20.33%`, `-£741,525.78`), donde el motivo mayoritario era `"No earlier purchase of the product by the customer"` con **`2,060` líneas** (`-£276,975.78`).

Al implementar en la **Etapa 2 (Conciliación Temporal Bidireccional)** el emparejamiento hacia adelante (`compra_posterior >= abono`), se resolvió la naturaleza real de los `19,103` abonos de la Ruta B (`18,390` con cliente identificado y `713` anónimos) y se deconstruyeron las `2,060` líneas sin compra previa:

| Arquetipo Temporal Bidireccional (Ruta B: `19,103` líneas `'C'`) | Líneas (Base Deduplicada A-3-4) | % sobre Total `'C'` (`19,103`) | % sobre Apareadas (`16,916`) | Equivalente Bruto (Fase A-3-3) | Unidades Devueltas | Importe Abonado (GBP) |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| **1. Devolución Pura Post-Compra (`todas las compras < C`)** | `9,765` | `51.12%` | **`57.73%`** | `9,769` (`58.04%`) | `383,465` | `-£685,154.01` |
| **2. Re-facturación en Caliente (`< 24h` después del abono `'C'`)** | `1,499` | `7.85%` | **`8.86%`** | `1,397` (`8.30%`) | `19,935` | `-£46,247.34` |
| *• Subgrupo inmediato ($\le 60$ minutos después del abono)* | *`1,181`* | *`6.18%`* | *`6.98%`* | — | — | — |
| **3. Re-facturación Rápida (`1 a 7 días` después del abono `'C'`)** | `640` | `3.35%` | **`3.78%`** | `1,820` (`10.81%`) | `7,463` | `-£15,637.65` |
| **4. Recompra en Ciclo Posterior (`> 7 días` después del abono `'C'`)** | `5,012` | `26.24%` | **`29.63%`** | `3,845` (`22.85%`) | `36,246` | `-£81,132.16` |
| *Subtotal Re-facturación / Compra Posterior (`2 + 3 + 4`)* | *`7,151`* | *`37.43%`* | ***`42.27%`*** | *`7,062` (`41.96%`)* | *`63,644`* | *`-£143,017.15`* |
| **5. Huérfanas por Censura a la Izquierda (Pre-Dic 2009 / Mostrador)** | `1,474` | `7.72%` | — | `1,484` (`7.92%`) | `19,356` | `-£256,641.82` |
| **6. Abonos sin Cliente Identificado (`CustomerID = <NA>`)** | `713` | `3.73%` | — | `750` | `10,355` | `-£377,611.20` |
| **Total Abonos Reconocidos en Ruta B** | **`19,103`** | **`100.00%`** | **`100.00%`** | `19,493` *(con Q<0)* | **`476,820`** | **`-£1,462,424.18`** |

#### 4.2. Deconstrucción Exacta de las `2,060` Líneas `"No earlier purchase"`
- **`1,474` líneas (`71.55%`, `-£256,641.82`):** Son **cancelaciones huérfanas genuinas** (`1,484` en el dataset original antes de deduplicar `10` copias exactas), correspondientes a mercancía vendida antes del inicio del registro (pre-diciembre de 2009) o adquirida sin cuenta en mostrador y devuelta posteriormente bajo un `CustomerID`.
- **`586` líneas (`28.45%`, `-£20,333.96`):** No eran devoluciones sin compra, sino **re-facturaciones hacia adelante** donde la primera compra positiva del cliente para ese SKU se asentó *después* de la anulación `'C'`:
  - **`168` líneas (`8.16%`)** en **`< 24` horas** (correcciones en caliente de carrito/pasarela).
  - **`87` líneas (`4.22%`)** entre **`1 y 7` días**.
  - **`331` líneas (`16.07%`)** en **`> 7` días**.

#### 4.3. Casos Verificados de Corrección en Caliente (1 a 5 Minutos)
- **Cliente `15967` (`SourceRow 1384`):** Anulación `C489570` (`2009-12-01 13:28:00`) $\rightarrow$ Factura positiva definitiva `489571` (`2009-12-01 13:29:00`), brecha de **`1.0` minuto** (`10` ítems re-facturados).
- **Cliente `12483` (`SourceRow 121853`):** Anulación `C501400` (`2010-03-16 11:28:00`) $\rightarrow$ Factura positiva definitiva `501403` (`2010-03-16 11:29:00`), brecha de **`1.0` minuto** (`11` ítems re-facturados).
- **Cliente `16713` (`SourceRow 420810`):** Anulación `C529568` (`2010-10-28 18:40:00`) $\rightarrow$ Factura positiva definitiva `529569` (`2010-10-28 18:41:00`), brecha de **`1.0` minuto** (`16` ítems re-facturados).
- **Cliente `12352` (`SourceRow 631026`):** Anulación `C545329` (`2011-03-01 15:47:00`) $\rightarrow$ Factura positiva definitiva `545332` (`2011-03-01 15:52:00`), brecha de **`5.0` minutos** (`2` ítems de alto valor re-facturados).

---

### 5. Mejora Clave 2: Aislamiento de Mermas/Deuda, Bifurcación y Proxies de Marketing

#### 5.1. Segregación de Mermas Físicas de Almacén y Deuda Incobrable Serie `'A'`
1. **Mermas Físicas de Almacén (`3,457` líneas brutas / `3,393` líneas deduplicadas):**
   - Suman `-569,314` unidades en `3,393` documentos distintos sin prefijo `'C'`.
   - El **100%** tiene `Price = £0.00` y `CustomerID = <NA>`, con descripciones operativas internas (*check [121], damages [83], ? [81], damaged [78], missing [27], sold as set on dotcom [20], smashed [9], thrown away [9]*).
   - Quedan **excluidas del resultado comercial** en ambas rutas (`£0.00` de impacto monetario) y se segregan hacia auditoría de inventario.
2. **Asientos Contables de Deuda Incobrable (Serie `'A'` / `StockCode = 'B'`):**
   - Las **5 partidas con precio negativo** (`A506401` por `-£53,594.36`, `A516228` por `-£44,031.79`, `A528059` por `-£38,925.87`, `A563186` por `-£11,062.06` y `A563187` por `-£11,062.06`, acumulando **`-£158,676.14`**) quedan **automáticamente excluidas** tanto en la Ruta A como en la Ruta B gracias a la condición `Price > 0`.
   - El único asiento serie `'A'` con precio positivo (`A563185` por `+£11,062.06`, `CustomerID = <NA>`) carece de cliente y queda marcado con `IsMerchandise = 0`, junto con los otros códigos no mercantiles (`POST`, `DOT`, `M`, `AMAZONFEE`, `BANK CHARGES`, `D`, `C2`, `ADJUST`, que suman `4,573` líneas y `£832,284.45` en compras retenidas), impidiendo que contamine los modelos de comportamiento de clientes en `A-3-5` y `A-3-6`.

#### 5.2. Bifurcación del Pipeline y Construcción de Variables Proxy de Marketing
Para resolver la ausencia de variables UTM y la presencia de `229,201` líneas anónimas en la Ruta B:

| Repositorio Bifurcado (Ruta B: `1,027,016` líneas) | Líneas Totales | % Líneas | Compras (`Purchase`) | Abonos (`Credit`) | Facturas Únicas | Clientes Únicos | Unidades Netas | Ingreso Neto (GBP) | % Ingreso | Líneas con `DOT` (Dotcom Web) |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **1. Repositorio CRM Clientes Identificados** | `797,815` | `77.68%` | `779,425` | `18,390` | `44,876` | `5,942` | `9,990,261` | `£16,289,991.29` | `85.67%` | `5,097` (`0.64%`) |
| **2. Repositorio Demanda Anónima (Dotcom/Mostrador)** | `229,201` | `22.32%` | `228,488` | `713` | `3,492` | `0` (`<NA>`) | `738,067` | `£2,723,844.98` | `14.33%` | **`206,506` (`90.10%`)** |
| **Total Ruta B Seleccionada** | **`1,027,016`** | **`100.00%`** | **`1,007,913`** | **`19,103`** | **`48,368`** | **`5,942`** | **`10,728,328`** | **`£19,013,836.27`** | **`100.00%`** | **`211,603` (`20.60%`)** |

**Variables Proxy de Ingeniería Construidas para `A-3-5`:**
- **`CohortMonth`:** `25` cohortes mensuales de adquisición (`2009-12` a `2011-12`) basadas en la primera compra positiva del cliente + `ORPHAN_CREDIT_ONLY` (`64` cuentas que solo registran devoluciones pre-2009) + `ANONYMOUS_GUEST`.
- **`IsUK`:** Segmentación geográfica binaria entre Reino Unido (`942,328` líneas, `91.75%`) y Exportación Internacional (`84,688` líneas, `8.25%` en `42` países).
- **`ChannelProxy` & Flags Indirectos (`DOTCOM_OrderFlag`, `AMAZON_OrderFlag`, `DISCOUNT_UserFlag`):**
  - `DIRECT_REGISTERED_ACCOUNT`: `792,718` líneas (`77.19%`, `£16,173,822.17`).
  - `DOTCOM_WEB_STORE` (`DOTCOM_OrderFlag == 1`): `211,603` líneas (`20.60%`, `£2,664,872.02`), explicando el `90.10%` de las transacciones sin `CustomerID`.
  - `COUNTER_OR_UNTRACKED_GUEST`: `22,659` líneas (`2.21%`, `£406,773.32`).
  - `AMAZON_MARKETPLACE` (`AMAZON_OrderFlag == 1`): `36` líneas (`0.0035%`, `-£231,631.24` por comisiones de marketplace).
  - `DISCOUNT_UserFlag`: `55` clientes mayoristas con descuentos manuales `StockCode == 'D'`, abarcando `56,637` líneas transaccionales.

---

### 6. Auditoría Forense de Validación Profunda (6 Hallazgos Estructurales Adicionales)

Al contrastar exhaustivamente el estado inicial frente a la base procesada, se verificaron y documentaron en el cuaderno **6 fenómenos estructurales sutiles** que gobiernan la transición hacia la Fase `A-3-5`:

| Dimensión Forense Auditada | Evidencia Cuantitativa Exacta | Diagnóstico y Regla de Gobernanza para `A-3-4` / `A-3-5` |
| :--- | :--- | :--- |
| **1a. Origen Dual de los `34,335` Duplicados Exactos (Solapamiento de Hojas vs. Intra-Factura)** | • **`22,523` líneas (`65.60%`)** en `1,088` facturas.<br>• **`11,812` líneas (`34.40%`)** intra-factura. | El `65.60%` de los duplicados proviene del solapamiento contable entre las dos hojas del Excel original (`Year 2009-2010` hasta fila `525,461` y `Year 2010-2011` del `01` al `09` de diciembre de 2010). El `keep='first'` purgó el **100% (`0` sobrevivientes)**. |
| **1b. Líneas Partidas del Mismo SKU Dentro de una Misma Factura** | **`11,109` pares `(Invoice, StockCode)`** (`61` grupos / `124` líneas en abonos `'C'`). | Renglones dentro de una misma factura donde el mismo producto se escaneó varias veces con *distinta* cantidad (ej. `6` u. y luego `12` u.), por lo que no son duplicados exactos. En `A-3-5` debe colapsarse por `(Invoice, StockCode)` al analizar cestas. |
| **2. Colisiones de Reloj en el Mismo Minuto (`Gap = 0.0 min`)** | **`82` líneas `'C'`** (`28` con `SourceRow_P < SourceRow_C`, `52` con `SourceRow_C < SourceRow_P`, `2` anónimas). | Como `InvoiceDate` carece de segundos (`:00`), la regla estricta `<` de la Etapa 1 ignoraba compras ocurridas en el mismo minuto. Las `52` re-facturaciones instantáneas fueron capturadas por la Etapa 2 (`ForwardGapHours >= 0`) y las `28` anulaciones inmediatas se desempatan por `SourceRow`. |
| **3. Desambiguación Determinista de los `5,393` Abonos "Ambiguos"** | **`5,393` líneas (`£132,723.50`)** con $\ge 2$ facturas previas candidatas. | **`1,794` líneas (`33.27%`)** coinciden exactamente con el tamaño de lote (`Units == ReturnedUnits`, `533` con candidato único), y el **100% (`5,393`)** se resuelve bajo criterio contable **LIFO** (factura previa más reciente con saldo), elevando la trazabilidad hacia atrás del `51.44%` al **`79.67%` (`15,220` líneas)**. |
| **4. Fragmentación de `StockCode` por Mayúsculas/Minúsculas** | **`172` SKUs desdoblados** (`4,932` códigos en crudo $\rightarrow$ `4,760` códigos normalizados). | Códigos como `'85123a'` vs. `'85123A'`, `'15056bl'` vs. `'15056BL'` o `'m'` vs. `'M'`. Causó `0` falsos negativos en la conciliación con cliente identificado, pero exige normalizar `StockCode.str.strip().str.upper()` en `A-3-5`. |
| **5. Partidas No Mercantiles Retenidas y Deuda Positiva (`A563185`)** | **`5,761` líneas en Ruta B** (`4,573` compras por `+£832,284.45` y `1,188` abonos por `-£745,928.65`; neto `+£86,355.80`). | Incluye portes (`POST`, `DOT`), manuales (`M`), comisiones (`AMAZONFEE`, `BANK CHARGES`, `CRUK`), tests (`TEST001`, `PADS`) y el asiento contable positivo `A563185` (`Adjust bad debt`, `+£11,062.06`). En `A-3-5` se debe filtrar `IsMerchandise == 1` (`1,021,255` líneas de mercancía pura) para métricas de producto/cesta. |
| **6. Clientes Multi-País y Países Indeterminados** | **`13` clientes** con 2 países distintos y **`813` líneas** en `Unspecified` / `European Community`. | `13` cuentas B2B cambian de país entre órdenes (incluyendo el Cliente `12745` entre `EIRE` y `United Kingdom`). En `A-3-5` **no** debe agruparse por `(CustomerID, Country)` sino asignar el país modal/canónico por `CustomerID` para evitar duplicar a estos `13` clientes. |

---

### 7. Justificación de la Decisión Final de Negocio: Selección de la Ruta B

Se selecciona formalmente la **Ruta B (Compras netas de abonos `'C'` reconocidos + Auditoría de Conciliación Bidireccional)** para alimentar las fases `A-3-5` (*Data Construction*) y `A-3-6` (*Modeling & Commercial Strategy*):
1. **Veracidad Financiera y Física:** Excluir los abonos `'C'` (Ruta A) sobreestima artificialmente los ingresos brutos en **`+£1,462,424.18` (`+7.69%` sobre el ingreso neto real)** y el volumen físico en **`+476,820` unidades (`+4.44%`)**, ocultando anulaciones masivas del mismo día como `C581484` (`-£168,469.60`) y `C541433` (`-£77,183.60`).
2. **Protección contra Fuga de Información (No Data Leakage):** Los abonos se registran en su fecha real de emisión sin reescribir retroactivamente facturas pasadas, preservando la integridad causal de las series temporales de `604` días.
3. **Neutralización del Sesgo en RFM y Churn mediante `NettedHotFixFlag`:** Al exportar la bandera `NettedHotFixFlag` y el `TemporalArchetype` en `outputs/auditoria_conciliacion_abonos.csv`, la Fase `A-3-5` puede netear las `1,499` correcciones en caliente (`< 24h`) sin inflar artificialmente la frecuencia de pedidos (`Frequency`) ni castigar como desertores/devolvedores a clientes fieles cuyas facturas sufrieron ajustes técnicos en minutos.

---

### 8. Inventario de Entregables Validados en `A-3-4_DataCleaning`
- **`NB3 Data Preparation and Processing - Online Retail II.ipynb`:** Cuaderno Jupyter oficial de `52` celdas (`30` de código y `22` Markdown) completamente ejecutado, sin errores, con todas las tablas y `5` figuras de alta resolución embebidas.
- **`outputs/transacciones_procesadas.csv`:** `1,027,016` filas × `12` columnas (`SourceRow`, `Invoice`, `StockCode`, `Description`, `Quantity`, `InvoiceDate`, `Price`, `CustomerID`, `Country`, `LineAmount`, `Date`, `MovementType`: `1,007,913 Purchase` + `19,103 Credit`).
- **`outputs/indicadores_diarios.csv`:** `604` días activos × `4` columnas (`Date`, `TotalOrders`, `TotalUnits`, `Revenue` de la Ruta B).
- **`outputs/indicadores_diarios_comparacion.csv`:** `1,208` filas × `5` columnas (`604` días Ruta A + `604` días Ruta B).
- **`outputs/auditoria_conciliacion_abonos.csv`:** `19,103` filas × `25` columnas (las `15` columnas base de conciliación conservadora más `10` columnas de conciliación bidireccional hacia adelante, arquetipo temporal y `NettedHotFixFlag`).
- **`outputs/registro_exclusiones.csv`:** `65,478` registros auditables (`34,335 Common` + `25,123 Route A` + `6,020 Route B`).
- **`outputs/resultados_informe.json`:** Diccionario maestro de métricas auditadas (incluyendo `conciliacion_bidireccional`, `bifurcacion_y_proxies` y `auditoria_forense`).
- **`figures/`:** `fig1_daily_units.png`, `fig2_daily_revenue.png`, `fig3_daily_differences.png`, `fig4_bidirectional_reconciliation.png` y `fig5_pipeline_bifurcation_and_proxies.png`.

