# Hormone-Modulated Kalman Filter Q-Learning for Home Energy Management

**Paper:** "Hormone-Modulated Kalman Filter Q-Learning for Home Energy Management: A Matched-Service Evaluation with Thermal Comfort Assessment"
**Authors:** Md. Alamgir Hossain and Md. Shahjahan
**Affiliation:** Department of Electrical and Electronic Engineering, Khulna University of Engineering & Technology (KUET), Bangladesh

**Release:** v2.0  
**DOI (Zenodo archive):** [10.5281/zenodo.23729891](https://doi.org/10.5281/zenodo.23729891)

## Repository Contents

| File | Description |
|------|-------------|
| `KFQL_Hormone_HEMS.ipynb` | All code: FFNN forecasting, KFQL simulation, service-referenced experiments, thermal experiments, statistical tests and figures (saved outputs included) |
| `solar.csv` | Hourly solar generation, PJM SOUTH region, Jan 2022 – Dec 2023 |
| `price.csv` | Hourly PJM day-ahead prices (column `system_energy_price_da`), Jan 2022 – Dec 2023 |
| `weather.json` | Hourly outdoor temperature, Richmond VA (Open-Meteo / ERA5), 14 Jan – 17 Feb 2022 |
| `forecasts_seed42.npz` | Stored FFNN forecasts used by all experiments (checksums: PV 360.4886, price 10204.0161) |
| `service_results.pkl` | Cached results of the appliance-level experiments (10 seeds × 3000 episodes) |
| `thermal_results.pkl` | Cached results of the thermal-comfort experiments |
| `beta_check_5.pkl`, `beta_check_15.pkl`, `beta_check_25.pkl` | Cached results of the reward-weight (β) check |
| `requirements.txt` | Python package dependencies |

## Data Sources

- Solar generation: [PJM Data Miner 2, solar_gen](https://dataminer2.pjm.com/feed/solar_gen)
- Day-ahead price: [PJM Data Miner 2, da_hrl_lmps](https://dataminer2.pjm.com/feed/da_hrl_lmps)
- Outdoor temperature: [Open-Meteo Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api) (ERA5 reanalysis)

**Pre-processing (notebook, first cell):** negative values clipped to zero; a contiguous subset of 840 hours starting at index 312 (14 Jan – 17 Feb 2022) is taken from both series with the same indices; both series are min–max normalised. The PV forecast is scaled to a 7 kWp rooftop system.

**Days used:** the first 25 days train the FFNN; 10 Feb 2022 is the main simulation day, and 9 and 11–17 Feb 2022 are held-out test days.

## System Description

| Agent | Type | Actions (kW) | Notes |
|-------|------|--------------|-------|
| Refrigerator | Non-shiftable | 0.5 | Fixed load (single action) |
| AC1, AC2 | Power-shiftable | 0.4–1.4 (step 0.1) | Learning agents |
| Heater | Power-shiftable | 0.5–1.5 (step 0.1) | Learning agent |
| Light1, Light2 | Time-shiftable | 0.2–0.6 (step 0.1) | Learning agents |
| Washing machine | Time-shiftable | 0 or 0.7 | On only 18–23 h |
| Dishwasher | Time-shiftable | 0 or 0.3 | On only 19–22 h |
| Battery | Storage | ±3.0 | Rule-based dispatch (not a learning agent) |

Seven appliance agents learn with tabular Kalman-filter Q-learning (KFQL). In the thermal model, AC1, AC2 and the heater are replaced by first-order RC room models, and comfort is evaluated with the ISO 7730 PMV/PPD index.

## Hormone Models

- **Melatonin:** cosine (peak 03:00 h), light–dark ODE, pharmacokinetic
- **Cortisol:** cosine (peak 08:00 h), pulsatile, cortisol awakening response (Gaussian, peak 08:00 h)

All curves are normalised to [0, 1]. The main configuration uses cosine melatonin and the cortisol awakening response.

## Key Parameters

| Parameter | Value |
|-----------|-------|
| Training episodes | 3000 (converged policy: last 500) |
| Discount factor γ | 0.9 |
| Exploration ε | 0.5 → 0.05, decay 0.9985 |
| Reward weights λ₁, λ₂, λ₃ | 2.5, 1.0, 0.5 |
| Reward scaling | r / 30 |
| Melatonin weight β | 0.75 |
| Kalman filter σ_w², σ_v², Σ₀ | 0.01, 0.1, 0.5 |
| PV / price bins | 3, 3 |
| Random seeds | 0–9 |

## How to Run

```bash
pip install -r requirements.txt
```

Python 3.13 was used for all reported results. Place all files in one folder and open the notebook; figures are saved to `images/` (created automatically). Run the cells in this order:

1. Data, FFNN forecasting, stored forecasts, simulation model (first four cells)
2. Main results, statistics and figures
3. **S-A → S-B → S-C**: service-referenced experiments (matched-service evaluation)
4. **T-A → T-B → T-C → T-D**: thermal-comfort experiments and sensitivity
5. **β check** (last cell)

With the cached `.pkl` files in the folder, the experiment cells load the stored runs instead of re-simulating, so every table and figure is regenerated in minutes. Without them, S-B takes about 75 min and T-B about 45 min.

To reproduce the fixed-learning-rate comparison (Fig. 13b), set `USE_KALMAN = False` in the simulation cell, run only the convergence cells, then set it back to `True`.

## Main Results (10 February 2022, 10 seeds)

- Hormone-modulated KFQL vs KFQL without hormones: 2.49% less energy (85.11 vs 87.28 kWh/day) and 7.3% less grid import; exact two-sided Wilcoxon W⁺ = 55, p = 0.002.
- Against a common, hormone-independent comfort reference, the saving comes from a lower night-time comfort setpoint (2.75 kWh/day more unserved comfort); a constant night setback reaches the same comfort with 0.45 kWh/day less energy.
- Thermal model: KFQL lowers energy cost by 0.4–35% relative to a thermostat on all nine days and reduces PMV/PPD discomfort on seven.

## Licence

Code is released under CC BY 4.0 (see `LICENSE`). Data files are subject to the PJM and Open-Meteo terms of use.

## Citation

```
[Full citation to be added upon publication]
```

## Contact

Md. Alamgir Hossain — mah@eee.kuet.ac.bd
Dept. of EEE, Khulna University of Engineering & Technology, Bangladesh
