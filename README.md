# 🏢 HR Attrition Analytics Dashboard
### Interactive Power BI Dashboard | Employee Attrition Analysis

![Power BI](https://img.shields.io/badge/Power%20BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)
![SQL](https://img.shields.io/badge/SQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![DAX](https://img.shields.io/badge/DAX-F2C811?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen?style=for-the-badge)

---

## 📌 Problem Statement

High employee attrition costs companies **1.5–2× an employee's annual salary**. HR teams need a clear, data-driven view of who is leaving, why, and when — to take proactive action before talent exits.

**Goal:** Build an interactive Power BI dashboard enabling HR leaders to monitor attrition rates across departments, age groups, salary bands, and job roles — surfacing the key drivers of exits.

---

## 📊 Dataset

| Attribute | Detail |
|---|---|
| Source | IBM HR Analytics Employee Attrition (Kaggle) |
| Rows | 1,470 employees |
| Target | `Attrition` (Yes / No) |
| Key features | Age, Dept, MonthlyIncome, JobRole, YearsAtCompany, JobSatisfaction, OverTime |

---

## 📁 Folder Structure

```
hr-attrition-dashboard/
│
├── data/
│   ├── raw/hr_attrition.csv
│   └── processed/hr_cleaned.csv
│
├── sql/
│   └── hr_analysis_queries.sql    ← 7 analysis queries
│
├── powerbi/
│   └── hr_dashboard.pbix
│
├── screenshots/
└── README.md
```

---

## 🔧 Key DAX Measures

```dax
Attrition Rate =
DIVIDE(
    CALCULATE(COUNT(hr[EmployeeNumber]), hr[Attrition] = "Yes"),
    COUNT(hr[EmployeeNumber])
) * 100

Avg Salary Leavers =
CALCULATE(AVERAGE(hr[MonthlyIncome]), hr[Attrition] = "Yes")

Avg Tenure Leavers =
CALCULATE(AVERAGE(hr[YearsAtCompany]), hr[Attrition] = "Yes")

Attrition Risk Flag =
IF(
    hr[JobSatisfaction] <= 2 &&
    hr[OverTime] = "Yes" &&
    hr[YearsAtCompany] < 3,
    "High Risk", "Normal"
)
```

---

## 📈 Key Insights

| Finding | Detail |
|---|---|
| Overall attrition rate | **16.1%** — above healthy 10% threshold |
| Highest attrition dept | Sales — **21% attrition** |
| Salary impact | Low earners (<₹3K) = **3× more likely to leave** |
| Age impact | Under-25 employees = **39% attrition** |
| Overtime link | Employees on overtime = **31%** vs **10%** without |
| Satisfaction score | Leavers avg **2.1/4** vs stayers' **2.7/4** |

---

## 🚀 How to Reproduce

```bash
# 1. Run SQL queries in MySQL Workbench
mysql -u root -p < sql/hr_analysis_queries.sql

# 2. Export results as CSV

# 3. Open powerbi/hr_dashboard.pbix in Power BI Desktop
#    → Transform Data → Update source path → Refresh
```

---

## 👩‍💻 Author
**Mohani Gupta** | 📧 mohanigupta279@gmail.com | 🔗 [LinkedIn](https://linkedin.com/in/mohanigupta)
