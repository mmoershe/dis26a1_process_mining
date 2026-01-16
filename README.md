# Woodcorp Order to Cash O2C Process Analysis
Process Mining Case Study DIS26a1  
Tool Celonis  
Team Project Jan Krings and Henri Moersheim

## Overview
Business focused analysis of the Order to Cash execution of a fictitious manufacturing company called Woodcorp.  
Based on event data, the project identifies execution deviations from the intended process flow, quantifies their operational and economic impact, and translates results into prioritized management actions for process owners.

## Key Findings
- Post release execution deviations increase median O2C throughput time by approximately four days
- A small number of recurring execution gaps explains most delays and planning instability
- Late quantity changes after shipment loading have low frequency but very high impact
- Repeated production rescheduling occurs frequently and causes systemic planning instability
- Credit blocks with downstream rework affect around ten percent of orders and cause very high delays
- Value exposure is mainly driven by late deliveries without quantity violations, requiring differentiated management responses

## Skills Demonstrated
- Process Mining with Celonis in the Order to Cash domain
- Business process analysis and deviation modeling
- KPI definition and impact based prioritization
- Root cause analysis using filters and segmentation
- Python for data validation, sequencing logic, and reproducibility
- Management oriented storytelling and decision framing

## Business Context
Woodcorp produces pallets and crates for retail and construction customers in a make to order setting.  
Order and execution changes after order receipt such as price rework, production rescheduling, or quantity corrections introduce planning instability and operational rework, particularly after order release when responsibility is handed over to production and logistics.

The analysis focuses on where execution deviates from plan, how material the impact is, and which deviations require management attention.

## Core Question
Where does actual O2C execution deviate from the intended operational flow, and which deviations create material execution risk requiring management action?

## Scope
In scope  
Order received, confirm sale, order release, production and logistics execution, goods delivered  

Out of scope  
Billing, invoicing, payment, returns, margin or profitability analysis, IT or system redesign

## Methodological Approach
The analysis follows the Celonis Enhancement Cycle.

Identify, Quantify, Analyze, Improve, Control

Key methodological principles
- A simplified Happy Path is defined as a stable analytical reference and not as a target state
- Systematic post release deviations are modeled as explicit and filterable execution gaps
- Event timestamps are used only for duration calculations, while execution order is derived from business defined sorting logic
- Execution gaps are prioritized by frequency, severity measured as throughput time delta, and value exposure
- Root cause analysis is conducted only for prioritized gaps using structured filtering by plant, product, customer or market, and logistics

## Deliverables
- Management presentation in the slides folder
- Selected Celonis dashboard screenshots and analytical plots in the assets folder
- Detailed documentation in the docs folder including assumptions, data description, and methodology
- Reproducible Python scripts for data validation and sequence handling

## Our Role
Data Analysts with a focus on Process Mining

Responsibilities
- Framing the business problem and analytical scope
- Defining the Happy Path, KPIs, and measurement logic
- Identifying and quantifying execution deviations using gap based analysis
- Prioritizing execution gaps by operational and economic impact
- Conducting filter based root cause analyses for high impact deviations
- Translating analytical findings into stakeholder ready insights and management actions

## Data Availability
The dataset is not included in this repository.  
No raw data files are committed. The repository contains documentation, analysis artifacts, and reproducible logic where possible.

## Status
Finished

Note  
The data used in this project is synthetically generated and represents a realistic but fictitious Order to Cash execution scenario.
