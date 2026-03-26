"""
HR Attrition Dashboard — analyse.py
Author  : Mohani Gupta | mohanigupta279@gmail.com
Purpose : Full Python analysis + chart generation for HR attrition data.
          Complements the Power BI dashboard with reproducible Python code.
Usage   : python src/analyse.py
"""

import os
import warnings
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns

warnings.filterwarnings("ignore")
sns.set_theme(style="darkgrid", palette="muted", font_scale=1.05)
os.makedirs("outputs/charts", exist_ok=True)

COLORS = {
    "yes"     : "#ef4444",
    "no"      : "#34d399",
    "primary" : "#4f8ef7",
    "warn"    : "#f59e0b",
    "purple"  : "#a78bfa",
}


# ── LOAD ─────────────────────────────────────────────────────────────────────

def load(path: str = "data/raw/hr_attrition.csv") -> pd.DataFrame:
    df = pd.read_csv(path)
    df["Attrition_bin"] = (df["Attrition"] == "Yes").astype(int)
    print(f"Loaded: {df.shape[0]:,} employees  |  "
          f"Attrition rate: {df['Attrition_bin'].mean()*100:.1f}%")
    return df


# ── REPORT ───────────────────────────────────────────────────────────────────

def print_report(df: pd.DataFrame) -> None:
    sep = "=" * 58
    total   = len(df)
    left    = df["Attrition_bin"].sum()
    stayed  = total - left
    rate    = left / total * 100

    print(f"\n{sep}")
    print("  HR ATTRITION ANALYSIS  —  Mohani Gupta")
    print(sep)
    print(f"\n{'📊 HEADLINE METRICS':}")
    print(f"  Total Employees   : {total:,}")
    print(f"  Active            : {stayed:,}  ({stayed/total*100:.1f}%)")
    print(f"  Attrited          : {left:,}   ({rate:.1f}%)  ← benchmark: <10%")
    print(f"  Avg Monthly Income: ₹{df['MonthlyIncome'].mean():,.0f}")
    print(f"  Avg Age           : {df['Age'].mean():.1f} years")
    print(f"  Avg Tenure        : {df['YearsAtCompany'].mean():.1f} years")

    print(f"\n{'🏢 ATTRITION BY DEPARTMENT':}")
    dept = (
        df.groupby("Department")
        .agg(Total=("Attrition_bin","count"),
             Attrited=("Attrition_bin","sum"))
        .assign(Rate=lambda x: (x.Attrited/x.Total*100).round(1))
        .sort_values("Rate", ascending=False)
    )
    for d, row in dept.iterrows():
        bar = "█" * int(row.Rate / 2)
        print(f"  {d:<30} {row.Rate:>5.1f}%  {bar}")

    print(f"\n{'💰 ATTRITION BY SALARY BAND':}")
    df["SalaryBand"] = pd.cut(
        df["MonthlyIncome"],
        bins=[0, 3000, 7000, 12000, 99999],
        labels=["Low (<₹3K)","Mid (₹3–7K)","High (₹7–12K)","Very High (₹12K+)"]
    )
    sal = (df.groupby("SalaryBand", observed=True)["Attrition_bin"]
             .mean() * 100).round(1)
    for band, rate in sal.items():
        bar = "█" * int(rate / 2)
        print(f"  {str(band):<22} {rate:>5.1f}%  {bar}")

    print(f"\n{'👤 ATTRITION BY AGE GROUP':}")
    df["AgeGroup"] = pd.cut(
        df["Age"],
        bins=[17, 24, 34, 44, 60],
        labels=["18–24","25–34","35–44","45+"]
    )
    age = (df.groupby("AgeGroup", observed=True)["Attrition_bin"]
             .mean() * 100).round(1)
    for grp, rate in age.items():
        print(f"  {str(grp):<8} {rate:>5.1f}%")

    print(f"\n{'⚠️  HIGH-RISK EMPLOYEE PROFILE':}")
    high_risk = df[
        (df["OverTime"]        == "Yes") &
        (df["MonthlyIncome"]   <  4000)  &
        (df["JobSatisfaction"] <= 2)     &
        (df["YearsAtCompany"]  <  3)
    ]
    hr_rate = high_risk["Attrition_bin"].mean() * 100
    print(f"  High-risk employees  : {len(high_risk):,}  ({len(high_risk)/total*100:.1f}% of workforce)")
    print(f"  Their attrition rate : {hr_rate:.1f}%  ← {hr_rate/rate:.1f}x the average!")
    print(f"\n  → Criteria: OverTime=Yes + Income<₹4K + Satisfaction≤2 + Tenure<3yrs")


