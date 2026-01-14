# Methodology

This document describes the analytical approach applied in this project.  
The focus is on **business-oriented process analysis**, transparent prioritization, and a clear separation between **observed execution behavior** and **data or logging artifacts**.

---

## Analytical Framing

The analysis is guided by the following management-oriented question:

**Where does actual Order-to-Cash (O2C) execution deviate from the intended operational flow, and which deviations create material execution risk requiring management attention?**

To ensure a structured and value-driven approach, the project follows the **Celonis Enhancement Cycle**:

Identify → Quantify → Analyze → Improve → Control.

![Celonis Enhancement Cycle](../assets/external/Celonis%20Enhancement%20Cycle.PNG)

The analytical focus is explicitly on **execution behavior and operational stability**, not on tool demonstration or system configuration.

---

## Event Ordering and Data Interpretation

An initial data assessment revealed that event timestamps in the activity log are **not sufficiently reliable to derive the true business execution sequence**.

Systematic inconsistencies occur due to:
- batch-based logging,
- delayed or retroactive status updates, and
- technical planning or release events logged independently of physical execution.

Therefore, **timestamp-based ordering is not used to define the process flow**.

Instead, the provided **SORTING attribute is used as the business reference order**, as it represents the **intended and logically defined execution sequence**.

Event timestamps are used exclusively for:
- duration measurement, and
- cycle-time calculation,

but **not for sequencing**.

---

## Happy Path Definition

A simplified **Happy Path** is defined as an analytical baseline representing the **business-intended O2C execution flow**, based on the SORTING logic.

The Happy Path includes the following core activities:

- Order received  
- Confirm sale  
- Start production *(interpreted as a planning or release trigger)*  
- Finished production  
- Load shipment  
- Goods delivered  

Change activities and rework loops (e.g. price changes, quantity changes, delivery date changes, production start date changes) are **explicitly excluded**.

The Happy Path is **not a normative target process**, but a **stable analytical reference** used to:
- quantify execution deviations,
- compare cycle times, and
- isolate post-release execution effects.

---

## Execution Gaps

Execution Gaps are defined as **systematic deviations from the Happy Path** observed in actual process executions.

Typical examples include:
- rework loops after order release,
- repeated changes to production start or delivery dates, and
- extended waiting times between core process steps.

Deviations caused solely by **timestamp inconsistencies or logging artifacts** (e.g. apparent activity order violations) are **explicitly excluded** from the Execution Gap analysis.

At this stage, Execution Gaps are treated as **observable symptoms**, not as root causes.

---

## Quantification & Prioritization Logic

Each identified Execution Gap is assessed using a consistent structure:

- affected order share (% of cases),
- additional cycle time compared to the Happy Path (median),
- qualitative **execution risk**, reflecting:
  - likelihood of occurrence,
  - severity of operational disruption, and
  - controllability once triggered.

Execution Gaps are prioritized based on **risk and actionability**, not on frequency alone.

---

## Root Cause Analysis

Root cause analysis is conducted **only for prioritized Execution Gaps**.

The analysis focuses on identifying **systematic concentrations and patterns** across relevant business dimensions, including:
- product type,
- production plant,
- order size,
- customer or market segment.

Isolated, low-frequency, or statistically unstable cases are explicitly excluded from root-cause conclusions.

---

## Improvement and Control Logic

Improvement measures are derived directly from validated root causes and evaluated based on:
- expected reduction of execution risk, and
- implementation or governance effort.

A focused set of operational KPIs is defined to:
- monitor execution behavior over time,
- validate improvement effects, and
- support continuous control under clear O2C ownership.
