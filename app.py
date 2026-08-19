import requests
import streamlit as st
import pandas as pd
import plotly.express as px
import os
import numpy as np
from io import BytesIO
from dotenv import load_dotenv
from openai import OpenAI

def generate_report(df):
    report = []

    report.append("AI DATA ANALYST AGENT - DATA ANALYSIS REPORT")
    report.append("=" * 55)
    report.append("")

    # Dataset Overview
    report.append("1. DATASET OVERVIEW")
    report.append("-" * 30)
    report.append(f"Total Rows: {len(df)}")
    report.append(f"Total Columns: {len(df.columns)}")
    report.append(f"Missing Values: {int(df.isnull().sum().sum())}")
    report.append(f"Duplicate Rows: {int(df.duplicated().sum())}")
    report.append("")

    # Column Information
    report.append("2. COLUMN INFORMATION")
    report.append("-" * 30)

    for column in df.columns:
        report.append(
            f"{column} | "
            f"Type: {df[column].dtype} | "
            f"Missing: {df[column].isnull().sum()} | "
            f"Unique: {df[column].nunique()}"
        )

    report.append("")

    # Statistical Summary
    report.append("3. STATISTICAL SUMMARY")
    report.append("-" * 30)

    numeric_df = df.select_dtypes(include=np.number)

    if not numeric_df.empty:
        summary = numeric_df.describe()

        for column in numeric_df.columns:
            report.append(
                f"{column}: "
                f"Mean={summary.loc['mean', column]:.2f}, "
                f"Min={summary.loc['min', column]:.2f}, "
                f"Max={summary.loc['max', column]:.2f}"
            )

    report.append("")

    # Product Analysis
    if "Product" in df.columns and "Sales" in df.columns:
        report.append("4. PRODUCT SALES ANALYSIS")
        report.append("-" * 30)

        product_sales = (
            df.groupby("Product")["Sales"]
            .sum()
            .sort_values(ascending=False)
        )

        for product, sales in product_sales.items():
            report.append(f"{product}: {sales:,.2f}")

    report.append("")
    report.append("END OF REPORT")

    return "\n".join(report)

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)
# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Data Analyst Agent",
    page_icon="🤖",
    layout="wide"
)

