# Registro Maestro de Actualizaciones, Auditoría y Mejoras del Proyecto (CRISP-DM)
**Proyecto:** North Quay Gifts (Online Retail II - UPY)

Este documento centraliza el estado de revisión, corrección de errores metodológicos, hallazgos de negocio y mejoras técnicas aplicadas a cada fase del proyecto para garantizar **trazabilidad al 100%** entre los cuadernos Jupyter (`.ipynb`) y los datos exportados en `outputs/`.

---

## 1. Resumen de Estado por Carpeta / Fase

| Fase CRISP-DM | Carpeta | Estado | Cuaderno Principal | Registro Detallado |
|---|---|---|---|---|
| **1. Business Understanding** | `A-3-2_BusinessUnderstanding` | Base Conceptual | *(Documentos de diseño y alcance)* | Integrado en marco general |
| **2. Data Understanding** | `A-3-3_DataUnderstanding` | **COMPLETADO (Auditado y Rehecho)** | `NB1` y `NB2` (`.ipynb` ejecutados) | [`A-3-3_DataUnderstanding/CAMBIOS_Y_MEJORAS.md`](file:///c:/Users/russe/Documents/github_repo/North_Quay_Gifts_UPY/A-3-3_DataUnderstanding/CAMBIOS_Y_MEJORAS.md) |
| **3. Data Cleaning & Processing** | `A-3-4_DataCleaning` | **COMPLETADO (Auditado y Rehecho)** | `NB3 Data Preparation and Processing` (`.ipynb` ejecutado) | [`A-3-4_DataCleaning/CAMBIOS_Y_MEJORAS.md`](file:///c:/Users/russe/Documents/github_repo/North_Quay_Gifts_UPY/A-3-4_DataCleaning/CAMBIOS_Y_MEJORAS.md) |
| **4. Data Construction (Feature Eng.)** | `A-3-5_DataConstruction` | **COMPLETADO (Auditado y Rehecho)** | `NB4 Analytical Dataset Construction` (`.ipynb` ejecutado) | [`A-3-5_DataConstruction/CAMBIOS_Y_MEJORAS.md`](file:///c:/Users/russe/Documents/github_repo/North_Quay_Gifts_UPY/A-3-5_DataConstruction/CAMBIOS_Y_MEJORAS.md) |
| **5. Modeling & Commercial Strategy** | `A-3-6_ModelingStrategy` | **COMPLETADO (Auditado y Rehecho)** | `NB5 Modeling and Commercial Strategy` (`.ipynb` ejecutado) | [`A-3-6_ModelingStrategy/CAMBIOS_Y_MEJORAS.md`](file:///c:/Users/russe/Documents/github_repo/North_Quay_Gifts_UPY/A-3-6_ModelingStrategy/CAMBIOS_Y_MEJORAS.md) |

---

## 2. Síntesis de Mejoras Consolidadas en `A-3-3_DataUnderstanding` (Completado)

1. **Corrección del filtro de Cancelaciones (`Invoice` con `'C'`):**
   - El código original usaba `startswith('C')` sensible a mayúsculas. Aunque en el archivo actual las `'C'` están en mayúsculas (`19,494` filas = `1.83%`), se blindó con `.str.strip().str.upper().startswith('C')` y se separó de las **facturas de ajuste contable por deuda incobrable con prefijo `'A'`** (`A506401`, `A516228`, `A528059`, `A563185`, `A563186`, `A563187`).
2. **Clasificación exacta de Anomalías de `Quantity <= 0` y `Price <= 0`:**
   - Se desglosaron las `22,950` filas con `Quantity <= 0` en **`19,493` cancelaciones `'C'`** y **`3,457` mermas/ajustes internos de inventario** (100% con `Price == 0.0` y sin `Customer ID`, ej. `"damaged"`, `"thrown away"`, `"missing"`).
   - Se corrigió el conteo de `Price <= 0` (`6,207` filas = `6,202` precios cero + `5` precios negativos de deuda incobrable `'B'`).
3. **Auditoría profunda de los `21` Códigos No Mercantiles (`5,950` filas = `£118,524.08` netos):**
   - Desglose completo de `DOT` (`£322,647.47`), `POST` (`£112,248.62`), `M` (`-£282,535.84`), `AMAZONFEE` (`-£235,038.36`), `B` (`-£147,614.08`), `D` (`-£13,066.64`), `CRUK` (`-£7,933.43`), `BANK CHARGES`, `PADS`, `TEST001`, `TEST002`, etc.
4. **Ceguera de Atribución de Marketing (0 UTMs / 0 Campañas) y Sesgo de Supervivencia de `Customer ID` (`22.84%` nulos):**
   - Se demostró que el `98.8%` de la facturación sin `Customer ID` (`£2.995M` brutos) son compras legítimas de invitados/mostrador y pasarela `DOTCOM POSTAGE` (`1,422` de `1,438` líneas de `DOT` carecen de `Customer ID`), con un ticket mediano por factura **1.54x superior** al de clientes registrados (`£472.22` vs `£307.50`).

---

## 3. Síntesis de Mejoras Consolidadas en `A-3-4_DataCleaning` (Completado)

1. **Conciliación Bidireccional de Abonos `'C'` ("Salía la verdadera después"):**
   - El pipeline inicial de `NB3` solo buscaba facturas de compra **anteriores** (`InvoiceDate_compra < InvoiceDate_abono`), dejando `4,096` líneas (`50.71%` del valor abonado, `-£741,525.78`) como *"No conciliables"* y desconociendo qué ocurría **después** del abono.
   - Se implementó un **motor de conciliación bidireccional (Backward + Forward)** sobre las `19,103` líneas de abono deduplicadas (`16,916` apareadas con cliente + `1,474` huérfanas + `713` anónimas):
     - **`7,151` líneas (`42.27%` de los `16,916` abonos apareados con cliente)** tienen una **compra positiva posterior** del mismo `(CustomerID, StockCode)`.
     - **`1,499` líneas (`8.86%`, `-£172,308.44`)** son **re-facturaciones en caliente en `< 24` horas** (`1,181` en `<= 60` minutos, ej. `C489449 -> 489450` en 3 min, `C489570 -> 489571` en 1 min, `C545329 -> 545332` en 5 min). Se etiquetaron con `NettedHotFixFlag = True`.
     - **`640` líneas (`3.78%`, `-£57,366.66`)** son re-facturaciones de corto plazo (`1 a 7` días).
     - **`5,012` líneas (`29.63%`, `-£215,969.62`)** son recompras en ciclos posteriores (`> 7` días).
     - **`1,474` líneas (`-£363,911.09`)** son abonos huérfanos por **censura por la izquierda (compras previas al `2009-12-01`)** o devoluciones de mostrador, explicando las `64` cuentas en la Base Común (`61` en Ruta B) que solo registran abonos `'C'`.
2. **Bifurcación Arquitectónica y Variables Proxy de Atribución de Marketing (0 UTMs):**
   - Se estructuró la separación entre el **Repositorio CRM Identificado** (`797,815` líneas, `£16,289,991.29` netos) y el **Repositorio de Demanda Anónima/Dotcom** (`229,201` líneas, `£2,723,844.98` netos).
   - Se construyeron las variables proxy: `CohortMonth` (`27` cohortes mensuales), `IsUK` (`942,328` UK vs `84,688` exportación), `DOTCOM_OrderFlag` (`211,603` líneas en pedidos con `StockCode == 'DOT'`), `AMAZON_OrderFlag` (`36` líneas), `DISCOUNT_UserFlag` (`55` clientes mayoristas con `StockCode == 'D'`, `56,637` líneas) y `ChannelProxy`.
3. **Descubrimiento y Gobernanza de 6 Hallazgos Forenses Adicionales:**
   - **Origen dual de los `34,335` duplicados exactos:** `65.60%` (`22,523` líneas en `1,088` facturas del `2010-12-01` al `2010-12-09`) provienen del **solapamiento entre las dos hojas del archivo original** (*Year 2009-2010* y *Year 2010-2011*), quedando **100% neutralizados (`0` sobrevivientes)**; además, se identificaron **`11,109` pares `(Invoice, StockCode)` partidos** en varias líneas con distinta cantidad dentro de una misma factura.
   - **Colisiones en el mismo minuto (`Gap = 0.0 min`):** `82` líneas de abono (`28` `Compra < Abono`, `52` `Abono < Compra` y `2` anónimas) ocurren en el mismo minuto que su compra debido al truncamiento de segundos (`:00`) del ERP.
   - **Desambiguación determinista de los `5,393` abonos `"Ambiguous"` (`-£132,723.50`):** `1,794` líneas empatan por tamaño exacto de lote (`Units == ReturnedUnits`) y el **100% (`5,393`) se resuelve por regla LIFO**, elevando la trazabilidad hacia atrás del `51.44%` al **`79.67%` (`15,220` líneas)**.
   - **Fragmentación de `StockCode` por mayúsculas/minúsculas:** `172` SKUs desdoblados (`4,932` crudos $\rightarrow$ `4,760` SKUs canónicos).
   - **Partidas no mercantiles y deuda positiva (`A563185`) en Ruta B:** `5,761` líneas (`+£86,355.80` netos), incluyendo la factura `A563185` (`Adjust bad debt`, `+£11,062.06`), aisladas mediante `IsMerchandise == 1` (`1,021,255` líneas de mercancía pura).
   - **Clientes Multi-País (`13` clientes B2B) y Geografías Indeterminadas (`813` líneas):** `13` clientes facturan en 2 países distintos (incluyendo `12745` entre `United Kingdom` y `EIRE`), exigiendo país canónico modal por `CustomerID`.

---

## 4. Síntesis de Mejoras Consolidadas en `A-3-5_DataConstruction` (Completado)

1. **Corrección del Sesgo por Re-facturación en Caliente (`NettedHotFixFlag == True`) en RFM y Clasificación:**
   - Se integró `auditoria_conciliacion_abonos.csv` (`19,103 × 25`) directamente en `NB4`.
   - En el universo RFM (`5,878` clientes), las `1,499` líneas de re-facturación en caliente (`< 24h`, `-£172,308.44` en `393` clientes) habían inflado artificialmente la frecuencia de pedidos y el ratio de devolución. Al construir **`Frequency_NetHotFix`**, se descontaron **`601` facturas positivas de reemplazo duplicadas** en `309` clientes con factura previa vinculada (`36,975` órdenes brutas $\rightarrow$ **`36,374` órdenes netas**; o `738` órdenes en `384` clientes considerando las `137` facturas adicionales donde el abono se digitó minutos antes que la primera compra).
   - Al construir **`TrueReturnRate`** (descontando los `-£172,308.44` de abonos técnicos en caliente, equivalentes al `16.83%` del valor abonado en RFM), la tasa de devolución agregada sobre compras brutas baja del `5.89%` (`-£1,023,763.31`) al **`4.90%` (`-£851,454.87`)**, y **`63` compradores leales pasan de tener una tasa de devolución falsa a exactamente `0.00%`**.
   - En la ventana histórica de 180 días de Clasificación (`[2011-01-02, 2011-07-01)`, `2,724` clientes), se identificaron `279` líneas de *Hot-Fix* (`-£41,643.11` en `97` clientes) y se construyó **`TotalOrders_NetHotFix`** (descontando `115` órdenes duplicadas en `83` clientes).
2. **Deconstrucción Forense de `Monetary <= 0` (`41` clientes en RFM) y `TotalSpent <= 0` (`9` clientes en Clasificación):**
   - Al separar `Monetary_Merchandise` (`IsMerchandise == 1`, aislando las `3,652` líneas no mercantiles en clientes identificados por `-£68,623.25` netos), se demostró que **`18` de los `20` clientes con `Monetary < 0` (`90.0%`)** en RFM estaban distorsionados por ajustes administrativos (`StockCode = 'M'`, `'D'`, `'ADJUST'`, `'BANK CHARGES'`) y ciclos de *Hot-Fix* (ej. Cliente `12918` con `-£10,953.50` por secuencia `C502262 -> 502263 -> C502264` en 4 min, pero `Monetary_Merchandise = £0.00`; Cliente `14063` con `Monetary = -£3,767.20`, pero `Monetary_Merchandise = +£9,471.50`). **Solo `2` clientes de `5,878` (`0.034%`, `13091` y `13112`)** tienen `Monetary_Merchandise < 0`, ambos por abonos huérfanos pre-Dic 2009.
   - En la verificación manual del cliente de alta frecuencia **`H = 17017`** (`Monetary = £6,553.79`), se probó que su abono más grande (`C504637` por `-£5,843.70`) es un cargo manual `StockCode = 'M'`, elevando su gasto mercantil real a **`Monetary_Merchandise = £12,397.49`** (tasa de devolución mercantil de `1.43%` en vez de `47.89%`).
3. **Trazabilidad LIFO + Lote Exacto entre Ventanas Temporales (`180d` y `90d`):**
   - Aplicando la resolución determinista **Stage 1 (`9,827`) + Lote Exacto (`1,794`) + LIFO (`3,599`)** sobre los `18,390` abonos con cliente (`15,220` resueltos = `82.76%`), se demostró que de los `3,543` abonos dentro de la ventana histórica `[2011-01-02, 2011-07-01)`, **`654` líneas (`18.46%`, `-£11,284.80`)** son devoluciones de compras realizadas **antes del `2011-01-02`** (en 2009–2010). Al excluir estos abonos de arrastre en **`TotalSpent_InWindowNet`**, **los `4` clientes que tenían `TotalSpent < 0` pasan a saldo positivo (`0` clientes quedan con `< £0.00`)**.
   - En la ventana de observación de 90 días (`[2011-07-01, 2011-09-29)`, `2,024` abonos), **`570` líneas (`28.16%`, `-£12,466.45`)** cancelan compras anteriores al corte `2011-07-01`. Para los **`28` clientes de Clase `0`** que solo tuvieron abonos en los 90 días (`88` líneas), LIFO demuestra que **`77` líneas (`87.50%`)** provienen de compras pre-corte (`76` de la ventana de `180d` y `1` pre-2011).
4. **Integración de Variables Proxy de Marketing, Normalización de Catálogo y Exportación Enriquecida:**
   - Se unificaron los `13` clientes multi-país bajo su `Country` modal canónico, se normalizaron los `4,760` SKUs (`StockCode_Norm`) y se colapsaron **`10,560` líneas de compra partidas intra-factura** en `1,529` clientes RFM (`PurchaseLines_Collapsed = 768,865`, `UniqueSKUs`).
   - Se cuantificó el alto poder discriminante de los proxies de marketing para la fase de modelado: la tasa de recompra a 90 días sube del **`36.48%`** en la Cohorte 2011 al **`52.65%`** en la Cohorte 2010 y al **`67.45%`** en la Cohorte 2009, mientras que los clientes mayoristas con descuento (`DISCOUNT_UserFlag == 1`) alcanzan un **`88.10%` de tasa de recompra** (`£15,036.14` de `Monetary` mediano en RFM vs. `£826.96` en cuentas estándar, y `48.96` órdenes netas medias vs. `5.78`).
   - Se exportaron `outputs/clientes_rfm.csv` (`5,878 × 17`), `outputs/clientes_clasificacion.csv` (`2,724 × 18`), `outputs/resultados_actividad3.json` y 3 figuras de alta resolución en `A-3-5_DataConstruction/figures/`.

---

## 5. Síntesis de Mejoras Consolidadas en `A-3-6_ModelingStrategy` (Completado)

1. **Benchmark Sistemático de Clasificación Supervisada (Base 3 vs. Enriquecido 9 Features):**
   - Se compararon 4 familias de modelos (`DecisionTree`, `LogisticRegression` con `RobustScaler`, `RandomForest` y `GradientBoosting`) bajo partición estratificada 80/20 (`2,179` train / `545` test) y CV 5-fold en train.
   - El conjunto enriquecido pre-corte (`< 2011-07-01` con cero leakage) superó al conjunto base en calibración probabilística y discriminación:
     - **Regresión Logística Enriquecida:** `Test F1 = 0.7104` (vs. `0.6851` base), `Test ROC-AUC = 0.7815`, `Test PR-AUC = 0.8084`, reduciendo el error cuadrático medio Brier a **`0.1906`**.
     - **Random Forest Enriquecido:** `Test PR-AUC = 0.8095` (vs. `0.7880` base), `Test ROC-AUC = 0.7765`, Brier a **`0.1905`**.
   - Las variables más determinantes según Gini MDI fueron `TotalSpent_Merchandise` (`22.42%`), `TotalSpent_InWindowNet` (`22.11%`), `TotalOrders_NetHotFix` (`14.97%`), `RecencyDays` (`14.14%`) y `TenureDays` (`13.45%`).
2. **Deconstrucción de Falsos Positivos: Los `462` Recompradores Estacionales Q4 de Clase `0`:**
   - Se probó empíricamente que **`462` de los `1,315` clientes de Clase `0` (`35.13%`)** regresaron a comprar durante la campaña navideña `[2011-09-29, 2011-12-10]`.
   - En el conjunto de test, el **`52.86%` de los Falsos Positivos predichos por el modelo (37 de 70)** son en realidad compradores leales de ciclo largo que el modelo detectó con una propensión superior ($\hat{p} = 0.415$ vs. $\hat{p} = 0.336$ en verdaderos desertores).
3. **Auditoría de Sensibilidad Forense en Clustering RFM ($K=4$):**
   - Sobre `5,825` cuentas en común, la estabilidad entre la segmentación clásica y la segmentación depurada (`Frequency_NetHotFix`, `Monetary_Merchandise`) es del **`98.42%`** (`96.83%` en cuentas afectadas por Hot-Fix).
   - Se comprobó que **18 de las 20 cuentas con `Monetary < 0` (`90.0%`)** tenían saldo deudor por partidas no mercantiles `'M'`.
   - Se rescató al cliente **`14063`** (`Monetary = -£3,767.20` $\rightarrow$ `Monetary_Merchandise = +£9,471.50`) reclasificándolo como *Cooling regulars*.
   - Se revalorizó al cliente de alta frecuencia **`17017`** de `£6,553.79` a **`£12,397.49`** netos mercantiles (tasa de devolución real física de `1.43%` vs. `47.89%` bruto).
4. **Caracterización Enriquecida con Proxies de Marketing y Matriz de Decisión Comercial:**
   - Se descubrió que el segmento **Champions** concentra el **`81.5%` de mayoristas con descuento negociado (`DISCOUNT_UserFlag == 1`)** y el `63.4%` de los clientes expuestos a fricción operativa de Hot-Fix, con un `91.8%` de retención histórica (cohortes 2009–2010).
   - Se diseñó la **Matriz Multidimensional de Acción Comercial** dividida en 4 programas con presupuestos y KPIs específicos:
     1. *B2B Key Accounts & VIPs* (Account Manager y rappel `StockCode='D'`).
     2. *Reactivación Estacional Q4* (catálogo anticipado en septiembre/octubre para los `462` clientes navideños).
     3. *Onboarding Cohorte 2011* (cross-selling para elevar recompra del `36.5%` al `50%`).
     4. *Exportación y Canal Dotcom* (bonificación de portes `POST` y autoservicio B2B).
5. **Artefactos Exportados y Ejecución al 100%:**
   - Se generaron 9 figuras en `A-3-6_ModelingStrategy/figures/` (incluyendo `fig7_supervised_models_roc_pr_cv.png`, `fig8_rfm_forensic_sensitivity_and_proxies.png` y `fig9_commercial_decision_matrix.png`).
   - Se exportaron los datasets en `outputs/`: `comparacion_modelos.csv`, `predicciones_clasificacion.csv`, `clientes_rfm_segmentados.csv`, `customer_priority_list.csv`, `rfm_segments.csv`, `forecast_test_predictions.csv` y `resultados_actividad4.json`.
   - El cuaderno `NB5 Modeling and Commercial Strategy - Online Retail II.ipynb` (`3.39 MB`) quedó **100% ejecutado** con sus 27 celdas de código completadas y con salidas enriquecidas.

---

## 6. Estado Final del Proyecto CRISP-DM

Con la culminación de la fase **A-3-6**, el ciclo metodológico completo de North Quay Gifts (*Online Retail II*) queda cerrado con éxito:
1. **Fase 2 (Data Understanding):** Auditoría forense del libro mayor atómico (`1,067,371` filas), segregación de mermas, cancelaciones y partidas no mercantiles.
2. **Fase 3 (Data Cleaning & Preparation):** Conciliación temporal bidireccional de abonos, neteo de Hot-Fixes en caliente y desambiguación determinista LIFO.
3. **Fase 4 (Data Construction):** Ingeniería de características analíticas limpias de sesgo operativo y construcción de variables proxy de marketing pre-corte.
4. **Fase 5 & 6 (Modeling & Evaluation):** Modelos predictivos de regresión y clasificación supervisada con calibración probabilística, clustering robusto y plan comercial multidimensional accionable.
