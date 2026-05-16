# Validation

The normalization logic has been validated through repeated reuse across
multiple independent user-generated content (UGC) datasets, primarily in
tourism and mobility research. Validation has emphasized robustness and
interpretability over recall.

## Validation criteria

Three properties have been monitored across datasets:

1. **Stability**
   Identical input strings consistently produce identical outputs,
   regardless of dataset, language mix, or sampling order. This is
   enforced by construction (deterministic regex + gazetteer lookup)
   and verified by re-running the normalization on previously normalized
   samples.

2. **Error containment**
   Inputs that cannot be reliably resolved are explicitly assigned to
   the `unidentified` label rather than forced into the nearest
   plausible country. Validation confirmed that ambiguous strings
   (continents, emojis, joke inputs, country abbreviations shared
   across nations) consistently fall into the unidentified bucket
   instead of contaminating real country counts.

3. **Downstream aggregation behavior**
   Normalized outputs were checked against aggregation tasks
   (country-level review counts, visitor-origin distributions) to
   confirm that the output vocabulary supports clean group-by
   operations without inflating dimensionality.

## Categories of inputs checked

The following input classes have been observed and verified to behave
as intended:

- Country names in multiple languages (e.g. *Italia*, *Türkiye*, *Brasil*)
- Country abbreviations and demonyms (e.g. *UK*, *USA*, *NZ*)
- City-only inputs resolvable via the gazetteer (e.g. *London*, *São Paulo*)
- State / province codes (e.g. *CA*, *TX*, *NY*, *SP*)
- State codes shared across countries (handled via the US/BR fallback in
  `cities.resolve_shared_state_code`)
- Continents and broad regions (e.g. *Europe*, *Middle East*) — mapped to
  `unidentified`
- Non-geographic strings, emojis, and self-presentation phrases — mapped
  to `unidentified`
- Empty strings, `None`, and whitespace-only inputs — mapped to
  `unidentified`

## What validation does *not* cover

- The method has not been benchmarked against a gold-standard labelled
  dataset of user-input locations; no such dataset is publicly available
  at sufficient scale.
- Precision at the sub-national level (city, region) is intentionally
  out of scope and has not been validated.
- The behavior of the geocoding fallback depends on a third-party
  service (e.g. Nominatim) and is not deterministic across releases
  of the underlying gazetteer or model.
- Manual override patterns (`patterns._manual_country_patterns`)
  reflect empirical observations from specific UGC platforms. Their
  coverage in other contexts has not been formally evaluated.

## Reproducing the validation

The `examples/basic_usage.py` script exercises a representative set
of inputs covering each of the categories above. Running it against
`data/cities.csv` should produce stable outputs on repeated runs.

A systematic test suite (`tests/`) covering the same input categories
is on the roadmap.
