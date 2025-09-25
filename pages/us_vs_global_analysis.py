import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# ------------------ Streamlit Config ------------------ #
st.set_page_config(page_title="US vs Global", layout="wide")
st.title("Data Science Salaries Dashboard")

# ------------------ Load & Preprocess Data ------------------ #
df = pd.read_csv("ds_salaries.csv")

# Drop irrelevant columns
df.drop(columns=["salary", "salary_currency", "employee_residence"], inplace=True)

# Label Mappings
company_size_map = {"S": "Small", "M": "Medium", "L": "Large"}
experience_map = {
    "SE": "Senior",
    "EN": "Entry Level",
    "EX": "Executive Level",
    "MI": "Mid/Intermediate Level"
}

# Apply mappings
df["company_size_label"] = df["company_size"].map(company_size_map)
df["experience_level_full"] = df["experience_level"].map(experience_map)
df["region"] = df["company_location"].apply(lambda x: "US" if x == "US" else "Other")

# ------------------ Sidebar Navigation ------------------ #
page = st.sidebar.radio("Navigation", ["Overview", "US vs Others"])

# ------------------ Overview Page ------------------ #
if page == "Overview":
    st.header("Global Overview of Data Science Salaries")
    st.markdown("These values are an aggregate from 2020 until 2023")

    # --- Average Salary by Company Size --- #
    st.subheader("Average Salary by Company Size")
    avg_salary_size = df.groupby("company_size_label")["salary_in_usd"].mean().reset_index()
    fig1, ax1 = plt.subplots(figsize=(8, 4))
    sns.barplot(data=avg_salary_size, x="company_size_label", y="salary_in_usd", palette="crest", ax=ax1)
    ax1.set_xlabel("Company Size")
    ax1.set_ylabel("Average Salary (USD)")
    st.pyplot(fig1)
    st.caption("Medium companies tend to offer higher salaries, while small companies offer the least on average.")

    st.divider()

    # --- Average Salary by Experience Level --- #
    st.subheader("Average Salary by Experience Level")
    avg_salary_exp = df.groupby("experience_level_full")["salary_in_usd"].mean().reset_index()
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    sns.barplot(data=avg_salary_exp, x="experience_level_full", y="salary_in_usd", palette="crest", ax=ax2)
    ax2.set_xlabel("Experience Level")
    ax2.set_ylabel("Average Salary (USD)")
    st.pyplot(fig2)
    st.caption("As expected, Executive and Senior roles earn significantly more than Entry-level positions.")

    st.divider()

    # --- Remote Ratio by Company Size --- #
    st.subheader("Remote Ratio by Company Size")
    fig3, ax3 = plt.subplots(figsize=(8, 4))
    sns.boxplot(data=df, x="company_size_label", y="remote_ratio", palette="crest", ax=ax3)
    ax3.set_xlabel("Company Size")
    ax3.set_ylabel("Remote Ratio (%)")
    st.pyplot(fig3)
    st.caption("Remote work distribution is relatively high across all company sizes, with some variation.")

# ------------------ US vs Others Page ------------------ #
elif page == "US vs Others":
    st.header("Comparison: US vs Rest of the World")
    st.markdown("These values are an aggregate from 2020 until 2023")
    # --- Average Salary by Region --- #
    st.subheader("Average Salary by Region")
    region_salary = df.groupby("region")["salary_in_usd"].mean().reset_index()
    fig4 = px.bar(
        region_salary, x="region", y="salary_in_usd", color="region",
        title="Average Salary: US vs Rest of the World",
        labels={"region": "Region", "salary_in_usd": "Average Salary (USD)"}
    )
    st.plotly_chart(fig4, use_container_width=True)
    st.caption("Data scientists in the US earn noticeably more on average than those in other regions.")

    st.divider()

    # --- Remote Ratio Distribution by Region --- #
    st.subheader("Remote Ratio by Region")
    fig5 = px.box(
        df, x="region", y="remote_ratio", color="region",
        title="Remote Ratio Distribution: US vs Others",
        labels={"region": "Region", "remote_ratio": "Remote Ratio (%)"}
    )
    st.plotly_chart(fig5, use_container_width=True)
    st.caption("Remote work is common both in and outside the US, though there is significant variability.")

    st.divider()

    # --- Salary by Experience Level --- #
    st.subheader("Salary by Experience Level and Region")
    fig6 = px.box(
        df, x="experience_level_full", y="salary_in_usd", color="region",
        title="Salary by Experience Level: US vs Others",
        labels={"experience_level_full": "Experience Level", "salary_in_usd": "Salary (USD)"}
    )
    st.plotly_chart(fig6, use_container_width=True)
    st.caption("Across all experience levels, US-based roles tend to pay more than roles elsewhere.")

    st.divider()

    # --- Salary by Company Size --- #
    st.subheader("Salary by Company Size and Region")
    fig7 = px.box(
        df, x="company_size_label", y="salary_in_usd", color="region",
        title="Salary by Company Size: US vs Others",
        labels={"company_size_label": "Company Size", "salary_in_usd": "Salary (USD)"}
    )
    st.plotly_chart(fig7, use_container_width=True)
    st.caption("Regardless of company size, US-based salaries are generally higher than global averages.")
