"""
First-order decay equations for LandGEM.
"""
import numpy as np


def first_order_decay(
    waste_years: np.ndarray,
    waste_amounts: np.ndarray,
    calculation_year: int,
    k: float,
    L0: float,
    time_increment: float = 0.1
) -> float:
    """
    Calculate methane generation using first-order decay model.

    Implements the EPA LandGEM equation:
    Q_CH4 = Σ(i=1 to n) Σ(j=0.0 to 1.0) (k × L0 × Mi / 10) × exp(-k × t_ij)

    Parameters
    ----------
    waste_years : np.ndarray
        Years when waste was accepted
    waste_amounts : np.ndarray
        Waste amounts (Mg) for each year
    calculation_year : int
        Year to calculate emissions for
    k : float
        Methane generation rate (1/year)
    L0 : float
        Potential methane capacity (m³/Mg)
    time_increment : float
        Sub-annual time increment (default: 0.1 year)

    Returns
    -------
    float
        Annual methane generation (m³/year)

    Notes
    -----
    The equation calculates emissions for waste accepted in the past
    by summing contributions from each waste cohort with exponential
    decay over time.
    """
    total_ch4 = 0.0

    # Iterate over each waste cohort
    for i, (year, amount) in enumerate(zip(waste_years, waste_amounts)):
        # Skip future waste
        if year > calculation_year:
            continue

        # Calculate sub-annual contributions
        # j ranges from 0.0 to 0.9 in increments of time_increment
        j_values = np.arange(0.0, 1.0, time_increment)

        for j in j_values:
            # Age of waste section j accepted in year i
            t_ij = calculation_year - year + (1 - j)

            # First-order decay calculation
            # Division by 10 accounts for time increment integration
            ch4_contribution = (k * L0 * amount / 10) * np.exp(-k * t_ij)
            total_ch4 += ch4_contribution

    return total_ch4


def calculate_waste_in_place(
    waste_years: np.ndarray,
    waste_amounts: np.ndarray,
    calculation_year: int,
    decay_fraction: float = 0.0
) -> float:
    """
    Calculate waste in place accounting for decomposition.

    Parameters
    ----------
    waste_years : np.ndarray
        Years when waste was accepted
    waste_amounts : np.ndarray
        Waste amounts (Mg) for each year
    calculation_year : int
        Year to calculate for
    decay_fraction : float
        Fraction of waste that has decayed (0-1)

    Returns
    -------
    float
        Waste in place (Mg)
    """
    # Sum waste accepted up to calculation year
    mask = waste_years <= calculation_year
    total_waste = np.sum(waste_amounts[mask])

    # Account for decay
    waste_in_place = total_waste * (1 - decay_fraction)

    return waste_in_place


def estimate_k_from_half_life(half_life_years: float) -> float:
    """
    Estimate k value from half-life.

    Parameters
    ----------
    half_life_years : float
        Half-life of methane generation (years)

    Returns
    -------
    float
        Methane generation rate k (1/year)

    Notes
    -----
    k = ln(2) / half_life
    """
    return np.log(2) / half_life_years


def estimate_half_life_from_k(k: float) -> float:
    """
    Estimate half-life from k value.

    Parameters
    ----------
    k : float
        Methane generation rate (1/year)

    Returns
    -------
    float
        Half-life (years)

    Notes
    -----
    half_life = ln(2) / k
    """
    return np.log(2) / k
