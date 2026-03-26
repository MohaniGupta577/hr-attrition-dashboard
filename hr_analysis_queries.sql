-- ================================================================
-- HR Attrition Dashboard — Analysis Queries
-- Author  : Mohani Gupta | mohanigupta279@gmail.com
-- Tools   : MySQL 8.0+
-- Dataset : IBM HR Analytics (1,470 employees)
-- ================================================================

-- ── 1. Overall Attrition Rate ─────────────────────────────────
SELECT
    COUNT(*)  AS total_employees,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) AS attrited,
    ROUND(
        SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2
    ) AS attrition_rate_pct
FROM hr_data;

-- ── 2. Attrition by Department ────────────────────────────────
SELECT
    department,
    COUNT(*)  AS total_employees,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) AS attrited,
    ROUND(
        SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2
    ) AS attrition_pct,
    ROUND(AVG(monthly_income), 0) AS avg_salary,
    ROUND(AVG(job_satisfaction), 2) AS avg_satisfaction
FROM hr_data
GROUP BY department
ORDER BY attrition_pct DESC;

-- ── 3. Attrition by Salary Band ───────────────────────────────
SELECT
    CASE
        WHEN monthly_income < 3000  THEN '1. Low   (<₹3K)'
        WHEN monthly_income < 7000  THEN '2. Mid   (₹3K–7K)'
        WHEN monthly_income < 12000 THEN '3. High  (₹7K–12K)'
        ELSE                             '4. VHigh (₹12K+)'
    END AS salary_band,
    COUNT(*)  AS employees,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) AS attrited,
    ROUND(
        SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2
    ) AS attrition_pct
FROM hr_data
GROUP BY salary_band
ORDER BY salary_band;

-- ── 4. Attrition by Age Group ─────────────────────────────────
SELECT
    CASE
        WHEN age < 25          THEN '< 25'
        WHEN age BETWEEN 25 AND 34 THEN '25–34'
        WHEN age BETWEEN 35 AND 44 THEN '35–44'
        ELSE                        '45+'
    END AS age_group,
    COUNT(*)  AS employees,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) AS attrited,
    ROUND(
        SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2
    ) AS attrition_pct,
    ROUND(AVG(monthly_income), 0) AS avg_salary
FROM hr_data
GROUP BY age_group
ORDER BY age_group;

-- ── 5. Job Role Risk Ranking ──────────────────────────────────
SELECT
    job_role,
    COUNT(*) AS total,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) AS attrited,
    ROUND(
        SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2
    ) AS attrition_pct,
    ROUND(AVG(job_satisfaction), 2) AS avg_satisfaction,
    ROUND(AVG(years_at_company), 1) AS avg_tenure_yrs
FROM hr_data
GROUP BY job_role
ORDER BY attrition_pct DESC;

-- ── 6. Overtime Impact ────────────────────────────────────────
SELECT
    over_time,
    COUNT(*) AS employees,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) AS attrited,
    ROUND(
        SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2
    ) AS attrition_pct
FROM hr_data
GROUP BY over_time;

-- ── 7. Satisfaction vs Attrition Matrix ───────────────────────
SELECT
    job_satisfaction,
    COUNT(*) AS employees,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) AS attrited,
    ROUND(
        SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2
    ) AS attrition_pct
FROM hr_data
GROUP BY job_satisfaction
ORDER BY job_satisfaction;
