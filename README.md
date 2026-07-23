# Circadian Hormone-Modulated Kalman Filter Q-Learning for Home Energy Management

**Paper:** "A Circadian Hormone-Modulated Kalman Filter Q-Learning Framework for Home Energy Management Systems"  
**Authors:** Md. Alamgir Hossain and Md. Shahjahan  
**Affiliation:** Department of Electrical and Electronic Engineering, Khulna University of Engineering & Technology (KUET), Bangladesh  
**Journal:** IEEE Access, 2025  
**Manuscript ID:** Access-2025-52365

DOI: 10.5281/zenodo.21510321 (https://doi.org/10.5281/zenodo.21510321)

## Repository Contents

| File | Description |
|------|-------------|
| `KFQL_Hormone_Revised.ipynb` | Main simulation notebook — FFNN forecasting, KFQL training, hormone sweep, statistical tests, all figures |
| `hormone_functions.py` | Standalone implementation of all six hormone models (3 melatonin × 3 cortisol) with plotting |
| `solar.csv` | Hourly solar generation data (kW), PJM South region, Jan 2022 – Dec 2023 |
| `price.csv` | Hourly electricity price data ($/MWh), PJM day-ahead LMP, Jan 2022 – Dec 2023 |
| `results_log.txt` | Full simulation output log — per-agent consumption, multi-seed summary, Wilcoxon test results |
| `requirements.txt` | Python package dependencies |

---

## Data Sources

Raw solar generation and electricity price data were downloaded from the **PJM Data Miner 2** portal:

- Solar generation: [https://dataminer2.pjm.com/feed/solar_gen](https://dataminer2.pjm.com/feed/solar_gen)  
- Day-ahead LMP price: [https://dataminer2.pjm.com/feed/da_hrl_lmps](https://dataminer2.pjm.com/feed/da_hrl_lmps)  
- Accessed: 10 December 2024  
- Region: SOUTH zone, PJM Interconnection  
- Period: 1 January 2022 – 31 December 2023 (17,520 hourly records)

**Pre-processing applied in `KFQL_Hormone_Revised.ipynb` (Cell 0):**
- Negative solar values clipped to zero
- 720-hour contiguous subset selected (indices 312–1032 for solar; 244–964 for price, offset by 68 h to align day-ahead prices with real-time solar)
- Both series normalised to [0, 1] using min-max scaling

---

## System Description

The proposed MA-HEMS manages nine controllable agents:

| Agent | Type | Power Range (kWh) | Usable Hours |
|-------|------|-------------------|--------------|
| Refrigerator | Non-shiftable (NS) | 0.5 | 0–23 |
| AC1 | Power-shiftable (PS) | 0.4–1.4 | 0–23 |
| AC2 | Power-shiftable (PS) | 0.4–1.4 | 0–23 |
| Heater | Power-shiftable (PS) | 0.5–1.5 | 0–23 |
| Light1 | Time-shiftable (TS) | 0.2–0.6 | 18–23 |
| Light2 | Time-shiftable (TS) | 0.2–0.6 | 18–23 |
| Washing Machine | Time-shiftable (TS) | 0–0.7 | 19–22 |
| Dishwasher | Time-shiftable (TS) | 0–0.3 | 20–22 |
| Battery | Storage | ±3.0 | 0–23 |

---

## Hormone Models

Six biologically-inspired circadian hormone signals are implemented in `hormone_functions.py`:

**Melatonin (3 models):**
- `M_cos` — Cosine circadian: `0.6 + 0.4·cos(2π(t−3)/24)`, peak at 03:00 h
- `M_ld` — Light-Dark ODE: `dM/dt = −k_m·M + S(t)`, k_m = 0.2 h⁻¹, synthesis during t ∈ [20,24)∪[0,6]
- `M_pk` — Pharmacokinetic: `(D/V)·(ka/(ka−ke))·(exp(−ke·t)−exp(−ka·t))`, D=V=ka=1.0, ke=0.3 h⁻¹

**Cortisol (3 models):**
- `C_cos` — Cosine circadian: `0.6 + 0.4·cos(2π(t−8)/24)`, peak at 08:00 h
- `C_pulse` — Pulsatile: sum of decaying pulses at t = {6, 10, 15, 20} h, amplitudes {1.0, 0.6, 0.5, 0.3}, k = 1.5 h⁻¹
- `C_car` — Cortisol Awakening Response (Gaussian): `exp(−(t−8)²/(2·2²))`, peak at 08:00 h

All models are normalised to [0, 1] after computation.

---

## Key Algorithm Parameters

| Parameter | Value |
|-----------|-------|
| Training episodes | 3000 |
| Discount factor γ | 0.9 |
| Learning rate α | 0.01 |
| Initial exploration ε₀ | 0.5 |
| Minimum exploration ε_min | 0.05 |
| Exploration decay ε_decay | 0.9985 |
| Reward weights λ₁, λ₂, λ₃ | 2.5, 1.0, 0.5 |
| Melatonin scaling β | 0.75 |
| Kalman process noise σ_w² | 0.01 |
| Kalman measurement noise σ_v² | 0.1 |
| PV / price bins n_PV, n_π | 3, 3 |
| Random seeds | 0–9 (10 seeds) |
| Best hormone combination | Mel = cos, Cor = car |

---

## How to Run

### Requirements

```bash
pip install -r requirements.txt
```

Python 3.13.7 was used for all reported results.

### Before running the notebook

1. Place `solar.csv` and `price.csv` in the **same directory** as the notebook.
2. Create an `images/` folder in the same directory (figures are saved there).
3. Update the `base_path` variable in **Cell 0** to your local directory:
   ```python
   base_path = r'your/local/path/here'
   ```

### Running

Open `KFQL_Hormone_Revised.ipynb` in Jupyter and run all cells in order. The notebook is structured as follows:

| Cell | Content |
|------|---------|
| 0 | Imports, data loading, preprocessing, raw data plots |
| 1 | FFNN implementation (Leaky ReLU, weight update) |
| 2 | KFQL simulation engine and hormone models |
| 3 | Aggregation utilities (`compute_power_stats`, `summarize_runs`) |
| 4–11 | Multi-seed runs, hormone sweep, Wilcoxon test, all figures |

Expected runtime on a standard laptop: approximately 15–20 minutes for 3000 episodes × 9 hormone combinations × 10 seeds.

---

## Reproducing Key Results

The best hormone combination (Mel = cos, Cor = car) achieves:

- **Total daily consumption:** 85.18 ± 0.08 kWh
- **Saving vs KFQL-None:** 2.15 kWh (2.46%)
- **Saving vs KFSARSA:** 1.40 kWh (1.62%)
- **Wilcoxon test:** W = 55, κ = 2.803, ρ < 0.001, ξ = 0.886 (large effect)
- **95% CI:** [85.12, 85.24] kWh (non-overlapping with KFQL-None [87.38, 87.55] kWh)

Full per-seed values and all results are in `results_log.txt`.

---

## Licence

Data files (`solar.csv`, `price.csv`): subject to PJM terms of use.  
Code files: MIT Licence.

---

## Citation

```bibtex
@article{hossain2025kfql,
  author  = {Hossain, Md. Alamgir and Shahjahan, Md.},
  title   = {A Circadian Hormone-Modulated {Kalman} Filter {Q}-Learning
             Framework for Home Energy Management Systems},
  journal = {IEEE Access},
  year    = {2025},
  doi     = {10.1109/ACCESS.2024.0429000}
}
```
