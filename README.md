# Woodcorp – Order-to-Cash (O2C) Process Analysis
*Process Mining case study (DIS26a1) | Tool: Celonis | Team project (Jan Krings & Henri Moersheim)*

## Overview
Business-focused analysis of the Order-to-Cash (O2C) execution of a fictitious manufacturing company (Woodcorp).  
Using event data, we identify **execution deviations** from the intended flow, quantify their **operational and economic relevance**, and translate findings into **prioritized management actions** for process owners.

## Business Context
Woodcorp produces pallets and crates for retail and construction customers in a make-to-order setting.  
Order and execution changes after receipt (e.g., price rework, production rescheduling, quantity corrections) introduce planning instability and operational rework—particularly **after order release** (handover to production and logistics).  
This project focuses on **where execution deviates**, **how material the impact is**, and **which gaps require management attention**.

## Core Question
**Where does actual O2C execution deviate from the intended operational flow, and which deviations create material execution risk requiring management attention?**

## Scope
**In scope:** Order received → Confirm sale → Order release → Production & logistics execution → Goods delivered  
**Out of scope:** Billing, invoicing, payment, returns, margin / profitability analysis, IT/system redesign

## Methodological Approach
The analysis follows the **Celonis Enhancement Cycle**:

**Identify → Quantify → Analyze → Improve → Control**

Key methodological principles:
- **Happy Path baseline:** Defined a simplified Happy Path as a stable analytical reference (not a target state)
- **Execution Gaps:** Modeled systematic post-release deviations from the Happy Path as explicit, filterable gap definitions
- **Sequencing logic:** Event timestamps are used for **durations only**; business execution order is derived from the provided **SORTING** logic to avoid logging artifacts
- **Prioritization:** Execution gaps are ranked by **frequency × severity (TPT delta) × value exposure**, not by frequency alone
- **RCA (filter-based):** Root cause analysis is conducted only for prioritized gaps via systematic filtering (plant, product, customer/market, logistics)

## Deliverables
- Slide deck / presentation material in `/slides` *(to be added)*  
- Selected dashboard screenshots and plots in `/assets` *(to be added)*  
- Documentation in `/docs`:
  - `assumptions.md`
  - `data_description.md`
  - `methodology.md`

## Our Role
Data Analysts (Process Mining)

We:
- framed the business question and analytical scope  
- defined the Happy Path, key measures, and KPI logic  
- identified and quantified execution deviations (gap-based analysis)  
- prioritized gaps by operational impact and economic exposure  
- conducted filter-based root cause analysis for high-impact gaps  
- translated findings into stakeholder-ready insights and improvement actions  

## Data Availability
The dataset is **not included** in this repository. Please do not commit any raw data files.  
This repository contains documentation, analysis artifacts, and reproducible logic where possible.

## Status
Finished

*Note: Woodcorp is a fictitious company. This project is for academic and portfolio purposes.*
