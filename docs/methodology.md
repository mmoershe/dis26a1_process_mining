# Methodology

This document describes the analytical approach applied in this project.  
The focus is on **business-oriented process analysis**, transparent decision-making, and a clear separation between **operational behavior** and **data or logging artifacts**.

---

## Analytical Framing

The analysis is guided by the following management-oriented question:

**Where does the actual Order-to-Cash (O2C) execution deviate from the intended operational flow, and which deviations are relevant from a business perspective?**

To ensure a structured and value-driven approach, the project follows the **Celonis Enhancement Cycle**:

Identify → Quantify → Analyze → Improve → Control.

![Celonis Enhancement Cycle](../assets/external/Celonis%20Enhancement%20Cycle.PNG)

---

## Event Ordering and Data Interpretation

An initial data assessment revealed that the event timestamps in the activity log are **not suitable for reliably deriving the process sequence**.  
A quantitative analysis shows that in **all cases at least one violation of the intended process order occurs** when activities are sorted purely by timestamp.

These inconsistencies are caused by system-related effects such as:
- batch-based logging,
- delayed status updates, and
- technical planning or release events being logged independently of physical execution.

Therefore, **timestamp-based sequencing is not used to define the process flow**.

Instead, the provided **SORTING attribute is used as the business reference order**, as it represents the **intended and didactically defined process sequence**.  
All subsequent analyses are performed relative to this business-oriented ordering.

Event timestamps are used exclusively for **duration and cycle time calculations**, not for sequencing.

---

## Happy Path Definition

A simplified **Happy Path** is defined as an analytical baseline representing the **business-intended O2C execution flow** according to the SORTING logic.

The Happy Path includes the following core activities:

- Order received  
- Confirm sale  
- Start production *(interpreted as a planning or release trigger)*  
- Finished production  
- Load shipment  
- Goods delivered  

Change activities and rework loops (e.g. price changes, delivery date changes, production start date changes) are **explicitly excluded**.

The Happy Path is **not intended as a normative or prescriptive process model**, but serves as a **reference baseline** to identify, quantify, and compare deviations in actual execution.

---

## Execution Gaps

Execution Gaps are defined as **systematic deviations from the Happy Path** observed in real process executions.

Examples include:
- rework loops after order release,
- repeated changes to production start or delivery dates, and
- extended waiting times between core process steps.

Deviations that result solely from **timestamp inconsistencies or logging artifacts** (e.g. *Start production* occurring before *Order received*) are **explicitly excluded** from the Execution Gap analysis.

At this stage, Execution Gaps are treated as **observable symptoms**, not as root causes.

---

## Quantification Logic

Each identified Execution Gap is assessed using a consistent and comparable structure:

- affected order volume (% of cases),
- additional cycle time compared to the Happy Path (median),
- qualitative business relevance (e.g. planning effort, operational instability, risk exposure).

This enables objective comparison across gaps and supports data-driven prioritization.

---

## Root Cause Analysis

Root cause analysis is conducted **only for prioritized Execution Gaps**.

The analysis focuses on identifying **systematic patterns** across relevant business dimensions, such as:
- product type,
- production plant,
- customer segment.

Isolated or non-recurring cases are explicitly excluded from root cause conclusions.

---

## Improvement and Control Logic

Improvement measures are derived directly from validated root causes and evaluated based on:
- expected business impact, and
- implementation effort.

A limited set of operational KPIs is defined to monitor execution behavior over time and support continuous improvement and control.