# -------------------------------
# Custom UI Styling
# -------------------------------
st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    h1 {
        font-size: 2.8rem !important;
        font-weight: 700 !important;
    }

    h2 {
        margin-top: 2rem !important;
    }

    h3 {
        margin-top: 1.5rem !important;
    }

        .hero {
        background: linear-gradient(135deg, #111827, #1e293b);
        border-radius: 18px;
        padding: 32px 38px;
        margin-bottom: 30px;
        display: flex;
        align-items: center;
        gap: 20px;
    }

    .hero-icon {
        font-size: 48px;
    }

    .hero h1 {
        color: white !important;
        margin: 0 !important;
        font-size: 2.6rem !important;
    }

    .hero p {
        color: #cbd5e1;
        margin: 8px 0 0 0;
        font-size: 1.05rem;
    }

    .upload-header {
        margin-top: 10px;
        margin-bottom: 10px;
    }

    .upload-header h2 {
        margin-bottom: 4px !important;
    }

    .upload-header p {
        color: #64748b;
        margin-top: 0;
    }
</style>
""", unsafe_allow_html=True)

def generate_ai_insights(dataset_summary):

    try:
        prompt = f"""
You are an expert data analyst.

Analyze the following dataset summary and provide
clear and useful business insights.

Dataset summary:
{dataset_summary}

Give the response in this format:

### Key Insights
- ...
- ...
- ...

### Business Interpretation
- ...
- ...

### Recommendations
- ...
- ...

Rules:
- Use only the information provided.
- Do not invent numbers.
- Keep the explanation concise.
"""

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "qwen3:1.7b",
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        response.raise_for_status()

        result = response.json()

        return result["response"]

    except Exception as e:

        return (
            "⚠️ Local AI analysis could not be generated.\n\n"
            f"Error: {e}"
        )

# -----------------------------
# Main Header
# -----------------------------
st.markdown("""
<div class="hero">
    <div class="hero-icon">🤖</div>
    <div>
        <h1>AI Data Analyst Agent</h1>
        <p>
            Upload your dataset, clean the data, visualize patterns,
            and generate intelligent business insights.
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Dataset Upload
# -----------------------------
st.markdown("""
<div class="upload-header">
    <h2>📂 Upload Your Dataset</h2>
    <p>Upload a CSV or Excel file to begin automated analysis.</p>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Choose a CSV or Excel file",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:

    try:

        # -----------------------------
        # Read Dataset
        # -----------------------------
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.success(
            f"Dataset loaded successfully: {uploaded_file.name}"
        )

        # -----------------------------
        # Dataset Overview
        # -----------------------------
        st.markdown("""
        <style>
        [data-testid="stMetric"] {
            background: #f8fafc;
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #e2e8f0;
        }
        </style>
        """, unsafe_allow_html=True)

        st.subheader("📊 Dataset Overview")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Rows", df.shape[0])

        with col2:
            st.metric("Total Columns", df.shape[1])

        with col3:
            st.metric(
                "Missing Values",
                int(df.isnull().sum().sum())
            )

        with col4:
            st.metric(
                "Duplicate Rows",
                int(df.duplicated().sum())
            )

        # -----------------------------
        # Dataset Preview
        # -----------------------------

        st.markdown("""
        <style>
        [data-testid="stDataFrame"] {
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid #e2e8f0;
        }
        </style>
        """, unsafe_allow_html=True)

        st.subheader("👀 Dataset Preview")

        st.dataframe(
            df.head(10),
            use_container_width=True
        )

        # -----------------------------
        # Column Information
        # -----------------------------

        st.markdown("""
        <style>
        .column-info-title {
            margin-top: 35px;
            margin-bottom: 15px;
            font-size: 1.8rem;
            font-weight: 700;
        }
        </style>
        """, unsafe_allow_html=True)

        st.markdown(
            '<div class="column-info-title">🏷️ Column Information</div>',
            unsafe_allow_html=True
        )

        

        column_info = pd.DataFrame({
            "Column": df.columns,
            "Data Type": df.dtypes.astype(str),
            "Missing Values": df.isnull().sum().values,
            "Unique Values": df.nunique().values
        })

        st.dataframe(
            column_info,
            use_container_width=True
        )

        # -----------------------------
        # Column Categories
        # -----------------------------
        st.subheader("🔢 Column Categories")

        numeric_columns = df.select_dtypes(
            include="number"
        ).columns.tolist()

        categorical_columns = df.select_dtypes(
            exclude="number"
        ).columns.tolist()

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Numeric Columns**")

            for column in numeric_columns:
                st.write(f"• {column}")

        with col2:
            st.write("**Categorical / Other Columns**")

            for column in categorical_columns:
                st.write(f"• {column}")

        # -----------------------------
        # Data Quality Check
        # -----------------------------
        st.markdown("""
        <style>
        .quality-box {
            background: #fff8e1;
            border: 1px solid #f1d48a;
            border-radius: 12px;
            padding: 16px 20px;
            margin: 15px 0;
        }

        .quality-box h3 {
            margin: 0 0 8px 0 !important;
        }
        </style>
        """, unsafe_allow_html=True)

        st.subheader("⚠️ Data Quality Check")

        missing_data = pd.DataFrame({
            "Column": df.columns,
            "Missing Values": df.isnull().sum().values
        })

        missing_data = missing_data[
            missing_data["Missing Values"] > 0
        ]

        if missing_data.empty:
            st.success("✅ No missing values found.")
        else:
            st.warning("Missing values detected:")
            st.dataframe(
                missing_data,
                use_container_width=True
            )

        duplicate_count = int(
            df.duplicated().sum()
        )

        if duplicate_count == 0:
            st.success("✅ No duplicate rows found.")
        else:
            st.warning(
                f"⚠️ {duplicate_count} duplicate row(s) detected."
            )

        # -----------------------------
        # Data Cleaning
        # -----------------------------

        st.markdown("""
        <style>
        .cleaning-section {
            margin-top: 35px;
            margin-bottom: 15px;
        }

        .cleaning-title {
            font-size: 1.8rem;
            font-weight: 700;
            margin-bottom: 18px;
        }
        </style>
        """, unsafe_allow_html=True)

        st.markdown(
            '<div class="cleaning-title">🧹 Data Cleaning</div>',
            unsafe_allow_html=True
        )

        

        cleaned_df = df.copy()

        original_rows = len(cleaned_df)
        original_missing = int(
            cleaned_df.isnull().sum().sum()
        )
        original_duplicates = int(
            cleaned_df.duplicated().sum()
        )

        cleaned_df = cleaned_df.drop_duplicates()

        for column in cleaned_df.columns:

            if cleaned_df[column].isnull().sum() > 0:

                if pd.api.types.is_numeric_dtype(
                    cleaned_df[column]
                ):

                    cleaned_df[column] = cleaned_df[
                        column
                    ].fillna(
                        cleaned_df[column].median()
                    )

                else:

                    mode = cleaned_df[column].mode()

                    if not mode.empty:
                        cleaned_df[column] = cleaned_df[
                            column
                        ].fillna(mode[0])
                    else:
                        cleaned_df[column] = cleaned_df[
                            column
                        ].fillna("Unknown")

        cleaned_rows = len(cleaned_df)
        cleaned_missing = int(
            cleaned_df.isnull().sum().sum()
        )

        removed_duplicates = (
            original_duplicates
            - int(cleaned_df.duplicated().sum())
        )

        # -----------------------------
        # Cleaning Summary
        # -----------------------------
        st.write("### Cleaning Summary")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Rows Before", original_rows)
            st.metric("Rows After", cleaned_rows)

        with col2:
            st.metric("Missing Before", original_missing)
            st.metric("Missing After", cleaned_missing)

        with col3:
            st.metric(
                "Duplicates Removed",
                removed_duplicates
            )

            st.metric(
                "Rows Removed",
                original_rows - cleaned_rows
            )

        st.success(
            "✅ Data cleaning completed successfully."
        )

        st.write("### 🧼 Cleaned Dataset Preview")

        st.dataframe(
            cleaned_df.head(10),
            use_container_width=True
        )

        # -----------------------------
        # Statistical Analysis
        # -----------------------------
        st.subheader("📈 Statistical Summary")

        cleaned_numeric_columns = cleaned_df.select_dtypes(
            include="number"
        ).columns.tolist()

        if cleaned_numeric_columns:

            st.dataframe(
                cleaned_df[
                    cleaned_numeric_columns
                ].describe(),
                use_container_width=True
            )

        # ==================================================
        # AUTOMATIC CHART GENERATION
        # ==================================================

        st.subheader("📊 Automatic Chart Generation")

        chart_created = False

        if categorical_columns and cleaned_numeric_columns:

            category_column = None

            for column in categorical_columns:

                unique_count = cleaned_df[
                    column
                ].nunique()

                if 2 <= unique_count <= 15:
                    category_column = column
                    break

            if category_column:

                if "Sales" in cleaned_numeric_columns:
                    numeric_column = "Sales"
                else:
                    numeric_column = cleaned_numeric_columns[0]

                grouped_data = (
                    cleaned_df
                    .groupby(category_column)[
                        numeric_column
                    ]
                    .sum()
                    .reset_index()
                    .sort_values(
                        numeric_column,
                        ascending=False
                    )
                )

                st.write(
                    f"### 📊 {numeric_column} by "
                    f"{category_column}"
                )

                fig = px.bar(
                    grouped_data,
                    x=category_column,
                    y=numeric_column,
                    title=(
                        f"{numeric_column} by "
                        f"{category_column}"
                    ),
                    text_auto=True
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

                chart_created = True

                # Pie Chart
                st.write(
                    f"### 🥧 {category_column} Distribution"
                )

                count_data = (
                    cleaned_df[
                        category_column
                    ]
                    .value_counts()
                    .reset_index()
                )

                count_data.columns = [
                    category_column,
                    "Count"
                ]

                fig_pie = px.pie(
                    count_data,
                    names=category_column,
                    values="Count",
                    title=(
                        f"{category_column} Distribution"
                    )
                )

                st.plotly_chart(
                    fig_pie,
                    use_container_width=True
                )

                chart_created = True

        # Histogram
        if cleaned_numeric_columns:

            histogram_column = (
                "Sales"
                if "Sales" in cleaned_numeric_columns
                else cleaned_numeric_columns[0]
            )

            st.write(
                f"### 📊 {histogram_column} Distribution"
            )

            fig_hist = px.histogram(
                cleaned_df,
                x=histogram_column,
                title=(
                    f"{histogram_column} Distribution"
                ),
                nbins=20
            )

            st.plotly_chart(
                fig_hist,
                use_container_width=True
            )

            chart_created = True

        # Correlation
        if len(cleaned_numeric_columns) >= 2:

            st.write("### 🔥 Correlation Analysis")

            correlation = cleaned_df[
                cleaned_numeric_columns
            ].corr()

            fig_corr = px.imshow(
                correlation,
                text_auto=True,
                title="Numeric Feature Correlation",
                aspect="auto"
            )

            st.plotly_chart(
                fig_corr,
                use_container_width=True
            )

            chart_created = True

        # ==================================================
        # INSIGHT GENERATION
        # ==================================================

        st.subheader("🧠 Automatically Generated Insights")

        insights = []

        # Dataset size insight
        insights.append(
            f"📊 The dataset contains "
            f"{cleaned_df.shape[0]:,} rows and "
            f"{cleaned_df.shape[1]} columns."
        )

        # Cleaning insight
        if original_missing > 0:
            insights.append(
                f"🧹 {original_missing} missing values "
                f"were handled during data cleaning."
            )

        if original_duplicates > 0:
            insights.append(
                f"🔄 {original_duplicates} duplicate rows "
                f"were removed from the dataset."
            )

        # Numeric insights
        if cleaned_numeric_columns:

            for column in cleaned_numeric_columns:

                mean_value = cleaned_df[column].mean()
                max_value = cleaned_df[column].max()
                min_value = cleaned_df[column].min()

                insights.append(
                    f"📈 {column}: average = "
                    f"{mean_value:,.2f}, "
                    f"minimum = {min_value:,.2f}, "
                    f"maximum = {max_value:,.2f}."
                )

        # Product / category insights
        if categorical_columns:

            for category in categorical_columns:

                unique_count = cleaned_df[
                    category
                ].nunique()

                if 2 <= unique_count <= 15:

                    counts = cleaned_df[
                        category
                    ].value_counts()

                    top_category = counts.index[0]
                    top_count = counts.iloc[0]

                    insights.append(
                        f"🏆 The most frequent "
                        f"{category} is "
                        f"'{top_category}' with "
                        f"{top_count} records."
                    )

                    break

        # Sales-specific insight
        if (
            "Sales" in cleaned_df.columns
            and "Product" in cleaned_df.columns
        ):

            product_sales = (
                cleaned_df
                .groupby("Product")["Sales"]
                .sum()
                .sort_values(
                    ascending=False
                )
            )

            top_product = product_sales.index[0]
            top_sales = product_sales.iloc[0]

            insights.append(
                f"💰 '{top_product}' generated the "
                f"highest total sales of "
                f"{top_sales:,.2f}."
            )

        # Correlation insight
        if len(cleaned_numeric_columns) >= 2:

            correlation = cleaned_df[
                cleaned_numeric_columns
            ].corr()

            best_pair = None
            best_value = 0

            for i in range(
                len(correlation.columns)
            ):

                for j in range(i + 1, len(
                    correlation.columns
                )):

                    value = abs(
                        correlation.iloc[i, j]
                    )

                    if value > best_value:

                        best_value = value

                        best_pair = (
                            correlation.columns[i],
                            correlation.columns[j]
                        )

            if best_pair:

                actual_value = correlation.loc[
                    best_pair[0],
                    best_pair[1]
                ]

                insights.append(
                    f"🔗 Strongest relationship found "
                    f"between '{best_pair[0]}' and "
                    f"'{best_pair[1]}' with a "
                    f"correlation of "
                    f"{actual_value:.2f}."
                )

        # Display insights
        for insight in insights:

            st.info(insight)

        # ==================================================
        # AI-POWERED INSIGHT GENERATION
        # ==================================================

        st.subheader("🤖 AI-Powered Data Analysis")

        dataset_summary = f"""
        Rows: {cleaned_df.shape[0]}
        Columns: {cleaned_df.shape[1]}

        Missing values before cleaning: {original_missing}
        Missing values after cleaning: {cleaned_missing}

        Duplicate rows removed: {removed_duplicates}

        Numeric columns:
        {cleaned_numeric_columns}

        Categorical columns:
        {categorical_columns}
        """

        if "Sales" in cleaned_df.columns:
            dataset_summary += f"""
        Sales:
        Average: {cleaned_df["Sales"].mean():,.2f}
        Minimum: {cleaned_df["Sales"].min():,.2f}
        Maximum: {cleaned_df["Sales"].max():,.2f}
        Total: {cleaned_df["Sales"].sum():,.2f}
        """

        if "Units_Sold" in cleaned_df.columns:
            dataset_summary += f"""
        Units Sold:
        Average: {cleaned_df["Units_Sold"].mean():,.2f}
        Minimum: {cleaned_df["Units_Sold"].min():,.2f}
        Maximum: {cleaned_df["Units_Sold"].max():,.2f}
        """

        if "Customer_Rating" in cleaned_df.columns:
            dataset_summary += f"""
        Customer Rating:
        Average: {cleaned_df["Customer_Rating"].mean():,.2f}
        Minimum: {cleaned_df["Customer_Rating"].min():,.2f}
        Maximum: {cleaned_df["Customer_Rating"].max():,.2f}
        """

        if "Product" in cleaned_df.columns:
            product_sales = (
                    cleaned_df
                    .groupby("Product")["Sales"]
                    .sum()
                    .sort_values(ascending=False)
                )

            dataset_summary += f"""
        Sales by Product:
        {product_sales.to_string()}
        """

        if "ai_result" not in st.session_state:
            st.session_state.ai_result = None

        if st.button("🧠 Generate AI Insights"):
            with st.spinner("AI is analyzing your dataset..."):
                st.session_state.ai_result = generate_ai_insights(
                    dataset_summary
                )

        if st.session_state.ai_result:
            st.markdown(st.session_state.ai_result)

            st.divider()

            st.subheader("📄 Automated Report")

            if "report_text" not in st.session_state:
                st.session_state.report_text = None

            
            if st.button("📊 Generate Report"):
                with st.spinner("Generating report..."):
                    st.session_state.report_text = generate_report(cleaned_df)

            if st.session_state.report_text:
                st.success("Report generated successfully!")

                st.text_area(
                    "Generated Report",
                    st.session_state.report_text,
                    height=400
                )

                st.download_button(
                    label="⬇️ Download Report",
                    data=st.session_state.report_text,
                    file_name="ai_data_analysis_report.txt",
                    mime="text/plain"
                )
    except Exception as e:
        st.error(
                f"Error while processing the dataset: {e}"
            )