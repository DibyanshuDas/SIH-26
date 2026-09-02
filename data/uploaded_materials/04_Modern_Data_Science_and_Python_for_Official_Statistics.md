
# Python & Polars Data Processing Standards for Official Statistics

## 1. High-Performance Microdata Ingestion
Official statistical surveys generate massive fixed-width ASCII or CSV files containing millions of record entries across hierarchical blocks (Household Level, Person Level, Enterprise Level). Modern data pipelines within MoSPI's Data Informatics & Innovation Division (DIID) utilize Python with `polars` and `pyarrow` for memory-mapped, zero-copy reads.

For fixed-width NSS files:
```python
import polars as pl

schema = {"fsu": pl.Utf8, "sss": pl.Int32, "weight": pl.Float64, "income": pl.Float64}
df = pl.read_csv("nss79_schedule.csv", schema=schema)
```

## 2. Weighted Aggregations & Sub-Sample Multiplier Rules
In NSS multi-stage sampling, each household record is accompanied by a sampling weight (multiplier):
Multiplier = (Total Frame Population in Stratum / Total Sample Selected) / 100.
When calculating population totals, estimates must always apply the normalized sampling weight:
Estimated Total = sum(x_i * weight_i).
When combining Central Sample and State Sample results (pooled estimation), sub-sample weights must be halved or normalized by the relative inverse variance matrix.

## 3. Automated Anomaly Detection & Consistency Checking
Automated validation scripts execute multi-rule logical consistency audits:
1. Demographic validation: Age of head of household vs. age of biological children (delta >= 14 years).
2. Economic plausibility: Total monthly expenditure vs reported detailed item purchases.
3. Outlier identification: Mahalanobis distance and Isolation Forest algorithms on unit values (price per kg) to catch decimal point entry errors by enumerators during CAPI tablet entry.
