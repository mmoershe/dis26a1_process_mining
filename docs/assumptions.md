# Assumptions

This document summarizes the key assumptions underlying the analysis to ensure transparency and proper interpretation of the results.

---

## Case Definition

- One case represents one customer order  
- All events linked to the same case key are treated as part of one O2C process instance  

---

## Time & Sequencing

- Event timestamps are assumed to reflect actual execution times  
- Logical activity order is used to resolve potential timestamp ambiguities where needed  
- Cycle time is measured from order receipt to production start  

---

## Business Metrics

- Order value is used as a proxy to assess business relevance at an operational level  
- No accounting or financial accuracy is implied  
- The analysis focuses on relative differences rather than absolute financial impact  

---

## Scope & Interpretation

- Findings reflect execution behavior, not system configuration  
- Master data quality issues are not analyzed  
- Results are interpreted at an operational management level  
