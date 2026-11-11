# STEP 3: how uncertain is the answer? (Monte Carlo with the IPCC ranges)
# In Colab, run the ch4_core.py cell first, then this one.
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(42)      # fixed seed: same answer every time
N = 10000                            # number of random trials

def draw(median, low, high):
    """Random values around the IPCC default, matching its low-high range
    (assumed to be a 95% interval, lognormal shape)."""
    if median == 0:
        return np.zeros(N)
    sigma = (np.log(high) - np.log(low)) / (2 * 1.96)
    return rng.lognormal(np.log(median), sigma, N)

# IPCC 2019 ranges (Tables 5.11, 5.11A, 5.12, 5.13, 5.14 and the Eq. 5.3 exponent)
region = "south_asia"
efc  = draw(EFC[region], 0.58, 1.26)            # shared by every scenario
days = draw(CULT_DAYS[region], 90, 140)         # shared
sfp  = draw(SFP["nonflooded_lt180d"], 0.88, 1.12)   # shared
expo = rng.normal(0.59, (0.64 - 0.54) / (2 * 1.96), N)   # exponent of Eq. 5.3
cfoa = draw(CFOA["straw_lt30d"], 0.85, 1.17)    # shared

def run(sfw_name, sfw_range, straw_t_ha=0):
    sfw = draw(SFW[sfw_name], *sfw_range)       # new draw for each water regime
    sfo = (1 + straw_t_ha * cfoa) ** expo
    return efc * sfw * sfp * sfo * days         # kg CH4 per ha per season

flooded = run("continuous_flood", (0.73, 1.27))
awd     = run("multiple_drainage", (0.41, 0.72))

def summary(name, x):
    lo, med, hi = np.percentile(x, [2.5, 50, 97.5])
    print(f"{name:8s} median {med:6.1f}   95% range {lo:6.1f} to {hi:6.1f}  kg CH4/ha/season")

summary("Flooded", flooded)
summary("AWD", awd)
saving = 100 * (1 - awd / flooded)
lo, med, hi = np.percentile(saving, [2.5, 50, 97.5])
print(f"AWD saving: median {med:.0f}%   95% range {lo:.0f}% to {hi:.0f}%")

fig, ax = plt.subplots(figsize=(8, 4.5))
ax.hist(flooded, bins=80, alpha=0.6, color="#4C72B0", label="Flooded: spread of 10,000 trials")
ax.hist(awd, bins=80, alpha=0.6, color="#55A868", label="AWD: spread of 10,000 trials")
ax.set_xlabel("Methane emitted (kg CH4 per hectare per season)")
ax.set_ylabel("Number of trials")
ax.set_title("Uncertainty from the IPCC default factors, South Asia")
ax.legend(title="Taller bar = more likely value")
plt.tight_layout()
plt.savefig("uncertainty.png", dpi=150)
plt.show()
