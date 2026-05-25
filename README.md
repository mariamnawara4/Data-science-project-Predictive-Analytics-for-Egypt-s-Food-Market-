# Data science project - Predictive Analytics for Egypt's Food Market
Machine learning pipeline to analyze and predict food price volatility in Egypt using PDF/Excel extraction from CAPMAS data (2018–2026). Unlike standard time-series models, this solution integrates macroeconomic shocks—specifically USD exchange rates and fuel prices—with seasonal events (Ramadan) and global crises.

### Data Extraction
- **2018–2020:** PDF extraction from semi-structured government reports
- **2021–2026:** Excel extraction from modern formatted files

### Preprocessing & Feature Engineering
- Integrated multiple sources into unified DataFrame
- Applied domain filtering (removed wholesale errors, kept inflation spikes)
- Added macroeconomic drivers (USD rates, fuel prices)
- Engineered calendar events (Ramadan, Eids) with Sin/Cos encoding

### Modeling
- **Algorithm:** XGBoost Regressor
- **Leakage Prevention:** Chronological split (Jan 2024 cutoff)
- **Validation:** 5-Fold Walk-Forward Time-Series Cross-Validation


#### Team
- Abrar Ahmed Gharbia
- Mariam Mohamed Elshilek
- Mariam Mohamed Nawara
- Norhan Hany Elladam
