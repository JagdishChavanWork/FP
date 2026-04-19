import streamlit as st
import sqlite3
import pandas as pd

from modules.admin.charts import *
from modules.admin.filters import apply_common_filters
from services.sla_service import (
    calculate_avg_resolution_time,
    analyst_avg_time,
    sla_breach_cases
)


def admin_dashboard():

    st.title("Operations Intelligence Dashboard")

    conn = sqlite3.connect("database/db.sqlite3")
    df = pd.read_sql_query("SELECT * FROM cases", conn)
    conn.close()

    if df.empty:
        st.warning("No case data available")
        return

    df_filtered = apply_common_filters(df, key_prefix="ops")

    # =========================================================
    # KPI SECTION
    # =========================================================
    st.header("Key Metrics")

    total_cases = len(df_filtered)
    completed_cases = len(df_filtered[df_filtered["status"] == "Completed"])
    pending_cases = len(df_filtered[df_filtered["status"] == "Pending"])

    avg_time = calculate_avg_resolution_time(df_filtered)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Cases", total_cases)
    col2.metric("Completed", completed_cases)
    col3.metric("Pending", pending_cases)
    col4.metric("Avg Resolution Time (sec)", f"{avg_time:.2f}")

    st.divider()

    # =========================================================
    # ANALYST TIME PERFORMANCE
    # =========================================================
    st.header("Analyst Time Performance")

    analyst_time = analyst_avg_time(df_filtered)

    if not analyst_time.empty:
        st.bar_chart(analyst_time)
    else:
        st.info("No timing data available")

    st.divider()

    # =========================================================
    # SLA BREACH
    # =========================================================
    st.header("SLA Breach Cases")

    sla_cases = sla_breach_cases(df_filtered, threshold_seconds=300)

    if not sla_cases.empty:
        st.warning(f"{len(sla_cases)} cases breached SLA (5 min)")

        st.dataframe(
            sla_cases[[
                "id",
                "assigned_to",
                "duration_seconds",
                "status"
            ]]
        )
    else:
        st.success("No SLA breaches")

    st.divider()

    # =========================================================
    # EXISTING ANALYTICS (KEEP YOUR CURRENT BLOCKS BELOW)
    # =========================================================

    st.header("Case Trend")

    if "step" in df_filtered.columns:
        line_trend(df_filtered, "step", "Cases Over Time")

    st.divider()

    st.header("Detailed Case Review")

    st.dataframe(
        df_filtered.sort_values(by="id", ascending=False),
        use_container_width=True
    )