# ── CHARTS ───────────────────────────────────────────────────────────────────

def plot_all(df: pd.DataFrame) -> None:
    print("\n📊 Generating charts...")

    # ── 1. Executive Overview (2×3) ──────────────────────────
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    fig.suptitle("HR Attrition Dashboard  —  Mohani Gupta",
                 fontsize=16, fontweight="bold", y=1.01)

    # 1a. Attrition donut
    vc = df["Attrition"].value_counts()
    wedge_props = {"width": 0.5, "edgecolor": "white", "linewidth": 2}
    axes[0, 0].pie(vc, labels=vc.index, autopct="%1.1f%%",
                   colors=[COLORS["no"], COLORS["yes"]],
                   wedgeprops=wedge_props, startangle=90)
    axes[0, 0].set_title("Overall Attrition Split", fontweight="bold")

    # 1b. Attrition by Department
    dept = (df.groupby("Department")["Attrition_bin"].mean() * 100).round(1).sort_values()
    axes[0, 1].barh(dept.index, dept.values,
                    color=[COLORS["yes"] if v > 15 else COLORS["primary"] for v in dept.values])
    axes[0, 1].set_title("Attrition Rate by Department (%)", fontweight="bold")
    axes[0, 1].set_xlabel("Attrition Rate (%)")
    for i, v in enumerate(dept.values):
        axes[0, 1].text(v + 0.3, i, f"{v}%", va="center", fontsize=10)

    # 1c. Monthly Income distribution by attrition
    df.boxplot(column="MonthlyIncome", by="Attrition",
               ax=axes[0, 2],
               boxprops=dict(color=COLORS["primary"]),
               medianprops=dict(color=COLORS["yes"], linewidth=2.5))
    axes[0, 2].set_title("Income Distribution by Attrition", fontweight="bold")
    axes[0, 2].set_xlabel("Attrition")
    axes[0, 2].set_ylabel("Monthly Income (₹)")
    plt.sca(axes[0, 2]); plt.title("Income vs Attrition")

    # 1d. Age group attrition
    df["AgeGroup"] = pd.cut(df["Age"], bins=[17,24,34,44,60],
                             labels=["18–24","25–34","35–44","45+"])
    age_attr = (df.groupby("AgeGroup", observed=True)["Attrition_bin"]
                  .mean() * 100).round(1)
    bars = axes[1, 0].bar(age_attr.index.astype(str), age_attr.values,
                          color=[COLORS["yes"] if v > 20 else COLORS["primary"]
                                 for v in age_attr.values])
    axes[1, 0].bar_label(bars, fmt="%.1f%%", padding=3)
    axes[1, 0].set_title("Attrition Rate by Age Group", fontweight="bold")
    axes[1, 0].set_ylabel("Attrition Rate (%)")

    # 1e. Overtime impact
    ot = df.groupby(["OverTime", "Attrition"]).size().unstack(fill_value=0)
    ot.plot(kind="bar", ax=axes[1, 1],
            color=[COLORS["no"], COLORS["yes"]], edgecolor="white")
    axes[1, 1].set_title("Overtime vs Attrition Count", fontweight="bold")
    axes[1, 1].tick_params(rotation=0)
    axes[1, 1].legend(title="Attrition")

    # 1f. Job Satisfaction vs Attrition rate
    jsat = (df.groupby("JobSatisfaction")["Attrition_bin"]
              .mean() * 100).round(1)
    axes[1, 2].plot(jsat.index, jsat.values,
                    marker="o", color=COLORS["yes"], linewidth=2.5, markersize=9)
    axes[1, 2].fill_between(jsat.index, jsat.values, alpha=0.15, color=COLORS["yes"])
    axes[1, 2].set_title("Attrition Rate by Job Satisfaction", fontweight="bold")
    axes[1, 2].set_xlabel("Job Satisfaction (1=Low, 4=High)")
    axes[1, 2].set_ylabel("Attrition Rate (%)")
    axes[1, 2].set_xticks([1, 2, 3, 4])

    plt.tight_layout()
    plt.savefig("outputs/charts/01_overview_dashboard.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("  ✓ 01_overview_dashboard.png")

    # ── 2. Salary Band Deep-Dive ──────────────────────────────
    df["SalaryBand"] = pd.cut(
        df["MonthlyIncome"],
        bins=[0, 3000, 7000, 12000, 99999],
        labels=["Low\n(<₹3K)", "Mid\n(₹3–7K)", "High\n(₹7–12K)", "V.High\n(₹12K+)"]
    )
    sal_stats = df.groupby("SalaryBand", observed=True).agg(
        Employees=("Attrition_bin", "count"),
        Attrition_Rate=("Attrition_bin", lambda x: x.mean() * 100),
        Avg_Income=("MonthlyIncome", "mean"),
        Avg_Satisfaction=("JobSatisfaction", "mean"),
    ).round(1)

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle("Attrition vs Salary Band", fontsize=14, fontweight="bold")

    axes[0].bar(sal_stats.index.astype(str), sal_stats["Attrition_Rate"],
                color=[COLORS["yes"] if v > 15 else COLORS["primary"]
                       for v in sal_stats["Attrition_Rate"]])
    axes[0].set_title("Attrition Rate by Salary Band")
    axes[0].set_ylabel("Attrition Rate (%)")
    for i, v in enumerate(sal_stats["Attrition_Rate"]):
        axes[0].text(i, v + 0.3, f"{v:.1f}%", ha="center", fontweight="bold")

    axes[1].bar(sal_stats.index.astype(str), sal_stats["Employees"],
                color=COLORS["primary"], alpha=0.8)
    axes[1].set_title("Employee Count by Salary Band")
    axes[1].set_ylabel("Employees")

    plt.tight_layout()
    plt.savefig("outputs/charts/02_salary_analysis.png", dpi=150)
    plt.close()
    print("  ✓ 02_salary_analysis.png")

    # ── 3. Job Role Heatmap ───────────────────────────────────
    role_dept = df.groupby(["JobRole", "Department"])["Attrition_bin"].mean() * 100
    role_pivot = role_dept.unstack(fill_value=0).round(1)

    fig, ax = plt.subplots(figsize=(10, 7))
    sns.heatmap(role_pivot, annot=True, fmt=".1f", cmap="RdYlGn_r",
                linewidths=0.5, ax=ax, cbar_kws={"label": "Attrition Rate (%)"})
    ax.set_title("Attrition Rate by Job Role & Department (%)",
                 fontsize=13, fontweight="bold")
    ax.set_xlabel("Department")
    ax.set_ylabel("Job Role")
    plt.tight_layout()
    plt.savefig("outputs/charts/03_role_heatmap.png", dpi=150)
    plt.close()
    print("  ✓ 03_role_heatmap.png")

    # ── 4. Tenure & YearsWithManager ─────────────────────────
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle("Tenure Patterns in Attrition", fontsize=13, fontweight="bold")

    for label, color in [("Yes", COLORS["yes"]), ("No", COLORS["no"])]:
        df[df["Attrition"] == label]["YearsAtCompany"].plot(
            kind="kde", ax=axes[0], color=color, linewidth=2.2, label=label
        )
    axes[0].set_title("Years at Company Distribution")
    axes[0].set_xlabel("Years at Company")
    axes[0].legend(title="Attrition")

    for label, color in [("Yes", COLORS["yes"]), ("No", COLORS["no"])]:
        df[df["Attrition"] == label]["YearsWithCurrManager"].plot(
            kind="kde", ax=axes[1], color=color, linewidth=2.2, label=label
        )
    axes[1].set_title("Years with Current Manager")
    axes[1].set_xlabel("Years with Manager")
    axes[1].legend(title="Attrition")

    plt.tight_layout()
    plt.savefig("outputs/charts/04_tenure_analysis.png", dpi=150)
    plt.close()
    print("  ✓ 04_tenure_analysis.png")

    print("\n✅ All 4 charts saved to outputs/charts/")


# ── MAIN ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    df = load()
    print_report(df)
    plot_all(df)
