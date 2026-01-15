# Methodology

This document describes the analytical approach applied in this project.  
The focus is on **business-oriented process analysis**, transparent prioritization, and a strict separation between **observable execution behavior** and **data or logging artifacts**.

---

## Analytical Framing

The analysis is guided by the following management-oriented question:

**Where does actual Order-to-Cash (O2C) execution deviate from the intended operational flow, and which deviations create material execution risk requiring management attention?**

The objective is **not** to describe the end-to-end process exhaustively, but to identify **execution instability with measurable business impact**.

To ensure a structured and value-driven approach, the project follows the **Celonis Enhancement Cycle**:

**Identify → Quantify → Analyze → Improve → Control**

The analytical focus is explicitly on **execution behavior and operational stability**, not on system configuration or tool demonstration.

---

## Event Ordering and Data Interpretation

An initial data assessment showed that activity timestamps in the event log are **not sufficiently reliable to derive the true business execution sequence**.

Systematic inconsistencies occur due to:
- batch-based logging,
- delayed or retroactive status updates,
- technical planning or release events logged independently of physical execution.

Therefore, **timestamp-based ordering is not used to define the process flow**.

Instead, the provided **SORTING attribute is used as the business reference order**, as it reflects the **intended and logically defined execution sequence**.

Timestamps are used exclusively for:
- duration measurement, and
- cycle-time calculation,

but **never for sequencing**.

This ensures that observed deviations reflect **real execution behavior**, not logging artifacts.

---

## Happy Path Definition

A simplified **Happy Path** is defined as an analytical baseline representing the **business-intended O2C execution flow**, derived from the SORTING logic.

The Happy Path includes only core execution steps:

- Order received  
- Confirm sale  
- Start production *(interpreted as a planning or release trigger)*  
- Finished production  
- Load shipment  
- Goods delivered  

All change and rework activities (e.g. price changes, quantity changes, delivery date changes, production start date changes) are **explicitly excluded**.

The Happy Path is:
- **not** a target-state process,
- **not** a best-practice claim,

but a **stable reference baseline** used to:
- quantify execution deviations,
- compare throughput times (TPT),
- isolate **post-release execution effects**.

---

## Execution Gaps

Execution Gaps are defined as **systematic deviations from the Happy Path** that occur **after order release** and affect execution stability.

Examples include:
- post-release quantity corrections,
- repeated production start date changes after production start,
- credit blocks,
- repeated price rework triggering downstream changes,
- extended waiting times between core execution steps.

Importantly:
- Deviations caused solely by timestamp inconsistencies or logging artifacts are **explicitly excluded**.
- Execution Gaps are treated as **observable symptoms**, not as root causes.

At this stage, the analysis answers **what breaks and where**, not **why it breaks**.

---

## Quantification & Prioritization Logic

Each identified Execution Gap is quantified using a consistent and transparent structure:

- **Share of affected orders** (% of cases),
- **Additional cycle time** compared to the Happy Path (median TPT delta),
- **Value exposure** (order value of affected cases),
- **Execution risk**, reflecting:
  - likelihood of occurrence,
  - severity of delay once triggered,
  - operational controllability.

Execution Gaps are **not prioritized by frequency alone**.

Priority is given to gaps that combine:
- material cycle-time impact,
- high value exposure,
- and clear operational actionability.

This ensures that management attention is directed toward **high-impact execution problems**, not statistical noise.

---

## Root Cause Analysis – Filter-Based Approach

Root cause analysis is conducted **only for prioritized Execution Gaps**.

For each prioritized gap, Celonis filters are applied systematically across relevant business dimensions, including:
- customer country,
- customer market,
- production plant,
- product type,
- delivery company,
- warehouse type.

The purpose of filtering is **not** segmentation for its own sake, but to identify:
- **systematic concentrations**,
- **stable patterns**, and
- **repeatable execution behavior**.

Filter candidates are evaluated and selected based on:
- OTIF failure rates (case-based and value-based),
- lateness vs. quantity deviation patterns,
- throughput time severity relative to the Happy Path,
- statistical stability (minimum case thresholds).

Dimensions or members that are:
- low-frequency,
- highly heterogeneous,
- or economically irrelevant

are explicitly excluded from root-cause conclusions.

## Example: How Filters Were Derived (CUST_COUNTRY Meta-Scatter)

## Example: How Filters Were Derived (CUST_COUNTRY)

![CUST_COUNTRY Meta-Scatter: Late Rate vs. Quantity Tolerance Violations](
../assets/woodcorp-otif-rootcause/plots/meta_scatter_cust_country_late_vs_tol_bubble_value.png
)

The country-level meta-scatter (Late Rate vs. Quantity Tolerance Violations; bubble = Order Value) was used to translate a visual pattern into **explicit Celonis filter candidates**.

