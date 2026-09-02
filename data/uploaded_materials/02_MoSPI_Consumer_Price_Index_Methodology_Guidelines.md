
# MoSPI Guidelines on Consumer Price Index (CPI) Compilation

## 1. Index Architecture and Weighting Framework
The Consumer Price Index (CPI) compiled by the Economic Statistics Division (ESD) measures changes over time in the general level of prices of goods and services that a reference population acquires, uses, or pays for consumption. The All-India CPI is constructed for three distinct series: CPI (Rural), CPI (Urban), and CPI (Combined).

The weighting diagram is derived from the nationwide Household Consumption Expenditure Survey (HCES). The compilation utilizes a modified Laspeyres price index formula with fixed base-period expenditure weights:
I = sum(w_i * (p_it / p_i0)) / sum(w_i)
Where w_i is the expenditure weight of item i in the base period, p_it is current price, and p_i0 is base price.

## 2. Elementary Aggregation: Jevons vs Dutot vs Carli
At the elementary aggregate level (lowest stratum where weights are not available), prices from multiple representative markets across states are aggregated. MoSPI standards mandate the Jevons Index (geometric mean of price relatives or ratio of geometric means) due to its axiomatic superiority in satisfying the time-reversal and transitivity tests, avoiding the upward bias inherent in the Carli arithmetic mean index.

## 3. Imputation of Missing Quotations & Seasonal Items
When a price quotation is unavailable due to temporary market closure or stock-out, the price is imputed based on the average price change of comparable varieties in the same subgroup within that state. For seasonal fruits and vegetables, zero-weight imputation is avoided; instead, the index uses varying monthly seasonal weights or carries forward the last available price adjusted by the subgroup inflation trend.

## 4. Housing Rent Index (Repeat Rent Method)
The housing rent index in CPI (Urban) is calculated through a semi-annual panel of sample dwellings across cities, using the Chain Base Method to capture actual rented dwelling disbursements and owner-occupied equivalent imputations.
