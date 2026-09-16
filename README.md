# Logistics Data Analyst Internship

A practical logistics data analytics project completed as part of a Data
Analyst Internship. The project focuses on data collection, cleaning,
preprocessing, validation, quality analysis, and operational insights
using Python and Pandas.

## Project Overview

This project uses a historical supply-chain delivery dataset to analyze
logistics performance and prepare reliable data for further analytics.

**Workflow:** Raw Data → Data Cleaning → Data Validation → Data Quality
Analysis → Business Insights

The dataset contains **10,324 shipment records and 35 original columns**
covering shipment details, vendors, countries, products, delivery dates,
quantities, values, weights, and freight costs.

## Objectives

-   Clean and preprocess raw logistics data
-   Standardize column names and data formats
-   Handle missing and inconsistent values
-   Convert numeric and date fields into usable formats
-   Identify duplicate records
-   Calculate delivery performance metrics
-   Identify potential freight-cost outliers
-   Calculate cost-per-unit metrics
-   Validate the cleaned dataset
-   Analyze delivery performance by country and shipment mode
-   Document the complete preprocessing methodology

## Dataset

The project uses a historical supply-chain and logistics delivery
dataset containing information about shipments, projects, purchase
orders, countries, vendors, shipment modes, products, delivery dates,
quantities, values, weights, freight costs, and manufacturing sites.

The raw Excel dataset is used as the source for preprocessing. The
cleaned CSV is the main analysis-ready output.

### Dataset Size

  Metric                Value
  ------------------ --------
  Original records     10,324
  Original columns         35
  Final columns            38
  Duplicate rows            0
  Final records        10,324

## Data Cleaning & Preprocessing

The `data_cleaning.py` script performs the main preprocessing pipeline.

### Column Name Cleaning

Column names are stripped of unnecessary whitespace and a known encoding
artifact in the ID column is removed.

### Duplicate Detection

Duplicate records are checked before and after cleaning.

**Result:** 0 duplicate rows.

### Missing Value Standardization

Common representations such as blank strings, `NA`, `N/A`, `NULL`, and
similar values are standardized to Pandas `NaN`.

### Missing Shipment Mode

The original dataset contained **360 missing Shipment Mode values**.
These were replaced with `Unknown` rather than deleting the records.

### Missing Dosage

The original dataset contained **1,736 missing Dosage values**. These
were replaced with `Unknown`.

### Numeric Conversion

Important numeric columns are converted using Pandas numeric conversion,
including:

-   Line Item Quantity
-   Line Item Value
-   Pack Price
-   Unit Price
-   Line Item Insurance (USD)
-   Weight (Kilograms)
-   Freight Cost (USD)

### Date Conversion

The following date fields are converted to datetime values:

-   PQ First Sent to Client Date
-   PO Sent to Vendor Date
-   Scheduled Delivery Date
-   Delivered to Client Date
-   Delivery Recorded Date

### Delivery Delay

A `Delivery Delay Days` metric is created:

**Delivery Delay Days = Delivered to Client Date − Scheduled Delivery
Date**

Negative values indicate early delivery, zero indicates delivery on
schedule, and positive values indicate late delivery.

### On-Time Delivery

An `On Time Delivery` flag is created:

-   Delay \<= 0 → `Yes`
-   Delay \> 0 → `No`

### Freight Cost per KG

A normalized freight metric is calculated:

**Freight Cost per KG = Freight Cost (USD) / Weight (Kilograms)**

The calculation is performed only when weight is greater than zero.

### Freight Cost Outlier Detection

Potential freight-cost outliers are identified using the Interquartile
Range (IQR) method.

**Upper Limit = Q3 + 1.5 × IQR**

Records above the upper limit are flagged as `Potential Outlier`. They
are not automatically deleted because an extreme value may be a
legitimate business event or may require further investigation.

### Cost per Unit

A `Cost per Unit` metric is calculated:

**Cost per Unit = Line Item Value / Line Item Quantity**

The calculation is performed only when quantity is greater than zero.

### Text Encoding Correction

A known country-name encoding issue was corrected:

