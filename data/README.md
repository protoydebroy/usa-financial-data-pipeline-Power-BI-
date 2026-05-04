# Data folder

This folder intentionally does not contain the real customer data files.

The pipeline ingests financial records that include personally identifiable information (PII) such as customer names, Social Security Numbers, occupations, and salary details. Committing this data to a public repository would violate privacy expectations.

For schema details, see [`sample_data_schema.md`](sample_data_schema.md).

If you want to test the pipeline yourself, generate synthetic data matching the schema above. A small Python script using `Faker` and `numpy.random` can produce realistic test data in a few minutes.
