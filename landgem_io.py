"""
Import/export functions for LandGEM.
"""
import pandas as pd
import numpy as np
from typing import Dict, Tuple, Union
from pathlib import Path


def export_to_csv(
    df: pd.DataFrame,
    filename: str,
    include_metadata: bool = True
) -> None:
    """
    Export emissions data to CSV file.

    Parameters
    ----------
    df : pd.DataFrame
        Emissions data from calculate_time_series
    filename : str
        Output CSV filename
    include_metadata : bool
        Whether to include metadata header
    """
    if include_metadata:
        with open(filename, 'w') as f:
            f.write("# LandGEM Emissions Data
")
            f.write(f"# Generated: {pd.Timestamp.now()}
")
            f.write("#
")
        df.to_csv(filename, mode='a', index=False)
    else:
        df.to_csv(filename, index=False)


def export_to_excel(
    df: pd.DataFrame,
    filename: str,
    sheet_name: str = 'Emissions',
    include_metadata: bool = True
) -> None:
    """
    Export emissions data to Excel file.

    Parameters
    ----------
    df : pd.DataFrame
        Emissions data
    filename : str
        Output Excel filename
    sheet_name : str
        Name of worksheet
    include_metadata : bool
        Whether to include metadata sheet
    """
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)

        if include_metadata:
            metadata = pd.DataFrame({
                'Parameter': ['Generated', 'Rows', 'Columns'],
                'Value': [
                    str(pd.Timestamp.now()),
                    len(df),
                    len(df.columns)
                ]
            })
            metadata.to_excel(writer, sheet_name='Metadata', index=False)


def import_waste_data(
    filename: str,
    year_column: str = 'year',
    amount_column: str = 'waste_mg'
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Import waste acceptance data from CSV or Excel.

    Parameters
    ----------
    filename : str
        Path to data file (CSV or Excel)
    year_column : str
        Name of year column
    amount_column : str
        Name of waste amount column

    Returns
    -------
    tuple
        (waste_years, waste_amounts) as numpy arrays
    """
    file_path = Path(filename)

    if file_path.suffix == '.csv':
        df = pd.read_csv(filename)
    elif file_path.suffix in ['.xlsx', '.xls']:
        df = pd.read_excel(filename)
    else:
        raise ValueError(f"Unsupported file format: {file_path.suffix}")

    if year_column not in df.columns:
        raise ValueError(f"Column '{year_column}' not found in {filename}")
    if amount_column not in df.columns:
        raise ValueError(f"Column '{amount_column}' not found in {filename}")

    waste_years = df[year_column].values
    waste_amounts = df[amount_column].values

    return waste_years, waste_amounts


def import_multi_stream_data(
    filename: str,
    stream_columns: Dict[str, str]
) -> Dict[str, Dict[str, np.ndarray]]:
    """
    Import multi-stream waste data.

    Parameters
    ----------
    filename : str
        Path to data file
    stream_columns : dict
        Mapping of stream names to column names
        Example: {'msw': 'msw_mg', 'organic': 'organic_mg'}

    Returns
    -------
    dict
        Waste data formatted for MultiStreamLandGEM
    """
    file_path = Path(filename)

    if file_path.suffix == '.csv':
        df = pd.read_csv(filename)
    elif file_path.suffix in ['.xlsx', '.xls']:
        df = pd.read_excel(filename)
    else:
        raise ValueError(f"Unsupported file format: {file_path.suffix}")

    waste_data = {}
    years = df['year'].values

    for stream_name, column_name in stream_columns.items():
        if column_name not in df.columns:
            raise ValueError(f"Column '{column_name}' not found")

        waste_data[stream_name] = {
            'years': years,
            'amounts': df[column_name].values
        }

    return waste_data
