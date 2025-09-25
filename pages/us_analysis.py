import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import pycountry
import plotly.express as px

# CONFIGURATION
st.set_page_config(page_title="Data Science Salaries In US", layout="wide")
sns.set_theme(style="whitegrid")


# LOAD DATA
df = pd.read_csv("ds_salaries.csv")


# HELPERS
def code_to_country(code):
    try:
        return pycountry.countries.get(alpha_2=code).name
    except:
        return code
    
experience_level_map = {"SE": "Senior", "EN": "Entry Level", "EX": "Executive Level", "MI": "Mid/Intermediate Level"}
employment_map = {"FL": "Freelancer", "CT": "Contract", "PT": "Part-time", "FT": "Full-time"}
company_size_map = {"S": "Small", "M": "Medium", "L": "Large"}
df['company_location_full'] = df['company_location'].apply(code_to_country)
df['experience_level_full'] = df['experience_level'].map(experience_level_map)
df["employment_type_label"] = df["employment_type"].map(employment_map)
df["company_size_label"] = df["company_size"].map(company_size_map)
df_original = df.copy()

# SIDEBAR FILTERS
with st.sidebar:
    st.header("Filters")
    year = st.selectbox("Select Year", sorted(df["work_year"].unique()), index=0)
    df = df[df["work_year"] == year]
    exp_levels = st.multiselect("Experience Level", df["experience_level_full"].unique(), default=df["experience_level_full"].unique())
    df = df[df["experience_level_full"].isin(exp_levels)]

# TITLE
st.title("Data Science Job Trends & Salaries In US")
st.markdown("Analyzing salaries, remote work, and job distributions in data science roles.")

st.divider()

# --- SECTION 1: Global View ---
st.header("Global Distribution")

# TOP COUNTRIES
top_countries = df['company_location_full'].value_counts().head(5).reset_index()
top_countries.columns = ['Country', 'Job Count']
fig1, ax1 = plt.subplots(figsize=(10, 5))
sns.barplot(data=top_countries, y='Country', x='Job Count', palette='crest', ax=ax1)
ax1.set_title('Top 5 Countries with Most Data Science Jobs')
st.pyplot(fig1)
st.divider()

# --- SECTION 2: US MARKET DEEP DIVE ---
# ... [All previous code remains unchanged]

# --- SECTION 2: US MARKET DEEP DIVE ---
st.header("US Job Market")
us_jobs = df[df["company_location"] == "US"]
us_domestic = us_jobs[us_jobs["employee_residence"] == "US"]

col1, col2 = st.columns(2)
with col1:
    st.subheader("Top 10 Paying Roles (US Companies)")
    top10 = us_jobs.groupby('job_title')['salary_in_usd'].mean().sort_values(ascending=False).head(10).reset_index()
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    sns.barplot(data=top10, x='salary_in_usd', y='job_title', palette='crest', ax=ax2)
    ax2.set_xlabel("Avg Salary (USD)")
    ax2.set_ylabel("Job Title")
    st.pyplot(fig2)
    st.caption("This chart displays the top 10 data science roles in U.S.-based companies ranked by average salary, highlighting the highest-paying titles overall.")

with col2:
    st.subheader("Top 10 Paying Roles (US to US Employees)")
    top10_us = us_domestic.groupby('job_title')['salary_in_usd'].mean().sort_values(ascending=False).head(10).reset_index()
    fig3, ax3 = plt.subplots(figsize=(8, 5))
    sns.barplot(data=top10_us, x='salary_in_usd', y='job_title', palette='crest', ax=ax3)
    ax3.set_xlabel("Avg Salary (USD)")
    ax3.set_ylabel("Job Title")
    st.pyplot(fig3)
    st.caption("This plot focuses on salaries paid by U.S. companies to U.S.-based employees, showing top-paying roles specifically for domestic hires.")

st.divider()

# --- SECTION 3: Remote Ratios ---
st.header("Remote Work Insights")
top5_unique = us_jobs.sort_values(by="salary_in_usd", ascending=False).drop_duplicates('job_title').head(5)
fig4, ax4 = plt.subplots(figsize=(10, 6))
sns.stripplot(data=top5_unique, x="job_title", y="remote_ratio", palette="crest", size=10, ax=ax4)
ax4.set_yticks([0, 50, 100])
ax4.set_yticklabels(["0%", "50%", "100%"])
ax4.set_title("Remote Ratio for Top 5 High Paying Jobs")
ax4.set_xlabel("Job Title")
ax4.set_ylabel("Remote Ratio")
plt.setp(ax4.get_xticklabels(), rotation=30)
st.pyplot(fig4)
st.caption("This visualization shows remote work ratios (0%, 50%, 100%) for the top 5 highest-paying U.S. roles, indicating how flexible each job is.")

