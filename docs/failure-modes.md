# Failure Modes

The normalization method may fail or produce unidentified outputs in the
following cases:

- Inputs containing emojis, jokes, slogans, or non-geographic identifiers
- References to continents or broad regions (e.g. "Europe", "Middle East")
- Ambiguous abbreviations shared across countries
- Misspellings or colloquial place names not covered by manual patterns
- Locations whose country cannot be reliably inferred even via geocoding
- Strategic self-presentation by users (e.g. "Citizen of the world")

In these cases, the method intentionally assigns an explicit unidentified label
rather than forcing a potentially incorrect classification.