import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import pycountry

# CONFIGURATION
st.set_page_config(page_title="Global Analysis", layout="wide")

# Load Data
df = pd.read_csv("ds_salaries.csv")

# HELPERS
def code_to_country(code):
    try:
        return pycountry.countries.get(alpha_2=code).name
    except:
        return code

df['company_location_full'] = df['company_location'].apply(code_to_country)
employment_map = {"FL": "Freelancer", "CT": "Contract", "PT": "Part-time", "FT": "Full-time"}
df["employment_type_label"] = df["employment_type"].map(employment_map)


# Title
st.title("Data Science Salaries Explorer Global")

with st.sidebar:
    # Sidebar Filters
    st.sidebar.header("Filter the dataset")

    year = st.selectbox("Select Year", sorted(df["work_year"].unique()), index=0)
    df = df[df["work_year"] == year]

    # Salary Range Filter
    salary_range = st.sidebar.slider("Salary Range (USD)", int(df.salary_in_usd.min()), int(df.salary_in_usd.max()), (50000, 200000))
    df = df[(df['salary_in_usd'] >= salary_range[0]) & (df['salary_in_usd'] <= salary_range[1])]

    # Experience Level Filter
    experience_levels = st.sidebar.multiselect("Experience Level", options=df.experience_level.unique(), default=list(df.experience_level.unique()))
    df = df[df['experience_level'].isin(experience_levels)]

    # Employment Type Filter
    employment_types = st.sidebar.multiselect("Employment Type", options=df.employment_type_label.unique(), default=list(df.employment_type_label.unique()))
    df = df[df['employment_type_label'].isin(employment_types)]


# KPI Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Average Salary", f"${df['salary_in_usd'].mean():,.0f}")
col2.metric("Total Records", len(df))
col3.metric("Countries Covered", df['company_location'].nunique())
st.caption("These metrics give a snapshot of the filtered dataset, showing average salary, number of job listings, and country coverage.")

st.divider()

# Seaborn Boxplot
st.subheader("Salary Distribution by Experience Level")
fig1, ax1 = plt.subplots(figsize=(10, 6))
sns.boxplot(x='experience_level', y='salary_in_usd', data=df, ax=ax1)
ax1.set_xlabel("Experience Level")
ax1.set_ylabel("Salary (USD)")
st.pyplot(fig1)
st.caption("This boxplot shows salary ranges for each experience level, helping identify variability and outliers in pay per level.")

st.divider()

# Plotly Scatterplot
st.subheader("Salary vs Remote Ratio (Interactive)")
fig2 = px.scatter(
    df, x='remote_ratio', y='salary_in_usd', color='experience_level',
    hover_data=['job_title', 'company_size'], title="Salary vs Remote Ratio (Interactive)",
    labels={"remote_ratio": "Remote Ratio",
            "salary_in_usd": "Salary (USD)",
            "experience_level": "Experience Level"})
st.plotly_chart(fig2, use_container_width=True)
st.caption("This scatterplot explores the relationship between remote work ratio and salary, segmented by experience level.")

st.divider()

# Grouped Bar Chart
st.subheader("Median Salary by Employment Type and Experience Level")
grouped_df = df.groupby(['employment_type_label', 'experience_level'])['salary_in_usd'].median().unstack()
viridis_colors = sns.color_palette("viridis", n_colors=grouped_df.shape[1])

grouped_df.plot(kind='bar', figsize=(12, 6), color=viridis_colors)
plt.ylabel("Median Salary (USD)")
plt.xlabel("Employment Type")
plt.xticks(rotation=0)
st.pyplot(plt.gcf())
st.caption("This bar chart shows how median salaries vary by contract type and experience level, highlighting earnings differences across job types.")

st.divider()

# Country Choropleth Map
st.subheader("Job Distribution by Country")
map_data = df['company_location_full'].value_counts().reset_index()
map_data.columns = ['country', 'count']
fig3 = px.choropleth(
    map_data, locations='country', locationmode='country names', color='count',
    color_continuous_scale="Blues")
st.plotly_chart(fig3, use_container_width=True)
st.caption("This choropleth map displays the distribution of job listings across countries, showing which locations dominate the dataset.")

st.divider()

# Download Filtered Data
st.subheader("Download the filtered dataset")
st.download_button("Download CSV", df.to_csv(index=False), "filtered_data.csv", "text/csv")
st.caption("Click to download the dataset with your selected filters applied, in CSV format.")
