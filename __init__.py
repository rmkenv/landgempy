"""
landgempy - Landfill Gas Emissions Model
EPA First-Order Decay Implementation

Python implementation of the EPA's Landfill Gas Emissions Model (LandGEM)
for estimating methane, carbon dioxide, and NMOC emissions from landfills
using first-order decay equations.

Author: Ryan Kmetz
License: MIT
"""

__version__ = "1.0.0"
__author__ = "Ryan Kmetz"
__license__ = "MIT"

# Core functionality
from .core import LandGEM
from .parameters import DefaultParameters
from .multi_stream import MultiStreamLandGEM

# Validation
from .validation import validate_inputs, validate_waste_data

# I/O functions
from .io import (
    export_to_csv,
    export_to_excel,
    import_waste_data,
    import_multi_stream_data
)

# Equations (useful for advanced users)
from .equations import (
    first_order_decay,
    calculate_waste_in_place,
    estimate_k_from_half_life,
    estimate_half_life_from_k
)

# Visualization
from .visualization import (
    plot_emissions_timeseries,
    plot_gas_composition,
    plot_multi_stream_comparison
)

__all__ = [
    # Version info
    '__version__',
    '__author__',
    '__license__',
    
    # Core classes
    'LandGEM',
    'DefaultParameters',
    'MultiStreamLandGEM',
    
    # Validation
    'validate_inputs',
    'validate_waste_data',
    
    # I/O
    'export_to_csv',
    'export_to_excel',
    'import_waste_data',
    'import_multi_stream_data',
    
    # Equations
    'first_order_decay',
    'calculate_waste_in_place',
    'estimate_k_from_half_life',
    'estimate_half_life_from_k',
    
    # Visualization
    'plot_emissions_timeseries',
    'plot_gas_composition',
    'plot_multi_stream_comparison',
]
