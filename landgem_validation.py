"""
Input validation for LandGEM parameters.
"""
import numpy as np
from typing import Union, List


def validate_inputs(k: float, L0: float, methane_content: float) -> None:
    """
    Validate LandGEM input parameters.

    Parameters
    ----------
    k : float
        Methane generation rate (1/year)
    L0 : float
        Potential methane capacity (m³/Mg)
    methane_content : float
        Methane fraction of LFG (0-1)

    Raises
    ------
    ValueError
        If any parameter is out of valid range
    TypeError
        If any parameter is not numeric
    """
    # Type checking
    if not isinstance(k, (int, float)):
        raise TypeError(f"k must be numeric, got {type(k)}")
    if not isinstance(L0, (int, float)):
        raise TypeError(f"L0 must be numeric, got {type(L0)}")
    if not isinstance(methane_content, (int, float)):
        raise TypeError(f"methane_content must be numeric, got {type(methane_content)}")

    # Range checking
    if k <= 0:
        raise ValueError(f"k must be positive, got {k}")
    if k > 1.0:
        raise ValueError(f"k unusually high (>1.0), got {k}. Check units (1/year)")

    if L0 <= 0:
        raise ValueError(f"L0 must be positive, got {L0}")
    if L0 > 500:
        raise ValueError(f"L0 unusually high (>500), got {L0}. Check units (m³/Mg)")

    if not 0 < methane_content < 1:
        raise ValueError(
            f"methane_content must be between 0 and 1, got {methane_content}"
        )
    if methane_content < 0.4 or methane_content > 0.6:
        import warnings
        warnings.warn(
            f"methane_content {methane_content} outside typical range (0.4-0.6)"
        )


def validate_waste_data(
    waste_years: Union[List, np.ndarray],
    waste_amounts: Union[List, np.ndarray]
) -> None:
    """
    Validate waste acceptance data.

    Parameters
    ----------
    waste_years : array-like
        Years when waste was accepted
    waste_amounts : array-like
        Waste amounts (Mg)

    Raises
    ------
    ValueError
        If data is invalid or inconsistent
    """
    waste_years = np.array(waste_years)
    waste_amounts = np.array(waste_amounts)

    if len(waste_years) == 0:
        raise ValueError("waste_years is empty")

    if len(waste_years) != len(waste_amounts):
        raise ValueError(
            f"waste_years and waste_amounts must have same length: "
            f"{len(waste_years)} != {len(waste_amounts)}"
        )

    if np.any(waste_amounts < 0):
        raise ValueError("waste_amounts cannot be negative")

    if not np.all(np.diff(waste_years) >= 0):
        raise ValueError("waste_years must be in ascending order")

    if np.any(np.diff(waste_years) == 0):
        import warnings
        warnings.warn("Duplicate years found in waste_years")
