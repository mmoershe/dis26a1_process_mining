# Methodology

This document describes the analytical approach applied in this project.  
The focus is on **business-oriented process analysis**, transparent prioritization, and a strict separation between **observable execution behavior** and **data or logging artifacts**.

The methodology is designed to support **management decision-making**, not technical system redesign or tool demonstration.

---

## Analytical Framing

The analysis is guided by the following management-oriented question:

**Where does actual Order-to-Cash (O2C) execution deviate from the intended operational flow, and which deviations create material execution risk requiring management attention?**

The objective is **not** to describe the end-to-end process exhaustively, but to identify **execution instability with measurable operational and economic impact**.

To ensure a structured and value-driven approach, the project follows the **Celonis Enhancement Cycle**:

**Identify → Quantify → Analyze → Improve → Control**

Celonis is used as an **analytical execution platform**.  
The underlying methodological logic is **tool-independent** and could be applied using any equivalent process mining environment.

---

## Scope and Methodological Boundaries

The methodology explicitly **does not aim to**:
- define a target-state or optimized O2C process,
- evaluate system configuration or IT architecture,
- perform compliance checking or conformance analysis,
- simulate alternative process designs.

The focus is strictly on **observed execution behavior** and its operational consequences.

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

but a **stable analytical reference** used to:
- quantify execution deviations,
- compare throughput times (TPT),
- isolate **post-release execution effects**.

---

## Execution Gap Definition

Execution Gaps are defined **conceptually**, not statistically, as:

> **Systematic deviations from the Happy Path that occur after order release and negatively affect execution stability.**

Examples include:
- post-release quantity corrections,
- repeated production start date changes after production start,
- credit blocks,
- repeated price rework triggering downstream changes,
- extended waiting times between core execution steps.

Key methodological clarifications:
- Execution Gaps are **defined independently of their measured impact**.
- Quantification is applied **after** conceptual definition.
- Deviations caused solely by timestamp inconsistencies or logging artifacts are **explicitly excluded**.
- Execution Gaps are treated as **observable symptoms**, not as root causes.

At this stage, the analysis answers **what breaks and where**, not **why it breaks**.

---

## Quantification & Prioritization Logic

Each identified Execution Gap is quantified using a consistent structure:

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

Filtering serves to identify:
- **systematic concentration**, not isolated cases,
- **stable execution patterns**, not one-off effects.

Filters are selected based on:
- OTIF failure rates (case-based and value-based),
- lateness vs. quantity deviation patterns,
- throughput-time severity relative to the Happy Path,
- statistical stability (minimum case thresholds).

Low-frequency, heterogeneous, or economically irrelevant segments are **explicitly excluded**.

---

## Separation of Problem Classes

A key methodological principle is the **explicit separation of execution problem classes**:

1. **Timeliness-driven execution gaps**  
   - High late rates  
   - Low or moderate quantity violations  

2. **Quantity / tolerance-driven execution gaps**  
   - Lower frequency  
   - High severity and strong concentration  

This separation prevents false causal attribution and ensures targeted improvement actions.

---

## Improvement and Control Logic

Improvement measures are derived **only from validated root causes**, not from symptoms.

Each initiative is evaluated based on:
- expected reduction of execution risk,
- business relevance,
- implementation and governance effort.

Finally, a focused set of KPIs is defined to:
- monitor execution behavior,
- validate improvement effects,
- support continuous control under clear O2C ownership.

---

## Reproducibility and Auditability

All analytical steps, filters, and metrics are:
- deterministic,
- reproducible,
- and explicitly documented.

This ensures transparency, auditability, and methodological robustness.

---

## Key Methodological Takeaway

The methodology deliberately narrows analytical focus to:
- execution-relevant deviations,
- economically meaningful patterns,
- operationally actionable root causes.

This ensures that root cause analysis leads to **management decisions**, not just analytical insight.
