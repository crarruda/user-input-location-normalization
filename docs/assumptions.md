# Assumptions

This method relies on the following assumptions:

1. User-input location fields are self-reported and may reflect identity,
   affiliation, or aspiration rather than actual residence.

2. Country-level aggregation is a defensible compromise between interpretability
   and reliability for large-scale UGC analysis.

3. Deterministic rules are preferred over probabilistic inference to ensure
   transparency and reproducibility.

4. External geocoding services, when enabled, are treated as weak evidence and
   are only used as a fallback after deterministic resolution fails.

5. The reference cities gazetteer is assumed to be sufficiently comprehensive
   for country-level normalization, but not exhaustive at sub-national scales.