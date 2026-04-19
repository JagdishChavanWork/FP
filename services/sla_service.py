import pandas as pd


def calculate_avg_resolution_time(df):
    df_valid = df[df["duration_seconds"].notna()]

    if df_valid.empty:
        return 0

    return df_valid["duration_seconds"].mean()


def analyst_avg_time(df):
    df_valid = df[df["duration_seconds"].notna()]

    if df_valid.empty:
        return pd.Series()

    return df_valid.groupby("assigned_to")["duration_seconds"].mean()


def sla_breach_cases(df, threshold_seconds=300):
    """
    Default SLA = 5 minutes (300 seconds)
    """

    df_valid = df[df["duration_seconds"].notna()]

    return df_valid[df_valid["duration_seconds"] > threshold_seconds]