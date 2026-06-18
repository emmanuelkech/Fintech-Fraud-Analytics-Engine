# Enterprise Fintech Fraud Analytics Engine

## Project Overview
This project builds an end-to-end relational data engine that aggregates 10,000 fintech transaction records to detect payment fraud patterns (such as high-value proxy/VPN transactions) and evaluate risk exposures across customer KYC levels.

## Tech Stack Used
- **Database Architecture:** PostgreSQL (Star Schema Data Modeling)
- **Data Engineering & Generation:** Python (SQLAlchemy, Pandas, Faker)
- **Business Intelligence & DAX:** Power BI Desktop

## Data Model (Star Schema)
- `fact_transactions`: Contains core transaction processing logs (Amounts, Timestamps, VPN flags).
- `dim_users`: Stores account information and customer identity verifications (KYC Tier 1, Tier 2, Tier 3).
- `dim_merchants`: Tracks merchant categories (Crypto, Gaming, E-Commerce).

## Key Business Insights Found
1. **VPN-Driven Fraud:** Transactions routing through VPN networks account for a disproportionately high fraud conversion rate, suggesting a need for stricter multi-factor challenges.
2. **Category Exposure:** The Crypto Exchange and Gaming merchant verticals demonstrated elevated chargeback vulnerabilities compared to retail food/grocery sectors.

## How to Run This Project Locally
1. Clone this repository.
2. Run `CREATE DATABASE fintech_fraud_db;` in your PostgreSQL server.
3. Update the connection parameters in `generate_data.py` and run it to populate the data.
4. Open `Fintech_Fraud_Analytics.pbix` using Power BI Desktop to view the fully interactive executive control suite.