st.divider()

# --- SECTION 4: Salary Drivers ---
st.header("Salary Distribution Analysis")

fig5, ax5 = plt.subplots(figsize=(12, 6))
sns.violinplot(data=us_jobs, x="experience_level_full", y="salary_in_usd", hue="company_size_label", split=True, palette="crest", ax=ax5)
ax5.set_title("Salary by Experience Level & Company Size")
ax5.set_xlabel("Experience Level")
ax5.set_ylabel("Salary (USD)")
ax5.legend(title="Company Size", bbox_to_anchor=(1.05, 1))
st.pyplot(fig5)
st.caption("This plot shows how salaries vary by experience level and company size, revealing trends such as higher pay in large firms for senior roles.")

# Correlation heatmap
st.subheader("Correlation Matrix")
cols = st.multiselect("Select numeric columns:", ["salary_in_usd", "remote_ratio", "work_year"], default=["salary_in_usd", "remote_ratio"])
if len(cols) >= 2:
    corr = df_original[cols].corr()
    fig6, ax6 = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr, annot=True, cmap="Blues", square=True, ax=ax6)
    st.pyplot(fig6)
    st.caption("The heatmap shows correlations between salary, remote ratio, and work year. It highlights which variables tend to rise or fall together.")
else:
    st.info("Select at least 2 columns to view correlation heatmap.")
st.divider()

# --- SECTION 5: Interactive Explorations ---
st.header("Interactive Job Comparison")
job_titles = us_jobs['job_title'].value_counts().index.tolist()
selected_jobs = st.multiselect("Select job titles:", job_titles, default=job_titles[:4])

if selected_jobs:
    cols = st.columns(2)
    for i, job in enumerate(selected_jobs):
        data = us_jobs[us_jobs['job_title'] == job]
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.scatterplot(data=data, x="remote_ratio", y="salary_in_usd", hue="experience_level_full", palette="viridis", s=80, alpha=0.7, ax=ax)
        ax.set_title(f"{job}")
        ax.set_xlabel("Remote Ratio (%)")
        ax.set_ylabel("Salary (USD)")
        ax.legend(title="Experience", bbox_to_anchor=(1.05, 1))
        cols[i % 2].pyplot(fig)
    st.caption("These scatter plots show how salary relates to remote ratio for selected U.S. job titles, with color indicating experience level.")
else:
    st.info("Select at least one job title.")

st.divider()

# --- SECTION 6: Employment Type Breakdown ---
st.header("Salaray by Employment Types")

fig10, ax10 = plt.subplots(figsize=(8, 4))
sns.boxplot(data=us_jobs, x="employment_type_label", y="salary_in_usd", palette="viridis", ax=ax10)
ax10.set_title("Salary by Employment Type")
ax10.set_ylabel("Salary (USD)")
ax10.set_xlabel("Employment Type")
st.pyplot(fig10)
st.caption("This boxplot compares salary ranges by employment type, revealing differences in compensation between full-time, freelance, and other roles.")

emp_counts = us_jobs["employment_type_label"].value_counts()
fig11, ax11 = plt.subplots(figsize=(8, 4))
sns.barplot(x=emp_counts.index, y=emp_counts.values, palette="viridis", ax=ax11)
ax11.set_title("Number of Employees by Employment Type")
labels = [f"{label}: {count}" for label, count in zip(emp_counts.index, emp_counts.values)]
ax11.legend(labels, title="Count", bbox_to_anchor=(1.05, 1))
ax11.set_ylabel("Employee Count")
ax11.set_xlabel("Employment Type")
st.pyplot(fig11)
st.caption("This bar chart shows how many individuals are employed under each contract type in U.S. data science roles.")
st.divider()

# --- SECTION 7: Salary Trends ---
st.header("Salary Trends")
trend_df = df_original.groupby(["work_year", "company_size_label"])["salary_in_usd"].mean().reset_index()

fig12 = px.line(
    trend_df,
    x="work_year",
    y="salary_in_usd",
    color="company_size_label",
    labels={
        "work_year": "Work Year",
        "salary_in_usd": "Salary (USD)",
        "company_size_label": "Company Size"
    },
    title="Average Salary Over Time by Company Size"
)
fig12.update_traces(
    mode="lines",
    hovertemplate="Year: %{x}<br>Salary: $%{y:,.0f}"
)
fig12.update_layout(xaxis=dict(tickmode='array', tickvals=[2020, 2021, 2022, 2023]))
st.plotly_chart(fig12, use_container_width=True)
st.caption("This interactive chart shows average salaries from 2020 to 2023, grouped by company size, highlighting growth patterns in the U.S. market.")
