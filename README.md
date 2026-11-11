# Rice methane model (IPCC 2019 Tier 1)
 
How much does methane from one rice crop in South Asia change under
alternate wetting and drying (AWD), with and without straw, and how
uncertain is the estimate?
 
## Result
- Flooded: 95.2 kg CH4/ha/season. AWD: 52.4. Saving: 45%
  (95% range 18% to 63%, 10,000 Monte Carlo trials).
- Straw (5 t/ha, mixed in < 30 days before planting) raises emissions
  by a factor of 2.88.
 
![Scenarios](figures/scenarios.png)
![Uncertainty](figures/uncertainty.png)
 
## How to run (Google Colab, no installation)
1. Open colab.research.google.com and start a new notebook.
2. Paste ch4_core.py into a cell and run it. Two lines should appear,
   ending with: All checks passed.
3. Paste step2_scenarios.py, then step3_uncertainty.py, into new cells
   and run them.
 
## Files
- ch4_core.py: the model (equations 5.1 to 5.3) and tests
- step2_scenarios.py: scenario table and chart
- step3_uncertainty.py: Monte Carlo uncertainty
- writeup.pdf: full write-up
 
## Method and assumptions
- Equations: EFi = EFc x SFw x SFp x SFo; SFo = (1 + sum(ROA x CFOA))^0.59.
- Values from IPCC (2019), Vol. 4, Ch. 5, Tables 5.11 to 5.14.
- AWD is the IPCC class 'multiple drainage periods' (Table 5.12, note b).
- IPCC ranges treated as 95% intervals, lognormal. The IPCC text is
  inconsistent on this (95% CI in the tables, standard deviation in
  Section 5.5.5).
- Tests include the IPCC worked example (410.47 Gg CH4/yr).
 
## Reference
IPCC (2019). 2019 Refinement to the 2006 IPCC Guidelines for National
Greenhouse Gas Inventories, Volume 4, Chapter 5, Section 5.5.
 
## Author and acknowledgements
Kessia Maria Kins. Guidance from Dr. Chalapathy Reddy. AI tools helped check code.
 
## Licence
MIT License. Copyright © 2026 kessiamk
<img width="451" height="589" alt="image" src="https://github.com/user-attachments/assets/4bab3f2d-5c5c-41c5-affa-7ae9c9f7b866" />
