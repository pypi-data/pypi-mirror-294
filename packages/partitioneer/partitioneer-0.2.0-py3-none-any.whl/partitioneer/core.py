import os
from typing import List, Union, Optional, Literal
from datetime import datetime, date
from dataclasses import dataclass
import pandas as pd

FilterType = Literal[
    "equals",
    "not_equal",
    "greater_than",
    "less_than",
    "greater_than_or_equal",
    "less_than_or_equal",
    "in",
    "not_in",
]

@dataclass
class PartitionFilter:
    """
    Represents a filter to be applied on partitioned data.

    Attributes:
        column (str): The name of the column to filter on.
        filter_type (FilterType): The type of filter to apply.
        value (Union[str, List[str], int, List[int], float, List[float]]): The value(s) to compare against.

    Example:
        PartitionFilter("age", "greater_than", 18)
        PartitionFilter("category", "in", ["A", "B", "C"])
    """
    column: str
    filter_type: FilterType
    value: Union[str, List[str], int, List[int], float, List[float]]

def write_data_to_partitions(
        df: pd.DataFrame,
        base_path: str,
        partition_cols: Optional[List[str]] = None,
        date_col: Optional[str] = None,
        override_existing: bool = False,
        data_file_name: str = "data.parquet"
) -> None:
    """
    Write data to partitioned Parquet files.

    Args:
        df (pd.DataFrame): The DataFrame to write.
        base_path (str): The base path to write the partitioned data to.
        partition_cols (Optional[List[str]]): The columns to partition by.
        date_col (Optional[str]): The date column to use for partitioning.
        override_existing (bool): Whether to override existing files.
        data_file_name (str): The name of the data file in each partition.

    Raises:
        ValueError: If neither partition_cols nor date_col is provided, or if both are provided.
    """
    if (partition_cols is None and date_col is None) or (partition_cols is not None and date_col is not None):
        raise ValueError("Either partition_cols or date_col must be provided, but not both.")

    if date_col:
        df[date_col] = pd.to_datetime(df[date_col])
        partition_cols = ['year', 'month', 'day']
        df['year'] = df[date_col].dt.year
        df['month'] = df[date_col].dt.month
        df['day'] = df[date_col].dt.day

    df = df.sort_values(by=partition_cols)

    for _, row in df.iterrows():
        path = base_path
        for col in partition_cols:
            path = os.path.join(path, f"{col}={row[col]}")

        os.makedirs(path, exist_ok=True)
        file_path = os.path.join(path, data_file_name)

        if not override_existing and os.path.exists(file_path):
            existing_df = pd.read_parquet(file_path)
            new_df = pd.concat([existing_df, row.to_frame().T], ignore_index=True)
            new_df.to_parquet(file_path, index=False)
        else:
            row.to_frame().T.to_parquet(file_path, index=False)
def convert_to_datetime(date_input: Optional[Union[str, datetime, date]]) -> Optional[datetime]:
    if date_input is None:
        return None
    if isinstance(date_input, datetime):
        return date_input
    if isinstance(date_input, date):
        return datetime(date_input.year, date_input.month, date_input.day)
    if isinstance(date_input, str):
        return datetime.strptime(date_input, "%Y-%m-%d")
    raise ValueError(f"Invalid date input: {date_input}")