### What the chart encodes
- **Y-axis (Late rate):** How often deliveries are late (timeliness issue).
- **X-axis (Qty tolerance violation rate):** How often quantity deviations occur (quantity issue).
- **Bubble size (Order value):** Economic exposure / value-at-risk.
- **Filter rule:** We prioritize countries that combine **(a) severity**, **(b) stability (sufficient cases)**, and **(c) business relevance (value exposure)**.

---

### Step-by-step filter selection logic (applied to the chart)

#### Step 1 — Define the analytical intent
For the prioritized Execution Gap, we want to isolate **countries where the same execution gap repeatedly materializes** and creates disproportionate delay / value exposure.

#### Step 2 — Translate intent into visual selection criteria
We selected countries that satisfy at least one of the following:

**A) Timeliness-driven severity (high Y)**
- High late rate, even if quantity violations are low/moderate  
- Interpreted as “execution stability / lead-time / carrier / handover issues”

**B) Quantity-driven severity (high X)**
- High tolerance violation rate paired with non-trivial late rate  
- Interpreted as “post-release corrections and rework driving delay”

**C) Business relevance (large bubble / high value exposure)**
- Even moderate rates become important if the value-at-risk is high.

**D) Statistical stability**
- Only countries with sufficient case volume (e.g., N ≥ 200) are treated as reliable root-cause candidates.

---

### Concrete filter candidates derived from the chart

#### 1) CH (Switzerland) — “High severity timeliness”
**Why it is selected:**
- Very high late rate (top of the chart)  
- Quantity violations are low-to-moderate (not the primary driver)
- Indicates a **timeliness-driven execution problem with high delay severity**

**Celonis filter example:**
- `CUST_COUNTRY = "CH"`
- combined with: `Execution Gap = <prioritized gap>` and/or `IS_LATE = true`

---

#### 2) NL (Netherlands) — “Mixed pattern”
**Why it is selected:**
- Both late rate and quantity violations are elevated (upper-right-ish zone)
- Indicates a **mixed execution issue** (both timeliness + quantity symptoms)
- Good candidate to test whether the gap is process-internal vs. market-specific

**Celonis filter example:**
- `CUST_COUNTRY = "NL"`

---

#### 3) ES (Spain) — “Scale / exposure”
**Why it is selected:**
- Moderate late rate, but **large bubble** (high value/volume exposure)
- Even if severity is not the maximum, the economic impact is structurally relevant
- Good candidate for “high-impact but not extreme rate” root-cause work

**Celonis filter example:**
- `CUST_COUNTRY = "ES"`

---

#### 4) US (United States) — “Quantity-driven exposure”
**Why it is selected:**
- High quantity violation rate (right side of chart)
- Non-trivial late rate
- Indicates **quantity-driven post-release correction** risk

**Celonis filter example:**
- `CUST_COUNTRY = "US"`

---

### Why not select every prominent point (e.g., DE / FR)?
Even if a country looks visible on the chart, it may be deprioritized when:
- it reflects a **baseline / expected mix** rather than a distinct pattern,
- it lacks incremental insight (e.g., already covered by plant/carrier filters),
- or it is not aligned with the **specific execution gap hypothesis** currently analyzed.

In other words: the chart is used to identify **the most diagnostic filters**, not to list “all countries with issues”.

---

### How this helps the root cause analysis
The country filters derived from the chart serve two purposes:
1. **Concentration test:** Does the execution gap cluster in specific markets?
2. **Drill-down entry point:** Once clustered, we investigate whether the real driver is:
   - a plant (FACTORY),
   - a carrier (DELIVERY_COMPANY),
   - a product type (PRODUCT_TYPE),
   - or a market/lead-time characteristic.

This turns a visual pattern into a repeatable, auditable filter-based RCA workflow.


---

## Separation of Problem Classes

A key methodological principle is the **explicit separation of two fundamentally different execution problem classes**:

1. **Timeliness-driven execution gaps**  
   - High late rates  
   - Low or moderate quantity violations  
   - Often widespread and value-driven  

2. **Quantity / tolerance-driven execution gaps**  
   - Lower frequency  
   - High severity and strong concentration  
   - Often linked to post-loading or post-release corrections  

This separation prevents false conclusions and ensures that:
- root causes are not mixed across fundamentally different problem types,
- improvement actions are targeted and effective.

---

## Improvement and Control Logic

Improvement measures are derived **only from validated root causes**, not from symptoms.

Each improvement initiative is evaluated based on:
- expected reduction of execution risk,
- business impact,
- implementation and governance effort.

Finally, a focused set of operational KPIs is defined to:
- monitor execution behavior over time,
- validate improvement effects,
- and support continuous control under clear O2C ownership.

---

## Key Methodological Takeaway

The methodology deliberately narrows analytical focus to:
- execution-relevant deviations,
- economically meaningful patterns,
- and operationally actionable root causes.

This ensures that root cause analysis leads to **management decisions**, not just analytical insights.
