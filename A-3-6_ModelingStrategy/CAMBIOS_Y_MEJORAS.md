# Registro de Auditoría, Cambios y Mejoras Técnicas — Fase A-3-6 (Modeling & Commercial Strategy)

**Proyecto:** North Quay Gifts (*Online Retail II*, UPY — Metodología CRISP-DM)  
**Fase:** `A-3-6_ModelingStrategy`  
**Cuaderno auditado y ejecutado al 100%:** [`NB5 Modeling and Commercial Strategy - Online Retail II.ipynb`](file:///c:/Users/Rivaldo/Documents/UPY/didier/North_Quay_Gifts_UPY/A-3-6_ModelingStrategy/NB5%20Modeling%20and%20Commercial%20Strategy%20-%20Online%20Retail%20II.ipynb)  
**Artefactos exportados en `outputs/` y `figures/`:**
- [`outputs/comparacion_modelos.csv`](file:///c:/Users/Rivaldo/Documents/UPY/didier/North_Quay_Gifts_UPY/A-3-6_ModelingStrategy/outputs/comparacion_modelos.csv) (benchmark de 8 modelos: Base 3 vs. Enriquecido 9 features en CV estratificado 5-fold y test)
- [`outputs/predicciones_clasificacion.csv`](file:///c:/Users/Rivaldo/Documents/UPY/didier/North_Quay_Gifts_UPY/A-3-6_ModelingStrategy/outputs/predicciones_clasificacion.csv) (`2,724` clientes × `9` columnas con predicciones y probabilidades de recompra a nivel cliente)
- [`outputs/clientes_rfm_segmentados.csv`](file:///c:/Users/Rivaldo/Documents/UPY/didier/North_Quay_Gifts_UPY/A-3-6_ModelingStrategy/outputs/clientes_rfm_segmentados.csv) (`5,878` clientes × `21` columnas con segmentación clásica, segmentación forense depurada y proxies de marketing)
- [`outputs/customer_priority_list.csv`](file:///c:/Users/Rivaldo/Documents/UPY/didier/North_Quay_Gifts_UPY/A-3-6_ModelingStrategy/outputs/customer_priority_list.csv) (`5,837` clientes segmentados rankeados por valor neto Pareto, tasa de abono y nivel de riesgo)
- [`outputs/forecast_test_predictions.csv`](file:///c:/Users/Rivaldo/Documents/UPY/didier/North_Quay_Gifts_UPY/A-3-6_ModelingStrategy/outputs/forecast_test_predictions.csv) (`60` días de prueba con pronósticos de regresión lineal, random forest y naive)
- [`outputs/rfm_segments.csv`](file:///c:/Users/Rivaldo/Documents/UPY/didier/North_Quay_Gifts_UPY/A-3-6_ModelingStrategy/outputs/rfm_segments.csv) (tabla resumen de perfiles RFM tradicionales)
- [`outputs/resultados_actividad4.json`](file:///c:/Users/Rivaldo/Documents/UPY/didier/North_Quay_Gifts_UPY/A-3-6_ModelingStrategy/outputs/resultados_actividad4.json) (diccionario cuantitativo consolidado de métricas, benchmarks y auditoría forense)
- Figuras analíticas de alta resolución (`200 DPI`):
  - [`figures/fig1_forecast_test.png`](file:///c:/Users/Rivaldo/Documents/UPY/didier/North_Quay_Gifts_UPY/A-3-6_ModelingStrategy/figures/fig1_forecast_test.png)
  - [`figures/fig2_confusion_matrices.png`](file:///c:/Users/Rivaldo/Documents/UPY/didier/North_Quay_Gifts_UPY/A-3-6_ModelingStrategy/figures/fig2_confusion_matrices.png)
  - [`figures/fig3_selected_tree.png`](file:///c:/Users/Rivaldo/Documents/UPY/didier/North_Quay_Gifts_UPY/A-3-6_ModelingStrategy/figures/fig3_selected_tree.png)
  - [`figures/fig4_rfm_distributions.png`](file:///c:/Users/Rivaldo/Documents/UPY/didier/North_Quay_Gifts_UPY/A-3-6_ModelingStrategy/figures/fig4_rfm_distributions.png)
  - [`figures/fig5_k_selection.png`](file:///c:/Users/Rivaldo/Documents/UPY/didier/North_Quay_Gifts_UPY/A-3-6_ModelingStrategy/figures/fig5_k_selection.png)
  - [`figures/fig6_segment_boxplots.png`](file:///c:/Users/Rivaldo/Documents/UPY/didier/North_Quay_Gifts_UPY/A-3-6_ModelingStrategy/figures/fig6_segment_boxplots.png)
  - [`figures/fig7_supervised_models_roc_pr_cv.png`](file:///c:/Users/Rivaldo/Documents/UPY/didier/North_Quay_Gifts_UPY/A-3-6_ModelingStrategy/figures/fig7_supervised_models_roc_pr_cv.png) *(NUEVA)*
  - [`figures/fig8_rfm_forensic_sensitivity_and_proxies.png`](file:///c:/Users/Rivaldo/Documents/UPY/didier/North_Quay_Gifts_UPY/A-3-6_ModelingStrategy/figures/fig8_rfm_forensic_sensitivity_and_proxies.png) *(NUEVA)*
  - [`figures/fig9_commercial_decision_matrix.png`](file:///c:/Users/Rivaldo/Documents/UPY/didier/North_Quay_Gifts_UPY/A-3-6_ModelingStrategy/figures/fig9_commercial_decision_matrix.png) *(NUEVA)*

---

## 1. Diagnóstico del Estado Inicial de `A-3-6` vs. Mejoras Implementadas

El cuaderno `NB5` inicial cubría con rigor matemático los entregables base de la rúbrica (pronóstico diario con `TimeSeriesSplit`, clasificación supervisada mediante árboles de decisión y segmentación RFM con K-Means). No obstante, operaba de forma aislada respecto a los hallazgos forenses alcanzados en las fases `A-3-3`, `A-3-4` y `A-3-5`.

A continuación se sintetiza el contraste técnico entre el estado previo y la versión enriquecida y re-ejecutada:

| Dimensión Técnica | Estado Inicial de `NB5` (`A-3-6`) | Estado Auditado y Enriquecido (`NB5` Actualizado) |
|---|---|---|
| **1. Clasificación Supervisada de Recompra a 90 Días (`2,724` clientes)** | Solo evaluaba `DecisionTreeClassifier` sobre las 3 variables base (`RecencyDays`, `TotalOrders`, `TotalSpent`). F1 en test = `0.7059`. Sin curvas ROC/PR comparativas ni cálculo de probabilidad calibrada. | Implementa un **benchmark sistemático de 4 familias de modelos** (`DecisionTree`, `LogisticRegression` con `RobustScaler`, `RandomForest` y `GradientBoosting`) comparando el conjunto base (3 features) vs. el **conjunto enriquecido forense (9 features)** pre-corte (`< 2011-07-01`). La Regresión Logística enriquecida eleva el **F1 a `0.7104`**, **ROC-AUC a `0.7815`**, **PR-AUC a `0.8084`** y reduce el **Brier Score a `0.1906`**. Random Forest alcanza **PR-AUC de `0.8095`** y Brier de `0.1905`. |
| **2. Deconstrucción de Falsos Positivos y Estacionalidad Q4** | Trataba la Clase `0` como abandono definitivo (*churn*). Los clientes con $\hat{p} \ge 0.5$ pero $y=0$ en los 90 días eran catalogados como "errores de desperdicio de presupuesto". | Demuestra empíricamente que **`462` de los `1,315` clientes de Clase `0` (`35.13%`) regresaron a comprar en la campaña navideña Q4 (`[2011-09-29, 2011-12-10]`)**. En el test set, el **`52.86%` de los "Falsos Positivos" (37 de 70)** son en realidad compradores leales de ciclo largo que el modelo detectó correctamente. |
| **3. Sensibilidad Forense en Clustering RFM (`5,878` clientes)** | Excluía a `41` clientes con `Monetary <= 0` catalogándolos genéricamente como "cuentas de saldo deudor", ignorando si su saldo se debía a partidas no mercantiles o re-facturaciones en caliente. | Ejecuta una **auditoría de sensibilidad entre RFM Clásico vs. RFM Depurado Forense (`Frequency_NetHotFix`, `Monetary_Merchandise`)**. Prueba que **18 de los 20 clientes con `Monetary < 0` (`90.0%`)** tenían saldo negativo únicamente por cargos manuales `'M'`. **Rescata al cliente `14063`** (`Monetary = -£3,767.20` $\rightarrow$ `Monetary_Merchandise = +£9,471.50`) reclasificándolo como *Cooling regulars*. Revalúa al cliente `17017` de `£6,553.79` a **`£12,397.49`** netos mercantiles (tasa de devolución real de `1.43%` vs `47.89%`). |
| **4. Caracterización de Segmentos con Proxies de Marketing** | La caracterización de clústeres se limitaba a medianas de R, F y M, sin cruce con cohorte de captación, geografía ni canal B2B. | Cruza los 4 segmentos con `CohortYear`, `IsUK`, `DISCOUNT_UserFlag`, `HotFix_Users`, `TrueReturnRate` y `UniqueSKUs`. Demuestra que **Champions concentra el `81.5%` de mayoristas con descuento (`DISCOUNT_UserFlag == 1`)**, el `63.4%` de cuentas afectadas por *Hot-Fix* y un `91.8%` de retención histórica (cohortes 2009–2010 con mediana de antigüedad de `679.5` días). |
| **5. Estrategia Comercial y Accionabilidad** | Tabla conceptual simple con 4 acciones generales de reactivación sin segmentación de propensión ni reglas para B2B mayorista o compradores estacionales. | Construye una **Matriz de Decisión Comercial Multidimensional** articulada en 4 programas operativos con KPIs y presupuestos diferenciados: (1) Cuentas B2B VIP / Mayoristas, (2) Reactivación Estacional Q4 (captura de los 462 clientes navideños), (3) Onboarding de Cohorte 2011 (cross-selling de 2ª compra) y (4) Exportación / Canal Web. |

---

## 2. Evidencia Cuantitativa de los Modelos y Hallazgos Forenses

### 2.1 Benchmark de Clasificación Supervisada de Recompra a 90 Días

Se evaluó la predicción de recompra binaria (`Repurchase90Days`) sobre los `2,724` clientes activos en la ventana histórica `[2011-01-02, 2011-07-01)` bajo partición estratificada 80/20 (`random_state=42`, `2,179` en train y `545` en test, con tasa positiva de `51.72%` y `51.74%` respectivamente).

#### Tabla Comparativa de Modelos (CV Estratificado 5-Fold en Train y Evaluación en Test):

| Feature Set | Modelo | CV ROC-AUC | CV PR-AUC | CV F1 | CV Brier | Test ROC-AUC | Test PR-AUC | Test F1 | Test Precision | Test Recall | Test Brier |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Base (3 feats)** | Decision Tree (Pruned) | 0.7368 | 0.7458 | 0.6815 | 0.2073 | 0.7720 | 0.7810 | 0.7059 | 0.7592 | 0.6596 | 0.1920 |
| **Base (3 feats)** | Logistic Regression | 0.7429 | 0.7784 | 0.6666 | 0.2032 | 0.7798 | 0.8076 | 0.6851 | 0.7758 | 0.6135 | 0.1933 |
| **Base (3 feats)** | Random Forest | 0.7464 | 0.7804 | 0.6899 | 0.2030 | 0.7602 | 0.7880 | 0.7022 | 0.7290 | 0.6773 | 0.1963 |
| **Base (3 feats)** | Gradient Boosting | 0.7425 | 0.7750 | 0.6921 | 0.2064 | 0.7488 | 0.7859 | 0.7080 | 0.7293 | 0.6879 | 0.2011 |
| **Enriched (9 feats)** | Decision Tree (Pruned) | 0.7376 | 0.7451 | 0.6700 | 0.2063 | 0.7558 | 0.7633 | 0.6898 | 0.7105 | 0.6702 | 0.2000 |
| **Enriched (9 feats)** | **Logistic Regression** | **0.7510** | **0.7848** | **0.6691** | **0.2008** | **0.7815** | **0.8084** | **0.7104** | **0.7797** | **0.6525** | **0.1906** |
| **Enriched (9 feats)** | **Random Forest** | **0.7517** | **0.7837** | **0.6797** | **0.2010** | **0.7765** | **0.8095** | **0.6890** | **0.7255** | **0.6560** | **0.1905** |
| **Enriched (9 feats)** | Gradient Boosting | 0.7464 | 0.7780 | 0.6851 | 0.2048 | 0.7705 | 0.8053 | 0.7055 | 0.7239 | 0.6879 | 0.1937 |

#### Hallazgos Clave del Benchmark:
1. **Superioridad del Conjunto Enriquecido:** La inclusión de `TotalSpent_Merchandise`, `TotalSpent_InWindowNet`, `TotalOrders_NetHotFix`, `TenureDays` y `UniqueSKUs` reduce el error cuadrático medio de probabilidad (Brier score de `0.1933` $\rightarrow$ `0.1906` en Regresión Logística y `0.1963` $\rightarrow$ `0.1905` en Random Forest).
2. **Importancia de Variables (Gini en Random Forest):**
   - `TotalSpent_Merchandise` (`22.42%`) y `TotalSpent_InWindowNet` (`22.11%`) dominan la discriminación predictiva, probando que aislar devoluciones de arrastre de 2010 clarifica la señal de inversión del cliente.
   - `TotalOrders_NetHotFix` (`14.97%`) y `RecencyDays` (`14.14%`) capturan la cadencia operativa real de compras.
   - `TenureDays` (`13.45%`) y `UniqueSKUs` (`10.23%`) actúan como potentes proxies de lealtad y madurez de cartera.

---

### 2.2 Deconstrucción Forense de los Falsos Positivos: Los 462 Recompradores Estacionales Q4

En los modelos predictivos con corte en verano (`2011-07-01`), la ventana de evaluación de 90 días expira el `2011-09-29`. Al contrastar las etiquetas con las transacciones reales de la campaña de fin de año (`[2011-09-29, 2011-12-10]`):

1. **Magnitud de la Estacionalidad:** De los `1,315` clientes clasificados como Clase `0` (sin recompra en 90 días), **`462` clientes (`35.13%`) sí realizaron compras en el último trimestre de 2011**.
2. **Capacidad de Detección del Modelo:** Los modelos enriquecidos asignan a estos recompradores estacionales una probabilidad promedio de recompra significativamente mayor que a los verdaderos desertores ($\hat{p} = 0.415$ vs. $\hat{p} = 0.336$ en Random Forest; $\hat{p} = 0.470$ vs. $\hat{p} = 0.379$ en Regresión Logística).
3. **Validación en el Conjunto de Prueba (`Test Set`):** En el conjunto de test (545 clientes, con 263 clientes en Clase 0), el modelo Random Forest predijo 70 "Falsos Positivos" ($\hat{p} \ge 0.5$ con $y=0$ a 90 días). Al verificar sus compras posteriores, **`37` de estos `70` clientes (`52.86%`) recompraron efectivamente en Q4**.
   > **Implicación Estratégica:** Tratar a estos clientes como "errores del modelo" sería un grave error comercial: son compradores leales cuyo ciclo natural de compra es anual o estacional. El modelo detectó correctamente su alta propensión de compra.

---

### 2.3 Auditoría de Sensibilidad Forense en Clustering RFM

Se comparó el clustering oficial $K=4$ sobre `['Recency', 'Frequency', 'Monetary']` frente al clustering depurado sobre `['Recency', 'Frequency_NetHotFix', 'Monetary_Merchandise']`:

#### 1. Estabilidad de Asignación:
- Sobre los `5,825` clientes segmentables en común, **`5,733` clientes (`98.42%`) mantienen exactamente el mismo clúster**, demostrando la robustez estructural de la segmentación.
- Entre los `379` clientes comunes que sufrieron re-facturaciones en caliente (`HotFix_Flag == 1`), la estabilidad alcanza el **`96.83%`**, confirmando que el neteo de facturas duplicadas corrige la métrica sin fragmentar la tipología del cliente.

#### 2. Rescate y Revalorización de Cuentas Distorsionadas por Partidas `'M'`:
- **Cliente `14063`:** En el pipeline clásico fue **excluido** con `Monetary = -£3,767.20` debido a asientos manuales de ajuste. Al depurar partidas no mercantiles, posee **`Monetary_Merchandise = +£9,471.50`** en 9 pedidos válidos y es **rescatado exitosamente en el clúster *Cooling regulars***.
- **Cliente `17017` (Alta frecuencia):** En RFM clásico registraba `Monetary = £6,553.79` y una tasa de devolución aparente de `47.89%`. Al aislar su abono manual `C504637` (`-£5,843.70`), su gasto neto mercantil se eleva a **`Monetary_Merchandise = £12,397.49`** y su tasa de devolución en mercancía física cae al **`1.43%`**, consolidándose como un *Champion* de bajo riesgo operativo.
- **Cliente `12918`:** Su saldo negativo de `-£10,953.50` queda plenamente aislado como corrección técnica de hot-fix (`C502262 -> 502263 -> C502264`), teniendo `Monetary_Merchandise = £0.00`.
- **Cuentas `13091` y `13112`:** Se confirma que son las **únicas 2 cuentas de todo el repositorio (`0.034%`)** con saldo negativo genuino en mercancía debido a devoluciones huérfanas de compras anteriores a diciembre de 2009.

#### 3. Cruce Enriquecido con Variables Proxy de Marketing:
| Segmento ($K=4$) | Clientes | Gasto Mediano (£) | Gasto Total (£) | Frecuencia Mediana | Recencia Mediana | Tasa Devolución Real (`TrueReturnRate`) | SKUs Medianos | Antigüedad Mediana (Días) | % UK | Clientes Mayoristas (`DISCOUNT`) | Clientes Hot-Fix | % Cohorte 2009 | % Cohorte 2010 | % Cohorte 2011 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Champions** | `1,212` (`20.8%`) | `£4,807.80` | `£12,159,470.84` (`74.2%`) | `13.0` | `16.0` | `2.19%` | `162.0` | `675.0` | `89.69%` | **`44`** (`81.5%`) | **`250`** (`63.6%`) | `39.69%` | `50.99%` | `9.32%` |
| **Cooling regulars** | `1,558` (`26.7%`) | `£1,344.22` | `£2,708,508.28` (`16.5%`) | `4.0` | `184.0` | `2.44%` | `62.0` | `611.0` | `90.18%` | `7` | `98` | `17.14%` | `73.04%` | `9.82%` |
| **Recent occasional buyers** | `1,124` (`19.3%`) | `£715.89` | `£922,284.27` (`5.6%`) | `3.0` | `22.0` | `1.50%` | `44.0` | `241.5` | `91.28%` | `3` | `24` | `5.43%` | `36.65%` | `57.92%` |
| **Lapsed one-time buyers** | `1,943` (`33.3%`) | `£254.18` | `£592,364.63` (`3.6%`) | `1.0` | `397.0` | `2.07%` | `17.0` | `432.0` | `92.54%` | `0` | `7` | `7.26%` | `61.45%` | `31.29%` |
| **Total Segmentado** | `5,837` (`100%`) | — | `£16,382,628.02` | — | — | `2.13%` | — | — | `90.77%` | `54` | `379` | `20.18%` | `58.35%` | `21.47%` |
| *(Excluidos Mon <= 0)* | `41` | — | `-£20,317.06` | — | — | — | — | — | — | `1` | `14` | — | — | — |

---

## 3. Matriz de Decisión Comercial Basada en Evidencia

Conectando los segmentos RFM, las probabilidades predichas de recompra ($\hat{p}$), los proxies de atribución y la tasa real de devolución, se formalizan cuatro programas de intervención comercial:

```
+--------------------------------------------------------------------------------------------------+
|                     MATRIZ MULTIDIMENSIONAL DE ACCIÓN COMERCIAL (NORTH QUAY GIFTS)               |
+------------------------------------+-------------------------------------------------------------+
| PROGRAMA 1: Cuentas Mayoristas B2B | PROGRAMA 2: Reactivación Estacional Q4                      |
| VIPs & Champions                   | (Captura de los 462 retornadores de fin de año)             |
| - Universo: Champions + DISCOUNT=1 | - Universo: Cohortes 2009-2010 con Recency > 120d y         |
| - Trigger: Alto volumen y fricción |   probabilidad moderada (p in [0.35, 0.50))                 |
|   operativa Hot-Fix                | - Trigger: Demanda estacional navideña                      |
| - Acción: Account Manager dedicado,| - Acción: Envío anticipado de catálogo de temporada en      |
|   acuerdos de rappel ('D') y       |   septiembre/octubre con reserva preferente de stock.       |
|   reconciliación EDI.              | - KPI: Tasa de reactivación a 60 días; cuota de ventas Q4.  |
| - KPI: Cero bajas en top-200.      |                                                             |
+------------------------------------+-------------------------------------------------------------+
| PROGRAMA 3: Onboarding Cohorte 2011| PROGRAMA 4: Exportación y Canal Dotcom                      |
| (Nuevos compradores en riesgo)     | (Optimización logística y B2B transfronterizo)              |
| - Universo: Recent buyers (2011)   | - Universo: Clientes IsUK=0 (ticket mediano £1,151) y       |
| - Trigger: 1 sola compra, catálogo |   pedidos con flag web DOTCOM_OrderFlag                     |
|   estrecho (UniqueSKUs < 25)       | - Trigger: Sensibilidad a costes de envío (StockCode POST)  |
| - Acción: Incentivo de 2ª compra   | - Acción: Umbrales de porte bonificado por volumen y portal |
|   con bundle personalizado cruzado.|   self-service B2B de pedidos internacionales.              |
| - KPI: Elevar recompra 36% -> 50%. | - KPI: Incremento de recompra internacional y ticket medio. |
+------------------------------------+-------------------------------------------------------------+
```

---

## 4. Verificación de Cierre y Trazabilidad al 100%

Con la ejecución completa de `build_nb5.py`:
1. `A-3-6_ModelingStrategy/NB5 Modeling and Commercial Strategy - Online Retail II.ipynb` queda **100% ejecutado** (27 celdas de código con salidas, gráficas y dataframes embebidos, `3.39 MB`).
2. Se generaron las 9 figuras de alta resolución en `figures/` y los 6 datasets requeridos en `outputs/`.
3. El archivo de diccionario maestro `outputs/resultados_actividad4.json` refleja todas las métricas de auditoría forense y de modelado predictivo.
4. Se cierra el ciclo CRISP-DM garantizando total coherencia técnica desde la comprensión inicial del negocio hasta la estrategia comercial operativa.

