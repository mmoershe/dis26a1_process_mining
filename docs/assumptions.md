# Assumptions

This document summarizes the key assumptions underlying the analysis to ensure transparency and proper interpretation of the results.

---

## Case Definition

- One case represents one customer order  
- All events linked to the same case key are treated as part of one O2C process instance  

---

## Time, Sequencing & Process Logic

- Event timestamps are used to measure **durations and cycle times**, but are **not assumed to always reflect the true business execution order**  
- Where timestamp ambiguities occur (e.g. batch postings, retroactive updates), **logical activity sequencing based on business rules** is applied  
- The **Happy Path** represents the intended best-case execution flow and is used **exclusively as an analytical reference**, not as a normative target  

---

## Cycle Time Measurement

- Overall O2C cycle time is measured from **order receipt to goods delivery**  
- Selected analyses focus on **post-release execution phases** to isolate the impact of execution deviations  
- All cycle-time comparisons are **relative**, not absolute  

---

## Business Metrics & Value Interpretation

- Order value is used as a **proxy for economic relevance** at an operational level  
- No accounting, margin, or financial accuracy is implied  
- The analysis focuses on **relative, value-weighted differences** rather than absolute financial impact  

---

## Scope, Interpretation & Limitations

- Findings reflect **observed execution behavior**, not system configuration or intended process design  
- Master data quality issues and upstream data generation are **out of scope**, except where they directly affect execution interpretation  
- Identified patterns represent **systematic correlations**, not proven causal relationships  
- Results are intended to support **operational management decision-making**, not detailed technical or IT redesign  
