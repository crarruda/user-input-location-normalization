## Reference Cities Dataset

This repository relies on an external cities gazetteer to support
deterministic normalization of user-input location strings.

### Source
Countries States Cities Database  
https://github.com/dr5hn/countries-states-cities-database

### License
MIT License (see original repository)

### File
`cities.csv`

### Fields used
- name
- state_code
- state_name
- country_name
- country_code

All other fields are ignored by the normalization logic.

### Role in the method
The dataset is used exclusively as a reference vocabulary to:
- identify valid country names
- resolve state-code ambiguities
- construct deterministic matching patterns

The dataset itself is not modified or enriched.
