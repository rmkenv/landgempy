"""
Core LandGEM model implementation.
"""
import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Union
from .equations import first_order_decay, calculate_waste_in_place
from .validation import validate_inputs


class LandGEM:
    """
    Landfill Gas Emissions Model (LandGEM) implementation.

    Based on EPA's first-order decay model for estimating 
    methane, CO2, and NMOC emissions from landfills.

    Parameters
    ----------
    k : float
        Methane generation rate constant (1/year)
    L0 : float
        Potential methane generation capacity (m³/Mg)
    methane_content : float
        Methane fraction of total LFG (default: 0.50)
    nmoc_concentration : float, optional
        NMOC concentration in ppm as hexane

    Examples
    --------
    >>> model = LandGEM(k=0.05, L0=170, methane_content=0.50)
    >>> waste_years = np.array([2020, 2021, 2022])
    >>> waste_amounts = np.array([5000, 5200, 5500])
    >>> results = model.calculate_emissions(
    ...     waste_years=waste_years,
    ...     waste_amounts=waste_amounts,
    ...     calculation_year=2030
    ... )
    >>> print(results['ch4_m3_year'])
    """

    def __init__(
        self,
        k: float,
        L0: float,
        methane_content: float = 0.50,
        nmoc_concentration: Optional[float] = None
    ):
        validate_inputs(k, L0, methane_content)

        self.k = k
        self.L0 = L0
        self.methane_content = methane_content
        self.nmoc_concentration = nmoc_concentration

    def calculate_emissions(
        self,
        waste_years: Union[List, np.ndarray],
        waste_amounts: Union[List, np.ndarray],
        calculation_year: int,
        collection_efficiency: float = 0.0,
        include_nmoc: bool = False
    ) -> Dict[str, float]:
        """
        Calculate emissions for a specific year.

        Parameters
        ----------
        waste_years : array-like
            Years when waste was accepted
        waste_amounts : array-like
            Amount of waste accepted each year (Mg)
        calculation_year : int
            Year to calculate emissions for
        collection_efficiency : float
            Fraction of gas collected (0-1), default 0.0
        include_nmoc : bool
            Whether to include NMOC calculations, default False

        Returns
        -------
        dict
            Dictionary containing:
            - ch4_m3_year: Methane generation (m³/year)
            - total_lfg_m3_year: Total landfill gas (m³/year)
            - co2_m3_year: Carbon dioxide generation (m³/year)
            - ch4_collected_m3_year: Collected methane (m³/year)
            - lfg_collected_m3_year: Collected LFG (m³/year)
            - nmoc_mg_year: NMOC emissions (Mg/year) if include_nmoc=True
        """
        waste_years = np.array(waste_years)
        waste_amounts = np.array(waste_amounts)

        if len(waste_years) != len(waste_amounts):
            raise ValueError("waste_years and waste_amounts must have same length")

        if not 0 <= collection_efficiency <= 1:
            raise ValueError("collection_efficiency must be between 0 and 1")

        # Calculate methane generation
        ch4_m3_year = first_order_decay(
            waste_years=waste_years,
            waste_amounts=waste_amounts,
            calculation_year=calculation_year,
            k=self.k,
            L0=self.L0
        )

        # Calculate total LFG
        total_lfg = ch4_m3_year / self.methane_content

        # Calculate CO2
        co2_m3_year = total_lfg * (1 - self.methane_content)

        # Calculate collected amounts
        ch4_collected = ch4_m3_year * collection_efficiency
        total_lfg_collected = total_lfg * collection_efficiency

        results = {
            'ch4_m3_year': ch4_m3_year,
            'total_lfg_m3_year': total_lfg,
            'co2_m3_year': co2_m3_year,
            'ch4_collected_m3_year': ch4_collected,
            'lfg_collected_m3_year': total_lfg_collected,
        }

        if include_nmoc and self.nmoc_concentration:
            nmoc_mg_year = self._calculate_nmoc(total_lfg)
            results['nmoc_mg_year'] = nmoc_mg_year

        return results

    def calculate_time_series(
        self,
        waste_years: Union[List, np.ndarray],
        waste_amounts: Union[List, np.ndarray],
        projection_years: Union[List, np.ndarray],
        collection_efficiency: float = 0.0,
        include_nmoc: bool = False
    ) -> pd.DataFrame:
        """
        Calculate emissions time series for multiple years.

        Parameters
        ----------
        waste_years : array-like
            Years when waste was accepted
        waste_amounts : array-like
            Amount of waste accepted each year (Mg)
        projection_years : array-like
            Years to calculate emissions for
        collection_efficiency : float
            Fraction of gas collected (0-1)
        include_nmoc : bool
            Whether to include NMOC calculations

        Returns
        -------
        pd.DataFrame
            DataFrame with columns:
            - year: Calculation year
            - ch4_m3_year: Annual methane generation
            - total_lfg_m3_year: Annual total LFG
            - co2_m3_year: Annual CO2 generation
            - cumulative_ch4_m3: Cumulative methane
            - cumulative_lfg_m3: Cumulative LFG
            And additional columns if collection/NMOC enabled
        """
        results = []

        for year in projection_years:
            emissions = self.calculate_emissions(
                waste_years=waste_years,
                waste_amounts=waste_amounts,
                calculation_year=year,
                collection_efficiency=collection_efficiency,
                include_nmoc=include_nmoc
            )
            emissions['year'] = year
            results.append(emissions)

        df = pd.DataFrame(results)

        # Calculate cumulative values
        df['cumulative_ch4_m3'] = df['ch4_m3_year'].cumsum()
        df['cumulative_lfg_m3'] = df['total_lfg_m3_year'].cumsum()

        # Reorder columns
        cols = ['year', 'ch4_m3_year', 'total_lfg_m3_year', 'co2_m3_year']
        if collection_efficiency > 0:
            cols.extend(['ch4_collected_m3_year', 'lfg_collected_m3_year'])
        if include_nmoc and self.nmoc_concentration:
            cols.append('nmoc_mg_year')
        cols.extend(['cumulative_ch4_m3', 'cumulative_lfg_m3'])

        return df[cols]

    def calculate_waste_in_place(
        self,
        waste_years: Union[List, np.ndarray],
        waste_amounts: Union[List, np.ndarray],
        calculation_year: int,
        decay_fraction: float = 0.0
    ) -> float:
        """
        Calculate waste in place at a given year.

        Parameters
        ----------
        waste_years : array-like
            Years when waste was accepted
        waste_amounts : array-like
            Amount of waste accepted each year (Mg)
        calculation_year : int
            Year to calculate for
        decay_fraction : float
            Fraction of waste that has decayed (0-1)

        Returns
        -------
        float
            Waste in place (Mg)
        """
        return calculate_waste_in_place(
            waste_years=np.array(waste_years),
            waste_amounts=np.array(waste_amounts),
            calculation_year=calculation_year,
            decay_fraction=decay_fraction
        )

    def _calculate_nmoc(self, total_lfg_m3_year: float) -> float:
        """
        Calculate NMOC emissions from total LFG generation.

        Based on EPA LandGEM methodology:
        NMOC (Mg/year) = (Concentration × MW × Total LFG) / (3.6 × 10^9)

        Parameters
        ----------
        total_lfg_m3_year : float
            Total landfill gas generation (m³/year)

        Returns
        -------
        float
            NMOC emissions (Mg/year)
        """
        if not self.nmoc_concentration:
            return 0.0

        # Molecular weight correction factor (hexane basis)
        MW_factor = 86.18 / 16.04  # Hexane MW / Methane MW

        # NMOC calculation
        # Concentration in ppm, total LFG in m³/year
        # Result in Mg/year
        nmoc_mg_year = (
            self.nmoc_concentration * MW_factor * total_lfg_m3_year
        ) / (3.6e9)

        return nmoc_mg_year

    def __repr__(self):
        return (
            f"LandGEM(k={self.k}, L0={self.L0}, "
            f"methane_content={self.methane_content}, "
            f"nmoc_concentration={self.nmoc_concentration})"
        )
