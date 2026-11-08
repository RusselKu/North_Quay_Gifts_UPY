# Registro de Auditoría, Cambios y Mejoras Técnicas — Fase A-3-5 (Data Construction / Feature Engineering)

**Proyecto:** North Quay Gifts (*Online Retail II*, UPY — Metodología CRISP-DM)  
**Fase:** `A-3-5_DataConstruction`  
**Cuaderno auditado y actualizado:** [`NB4 Analytical Dataset Construction - Online Retail II.ipynb`](file:///c:/Users/russe/Documents/github_repo/North_Quay_Gifts_UPY/A-3-5_DataConstruction/NB4%20Analytical%20Dataset%20Construction%20-%20Online%20Retail%20II.ipynb)  
**Artefactos exportados en `outputs/` y `figures/`:**
- [`outputs/clientes_rfm.csv`](file:///c:/Users/russe/Documents/github_repo/North_Quay_Gifts_UPY/A-3-5_DataConstruction/outputs/clientes_rfm.csv) (`5,878` clientes × `17` columnas: `4` variables núcleo RFM + `13` variables forenses, de neteo en caliente y proxies de atribución de marketing)
- [`outputs/clientes_clasificacion.csv`](file:///c:/Users/russe/Documents/github_repo/North_Quay_Gifts_UPY/A-3-5_DataConstruction/outputs/clientes_clasificacion.csv) (`2,724` clientes × `18` columnas: `5` variables núcleo de clasificación + `13` variables forenses y proxies pre-corte con cero fuga de información)
- [`outputs/resultados_actividad3.json`](file:///c:/Users/russe/Documents/github_repo/North_Quay_Gifts_UPY/A-3-5_DataConstruction/outputs/resultados_actividad3.json) (diccionario completo de métricas y verificaciones de la fase)
- Figuras analíticas de alta resolución (`200 DPI`):
  - [`figures/fig1_hotfix_and_nonmerch_rfm.png`](file:///c:/Users/russe/Documents/github_repo/North_Quay_Gifts_UPY/A-3-5_DataConstruction/figures/fig1_hotfix_and_nonmerch_rfm.png)
  - [`figures/fig2_classification_windows_lifo_leakage.png`](file:///c:/Users/russe/Documents/github_repo/North_Quay_Gifts_UPY/A-3-5_DataConstruction/figures/fig2_classification_windows_lifo_leakage.png)
  - [`figures/fig3_marketing_proxies_and_forensic_governance.png`](file:///c:/Users/russe/Documents/github_repo/North_Quay_Gifts_UPY/A-3-5_DataConstruction/figures/fig3_marketing_proxies_and_forensic_governance.png)

---

## 1. Diagnóstico del Estado Inicial de `A-3-5` vs. Mejoras Implementadas

El cuaderno `NB4` inicial construía correctamente las tablas básicas de RFM (`5,878` clientes) y de clasificación supervisada de recompra a 90 días (`2,724` clientes), respetando el corte temporal (`CUTOFF = 2011-07-01 00:00:00`) y auditando la fuga de información (*data leakage*). Sin embargo, presentaba **cuatro limitaciones estructurales** al no conectar los hallazgos forenses de `A-3-3` y `A-3-4`:

| Dimensión Técnica | Estado Inicial de `NB4` (`A-3-5`) | Estado Auditado y Mejorado (`NB4` Actualizado) |
|---|---|---|
| **1. Sesgo por Re-facturación en Caliente (*"Salía la verdadera después"* / `NettedHotFixFlag`)** | Leía únicamente `transacciones_procesadas.csv` e ignoraba `auditoria_conciliacion_abonos.csv`. Contabilizaba las re-facturaciones técnicas en minutos (`Factura + C + Factura de reemplazo`) como órdenes adicionales en `Frequency` y como devoluciones reales del cliente. | Integra `auditoria_conciliacion_abonos.csv` (`19,103 × 25`). Identifica las **`1,499` líneas de abono en caliente (`< 24h`, `-£172,308.44`, `393` clientes)** y construye `Frequency_NetHotFix` (descontando **`601` facturas de reemplazo duplicadas** en `309` clientes con compra previa, o `738` en `384` clientes considerando todo match `< 24h`) y `TrueReturnRate` (**devolviendo a `0.00%` la tasa de devolución de `63` clientes leales**). |
| **2. Deconstrucción Forense de `Monetary <= 0` (`41` clientes en RFM y `9` en Clasificación)** | Reportaba `41` clientes con `Monetary <= 0` (`20` con `< £0` y `21` con `£0`) y `9` con `TotalSpent <= 0` sin aislar partidas no mercantiles ni devoluciones que cruzaban fronteras de ventana. | Demuestra que **`18` de los `20` clientes con `Monetary < 0` (`90.0%`)** son provocados por **partidas administrativas no mercantiles (`StockCode = 'M'`, `'D'`, `'ADJUST'`, `'BANK CHARGES'`)** y ciclos de *Hot-Fix* (ej. `12918`: `C502262 -> 502263 -> C502264` en 4 min), quedando **solo `2` clientes (`0.034%`)** con `Monetary_Merchandise < 0` por abonos huérfanos pre-Dic 2009 (`13091` y `13112`). En Clasificación, al filtrar por LIFO los abonos de compras previas a `2011-01-02` (`TotalSpent_InWindowNet`), **`0` clientes quedan con gasto negativo (`< £0.00`)**. |
| **3. Trazabilidad LIFO + Lote Exacto entre Ventanas Temporales** | No vinculaba cada abono `'C'` con la fecha exacta de su factura de compra original, impidiendo saber cuántos abonos dentro de la ventana histórica (`180d`) u observacional (`90d`) provenían de compras de periodos anteriores. | Aplica **Stage 1 (`9,827` líneas) + Lote Exacto (`1,794` líneas) + LIFO (`3,599` líneas)** para resolver el **100% de los `5,393` abonos ambiguos (`15,220` líneas resueltas = `82.76%` de los abonos con cliente)**. Demuestra que **`654` abonos (`18.46%`, `-£11,284.80`)** en la ventana de `180d` provienen de compras de 2009–2010, y que en los **`28` clientes de Clase `0`** con solo abonos en la ventana de `90d`, **`77` de sus `88` líneas (`87.50%`)** son devoluciones probadas de compras pre-corte (`< 2011-07-01`). |
| **4. Variables Proxy de Atribución de Marketing (0 UTMs) y Reglas de Gobernanza** | Exportaba únicamente 4 columnas en `clientes_rfm.csv` y 5 en `clientes_clasificacion.csv`, sin variables de cohorte, canal, geografía ni diversidad de catálogo, y sin visualizaciones (`0` figuras). | Incorpora de forma retrocompatible en ambos CSVs las variables proxy (`CohortMonth`, `TenureDays`, `Country` canónico para los `13` clientes multi-país, `IsUK`, `DOTCOM_OrderFlag`, `DISCOUNT_UserFlag`), las métricas de catálogo normalizadas (`4,932 -> 4,760` SKUs, `UniqueSKUs`, `PurchaseLines_Collapsed` eliminando `10,560` líneas partidas intra-factura) y genera **3 figuras multipanel de alta resolución** en `figures/`. |

---

## 2. Evidencia Cuantitativa de los Hallazgos Forenses en `A-3-5`

### 2.1 Corrección del Sesgo por Re-facturación en Caliente (`NettedHotFixFlag == True`)
Al cruzar las `19,103` líneas de abono `'C'` de `transacciones_procesadas.csv` con `auditoria_conciliacion_abonos.csv`:
- **`18,390` líneas (`-£1,084,812.98`)** tienen `CustomerID` identificado (`16,916` apareadas con compras del mismo producto en el historial de 2 años + `1,474` líneas huérfanas `5. Left-Censored Orphan`) y **`713` líneas (`-£377,611.20`)** son anónimas (`6. Anonymous Credit`).
- Dentro de las `16,916` líneas apareadas con cliente, **`7,151` líneas (`42.27%`)** registran una compra positiva posterior del mismo `(CustomerID, StockCode)`:
  - **`1,499` líneas (`8.15%` de los abonos con cliente, `-£172,308.44` en `767` facturas de abono y `749` facturas positivas de reemplazo)** corresponden al **Arquetipo 2 (`2. Hot-Fix Re-Invoicing < 24h Forward Match`, `NettedHotFixFlag == True`)**, de las cuales **`1,181` líneas (`78.79%`)** fueron re-facturadas en **$\le 60$ minutos** (ej. Cliente `16321`: `C489449 -> 489450` en `3` min; Cliente `15967`: `C489570 -> 489571` en `1` min; Cliente `12483`: `C501400 -> 501403` en `1` min; Cliente `12352`: `C545329 -> 545332` en `5` min).
- **Impacto directo sobre las métricas de los `5,878` clientes del universo RFM:**
  1. **Corrección de `Frequency` (`Frequency` vs. `Frequency_NetHotFix`):** En `1,223` líneas de *Hot-Fix* (`602` facturas de abono y `601` facturas positivas de reemplazo en `309` clientes), existía tanto la factura original previa como la factura de reemplazo en `< 24h`, inflando artificialmente el número de pedidos en **`601` órdenes duplicadas** (`36,975` órdenes brutas $\rightarrow$ **`36,374` órdenes netas** en `Frequency_NetHotFix`; si se descuentan además las `137` facturas de reemplazo donde el abono se digitó minutos antes que la primera factura positiva, el ajuste alcanza **`738` órdenes en `384` clientes**, dejando `36,237` órdenes).
  2. **Corrección de la Tasa de Devolución (`RawCreditRate` vs. `TrueReturnRate`):** Al excluir los `-£172,308.44` de re-facturaciones técnicas en caliente (`16.83%` del valor total abonado en clientes RFM), el volumen de devolución comercial real pasa de `-£1,023,763.31` (`5.89%` de las compras brutas) a **`-£851,454.87` (`4.90%` de las compras brutas)**. La tasa media de devolución por cliente baja de `3.26%` a **`2.78%`** (y entre clientes con algún abono, de `7.63%` a **`6.51%`**), **liberando a `63` compradores leales cuya tasa de devolución real cae exactamente a `0.00%`**.
  3. **Reconciliación de Cuentas Solo-Abono (`64` en Base Común vs. `61` en Ruta B):** En la Base Común deduplicada existían `5,942` clientes (`5,878` con compras válidas + `64` sin compras con `Price > 0`). Al aplicar la regla de Ruta B (`Price > 0`), `3` clientes que solo tenían líneas con `Price == 0` fueron excluidos por completo y `3` clientes pasaron a tener únicamente abonos `'C'`, resultando en **`5,939` clientes en Ruta B** (`5,878` en RFM + **`61` cuentas solo-abono** con `128` líneas, `65` facturas y `-£61,049.67`, el **100%** clasificadas bajo `5. Left-Censored Orphan`).

---

### 2.2 Aplicación de las 6 Reglas de Gobernanza Forense a Nivel Cliente

1. **Prohibición de Agrupar por `['CustomerID', 'Country']` (`13` Clientes Multi-País B2B):**
   - Los `13` clientes multi-país identificados en `A-3-4` (`12370` [Cyprus/Austria], `12394` [Belgium/Denmark], `12413` [France/Spain], `12417` [Belgium/Spain], `12422` [Switzerland/Australia], `12423` [Belgium/Denmark], `12429` [Denmark/Austria], `12431` [Australia/Belgium], `12449` [Belgium/Denmark], `12455` [Cyprus/Spain], `12457` [Switzerland/Cyprus], `12652` [France/Germany] y `12745` [United Kingdom/EIRE]) están todos presentes en el universo RFM (`5,878`).
   - Agrupar por `['CustomerID', 'Country']` habría generado `5,891` filas en lugar de `5,878` (`13` clientes duplicados con historias partidas). En `NB4` se agrupa estrictamente por `CustomerID` y se asigna su `Country` modal canónico.

2. **Aislamiento de Partidas No Mercantiles (`5,761` líneas en Ruta B / `3,652` en Clientes Identificados):**
   - En el subconjunto con `CustomerID` (`797,815` líneas) existen **`3,652` líneas no mercantiles** (`2,848` compras por `+£306,236.30` y `804` abonos por `-£374,859.55`, saldo neto `-£68,623.25`), dominadas por ajustes manuales `StockCode = 'M'` (`1,078` líneas, `-£185,701.19` neto), portes `POST`/`C2` (`2,237` líneas, `+£122,609.51` neto), descuentos mayoristas `D` (`170` líneas, `-£12,785.34` neto), cargos web `DOT` (`16` líneas, `+£11,906.36`) y comisiones `CRUK` (`16` líneas, `-£7,933.43`). La factura de deuda incobrable positiva **`A563185` (`StockCode = 'B'`, `+£11,062.06`)** carece de `CustomerID` y queda aislada tanto del repositorio CRM como del filtro `IsMerchandise == 1`.
   - En la verificación manual del cliente de alta frecuencia **`H = 17017`** (`Monetary = £6,553.79`), separar `IsMerchandise == 1` revela que su abono más grande (`C504637` por `-£5,843.70`) es un ajuste manual `StockCode = 'M'`; su gasto neto en mercancía real es **`Monetary_Merchandise = £12,397.49`** (`TrueReturnRate` mercantil de solo `1.43%` frente al `47.89%` bruto).

3. **Normalización de `StockCode` (`4,932` $\rightarrow$ `4,760` SKUs) y Colapso de Líneas Partidas Intra-Factura (`10,560` líneas en exceso en RFM):**
   - La normalización `StockCode_Norm = StockCode.str.strip().str.upper()` unifica los `172` SKUs desdoblados por mayúsculas/minúsculas across `3,322` filas.
   - Al colapsar los `10,291` pares `(Invoice, StockCode_Norm)` repetidos dentro de una misma factura en clientes identificados, las `779,425` líneas de compra de los `5,878` clientes RFM se reducen a **`768,865` líneas únicas de factura-producto (`PurchaseLines_Collapsed`)**, eliminando **`10,560` líneas partidas en exceso en `1,529` clientes (`26.01%` de la base)** y garantizando un conteo exacto de `UniqueSKUs` mercantiles (media `61.22` SKUs, mediana `35.0` SKUs por cliente).

4. **Desambiguación Determinista LIFO + Lote Exacto en Ventanas de Clasificación (`180d` y `90d`):**
   - De los **`3,543` abonos `'C'`** dentro de la ventana histórica `[2011-01-02, 2011-07-01)`, **`2,570` líneas (`72.54%`, `-£156,997.81`)** corresponden a compras realizadas dentro de la propia ventana de `180d`, mientras que **`654` líneas (`18.46%`, `-£11,284.80`)** son devoluciones de arrastre (*carry-over returns*) cuyas compras originales ocurrieron **antes del `2011-01-02`** (en 2009–2010), y `319` (`9.00%`) son ajustes/huérfanos no conciliables.
   - Al calcular `TotalSpent_InWindowNet` (descontando únicamente abonos originados en compras dentro de `[2011-01-02, 2011-07-01)`), **los `4` clientes que tenían `TotalSpent < 0` (`12755`, `14146`, `15197`, `13672`) pasan a tener gasto positivo (`> £0.00`)**, demostrando que su saldo negativo en la ventana de 180 días era un artefacto de corte temporal por devoluciones de compras de 2010 (destacando el cliente `14146`, con `TotalSpent = -£579.13` por `24` líneas de abono de compras de 2010, pero `TotalSpent_InWindowNet = +£662.30` y recompra efectiva en los 90 días siguientes [`Repurchase90Days = 1`]).
   - De los **`2,024` abonos `'C'`** dentro de la ventana de observación `[2011-07-01, 2011-09-29)`, **`570` líneas (`28.16%`, `-£12,466.45`)** cancelan compras anteriores al corte `2011-07-01` (`475` de la ventana histórica de `180d` y `95` previas a 2011). En los **`28` clientes de Clase `0`** que solo registraron abonos en la ventana de 90 días (`88` líneas por `-£1,206.92`), **`77` líneas (`87.50%`)** son devoluciones probadas de compras pre-corte (`76` de la ventana de `180d` y `1` pre-2011).

---

### 2.3 Poder Predictivo y Comercial de las Variables Proxy de Atribución de Marketing

Al incorporar `CohortMonth`, `TenureDays`, `IsUK`, `DOTCOM_OrderFlag` y `DISCOUNT_UserFlag` en `clientes_rfm.csv` y `clientes_clasificacion.csv`:

| Segmento Proxy de Marketing | Clientes en RFM (`5,878`) | Mediana `Monetary` RFM (£) | Media `Frequency_NetHotFix` RFM | Clientes en Clasificación (`2,724`) | Tasa de Recompra a 90 Días (`Repurchase90Days`) | Mediana `TotalSpent` 180d (£) |
|---|---:|---:|---:|---:|---:|---:|
| **Cohorte 2009 (`Dic 2009`)** | `955` (`16.25%`) | `£2,723.55` | `15.70` | `593` (`21.77%`) | **`67.45%`** | `£840.83` |
| **Cohorte 2010 (`Ene–Dic 2010`)** | `3,387` (`57.62%`) | `£877.70` | `5.15` | `1,432` (`52.57%`) | **`52.65%`** | `£463.67` |
| **Cohorte 2011 (`Ene–Dic 2011` / Pre-Corte)** | `1,536` (`26.13%`) | `£465.13` | `2.57` | `699` (`25.66%`) | **`36.48%`** | `£334.05` |
| **Mercado Doméstico UK (`IsUK == 1`)** | `5,350` (`91.02%`) | `£803.72` | `6.17` | `2,460` (`90.31%`) | **`51.38%`** | `£449.51` |
| **Exportación Internacional (`IsUK == 0`)** | `528` (`8.98%`) | `£1,151.03` | `6.39` | `264` (`9.69%`) | **`54.92%`** | `£802.87` |
| **Mayoristas con Descuento (`DISCOUNT_UserFlag == 1`)** | `55` (`0.94%`) | **`£15,036.14`** | **`48.96`** | `42` (`1.54%`) | **`88.10%`** | **`£3,262.24`** |
| **Cuentas Estándar (`DISCOUNT_UserFlag == 0`)** | `5,823` (`99.06%`) | `£826.96` | `5.78` | `2,682` (`98.46%`) | **`51.16%`** | `£469.88` |

- **Gradiente de Lealtad por Cohorte (`CohortMonth`):** La tasa de recompra a 90 días presenta una separación monotónica de **+30.97 puntos porcentuales** entre los clientes captados en la cohorte fundacional de 2009 (`67.45%`) y los captados en el primer semestre de 2011 (`36.48%`), confirmando que `TenureDays` / `CohortMonth` es un predictor de primer orden para `A-3-6`.
- **Segmento B2B con Descuento Negociado (`DISCOUNT_UserFlag == 1`):** Los `55` clientes con descuentos manuales `StockCode = 'D'` multiplican por **18.2x** la mediana de gasto en RFM (`£15,036.14` vs. `£826.96`), por **8.5x** la frecuencia neta de pedidos (`48.96` vs. `5.78`) y alcanzan un **`88.10%` de tasa de recompra a 90 días** (`37` de `42` recompran en el trimestre siguiente).
- **Cuenta Institucional Dotcom (`DOTCOM_OrderFlag == 1`):** En el repositorio identificado CRM, el flag `DOT` aísla específicamente la cuenta institucional `14096` (`5,128` líneas totales, `5,097` líneas en facturas con `StockCode = 'DOT'`, `34` facturas y `£57,120.91` de gasto neto).

---

## 3. Estructura de Columnas Exportadas hacia `A-3-6_ModelingStrategy`

Ambos archivos CSV mantienen en sus primeras posiciones las columnas exactas exigidas por la rúbrica original y por `NB5`, añadiendo a continuación las nuevas variables auditadas sin valores nulos (`0 NaNs`):

1. **`outputs/clientes_rfm.csv` (`5,878` filas × `17` columnas):**
   - `CustomerID`, `Recency`, `Frequency`, `Monetary` *(4 columnas núcleo originales)*
   - `Frequency_NetHotFix`, `Monetary_Merchandise`, `RawCreditRate`, `TrueReturnRate`, `HotFix_Flag`, `UniqueSKUs`, `PurchaseLines_Collapsed` *(7 columnas de depuración forense y cesta mercantil)*
   - `CohortMonth`, `TenureDays`, `Country`, `IsUK`, `DOTCOM_OrderFlag`, `DISCOUNT_UserFlag` *(6 variables proxy de atribución de marketing y geografía canónica)*

2. **`outputs/clientes_clasificacion.csv` (`2,724` filas × `18` columnas, todas las features $X$ calculadas estrictamente en `< 2011-07-01 00:00:00`):**
   - `CustomerID`, `RecencyDays`, `TotalOrders`, `TotalSpent`, `Repurchase90Days` *(5 columnas núcleo originales)*
   - `TotalOrders_NetHotFix`, `TotalSpent_Merchandise`, `TotalSpent_InWindowNet`, `RawCreditRate`, `TrueReturnRate`, `HotFix_Flag`, `UniqueSKUs` *(7 columnas de depuración forense y LIFO intra-ventana)*
   - `CohortMonth`, `TenureDays`, `Country`, `IsUK`, `DOTCOM_OrderFlag`, `DISCOUNT_UserFlag` *(6 variables proxy pre-corte sin fuga de información)*
