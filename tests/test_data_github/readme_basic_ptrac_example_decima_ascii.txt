Basic PTRAC Example - DECIMA (ASCII)

Geometry:
- Three concentric spherical shells:
  • Cell 501: HEU (Highly Enriched Uranium), radius ≤ 5 cm (surface 401)
  • Cell 502: Water moderator, 5–6 cm (bounded by surfaces 401 and 402)
  • Cell 503: Air, 6–7 cm (bounded by surfaces 402 and 403)
  • Outside (cell 999): void (beyond surface 403)

Surfaces:
- 401: Sphere of radius 5 cm
- 402: Sphere of radius 6 cm
- 403: Sphere of radius 7 cm

Source:
- Neutron source defined with SDEF
- Located at the center (0,0,0), inside cell 501
- Energy spectrum: Cf-252 spontaneous fission (using SI1/SP1)
- Angular distribution: anisotropic (SI2/SP2)

Materials:
- m601: Highly Enriched Uranium (U-235 ~93%)
- m602: Liquid water (H2O) at room temperature
- m603: Dry air near sea level

Physics & Output:
- Mode n p (neutrons and protons)
- One tally: F4 (flux) in cell 501, with energy bins
- PTRAC: ASCII file output enabled (write=all)
- 10,000 particle histories (nps 10000)

Purpose:
This input provides a simple yet representative case for PTRAC analysis in DECIMA.
It includes realistic nuclear data (HEU, water, air), a Cf-252 source, and a tally
to compare simulated neutron transport with tracking information.
