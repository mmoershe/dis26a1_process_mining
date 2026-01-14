# Data Description

This document provides a structured overview of the data used in this project and its analytical characteristics.  
No raw data files are included in this repository.

---

## Data Sources

The analysis is based on two structured datasets:

- **Activity Table**  
  Contains executed process events of the Order-to-Cash (O2C) process at event level.

- **Case Table**  
  Contains business context and attributes per customer order (case).

Each case represents **one customer order** and one O2C process instance.

---

## Event Log Structure

The activity table represents the O2C process as an event log with the following core elements:

- Case identifier (order)
- Activity name
- Event timestamp
- Logical activity order

Change-related activities (e.g. **production start date changes, quantity changes**) are explicitly recorded as separate events and are therefore directly observable.

This enables a **direct and reliable analysis of rework, replanning behavior, and execution deviations**, particularly after order release.

---

## Case Attributes

The case table provides contextual attributes used for segmentation and root-cause analysis, including:

- Customer market and region
- Product type
- Production plant
- Order quantities and delivery dates
- Order value

These attributes are not analyzed in isolation but are used to identify **systematic patterns and concentrations** across execution deviations.

---

## Data Characteristics & Quality

- Most cases follow a stable baseline execution with a limited number of events  
- A smaller but operationally relevant subset shows significantly higher activity counts, indicating rework and replanning behavior  
- Event timestamps exhibit limited granularity and occasional ties  
- Structural completeness of both tables is very high, with no systematic missing values  

Overall, the dataset is **well suited for process mining and execution analysis**, with challenges primarily related to sequencing and interpretation rather than data completeness.

---

## Sequencing & Interpretation

Due to timestamp ties and technical logging effects, a deterministic sequencing approach is applied:

- Primary ordering by event timestamp  
- Secondary ordering by logical activity order based on business rules  

Timestamps are used for **duration and cycle-time measurement**, while the logical order defines the **intended business execution sequence**.

This ensures a consistent and reproducible event log for process analysis and KPI calculation.

---

## Data Limitations

- No invoicing or payment data is available  
- Timestamp granularity limits fine-grained intra-day time analysis  
- Order value is used as a **business relevance proxy**, not as an accounting or financial metric  

The analysis therefore focuses on **operational execution behavior and planning stability**, not on financial reconciliation, margin analysis, or system configuration.
