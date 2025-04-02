import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database.queries import aggregate_monthly_sinkings
import pandas as pd
from datetime import datetime

def test_aggregate_monthly_sinkings():
    # Test without date filters
    df = aggregate_monthly_sinkings()
    assert isinstance(df, pd.DataFrame)
    assert 'sunk_month_year' in df.columns
    assert 'total_sinkings' in df.columns
    assert 'total_tonnage' in df.columns
    assert len(df) > 0  # Should have data
    
    # Test with date filters for 1942
    df_1942 = aggregate_monthly_sinkings('1942-01-01', '1942-12-31')
    assert isinstance(df_1942, pd.DataFrame)
    assert len(df_1942) == 12  # Should have 12 months for 1942
    assert all(pd.to_datetime(df_1942['sunk_month_year']).dt.year == 1942)
    
    # Test specific month (December 1941)
    df_dec_1941 = aggregate_monthly_sinkings('1941-12-01', '1941-12-31')
    assert len(df_dec_1941) == 1
    assert df_dec_1941.iloc[0]['total_sinkings'] == 24  # Known value from our data
    assert df_dec_1941.iloc[0]['total_tonnage'] == 71426.0  # Known value from our data
