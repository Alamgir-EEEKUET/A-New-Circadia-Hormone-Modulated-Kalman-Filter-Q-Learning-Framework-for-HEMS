import numpy as np
import matplotlib.pyplot as plt

# Set font configurations
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams.update({
    "axes.titlesize": 12,
    "axes.labelsize": 12,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10
})

# ----------------- Utility -----------------
def normalize(x):
    return (x - np.min(x)) / (np.max(x) - np.min(x) + 1e-8)

# Time vector
t = np.arange(0, 24, 0.1)

# ----------------- MELATONIN MODELS -----------------
M_cos = normalize(0.6 + 0.4 * np.cos(2 * np.pi * (t - 3) / 24))

S = np.where((t >= 20) | (t <= 6), 1, 0)
k_m = 0.2
M_ld = np.zeros_like(t)
for i in range(1, len(t)):
    dt = t[i] - t[i-1]
    M_ld[i] = M_ld[i-1] + dt * (-k_m*M_ld[i-1] + S[i])
M_ld = normalize(M_ld)

D, V, ka, ke = 1, 1, 1, 0.3
M_pk = normalize(np.clip((D/V)*(ka/(ka-ke))*(np.exp(-ke*t)-np.exp(-ka*t)), 0, None))

# ----------------- CORTISOL MODELS -----------------
C_cos = normalize(0.6 + 0.4 * np.cos(2 * np.pi * (t - 8) / 24))

C_pulse = np.zeros_like(t)
ti = [6, 10, 15, 20]
Ai = [1, 0.6, 0.5, 0.3]
k = 1.5
for j in range(len(ti)):
    C_pulse += Ai[j] * np.exp(-k * np.maximum(t - ti[j], 0))
C_pulse = normalize(C_pulse)

A, t0, sigma = 1.0, 8, 2
C_car = normalize(A*np.exp(-((t-t0)**2)/(2*sigma**2)))

# ----------------- PLOTTING -----------------
# 2 Rows, 3 Columns (Wider aspect ratio is better for 3 columns)
fig, axs = plt.subplots(2, 3, figsize=(12, 7))

# Row 0: Melatonin models
axs[0,0].plot(t, M_cos, 'b', lw=2)
axs[0,1].plot(t, M_ld, 'm', lw=2)
axs[0,2].plot(t, M_pk, 'g', lw=2)

# Row 1: Cortisol models
axs[1,0].plot(t, C_cos, 'r', lw=2)
axs[1,1].plot(t, C_pulse, 'c', lw=2)
axs[1,2].plot(t, C_car, '-b', lw=2)

# Row-major ordering: first 3 are Melatonin (a, b, c), next 3 are Cortisol (d, e, f)
labels = ['(a)', '(b)', '(c)', '(d)', '(e)', '(f)']
plot_titles = [
    "Melatonin – Cosine", "Melatonin – Light/Dark", "Melatonin – Pharmacokinetic",
    "Cortisol – Cosine", "Cortisol – Pulsatile", "Cortisol – CAR"
]

# Apply styling, labels, titles, and subfigure letters
for idx, ax in enumerate(axs.flat):
    ax.set_title(plot_titles[idx], pad=10)
    ax.set_xlabel("Time (Hour)")
    ax.set_ylabel("Normalized Value")
    ax.grid(True)

    # Place subfigure label (a, b, c...) slightly below the x-axis
    ax.text(0.5, -0.25, labels[idx],
            transform=ax.transAxes,
            ha="center", va="center",
            fontsize=12, fontweight='normal')

# Prevent overlapping layout elements
plt.tight_layout()
plt.subplots_adjust(hspace=0.45, wspace=0.3)
plt.show()