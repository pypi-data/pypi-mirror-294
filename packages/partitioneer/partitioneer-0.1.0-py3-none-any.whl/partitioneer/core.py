import os
import pandas as pd


def read_data_from_partitions(base_path):
    all_files = []
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith(".parquet"):
                all_files.append(os.path.join(root, file))
    return pd.concat([pd.read_parquet(f) for f in all_files])


def write_data_to_partitions(df, base_path, partition_cols):
    for _, row in df.iterrows():
        path = base_path
        for col in partition_cols:
            path = os.path.join(path, f"{col}={row[col]}")
        os.makedirs(path, exist_ok=True)
        file_path = os.path.join(path, "data.parquet")
        row.to_frame().T.to_parquet(file_path)
