Logistics Data Analyst Internship

A practical logistics data analytics project completed as part of a Data Analyst Internship. The project focuses on logistics data collection, cleaning, preprocessing, data quality validation, and operational analysis using Python and Pandas.

Project Overview

This project analyzes historical logistics delivery data to identify delivery performance, shipment delays, data quality issues, freight-cost anomalies, and country/shipment-mode performance.

The project follows a structured data analytics workflow:

Raw Data → Data Cleaning → Data Validation → Quality Analysis → Business Insights

Objectives
Clean and preprocess raw logistics data
Handle missing and inconsistent values
Standardize column names and data types
Convert and validate date fields
Calculate delivery performance metrics
Identify potential freight-cost outliers
Calculate cost-per-unit metrics
Analyze shipment performance by country and shipment mode
Validate the final cleaned dataset
Document the complete preprocessing methodology
Dataset

The project uses a historical supply-chain and logistics delivery dataset containing 10,324 shipment records and 35 original columns.

The dataset contains information related to:

Shipment identification
Project and purchase order information
Country
Vendor
Shipment mode
Product information
Delivery dates
Quantity and value
Weight
Freight cost
Insurance cost
Manufacturing site

The cleaned dataset contains 10,324 records and 38 columns, including additional analytical metrics created during preprocessing.

Project Structure
logistics-data-analyst-internship/
│
├── data/
│   └── SCMS_Delivery_History_Cleaned.csv
│
├── reports/
│   ├── Week_1_Strategic_Planning_Logistics.docx
│   └── Week_2_Data_Cleaning_Preprocessing_Logistics_Updated.docx
│
├── scripts/
│   ├── data_cleaning.py
│   ├── validate_cleaned_data.py
│   ├── quality_analysis.py
│   └── logistics_analysis.py
│
├── .gitignore
└── README.md
Data Cleaning Process

The data_cleaning.py script performs the main preprocessing workflow.

1. Column Name Cleaning

Column names are stripped of unnecessary spaces and known encoding issues are corrected.

2. Duplicate Detection

Duplicate records are checked and removed if present.

The dataset contained 0 duplicate rows.

3. Missing Value Handling

Missing values are standardized and selected categorical fields are assigned meaningful values.

For example:

Missing Shipment Mode → Unknown
Missing Dosage → Unknown

Other missing values, such as freight cost, weight, and vendor-related dates, are retained as missing because replacing them with arbitrary values could distort the analysis.

4. Numeric Data Conversion

Important financial and quantity fields are converted into numeric data types, including:

Line Item Quantity
Line Item Value
Pack Price
Unit Price
Line Item Insurance
Weight
Freight Cost
5. Date Conversion

The following fields are converted to datetime format:

PQ First Sent to Client Date
PO Sent to Vendor Date
Scheduled Delivery Date
Delivered to Client Date
Delivery Recorded Date
6. Delivery Delay Calculation

A new metric called Delivery Delay Days is created:

Delivery Delay Days = Delivered to Client Date − Scheduled Delivery Date

A negative value indicates delivery before the scheduled date, while a positive value indicates a delay.

7. On-Time Delivery Flag

A new On Time Delivery field is created.

Shipments delivered on or before the scheduled delivery date are classified as:

Yes

Shipments delivered after the scheduled delivery date are classified as:

No

8. Freight Cost per KG

A new metric is calculated:

Freight Cost per KG = Freight Cost (USD) / Weight (Kilograms)

The calculation is performed only when the shipment has a positive weight.

9. Freight Cost Outlier Detection

Potential freight-cost outliers are identified using the Interquartile Range (IQR) method.

The upper threshold is calculated as:

Upper Limit = Q3 + 1.5 × IQR

Records above this threshold are flagged as:

Potential Outlier

These records are flagged rather than automatically deleted because an unusually high freight cost may represent a genuine logistics event rather than an error.

10. Cost per Unit

A new metric is calculated:

Cost per Unit = Line Item Value / Line Item Quantity

