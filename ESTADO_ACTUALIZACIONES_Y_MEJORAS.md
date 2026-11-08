# Estado Global de Actualizaciones y Mejoras — North Quay Gifts (UPY)

**Proyecto:** North Quay Gifts — Ciencia de Datos / Minería de Datos (Metodología CRISP-DM)  
**Institución:** Facultad de Ingeniería de Datos, Universidad Politécnica de Yucatán (UPY)  
**Docente Asesor:** Didier Omar Gamboa Angulo  
**Equipo de Trabajo:**
- Russel Emmanuel Ku Aguilar (ID: 2309131)
- Damian Nicolas Sanchez Novelo (ID: 2109134)
- Jonathan Abisai Velasco Martín (ID: 2309060)
- Ángel Rivaldo Canché Chuc (ID: 2309030)
- Bianca Alexandra Acosta Castellanos (ID: 2309001)

---

## 1. Tablero de Control de Fases CRISP-DM

| Fase | Identificador | Estado | Entregables Principales | Foco de Mejora y Actualización |
| :--- | :--- | :---: | :--- | :--- |
| **Entendimiento de Datos** | `A-3-3_DataUnderstanding` | **COMPLETADO (Auditado y Rehecho)** | • `NB2 Exploración de Datos - Online Retail II.ipynb`<br>• `CAMBIOS_Y_MEJORAS.md`<br>• `figures/fig7_cancellations_anatomy.png`<br>• `figures/fig8_marketing_tracking_audit.png` | Diagnóstico de ausencia de variables de marketing (ceguera de atribución) y deconstrucción empírica de cancelaciones complejas / re-facturaciones en caliente ("salía la verdadera después"). |
| **Preparación y Procesamiento** | `A-3-4_DataCleaning` | **COMPLETADO (Auditado y Rehecho)** | • `NB3 Data Preparation and Processing - Online Retail II.ipynb`<br>• `CAMBIOS_Y_MEJORAS.md`<br>• `outputs/*.csv` & `resultados_informe.json`<br>• `figures/fig4_bidirectional_reconciliation.png`<br>• `figures/fig5_pipeline_bifurcation_and_proxies.png` | Conciliación temporal bidireccional (hacia atrás + hacia adelante `<24h`, `1-7d`, `>7d`); deconstrucción de las `2,060` líneas sin compra previa (`586` re-facturadas hacia adelante vs. `1,474` huérfanas pre-2009); bifurcación CRM (`797,815`) vs. Dotcom/Anónimos (`229,201`); aislamiento de mermas (`3,457` brutas / `3,393` dedup) y deuda serie `'A'`; proxies de marketing (`CohortMonth`, `IsUK`, `DOTCOM`, `AMAZON`, `DISCOUNT_USER`). |
| **Construcción de Datasets** | `A-3-5_DataConstruction` | *Pendiente (Siguiente paso)* | • `NB4 Analytical Dataset...ipynb`<br>• `CAMBIOS_Y_MEJORAS.md` | Ingeniería de características sin sesgo de doble contabilización: uso de `NettedHotFixFlag` para depurar `Frequency` y tasa real de devolución en RFM; integración de cohortes de adquisición mensual (`CohortMonth`) y flags de canal (`DOTCOM` / `IsUK`). |
| **Estrategia y Modelado** | `A-3-6_ModelingStrategy` | *Pendiente* | • `NB5 Modeling and Commercial Strategy...ipynb`<br>• `CAMBIOS_Y_MEJORAS.md` | Modelos de valor neto (CLV) y churn ajustados sin penalización injusta a clientes con re-facturaciones técnicas en caliente; estrategia comercial diferenciada por canal proxy y cohorte. |

---

## 2. Detalle de Intervención: Fase A-3-3 (Data Understanding)

### 2.1. Diagnóstico del Estado Previo
La versión anterior presentaba debilidades conceptuales y analíticas que comprometían la calidad técnica del proyecto:
1. **Omisión de la Dimensión de Marketing:** Se asumía tácitamente la optimización comercial o el retorno del gasto publicitario (ROMI) sin auditar si la base de datos permitía rastrear canales o campañas de captación.
2. **Confusión en Cancelaciones y Devoluciones:** Se trataban indistintamente todas las líneas con prefijo `'C'` o con cantidades negativas como devoluciones simples de producto, pasando por alto que en muchos casos se emitían varias anulaciones para una misma orden y que, poco tiempo después, se asentaba la factura verdadera o corregida.

