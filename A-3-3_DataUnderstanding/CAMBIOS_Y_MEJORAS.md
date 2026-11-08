# Fase A-3-3: Entendimiento y Exploración de Datos (Data Understanding)
## Registro de Actualizaciones, Auditoría de Marketing y Análisis de Cancelaciones

**Proyecto:** North Quay Gifts — CRISP-DM Fase 2: Data Understanding  
**Dataset:** `online_retail_II.csv` (1,067,371 filas × 8 columnas)  
**Fecha de Actualización:** Noviembre 2026  
**Equipo:** Russel Ku, Damian Sanchez, Jonathan Velasco, Ángel Canché, Bianca Acosta  

---

### 1. Resumen Ejecutivo de la Intervención
En esta revisión integral se subsanaron las deficiencias críticas de calidad analítica de la entrega previa, abordando dos ejes cardinales que estaban ausentes o generaban confusión metodológica:
1. **Auditoría de Gobernanza y Ceguera de Atribución de Marketing:** Se diagnosticó la ausencia absoluta de variables de tracking en la base transaccional y se formularon las restricciones de negocio y la estrategia de mitigación mediante variables proxy para las fases subsecuentes.
2. **Anatomía Empírica de Cancelaciones y Re-facturación ("Al tiempo después salía la verdadera"):** Se desentrañó el comportamiento de las líneas con prefijo `'C'` y cantidades negativas, demostrando con evidencia cuantitativa que más del 41% de las cancelaciones están ligadas a sustituciones temporales, carritos re-facturados en caliente y pedidos definitivos posteriores.

---

### 2. Auditoría de Trazabilidad y Variables de Marketing (Tracking Blind Spot)

#### 2.1. Diagnóstico del Esquema Original
El archivo `online_retail_II.csv` contiene únicamente 8 atributos operativos:
`Invoice`, `StockCode`, `Description`, `Quantity`, `InvoiceDate`, `Price`, `Customer ID`, `Country`.

Se constata una **ausencia total (0 variables)** de metadatos de marketing digital:
- **Sin parámetros UTM:** Ausencia de `utm_source`, `utm_medium`, `utm_campaign`, `utm_content` y `utm_term`.
- **Sin canal de captación:** No se distingue entre tráfico orgánico, campañas de pago (Google Ads, Facebook Ads), email marketing, afiliados o venta directa.
- **Sin cupones o promociones ligadas al pedido:** No existe un identificador de código promocional o campaña de descuento en cabecera de factura.
- **Sin telemetría de navegación (Clickstream):** No se dispone de identificador de sesión web, URL de referencia (referrer) ni embudo de conversión.
- **Sin fecha explícita de captación:** La fecha de adquisición del cliente solo puede inferirse a partir de su primera compra observada en el ledger.

#### 2.2. Impacto Analítico y de Negocio
- **Ceguera de Atribución Comercial:** Es matemáticamente imposible atribuir transacciones, ingresos o cancelaciones a campañas de marketing específicas.
- **Imposibilidad de cálculo directo de CAC y ROMI:** No se puede computar el Costo de Adquisición de Clientes (CAC) ni el Retorno del Gasto en Marketing (ROMI) a nivel transaccional ni de cliente individual.
- **Riesgo de Antiselección Promocional no Observable:** No es posible medir directamente si los cupones de descuento agresivos atrajeron compradores con mayor propensión a la devolución de producto o deserción prematura (churn).

#### 2.3. Señales Indirectas y Estrategia de Mitigación
Se auditaron descripciones y códigos especiales que dan cuenta de la operación comercial externa:
- **Descuentos Comerciales Manuales (`StockCode == 'D'`):** 177 líneas acumulando $-\pounds 13,484.54$ distribuidas en 55 clientes mayoristas.
- **Ventas Directas de Comercio Electrónico (`StockCode == 'DOT'`):** 1,446 líneas de *DOTCOM POSTAGE*, evidenciando costos de envío de plataforma web propia.
- **Comisiones de Plataforma Externa (`Description` con *'AMAZON FEE'*):** 39 líneas con comisiones deducidas por ventas en el marketplace de Amazon.

**Estrategia para Fases 3, 4 y 5:**
1. *Cohortes Mensuales de Adquisición:* Agrupar clientes por mes de primera transacción observada para rastrear la retención y valor neto en el tiempo.
2. *Segmentación Geográfica y Estacional:* Diferenciar la base británica local (91.94% de líneas) del mercado internacional (8.06%) y sus picos estacionales del último trimestre (Navidad / Black Friday).
3. *Recomendación a IT/Ingeniería Web:* Instrumentar la pasarela de pago para capturar obligatoriamente los parámetros UTM y códigos de cupón en la tabla transaccional.
4. *Soporte Visual:* Se incorporó la **Figura 8** (`figures/fig8_marketing_tracking_audit.png`) detallando la comparativa entre variables disponibles vs. faltantes y la cobertura de los proxies.

