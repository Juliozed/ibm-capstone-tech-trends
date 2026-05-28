# Project Name

One sentence description of what this project does and what business problem it solves.

## Overview

2-3 sentences expanding on the project. What data? What questions does it answer? What did you find?

## Tech Stack

| Tool | Purpose |
|------|---------|
| PostgreSQL | Data warehouse |
| Python / pandas | Data cleaning and analysis |
| dbt | ELT transformation layer |
| Power BI | Dashboard and visualization |
| SQL | Ad-hoc analysis and querying |

## Project Structure

```
project-name/
├── notebooks/
│   └── 01_analysis.ipynb      ← EDA and analysis
├── scripts/
│   ├── db_connect.py           ← database connection
│   ├── cleaning_utils.py       ← data cleaning functions
│   ├── chart_templates.py      ← reusable chart functions
│   └── report_generator.py     ← automated Excel report
├── dbt_project/
│   └── models/
│       ├── staging/            ← data cleaning models
│       └── marts/              ← business logic models
├── reports/                    ← generated outputs
├── data/
│   └── processed/              ← cleaned data
├── .env.example                ← credentials template
├── requirements.txt            ← Python dependencies
└── README.md
```

## Setup

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/project-name.git
cd project-name

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure credentials
cp .env.example .env
# Edit .env with your database credentials

# 5. Run dbt
cd dbt_project
dbt debug --profiles-dir .
dbt run --profiles-dir .
dbt test --profiles-dir .

# 6. Generate report
python scripts/report_generator.py
```

## Key Findings

- **Finding 1:** Replace with actual finding + supporting number
- **Finding 2:** Replace with actual finding + supporting number  
- **Finding 3:** Replace with actual finding + supporting number

## Dashboard Preview

![Dashboard Screenshot](reports/dashboard_screenshot.png)

*Add your Power BI dashboard screenshot here*

## Data Model

```
source_table_1 ──→ stg_table_1 ──→ fct_main
source_table_2 ──→ stg_table_2 ──→
                                 ──→ mart_summary
```

## Skills Demonstrated

`SQL` `PostgreSQL` `Python` `pandas` `dbt` `Power BI` `ELT` `Data Modeling` `Automated Reporting`

---

*Built as part of data analytics portfolio — CDMX & US Remote job market*
