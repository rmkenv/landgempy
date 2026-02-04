"""
Multi-stream waste modeling for LandGEM.
"""
import numpy as np
import pandas as pd
from typing import Dict, List, Union
from .core import LandGEM


class MultiStreamLandGEM:
    """
    Multi-stream waste modeling with different L0 values.

    Allows modeling of different waste types (MSW, organic,
    construction, etc.) with distinct methane generation potentials.

    Parameters
    ----------
    k : float
        Methane generation rate (1/year) - shared across streams
    methane_content : float
        Methane fraction of LFG (default: 0.50)
    nmoc_concentration : float, optional
        NMOC concentration in ppm

    Examples
    --------
    >>> model = MultiStreamLandGEM(k=0.05, methane_content=0.50)
    >>> model.add_stream('msw', L0=170)
    >>> model.add_stream('organic', L0=200)
    >>> results = model.calculate_multi_stream(
    ...     waste_data={
    ...         'msw': {'years': [2020, 2021], 'amounts': [5000, 5200]},
    ...         'organic': {'years': [2020, 2021], 'amounts': [1000, 1100]}
    ...     },
    ...     calculation_year=2030
    ... )
    """

    def __init__(
        self,
        k: float,
        methane_content: float = 0.50,
        nmoc_concentration: float = None
    ):
        self.k = k
        self.methane_content = methane_content
        self.nmoc_concentration = nmoc_concentration
        self.streams = {}

    def add_stream(self, name: str, L0: float) -> None:
        """
        Add a waste stream with specific L0 value.

        Parameters
        ----------
        name : str
            Stream identifier (e.g., 'msw', 'organic')
        L0 : float
            Potential methane capacity for this stream (m³/Mg)
        """
        model = LandGEM(
            k=self.k,
            L0=L0,
            methane_content=self.methane_content,
            nmoc_concentration=self.nmoc_concentration
        )
        self.streams[name] = model

    def calculate_multi_stream(
        self,
        waste_data: Dict[str, Dict[str, Union[List, np.ndarray]]],
        calculation_year: int,
        collection_efficiency: float = 0.0,
        include_nmoc: bool = False
    ) -> Dict[str, float]:
        """
        Calculate emissions from multiple waste streams.

        Parameters
        ----------
        waste_data : dict
            Dictionary mapping stream names to waste data:
            {'stream_name': {'years': [...], 'amounts': [...]}}
        calculation_year : int
            Year to calculate emissions for
        collection_efficiency : float
            Fraction of gas collected (0-1)
        include_nmoc : bool
            Whether to include NMOC calculations

        Returns
        -------
        dict
            Combined emissions from all streams
        """
        total_results = {
            'ch4_m3_year': 0.0,
            'total_lfg_m3_year': 0.0,
            'co2_m3_year': 0.0,
            'ch4_collected_m3_year': 0.0,
            'lfg_collected_m3_year': 0.0
        }

        stream_results = {}

        for stream_name, data in waste_data.items():
            if stream_name not in self.streams:
                raise ValueError(f"Stream '{stream_name}' not defined")

            model = self.streams[stream_name]

            results = model.calculate_emissions(
                waste_years=data['years'],
                waste_amounts=data['amounts'],
                calculation_year=calculation_year,
                collection_efficiency=collection_efficiency,
                include_nmoc=include_nmoc
            )

            stream_results[stream_name] = results

            # Accumulate totals
            for key in total_results.keys():
                total_results[key] += results.get(key, 0.0)

        # Add NMOC if requested
        if include_nmoc and self.nmoc_concentration:
            total_results['nmoc_mg_year'] = sum(
                r.get('nmoc_mg_year', 0.0) for r in stream_results.values()
            )

        # Add stream-specific results
        total_results['streams'] = stream_results

        return total_results

    def calculate_time_series_multi_stream(
        self,
        waste_data: Dict[str, Dict[str, Union[List, np.ndarray]]],
        projection_years: Union[List, np.ndarray],
        collection_efficiency: float = 0.0
    ) -> pd.DataFrame:
        """
        Calculate time series for multiple streams.

        Parameters
        ----------
        waste_data : dict
            Waste data for each stream
        projection_years : array-like
            Years to calculate emissions for
        collection_efficiency : float
            Fraction of gas collected

        Returns
        -------
        pd.DataFrame
            Time series with total and per-stream emissions
        """
        results = []

        for year in projection_years:
            year_results = self.calculate_multi_stream(
                waste_data=waste_data,
                calculation_year=year,
                collection_efficiency=collection_efficiency
            )

            row = {
                'year': year,
                'total_ch4_m3_year': year_results['ch4_m3_year'],
                'total_lfg_m3_year': year_results['total_lfg_m3_year'],
                'total_co2_m3_year': year_results['co2_m3_year']
            }

            # Add per-stream values
            for stream_name, stream_res in year_results['streams'].items():
                row[f'{stream_name}_ch4_m3_year'] = stream_res['ch4_m3_year']

            results.append(row)

        df = pd.DataFrame(results)
        df['cumulative_ch4_m3'] = df['total_ch4_m3_year'].cumsum()

        return df

    def __repr__(self):
        streams_str = ', '.join(self.streams.keys())
        return f"MultiStreamLandGEM(k={self.k}, streams=[{streams_str}])"
