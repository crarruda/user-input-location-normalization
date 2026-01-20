# User-Input Location Normalization

## Overview

User-reported location fields are a common component of user-generated content (UGC) platforms.
However, these fields are typically free-text, optional, and highly heterogeneous, resulting in extremely high cardinality and inconsistent geographic semantics.

This repository provides a deterministic method to **normalize noisy user-input location strings into a controlled country-level taxonomy**.
It handles explicit ambiguity, missingness, and non-geographic inputs.

The method has been developed and reused across multiple academic and applied projects involving large-scale UGC data, including tourism and mobility analysis, where robustness and interpretability are preferred over probabilistic inference.

## Problem Definition

User-input location fields suffer from several structural issues:

* Free-text input (no controlled vocabulary)
* Mixed geographic scales (city, region, country, continent)
* Non-geographic values (emojis, jokes, affiliations)
* Language variation and abbreviations
* Inconsistent formatting and spelling
* Strategic self-presentation by users

Left untreated, this variability:

* inflates dimensionality,
* prevents meaningful aggregation,
* introduces silent bias in downstream spatial or demographic analyses.

The goal of this repository is **not** to infer precise user location, but to **reduce uncontrolled variability** while preserving uncertainty.

---

## Design Principles

The normalization strategy follows four explicit principles:

1. **Country-level resolution**  
   Normalization is performed at the country level only.  
   Finer geographic inference (city, region) is intentionally avoided due to unreliability and bias in self-reported data.

2. **Deterministic over probabilistic logic**  
   Rule-based matching is preferred over probabilistic or model-based inference to ensure transparency, reproducibility, and auditability.

3. **Explicit handling of ambiguity**  
   Inputs that cannot be reliably mapped are preserved as *unidentified* rather than force-assigned.

4. **Stability across datasets**  
   The method prioritizes consistent behavior across datasets and projects over maximal recall in any single case.

---

## Method Overview

The normalization process consists of the following stages:

1. **Pre-cleaning**  
   Basic normalization of casing, whitespace, punctuation, and known noise patterns.

2. **Rule-based matching**  
   Matching against a curated mapping of country names, common variants, abbreviations, and demonyms.

3. **Controlled vocabulary assignment**  
   Valid inputs are mapped to a predefined list of standardized country identifiers.

4. **Fallback and ambiguity handling**  
   Inputs that are empty, non-geographic, or ambiguous are assigned to an explicit `unidentified` category.

At no stage is geographic inference extrapolated beyond what the input plausibly supports.

---

## Public API

The repository exposes a single public entry point:

```python
normalize_location(
    raw_location: str | None,
    *,
    cities_df: pandas.DataFrame,
    unidentified_label: str = "unidentified",
    use_geocoding: bool = True,
    geolocator = None,
) -> str
```

The function applies a strict resolution hierarchy:

1. Deterministic pattern-based matching using a reference cities gazetteer
2. Optional external geocoding fallback (e.g. Nominatim)
3. Explicit assignment to an unidentified category

Batch processing, caching, and pipeline orchestration are intentionally out of scope.

---

## Validation Strategy

The method has been validated empirically through repeated reuse across independent datasets, focusing on:

* **Stability**: identical inputs consistently map to identical outputs
* **Error containment**: ambiguous cases are isolated rather than propagated
* **Downstream impact**: normalized outputs support aggregation without artificial inflation of categories

Validation emphasizes *robustness* rather than completeness. The objective is to avoid false precision.

---

## Known Limitations

This approach intentionally accepts several limitations:

* Country-level aggregation obscures sub-national variation
* Self-reported locations may reflect identity rather than residence
* Language-specific edge cases are handled conservatively
* No attempt is made to infer location from indirect signals

These limitations are not implementation flaws, but methodological choices aligned with the intended use of the data.

---

## Intended Use

This repository is intended for:

* Preprocessing UGC datasets prior to spatial or demographic analysis
* Reducing dimensionality in user-reported location fields
* Ensuring reproducible and transparent handling of noisy location inputs
* Supporting research where interpretability and robustness are prioritized over inference

It is **not** intended for individual-level geolocation or high-precision spatial analysis.

---

## Dependencies

This implementation relies on an openly licensed reference cities gazetteer:

**Countries States Cities Database**
https://github.com/dr5hn/countries-states-cities-database
License: MIT

The dataset is used exclusively as a reference vocabulary and is included
unchanged for reproducibility.

## Citation and Reuse

If you reuse or adapt this method in academic work, please cite the repository
and clearly state the chosen level of geographic aggregation and its implications.

---

## License

**Code**

The code in this repository is released under the MIT License.
See the LICENSE file for details.

**Third-party data**

The included cities.csv dataset is licensed under the MIT License
by its original authors and is redistributed here under the same terms.

---

*This repository represents a reusable methodological component extracted from a broader research pipeline and is published as a standalone artefact to support transparency and reproducibility.*