The calculation is performed only when the line item quantity is greater than zero.

11. Text Encoding Correction

Known encoding problems in country names are corrected, including the incorrect representation of Côte d'Ivoire.

Data Validation

The validate_cleaned_data.py script validates the cleaned dataset by checking:

Dataset dimensions
Data types
Date ranges
Delivery delay statistics
On-time delivery counts
Freight cost per KG statistics
Cost per unit statistics
Remaining missing values
Duplicate records

The final validation confirmed:

10,324 records
38 columns
0 duplicate rows
Scheduled delivery dates ranging from 2006 to 2015
On-time deliveries: 9,138
Delayed deliveries: 1,186
Overall on-time delivery rate: 88.51%
Quality Analysis

The quality_analysis.py script performs additional data-quality and logistics-performance analysis.

Key checks include:

Delivery performance
Delivery delays
Zero quantities and values
Zero unit prices
Zero weights
Freight-cost outliers
Cost-per-unit outliers
Missing-value analysis
Shipment-mode performance
Country-level performance
Key Findings
Delivery Performance

The dataset contains:

88.51% on-time deliveries
11.49% delayed deliveries

This indicates generally strong delivery performance, but the delayed shipments still represent a significant operational area for improvement.

Shipment Mode Performance

The analysis shows differences in delivery performance across shipment modes.

Shipment Mode	Shipments	On-Time Rate
Air	6,113	90.40%
Air Charter	650	88.46%
Ocean	371	82.48%
Truck	2,830	83.92%
Unknown	360	98.89%

The Unknown category should be interpreted carefully because missing shipment-mode information can distort comparisons.

Country Performance

There are also significant differences between countries.

For example:

Vietnam recorded an on-time rate of 99.13%
South Africa recorded 91.82%
Congo, DRC recorded 75.08%
Mozambique recorded 81.62%

Congo, DRC therefore represents an important area for further investigation because it combines a relatively low on-time rate with an average positive delivery delay.

Data Quality Issues Identified

The analysis identified several important data-quality issues:

Missing vendor-related dates
Missing weight values
Missing freight costs
Missing insurance values
Zero unit prices
Zero line-item values
Potential freight-cost outliers
Potential cost-per-unit outliers
Previously inconsistent country encoding
Missing shipment-mode values

Rather than blindly deleting these records, the preprocessing pipeline distinguishes between values that can safely be standardized and values that should remain missing for further investigation.

Technologies Used
Python
Pandas
NumPy
Jupyter/VS Code
Git
GitHub
Microsoft Excel
How to Run the Project

Clone the repository and navigate to the project directory.

Install the required Python libraries:

pip install pandas numpy openpyxl

Run the data-cleaning script:

python scripts/data_cleaning.py

Validate the cleaned dataset:

python scripts/validate_cleaned_data.py

Run the data-quality analysis:

python scripts/quality_analysis.py

Run the logistics analysis:

python scripts/logistics_analysis.py
Reports

The reports folder contains the internship documentation:

Week 1 – Strategic Planning for Logistics
Week 2 – Data Cleaning and Preprocessing for Logistics Analysis

These reports explain the business context, analytical approach, preprocessing methodology, and findings.

Business Value

High-quality logistics data is essential for reliable decision-making.

Accurate preprocessing enables organizations to:

Monitor delivery performance
Identify problematic shipment modes
Detect high-risk countries
Investigate unusual freight costs
Improve logistics planning
Reduce reporting errors
Build reliable dashboards and KPIs
Support data-driven operational decisions
Future Improvements

The project can be extended by developing:

Power BI logistics dashboards
Vendor performance analysis
Monthly delivery trends
Freight-cost benchmarking
Country risk analysis
Shipment-mode optimization
Vendor-level KPIs
Predictive delivery-delay models
Author

Nikita Bhandari

B.Sc. Information Technology
Data Analytics | Python | SQL | Excel | Power BI

GitHub: https://github.com/bhandari-nikita