---

### 3. Anatomía Empírica de Cancelaciones y Re-facturación

#### 3.1. Hallazgo Central: "Salía la Verdadera Después"
El análisis previo trataba ingenuamente cualquier registro con prefijo `'C'` o cantidad negativa como una devolución de mercancía simple o un abandono. El análisis cruzado de transacciones positivas y negativas para una misma combinación de `Customer ID` y `StockCode` revela una realidad operativa más compleja:

| Arquetipo de Transacción Negativa | Líneas | % sobre Líneas Apareadas / Totales | Explicación Operativa |
| :--- | :--- | :--- | :--- |
| **Devoluciones Puras Post-Compra** | `9,769` | **58.04%** | Compra positiva regular seguida días o semanas después por nota de crédito / devolución física. |
| **Re-facturación y Sustitución Posterior** | `7,062` | **41.96%** | La anulación precede o coexiste con una factura de venta positiva posterior para el mismo ítem. |
| *• Correcciones en caliente (< 24 horas)* | `1,397` | **8.30%** | Corrección inmediata en 1 a 5 minutos por cambio en carrito, error tipográfico o fallo de pasarela. |
| *• Re-facturación rápida (1 a 7 días)* | `1,820` | **10.81%** | Recompra tras confirmación de stock o clarificación de pago. |
| *• Recompra en ciclo posterior (> 7 días)* | `3,845` | **22.85%** | Devolución seguida de nueva orden regular en compras subsecuentes. |
| **Cancelaciones Huérfanas (Censuradas)** | `1,484` | **7.92% de líneas C con cliente** | Devoluciones sin compra positiva registrada en 2009–2011 (compras pre-diciembre 2009 o compras en mostrador devueltas con ticket). |
| **Cancelaciones Múltiples Repetidas** | `1,993 parejas` | **12.86% de parejas con C** | Parejas Cliente-SKU con $\ge 2$ cancelaciones registradas (hasta 61 cancelaciones por reintentos de sistema o devoluciones escalonadas de lotes mayoristas). |
| **Mermas de Almacén sin Prefijo C** | `3,457` | **15.06% de todos los negativos** | 100% con `Price = £0.00` y `Customer ID = NaN` (*damages, check, smashed, thrown away*). Pérdidas físicas de bodega, **no** comportamiento del cliente. |
| **Ajustes Contables de Deuda Incobrable** | `5` | **0.0005%** | Facturas serie `'A'` (`StockCode B`, hasta $-\pounds 53,594.36$). Asientos financieros corporativos sin mercancía. |

#### 3.2. Casos Concretos de Corrección en Minutos Verificados
- **Cliente 15967.0:** Anulación `C489570` (2009-12-01 13:28) $\rightarrow$ Factura limpia definitiva `489571` (2009-12-01 13:29), brecha de **1 minuto**.
- **Cliente 12352.0:** Anulación `C545329` (2011-03-01 15:47) $\rightarrow$ Factura definitiva corregida `545332` (2011-03-01 15:52), brecha de **5 minutos**.
- **Cliente 12483.0:** Anulación `C501400` (2010-03-16 11:28) $\rightarrow$ Factura limpia `501403` (2010-03-16 11:29), brecha de **1 minuto**.
- **Cliente 16713.0:** Anulación `C529568` (2010-10-28 18:40) $\rightarrow$ Factura definitiva `529569` (2010-10-28 18:41), brecha de **1 minuto**.

#### 3.3. Peligro Metodológico de la Doble Contabilización
Si en la preparación de datos se suman las compras brutas y se restan las cancelaciones de manera no apareada:
1. Se sobrestima artificialmente la frecuencia de compra del cliente (un solo pedido cuenta como 3 transacciones: compra errónea, anulación y compra corregida).
2. Se distorsiona el ticket promedio y la propensión real a la devolución, castigando en los modelos a compradores fieles cuyos pedidos sufrieron ajustes administrativos.
3. **Decisión metodológica para Fase A-3-4:** Ejecutar un algoritmo de conciliación temporal que netee las parejas de anulación/re-facturación inmediatas antes de calcular métricas de RFM y propensión al abandono.

---

### 4. Matriz Estratégica del Plan de Acción (Fase 3)

