# IBM Data Analytics Capstone
## Technology Trends Analysis — Stack Overflow Developer Survey 2024

A complete end-to-end data analytics project analyzing global technology trends from the 2024 Stack Overflow Developer Survey. Built as the capstone project for the IBM Data Analytics Professional Certificate.

---

## Project Overview

This project analyzes the current and future technology landscape by examining what 18,845 developers worldwide are using today and what they want to learn next. The findings provide strategic insights for organizations looking to align their talent and technology investments with where the industry is heading.

**Key Question:** What technologies are developers using today — and where is the industry heading next?

---

## Key Findings

- **Python is the future** — ranks 5th in current use but #1 in desired learning, driven by AI and data science demand
- **AI is already mainstream** — 57% of developers use AI tools daily in 2024
- **PostgreSQL overtook MySQL** — open-source enterprise databases are winning
- **Remote work is permanent** — 76% of developers work remotely or hybrid
- **C++ dominates job postings** — 26,000+ postings vs Python's strong salary average of $114,383

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python (pandas, requests) | Data extraction via API and wrangling |
| BeautifulSoup | Web scraping salary and language data |
| dbt | ELT transformation layer |
| PostgreSQL | Data warehouse |
| Google Looker Studio | Interactive dashboards |
| Groq AI (Llama 3.3) | AI-generated executive narrative |
| Gamma + PowerPoint | Presentation |
| Git / GitHub | Version control |

---

## Data Sources

| Source | Method | Records |
|--------|--------|---------|
| Stack Overflow Developer Survey 2024 | API extraction (requests) | 18,845 respondents |
| IBM Jobs Dataset | API extraction (requests) | 2,700 job postings |
| Programming Languages Salary Data | Web scraping (BeautifulSoup) | 11 languages |

---

## Project Structure

```
ibm-capstone-tech-trends/
├── notebooks/
│   └── 01_data_collection.ipynb   ← API extraction, wrangling, EDA, charts
├── scripts/
│   ├── db_connect.py              ← PostgreSQL connection
│   ├── cleaning_utils.py          ← data cleaning functions
│   ├── chart_templates.py         ← reusable chart library
│   └── report_generator.py        ← automated Excel reports
├── dbt_project/
│   └── models/
│       ├── staging/               ← data cleaning models
│       └── marts/                 ← business logic models
├── reports/
│   └── IBM_Capstone_Presentation.pptx  ← final presentation
├── .env.example                   ← credentials template
├── requirements.txt               ← Python dependencies
└── README.md
```

---

## Dashboards

Built in Google Looker Studio with 3 interactive tabs:

**Tab 1 — Current Technology Usage**
Top 10 languages, databases, platforms, and web frameworks developers use today.

**Tab 2 — Future Technology Trends**
Top 10 technologies developers want to learn next year.

**Tab 3 — Demographics**
Respondent breakdown by age, country, education level, and work arrangement.

---

## Setup

```bash
# 1. Clone the repository
git clone https://github.com/Juliozed/ibm-capstone-tech-trends.git
cd ibm-capstone-tech-trends

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure credentials
cp .env.example .env
# Edit .env with your database credentials

# 5. Verify setup
python setup_project.py

# 6. Open notebook
jupyter notebook notebooks/01_data_collection.ipynb
```

---

## Analysis Workflow

```
API Extraction (requests)
        ↓
Web Scraping (BeautifulSoup)
        ↓
Data Wrangling (pandas)
        ↓
Load to PostgreSQL (SQLAlchemy)
        ↓
Transform with dbt
        ↓
Visualize in Looker Studio
        ↓
AI Narrative (Groq — Llama 3.3)
        ↓
Present findings (PowerPoint)
```

---

## Skills Demonstrated

`Python` `pandas` `API Extraction` `Web Scraping` `SQL` `PostgreSQL` `dbt` `ELT Pipelines` `Google Looker Studio` `Data Visualization` `Groq AI` `Git`

---

## Certification

IBM Data Analytics Professional Certificate — 2026
IBM Generative AI for Data Analysts Certificate — 2026

---

*Julio Cesar Zamora Ramirez | github.com/Juliozed | CDMX, Mexico*
