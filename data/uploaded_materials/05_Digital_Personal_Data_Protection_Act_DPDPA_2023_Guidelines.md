
# DPDPA 2023 & Statistical Confidentiality Directives

## 1. Statutory Role as Data Fiduciary
Under the Digital Personal Data Protection Act 2023 (DPDPA), the Ministry of Statistics & Programme Implementation acts as a Significant Data Fiduciary when collecting, storing, and processing digital household and enterprise records. The Collection of Statistics Act 2008 grants statutory authority for compulsory data gathering, but DPDPA 2023 imposes strict data minimization, purpose specification, and security safeguards.

## 2. Statistical Anonymization Standards
Prior to releasing public microdata files on the MoSPI Data Portal, statistical disclosure control (SDC) must be executed:
- **Direct Identifiers Elimination**: Complete removal of Aadhaar numbers, PAN, phone numbers, exact residential street addresses, and names.
- **k-Anonymity (k >= 5)**: In any public microdata release, any combination of quasi-identifiers (such as Age, Gender, District Code, Religion, and Occupation) must be identical for at least k distinct individuals.
- **Top-Coding and Bottom-Coding**: Extreme values of income or asset holdings (e.g., top 1% percentile) are top-coded with a single threshold value to prevent re-identification through public auxiliary registers.

## 3. Penalty Framework and Breach Notification
Section 8(6) of DPDPA mandates that in the event of a personal data breach, the data fiduciary must notify the Data Protection Board of India and each affected data principal within the prescribed timeframe. Significant financial penalties (up to ₹250 Crore) are stipulated for failure to take reasonable security safeguards.