| Problema Identificado | Evidencia Cuantitativa | Posible Impacto Empresarial | Tratamiento Propuesto |
| :--- | :--- | :--- | :--- |
| **Nulos en Customer ID** | 243,007 líneas (22.77% del dataset). | Sesgo grave en CLV y segmentación; descartarlas pierde 22.8% de ventas en caja. | **Pipeline Bifurcado:** Aislar cuentas identificadas para CRM/CLV; retener compras anónimas como demanda agregada de almacén. |
| **Duplicados Exactos** | 34,335 líneas adicionales (3.22%). Ejemplo: Factura 489517 a las 11:34:00. | Inflación artificial de unidades vendidas, ingresos facturados y frecuencia. | Deduplicar mediante `df.drop_duplicates(keep='first')`. Auditar reintentos de red en pasarela web. |
| **Mermas sin Prefijo C** | 3,457 líneas (0.32%), 100% `Price=0` y `Customer ID` nulo (*check, damages*). | Confusión entre mermas físicas de almacén y comportamiento de devolución de clientes. | **Segregación Operativa:** Canalizar a auditoría de merma de inventario; excluir permanentemente de ventas retail. |
| **Precios No Positivos** | 5 líneas con `Price < 0` (hasta $-\pounds 53,594.36$ en A506401); 6,202 con `Price = 0`. | Distorsión masiva de ingresos y márgenes brutos por asientos contables de deuda incobrable. | Excluir partidas contables serie `'A'` de ventas comerciales. Auditar registros en cero como muestras promocionales. |
| **Cancelaciones Comerciales ('C')** | 19,494 líneas (1.83%), 19,493 $Q<0$ y 1 $Q>0$ (`C496350`, Manual). | Cálculo erróneo de ingresos brutos si no se concilian con la venta original. | Conciliar cancelaciones con órdenes originales para calcular ventas netas y tasa de devolución individual. |
| **Re-facturaciones y Desfase Temporal** | 7,062 líneas C seguidas de venta positiva (41.96%), 1,397 en $<24$h; 1,484 líneas huérfanas pre-2009. | Doble contabilización de ingresos y distorsión de la tasa real de abandono/devolución. | **Algoritmo de Conciliación Temporal:** Netear cancelaciones inmediatas con su orden corregida antes de calcular frecuencia y CLV. |
| **Ceguera de Atribución de Marketing** | 0 variables de tracking (sin UTMs, sin canal, sin código de cupón/descuento por orden). | Imposibilidad de atribuir ventas/churn a campañas o calcular CAC y ROMI transaccional. | Instrumentar captura obligatoria de UTMs y cupones en pasarela web; emplear cohortes mensuales de captación como proxy analítico. |

---

### 5. Prioridad de Preparación y Riesgo Residual (Pregunta 14)

**Prioridad y justificación:**  
La prioridad inmediata es la bifurcación del pipeline respecto a los nulos en `Customer ID` (243,007 líneas, 22.77%), la exclusión de partidas contables no comerciales (6,207 líneas con `Price <= 0`) y la conciliación temporal de cancelaciones re-facturadas (7,062 líneas con compras posteriores). Intentar entrenar modelos de Valor de Vida del Cliente (CLV) o churn sin netear anulaciones inmediatas (como `C489570` y `489571` en 1 minuto) sobrestimaría la frecuencia y penalizaría falsamente a clientes recurrentes. Debemos separar los datos: clientes identificados y saneados alimentan los modelos predictivos de CRM, mientras que ventas anónimas se retienen para demanda agregada de bodega.

**Riesgo residual persistente:**  
La ceguera de atribución de marketing (0 variables UTM o canal) y la heterogeneidad de compradores mayoristas B2B. Sus compras masivas e intermitentes pueden sesgar las predicciones minoristas, y al no disponer de costos logísticos ni etiquetas de campaña de origen, los modelos quedan expuestos a fluctuaciones de pedidos al por mayor y no pueden realizar atribución multitáctil.

---

### 6. Estado de Entregables Técnicos en la Carpeta
- `NB2 Exploración de Datos - Online Retail II.ipynb`: Cuaderno Jupyter de 49 celdas completamente estructurado y ejecutado, incluyendo las tablas de diagnóstico de marketing y cancelaciones temporales.
- `figures/fig7_cancellations_anatomy.png`: Gráfico de alta resolución con la anatomía empírica de cancelaciones y ventanas de re-facturación.
- `figures/fig8_marketing_tracking_audit.png`: Gráfico de gobernanza con la brecha de variables de marketing y estrategia de proxies.
- `CAMBIOS_Y_MEJORAS.md`: Este documento de auditoría y control de cambios para la fase.