`CÃ_x0083_Â´te d'Ivoire` → `Côte d'Ivoire`

### Metadata Removal

Temporary local metadata columns such as `Load_Date` and `Source_System`
are removed when present because they are not required for the analysis.

## Data Validation

The `validate_cleaned_data.py` script checks:

-   Dataset dimensions
-   Data types
-   Delivery date ranges
-   Delivery delay statistics
-   On-time versus late deliveries
-   Freight cost per kilogram statistics
-   Cost per unit statistics
-   Remaining missing values
-   Duplicate records

The validated cleaned dataset contains **10,324 records and 38
columns**.

## Key Data Quality Findings

### Missing Values

Important missing-value counts include:

  Column                           Missing Records
  ------------------------------ -----------------
  PO Sent to Vendor Date                     5,732
  Freight Cost per KG                        4,150
  Freight Cost (USD)                         4,126
  Weight (Kilograms)                         3,952
  PQ First Sent to Client Date               2,681
  Line Item Insurance (USD)                    287

These values were retained where reliable imputation could not be
justified.

### Zero Values

  Field                  Zero Values
  -------------------- -------------
  Line Item Quantity               0
  Line Item Value                 17
  Unit Price                     103
  Weight                           1
  Freight Cost                     0

These were treated as data-quality observations rather than blindly
removed.

## Delivery Performance

Overall results:

-   **Total shipments:** 10,324
-   **On-time deliveries:** 9,138
-   **Late deliveries:** 1,186
-   **On-time delivery rate:** 88.51%
-   **Late delivery rate:** 11.49%

### Delivery Delay Statistics

  Metric       Days
  --------- -------
  Mean        -6.02
  Median          0
  Minimum      -372
  Maximum       192

The negative mean indicates that many shipments were delivered before
their scheduled dates, while a smaller number of highly delayed
shipments contribute to the wide range.

## Shipment Mode Performance

  Shipment Mode     Shipments   Average Delay   On-Time Rate
  --------------- ----------- --------------- --------------
  Air                   6,113           -3.76         90.40%
  Air Charter             650          -19.04         88.46%
  Ocean                   371            5.87         82.48%
  Truck                 2,830           -9.92         83.92%
  Unknown                 360           -2.51         98.89%

Among the identified transportation modes, Air has the highest on-time
rate at **90.40%**, while Ocean has the lowest at **82.48%**. The
Unknown category represents missing source information and should
therefore be interpreted cautiously.

## Country Performance

Selected results:

  Country           Shipments   Average Delay   On-Time Rate
  --------------- ----------- --------------- --------------
  South Africa          1,406          -12.22         91.82%
  Nigeria               1,194          -11.22         88.11%
  Côte d'Ivoire         1,083           -5.38         87.63%
  Uganda                  779           -7.58         87.42%
  Vietnam                 688           -0.35         99.13%
  Zambia                  683           -5.23         84.19%
  Haiti                   655           -2.43         90.53%
  Mozambique              631           -1.21         81.62%
  Zimbabwe                538          -11.01         85.69%
  Congo, DRC              333           11.24         75.08%

Congo, DRC shows comparatively weak delivery performance, with a
**75.08% on-time rate** and an average delay of **11.24 days**.

## Freight Cost & Cost Outliers

Potential freight-cost anomalies were detected using the IQR method.

Examples from the analysis include:

-   Nigeria, Air Charter: **\$31,087.71/kg**
-   Nigeria, Air Charter: **\$22,590.31/kg**
-   Nigeria, Air: **\$19,480.97/kg**
-   Côte d'Ivoire, Unknown mode: **\$9,789.07/kg**

These records should be investigated before being used for business
decisions. An outlier can represent a genuine special shipment, unusual
transportation conditions, or a data-entry problem.

Potential cost-per-unit outliers were also identified, including
high-cost HRDT records.

## Business Insights

1.  Overall on-time delivery performance is **88.51%**, but the 11.49%
    late-delivery rate remains an important operational area to
    investigate.
2.  Ocean shipments have the lowest on-time rate among the identified
    shipment modes.
