import os
import pandas as pd
from partitioneer import read_data_from_partitions, write_data_to_partitions


def test_write_and_read_data():
    df = pd.DataFrame({
        'year': [2023, 2023],
        'month': [10, 10],
        'day': [1, 2],
        'value': [100, 200]
    })
    base_path = './test_data'
    write_data_to_partitions(df, base_path, ['year', 'month', 'day'])
    result_df = read_data_from_partitions(base_path)
    assert df.equals(result_df)
    # Clean up
    import shutil
    shutil.rmtree(base_path)