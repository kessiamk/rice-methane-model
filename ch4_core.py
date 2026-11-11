"""Core rice CH4 model: IPCC 2019 Refinement, Vol. 4, Ch. 5, Section 5.5 (Tier 1).

Equations
  EF_i  = EFc * SFw * SFp * SFo                  (Eq. 5.2)
  SFo   = (1 + sum(ROA_i * CFOA_i)) ** 0.59      (Eq. 5.3)
  CH4   = sum(EF_i * t * A) * 1e-6  [Gg/yr]      (Eq. 5.1)

All defaults below were read from the 2019 Refinement PDF. Check every number
against Tables 5.11, 5.11A, 5.12, 5.13, 5.14 (pp. 5.53-5.56) before you cite it.
"""

# Table 5.11: baseline EFc, kg CH4 ha-1 d-1 (continuously flooded, no amendments)
EFC = {
    "world": 1.19, "east_asia": 1.32, "southeast_asia": 1.22, "south_asia": 0.85,
    "europe": 1.56, "north_america": 0.65, "south_america": 1.27,
}

# Table 5.11A: default cultivation period, days
CULT_DAYS = {
    "world": 113, "east_asia": 112, "southeast_asia": 102, "south_asia": 112,
    "europe": 123, "north_america": 139, "south_america": 124,
}

# Table 5.12: SFw, water regime during cultivation (disaggregated column)
SFW = {
    "continuous_flood": 1.00, "single_drainage": 0.71, "multiple_drainage": 0.55,
    "rainfed_regular": 0.54, "rainfed_drought_prone": 0.16, "deep_water": 0.06,
    "upland": 0.0,
}

# Table 5.13: SFp, water regime before cultivation
SFP = {
    "nonflooded_lt180d": 1.00, "nonflooded_gt180d": 0.89,
    "flooded_gt30d": 2.41, "nonflooded_gt365d": 0.59,
}

# Table 5.14: CFOA, conversion factors for organic amendments
CFOA = {
    "straw_lt30d": 1.00, "straw_gt30d": 0.19, "compost": 0.17,
    "farmyard_manure": 0.21, "green_manure": 0.45,
}

SFO_EXPONENT = 0.59


def sf_o(amendments=None):
    """Eq. 5.3. amendments: {name: rate in t/ha} (dry weight for straw, fresh for others)."""
    amendments = amendments or {}
    total = sum(rate * CFOA[name] for name, rate in amendments.items())
    return (1.0 + total) ** SFO_EXPONENT


def adjusted_ef(region, water, pre_season, amendments=None):
    """Eq. 5.2: adjusted daily emission factor, kg CH4 ha-1 d-1."""
    return EFC[region] * SFW[water] * SFP[pre_season] * sf_o(amendments)


def season_ch4_per_ha(region, water, pre_season, amendments=None, days=None):
    """Seasonal CH4, kg CH4 ha-1 (EF x cultivation days)."""
    t = CULT_DAYS[region] if days is None else days
    return adjusted_ef(region, water, pre_season, amendments) * t


def total_ch4_gg(region, water, pre_season, area_ha, amendments=None, days=None):
    """Eq. 5.1 for one stratum: Gg CH4 per year."""
    return season_ch4_per_ha(region, water, pre_season, amendments, days) * area_ha * 1e-6


def to_co2e(kg_ch4, gwp):
    """Convert CH4 to CO2e. gwp is an input: state the IPCC report you take it from."""
    return kg_ch4 * gwp


if __name__ == "__main__":
    # Tests: hand-calculated values, then the model
    assert abs(sf_o({"straw_lt30d": 5}) - 2.88) < 0.005          # 6 ** 0.59
    assert abs(sf_o({"straw_gt30d": 2}) - 1.21) < 0.005          # 1.38 ** 0.59
    cf = season_ch4_per_ha("south_asia", "continuous_flood", "nonflooded_lt180d")
    awd = season_ch4_per_ha("south_asia", "multiple_drainage", "nonflooded_lt180d")
    assert abs(cf - 95.2) < 1e-9                                  # 0.85 x 112
    assert abs(awd - 52.36) < 1e-9                                # 0.85 x 0.55 x 112
    assert abs(total_ch4_gg("south_asia", "continuous_flood",
                            "nonflooded_lt180d", 100) - 0.00952) < 1e-12
    # IPCC worked example (Section 5.5.4, Tables 5.14b/5.14c): total 410.47 Gg CH4/yr.
    # The example's text says straw <30 d (CFOA 1.0), but its printed SFo of 1.21 equals
    # CFOA 0.19 (>30 d), so the test uses straw_gt30d. The IPCC rounds EF to 2 decimals.
    sfo_ex = round(sf_o({"straw_gt30d": 2}), 2)
    ex = [(1.5e6, 1.22 * 1.00 * 1.00 * sfo_ex, 102), (1.5e6, 1.22 * 0.55 * 1.00 * sfo_ex, 102),
          (9e5, 1.22 * 0.54 * 0.89, 102), (1.5e5, 1.22 * 0.06 * 2.41, 220)]
    assert abs(sum(a * round(ef, 2) * t * 1e-6 for a, ef, t in ex) - 410.47) < 0.01
    print(f"South Asia, 112 d: flooded {cf:.2f}, AWD {awd:.2f} kg CH4/ha/season, "
          f"reduction {100 * (1 - awd / cf):.0f}%")
    print("All checks passed")