3.  Congo, DRC has comparatively weak delivery performance and positive
    average delay.
4.  Freight cost per kilogram contains extreme values, especially for
    very low-weight shipments.
5.  Missing weight and freight-cost information limits some
    cost-efficiency analysis.
6.  Missing shipment-mode information should be investigated at the
    source; labeling it `Unknown` preserves the records but does not
    explain the missing data.

## Project Structure

logistics-data-analyst-internship/
│
├── data/
│   ├── SCMS_Delivery_History_Raw_Data.xlsx
│   └── SCMS_Delivery_History_Cleaned.csv
│
├── reports/
│   └── week3_visualizations/
│       ├── 01_on_time_vs_delayed.png
│       ├── 02_shipment_volume_by_mode.png
│       ├── 03_delivery_delay_distribution.png
│       ├── 04_average_delay_by_mode.png
│       ├── 05_freight_cost_by_mode.png
│       ├── 06_freight_cost_per_kg_distribution.png
│       ├── 07_top_10_countries.png
│       ├── 08_on_time_rate_by_mode.png
│       ├── 09_weight_vs_freight_cost.png
│       └── 10_yearly_shipment_trend.png
│
├── week3_outputs/
│   ├── correlation_matrix.csv
│   ├── country_analysis.csv
│   ├── freight_analysis.csv
│   ├── freight_cost_outliers.csv
│   ├── product_group_analysis.csv
│   ├── shipment_mode_analysis.csv
│   └── vendor_analysis.csv
│
├── scripts/
│   ├── data_cleaning.py
│   ├── validate_cleaned_data.py
│   ├── quality_analysis.py
│   ├── logistics_analysis.py
│   ├── week3_analysis.py
│   └── week3_eda_visualization.py
│
├── analysis_findings.docx
├── Week_1_Strategic_Planning_Logistics.docx
├── Week_2_Data_Cleaning_Preprocessing_Logistics_Updated.docx
├── .gitignore
└── README.md

## Technologies Used

-   Python
-   Pandas
-   NumPy
-   openpyxl
-   Git
-   GitHub
-   Visual Studio Code

## How to Run

Install the required libraries:

``` bash
pip install pandas numpy openpyxl
```

Run the cleaning pipeline:

``` bash
python scripts/data_cleaning.py
```

Validate the cleaned dataset:

``` bash
python scripts/validate_cleaned_data.py
```

Run quality analysis:

``` bash
python scripts/quality_analysis.py
```

Run logistics analysis:

``` bash
python scripts/logistics_analysis.py
```

## Reports

The `reports` folder contains:

-   **Week 1 -- Strategic Planning & Logistics Analysis**
-   **Week 2 -- Data Cleaning & Preprocessing for Logistics Analysis**

The Week 2 report documents the data collection approach, preprocessing
methodology, missing-value handling, outlier detection, Python
implementation, validation, and reflection.

## Limitations

-   The dataset contains historical logistics records and should not
    automatically be interpreted as current operational performance.
-   Several operational and freight-related fields contain missing
    values.
-   Potential outliers are flagged rather than automatically removed.
-   `Unknown` shipment mode represents missing source information, not a
    real transportation mode.
-   Additional business context would be required to determine the root
    causes of delivery delays and freight-cost anomalies.

## Future Improvements

-   Build an interactive Power BI dashboard
-   Analyze monthly delivery trends
-   Create vendor performance scorecards
-   Perform route and country risk analysis
-   Investigate root causes of major delays
-   Analyze freight-cost efficiency
-   Build predictive models for late-delivery risk

## Conclusion

This project demonstrates an end-to-end data preprocessing and logistics
analytics workflow. The approach focuses on preserving useful
information, clearly handling unknown values, validating
transformations, calculating meaningful logistics KPIs, and flagging
anomalies for further investigation.

The cleaned dataset provides a reliable foundation for future dashboard
development, business intelligence, and advanced logistics analysis.

## Author

**Nikita Bhandari**

Data Analyst \| Python \| Pandas \| SQL \| Excel \| Power BI

GitHub: https://github.com/bhandari-nikita