### 2.2. Mejoras y Hallazgos Cuantitativos Incorporados en A-3-3

#### A. Auditoría de Trazabilidad y Variables de Marketing (Tracking Blind Spot)
- **Diagnóstico del Esquema:** El dataset cuenta estrictamente con 8 columnas (`Invoice`, `StockCode`, `Description`, `Quantity`, `InvoiceDate`, `Price`, `Customer ID`, `Country`). Existen **cero (0) variables** para parámetros UTM, canal de captación (orgánico, pago, email, afiliados), cupones de descuento a nivel de cesta o analítica web (clickstream).
- **Impacto Empresarial:** North Quay Gifts opera bajo una *ceguera de atribución comercial*. No es factible calcular directamente el Costo de Adquisición de Clientes (CAC) ni evaluar si ciertas campañas agresivas atraen clientes con alta propensión a la devolución.
- **Señales Indirectas Detectadas:** `177` líneas con `StockCode == 'D'` (descuentos manuales acumulando `-£13,484.54` en `55` clientes), `1,446` líneas de `DOTCOM POSTAGE` (operaciones de e-commerce web propio) y `39` líneas de comisiones de plataforma (`AMAZON FEE`).
- **Evidencia Visual:** Generación de la **Figura 8** (`figures/fig8_marketing_tracking_audit.png`).

#### B. Anatomía de Cancelaciones y Re-facturación ("Al tiempo después salía la verdadera")
- **Población Total Analizada en Bruto:** `1,067,371` filas; `19,494` líneas con prefijo `'C'`; `22,950` líneas con cantidad negativa.
- **Arquetipos de Transacción Negativa Identificados:**
  1. *Devoluciones Puras Post-Compra (`58.04%`, `9,769` líneas apareadas):* Compra positiva habitual seguida días o semanas después por su devolución física o nota de crédito.
  2. *Re-facturación y Sustitución Temporal ("Salía la verdadera después", `41.96%`, `7,062` líneas apareadas):* Transacciones donde la anulación con `'C'` precede temporalmente o coexiste con una factura positiva posterior que consolida la orden verdadera (`1,397` líneas en `< 24` horas).
  3. *Cancelaciones Huérfanas / Censuradas a la Izquierda (`1,484` líneas brutas, `7.92%`):* Devoluciones de clientes sin compra previa registrada en el horizonte 2009–2011.
  4. *Mermas de Bodega sin Prefijo C (`3,457` líneas brutas):* `100%` con `Price = £0.00` y `Customer ID = NaN`.
  5. *Asientos Contables de Deuda Incobrable:* `5` líneas con precio negativo (hasta `-£53,594.36` en `A506401`).
- **Evidencia Visual:** Generación de la **Figura 7** (`figures/fig7_cancellations_anatomy.png`).

---

## 3. Detalle de Intervención: Fase A-3-4 (Data Cleaning & Processing)

### 3.1. Trazabilidad y Contraste de Estrategias (Ruta A vs. Ruta B)
- **Control de Base Común:** De las `1,067,371` filas originales (con clave inmutable `SourceRow`), se excluyeron `34,335` copias duplicadas exactas adicionales (`32,907` grupos duplicados), consolidando una **base común trazable de `1,033,036` líneas**.
- **Ruta A (Exclusión pura):** Retiene únicamente las `1,007,913` compras positivas válidas (`25,123` excluidas), sumando `40,077` órdenes diarias, `11,205,148` unidades y `£20,476,260.45` en `604` días activos.
- **Ruta B (Reconocimiento de abonos `'C'` — Seleccionada):** Conserva las mismas `1,007,913` compras más `19,103` abonos `'C'` documentados (`1,027,016` líneas totales; `6,020` excluidas), resultando en `10,728,328` unidades netas ($\Delta = -476,820$, `-4.26%`) y **`£19,013,836.27`** de ingreso neto ($\Delta = -\pounds 1,462,424.18$, `-7.14%`).