def read_data_from_partitions(
        base_path: str,
        filters: Optional[Union[PartitionFilter, List[PartitionFilter]]] = None,
        add_partition_date: bool = False,
        start_date: Optional[Union[str, datetime, date]] = None,
        end_date: Optional[Union[str, datetime, date]] = None
) -> pd.DataFrame:
    """
    Read data from partitioned Parquet files.

    Args:
        base_path (str): The base path containing partitioned Parquet files.
        filters (Optional[Union[PartitionFilter, List[PartitionFilter]]]): Filters to apply to the data.
        add_partition_date (bool): Whether to add a partition_date column to the result.
        start_date (Optional[Union[str, datetime, date]]): The start date for filtering (inclusive).
        end_date (Optional[Union[str, datetime, date]]): The end date for filtering (inclusive).

    Returns:
        pd.DataFrame: The combined and filtered data from all partitions.

    Raises:
        ValueError: If an invalid filter type is provided.
    """
    start_date = convert_to_datetime(start_date)
    end_date = convert_to_datetime(end_date)

    all_files = []
    for root, _, files in os.walk(base_path):
        for file in files:
            if file.endswith(".parquet"):
                all_files.append(os.path.join(root, file))

    dfs = []
    partition_cols = []
    for file in all_files:
        df = pd.read_parquet(file)

        # Extract partition information from the file path
        parts = file.split(os.path.sep)
        date_parts = {}
        for part in parts:
            if '=' in part:
                col, val = part.split('=')
                if col not in df.columns:
                    df[col] = val
                if col not in partition_cols:
                    partition_cols.append(col)
                if col in ['year', 'month', 'day']:
                    date_parts[col] = int(val)

        if filters:
            if isinstance(filters, PartitionFilter):
                filters = [filters]

            for filter in filters:
                if filter.filter_type == "equals":
                    df = df[df[filter.column] == filter.value]
                elif filter.filter_type == "not_equal":
                    df = df[df[filter.column] != filter.value]
                elif filter.filter_type == "greater_than":
                    df = df[df[filter.column] > filter.value]
                elif filter.filter_type == "less_than":
                    df = df[df[filter.column] < filter.value]
                elif filter.filter_type == "greater_than_or_equal":
                    df = df[df[filter.column] >= filter.value]
                elif filter.filter_type == "less_than_or_equal":
                    df = df[df[filter.column] <= filter.value]
                elif filter.filter_type == "in":
                    df = df[df[filter.column].isin(filter.value)]
                elif filter.filter_type == "not_in":
                    df = df[~df[filter.column].isin(filter.value)]
                else:
                    raise ValueError(f"Invalid filter type: {filter.filter_type}")

        if len(date_parts) == 3:
            partition_date = datetime(date_parts['year'], date_parts['month'], date_parts['day'])
            if start_date and partition_date < start_date:
                continue
            if end_date and partition_date > end_date:
                continue
            if add_partition_date:
                df['partition_date'] = partition_date

        dfs.append(df)

    result = pd.concat(dfs, ignore_index=True)
    return result.sort_values(by=partition_cols) if partition_cols else result
def get_latest_partition_date(base_path: str) -> Optional[datetime]:
    """
    Get the latest partition date from the directory structure.

    Args:
        base_path (str): The base path containing partitioned Parquet files.

    Returns:
        Optional[datetime]: The latest partition date, or None if no date partitions found.
    """
    latest_date = None
    for root, dirs, files in os.walk(base_path):
        if 'year=' in root and 'month=' in root and 'day=' in root:
            parts = root.split(os.path.sep)
            year = int(next(part.split('=')[1] for part in parts if part.startswith('year=')))
            month = int(next(part.split('=')[1] for part in parts if part.startswith('month=')))
            day = int(next(part.split('=')[1] for part in parts if part.startswith('day=')))
            current_date = datetime(year, month, day)
            if latest_date is None or current_date > latest_date:
                latest_date = current_date
    return latest_date

def get_first_partition_date(base_path: str) -> Optional[datetime]:
    """
    Get the first partition date from the directory structure.

    Args:
        base_path (str): The base path containing partitioned Parquet files.

    Returns:
        Optional[datetime]: The first partition date, or None if no date partitions found.
    """
    first_date = None
    for root, dirs, files in os.walk(base_path):
        if 'year=' in root and 'month=' in root and 'day=' in root:
            parts = root.split(os.path.sep)
            year = int(next(part.split('=')[1] for part in parts if part.startswith('year=')))
            month = int(next(part.split('=')[1] for part in parts if part.startswith('month=')))
            day = int(next(part.split('=')[1] for part in parts if part.startswith('day=')))
            current_date = datetime(year, month, day)
            if first_date is None or current_date < first_date:
                first_date = current_date
    return first_date