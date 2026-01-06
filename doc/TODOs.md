# Woodcorp O2C Process Mining (Celonis)  
## TODO & Arbeitsteilung (Team: 2)

> **Projektziel:**  
> Die O2C-Ausführung (Order Received → Changes → Start Production) datenbasiert analysieren, **Execution Gaps** identifizieren und quantifizieren, Ursachen herleiten sowie **priorisierte Verbesserungsmaßnahmen** ableiten (Celonis Enhancement Cycle).

---

## 0) Setup & Rollenklärung

- [ ] **Team-Rollen fixieren**
  - **Jan (Business / Storyline / Owner-Perspektive):**  
    Verantwortung für Unternehmenskontext, Zielgruppenadressierung, Projekt-Narrativ, Ableitung und Bewertung von Maßnahmen, **KPI-Definitionen** sowie **Hauptverantwortung für Texte und PowerPoint**.
  - **Henri (Analytics / Evidence):**  
    Verantwortung für **Happy Path Definition**, Identifikation und Quantifizierung der **Execution Gaps**, Root-Cause-Analysen, Aufbau der **Celonis Views und Dashboards** sowie Bereitstellung belastbarer **Evidenz (Screenshots, Tabellen)**.

---

## 1) TODOs bis zum nächsten Meeting

### Aufgaben – Jan (Business & Storyline)

- [ ] PowerPoint-Struktur aufsetzen (Storyline entlang Enhancement Cycle)
- [ ] Zielgruppe klar benennen und adressieren
- [ ] Project Goal & Scope definieren (In Scope / Out of Scope)
- [ ] Data Basis und Assumptions dokumentieren
- [ ] Unternehmenskontext und Business-Relevanz von Prozessmanagement ausarbeiten

---

### Aufgaben – Henri (Analytics & Evidence)

- [ ] Happy Path(-s) definieren und technisch in Celonis umsetzen
- [ ] Mindestens **5 Execution Gaps** identifizieren  
      (mit Fokus auf Gaps, die voraussichtlich **hohe Priorität** in der Quantifizierung erreichen)

---

## 2) Quantifizierungsvorlage – verpflichtend pro Execution Gap

Für **jedes Execution Gap** sind folgende Punkte vollständig auszuarbeiten:

- **Dimension**  
  (z. B. Product Type, Factory, Customer Market, Warehouse Type)

- **Analytische Fragestellung**  
  (z. B. „In welchen Segmenten treten Preisänderungen überproportional häufig auf?“)

- **Volume**  
  - Wie viele Cases sind betroffen?  
  - Anteil am Gesamtvolumen (%)

- **Time**  
  - Wie viel zusätzliche Zeit entsteht?  
  - Δ Cycle Time im Vergleich zum Happy Path (z. B. Median in Tagen)

- **Value (Business Impact)**  
  - Welcher Geschäftshebel ist betroffen?  
    - Produktions- und Kapazitätsplanung  
    - Termintreue / Customer Experience  
    - Operativer Aufwand im Order Management  
  - Optional: Ø / Sum ORDER_VALUE als Proxy

- **Priority**  
  - Lohnt sich eine vertiefte Analyse? (Ja/Nein)  
  - Kurze Begründung auf Basis von Volume, Time und Value

---

> **Hinweis:**  
> Nur Execution Gaps mit klarer **Business-Relevanz** und belastbarer **Daten-Evidenz** werden in die Root-Cause-Analyse und den Improvement Plan übernommen.