### 3.2. Conciliación Temporal Bidireccional (Resolución del Sesgo de las `2,060` Líneas)
- En el algoritmo unidireccional previo (Etapa 1: solo `compra < abono`), `9,827` líneas (`51.44%`) se conciliaban hacia atrás, `5,393` (`28.23%`) resultaban ambiguas y `3,883` (`20.33%`) quedaban no conciliadas, incluyendo **`2,060` líneas bajo el motivo *"No earlier purchase of the product by the customer"***.
- Al implementar la **Etapa 2 (Conciliación Bidireccional Hacia Adelante)** sobre los `18,390` abonos `'C'` con cliente en la base deduplicada (`16,916` apareados con compras):
  - Se demostró que **`586` de las `2,060` líneas (`28.45%`)** sí tenían compra del cliente en el archivo, pero registrada **después** del abono (`168` correcciones en caliente en `< 24h`, `87` en `1–7d` y `331` en `> 7d`).
  - Las restantes **`1,474` líneas deduplicadas** (`1,484` en bruto antes de purgar `10` duplicados exactos) son devoluciones huérfanas legítimas por censura a la izquierda (ventas previas a diciembre de 2009 o compras de mostrador).
  - En el total de `16,916` abonos apareados de la Ruta B, **`9,765` líneas (`57.73%`)** son devoluciones puras post-compra y **`7,151` líneas (`42.27%`)** tienen compra positiva posterior, destacando **`1,499` correcciones en caliente en `< 24` horas** (`1,181` en $\le 60$ minutos, como `C489570 → 489571` en `1` min y `C545329 → 545332` en `5` min), marcadas con `NettedHotFixFlag = True` en `outputs/auditoria_conciliacion_abonos.csv`.
- **Evidencia Visual:** Generación de la **Figura 4** (`A-3-4_DataCleaning/figures/fig4_bidirectional_reconciliation.png`).

### 3.3. Aislamiento Contable, Bifurcación del Pipeline y Proxies de Marketing
- **Aislamiento de Mermas y Deuda Incobrable:** Se segregaron las `3,457` líneas brutas (`3,393` deduplicadas, `-569,314` unidades, `100% Price = £0.00` y sin cliente) de merma de almacén y las `5` partidas de deuda incobrable serie `'A'` con precio negativo (`-£158,676.14`), además de etiquetar con `IsMerchandise = 0` el asiento positivo `A563185` (`+£11,062.06`) y los códigos administrativos (`POST`, `DOT`, `M`, `AMAZONFEE`, `BANK CHARGES`, `D`, `C2`, `ADJUST`).
- **Bifurcación Operativa de la Ruta B (`1,027,016` líneas):**
  1. *Repositorio CRM Clientes Identificados:* `797,815` líneas (`77.68%`; `779,425` compras + `18,390` abonos en `5,942` clientes; `£16,289,991.29`).
  2. *Repositorio Demanda Anónima (Dotcom/Mostrador):* `229,201` líneas (`22.32%`; `£2,723,844.98`), demostrando que **`206,506` líneas (`90.10%`)** provienen de facturas con `StockCode == 'DOT'` (*DOTCOM POSTAGE*, ventas web sin login).
- **Proxies de Atribución de Marketing Construidos:** `CohortMonth` (`25` cohortes mensuales de adquisición), `IsUK` (`942,328` líneas UK [`91.75%`] vs. `84,688` exportación [`8.25%`]), `DOTCOM_OrderFlag` (`211,603` líneas), `AMAZON_OrderFlag` (`36` líneas) y `DISCOUNT_UserFlag` (`55` clientes mayoristas con `56,637` líneas).
- **Evidencia Visual:** Generación de la **Figura 5** (`A-3-4_DataCleaning/figures/fig5_pipeline_bifurcation_and_proxies.png`).

