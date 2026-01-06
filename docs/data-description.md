# Data Description

This document provides a structured overview of the data used in this project and its analytical characteristics.
No raw data files are included in this repository.

---

## Data Sources

The analysis is based on two structured datasets:

- **Activity Table**  
  Contains the executed process events of the Order-to-Cash (O2C) process.

- **Case Table**  
  Contains business context and attributes per order (case).

Each case represents one customer order.

---

## Event Log Structure

The activity table represents the O2C process as an event log with the following core elements:

- case identifier (order)
- activity name
- event timestamp
- logical activity order

Change-related activities (e.g. production start date changes) are explicitly recorded and therefore directly observable in the event log.
This enables a clear analysis of rework and execution deviations.

---

## Case Attributes

The case table provides contextual attributes used for segmentation and root-cause analysis, including:

- customer market and region
- product type
- production plant
- quantities and delivery dates
- order value

These attributes are not analyzed individually but are used to identify **systematic patterns** across execution deviations.

---

## Data Characteristics & Quality

- Most cases follow a stable baseline with a limited number of events  
- A smaller but relevant subset shows significantly higher activity counts, indicating rework behavior  
- Event timestamps show limited granularity and occasional ties  
- Structural completeness of both tables is very high, with no systematic missing values  

Overall, the dataset is well suited for process analysis, with challenges primarily related to sequencing and interpretation rather than data completeness.

---

## Sequencing & Interpretation

Due to timestamp ties, a deterministic sequencing approach is required:

- primary ordering by event timestamp  
- secondary ordering by logical activity order  

This ensures a consistent and reproducible event sequence for process analysis and KPI calculation.

---

## Data Limitations

- No invoicing or payment data is available  
- Timestamp granularity limits fine-grained time analysis  
- Order value is used as a business proxy, not as an accounting metric  

The analysis therefore focuses on **operational execution behavior**, not on financial reconciliation or system configuration.