### 3.4. Auditoría Forense de Validación Profunda (6 Hallazgos Estructurales Adicionales)
1. **Origen Dual de los `34,335` Duplicados Exactos:** El **`65.60%` (`22,523` líneas en `1,088` facturas)** proviene del solapamiento de corte entre las dos hojas del Excel original (`Year 2009-2010` hasta fila `525,461` y `Year 2010-2011` del `01` al `09` de diciembre de 2010; `100%` purgado con `0` sobrevivientes), mientras que el **`34.40%` (`11,812` líneas)** son repeticiones intra-factura. Además, se identificaron **`11,109` pares `(Invoice, StockCode)`** (`61` grupos / `124` líneas en abonos `'C'`) con el mismo SKU escaneado en varios renglones de la misma factura con distinta cantidad.
2. **Colisiones de Reloj en el Mismo Minuto (`82` líneas `'C'` con `Gap = 0.0 min`):** Debido al truncamiento de segundos (`:00`), `82` abonos coinciden en el mismo minuto exacto con su compra (`28` con `SourceRow_P < SourceRow_C` desempatados por `SourceRow`, y `52` con `SourceRow_C < SourceRow_P` capturados por `ForwardGapHours >= 0`).
3. **Resolución Determinista de los `5,393` Abonos "Ambiguos" (`£132,723.50`):** `1,794` líneas (`33.27%`) coinciden con el tamaño exacto de lote (`Units == ReturnedUnits`, `533` con candidato único) y el **`100%` (`5,393` líneas)** es resoluble mediante regla contable **LIFO** (factura previa más reciente con saldo disponible), elevando la trazabilidad hacia atrás del `51.44%` al **`79.67%` (`15,220` líneas)**.
4. **Fragmentación de `StockCode` por Capitalización (`172` SKUs desdoblados):** `4,932` códigos en crudo colapsan a `4,760` al normalizar mayúsculas (`'85123a'` vs. `'85123A'`, `'m'` vs. `'M'`). Causó `0` fallos en conciliación de clientes identificados, pero requiere normalización en `A-3-5`.
5. **Supervivencia del Asiento Positivo `A563185` (`+£11,062.06`) y `5,761` Líneas No Mercantiles:** Dentro de la Ruta B permanecen `4,573` compras (`+£832,284.45`) y `1,188` abonos (`-£745,928.65`) de códigos operativos (`POST`, `DOT`, `M`, `AMAZONFEE`, `BANK CHARGES`, `CRUK`, `TEST001`, `PADS`) y la factura `A563185` (`Adjust bad debt`, `+£11,062.06`), aislados mediante la bandera `IsMerchandise == 1` (`1,021,255` líneas de mercancía pura).
6. **Clientes Multi-País (`13` cuentas B2B) y Países Indeterminados (`813` líneas):** `13` clientes cambian de país entre facturas (incluyendo el Cliente `12745` entre `EIRE` y `United Kingdom`) y `813` líneas registran `Unspecified` / `European Community`.

---

## 4. Hoja de Ruta hacia la Fase A-3-5 (Data Construction / Feature Engineering)

Con los archivos auditados y exportados en `A-3-4_DataCleaning/outputs/`, la **Fase A-3-5** procederá con:
1. **Ingesta de `transacciones_procesadas.csv` y `auditoria_conciliacion_abonos.csv`:** Cruzar la bandera `NettedHotFixFlag` para consolidar órdenes re-facturadas en `< 24` horas antes de calcular `Frequency`, `Monetary` neto e intervalos entre compras (`InterPurchaseTime`).
2. **Separación de Mercancía Pura (`IsMerchandise == 1`) y Normalización de `StockCode`:** Filtrar las `5,761` líneas no mercantiles (incluyendo `A563185`), normalizar `StockCode.str.strip().str.upper()` (`4,760` SKUs canónicos) y colapsar los `11,109` pares `(Invoice, StockCode)` partidos dentro de una misma factura.
3. **Integración de Variables Proxy de Marketing y País Canónico por Cliente:** Incorporar `CohortMonth`, `IsUK`, `DOTCOM_OrderFlag` y `DISCOUNT_UserFlag`, asignando el país modal por `CustomerID` para no duplicar a los `13` clientes multi-país en la tabla analítica de `A-3-5`.
