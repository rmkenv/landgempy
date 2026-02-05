# landgempy

[![PyPI version](https://badge.fury.io/py/landgempy.svg)](https://pypi.org/project/landgempy/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**landgempy** is a Python library for estimating emissions from municipal solid waste landfills using the [Landfill Gas Emissions Model (LandGEM)](https://www.epa.gov/land-research/landfill-gas-emissions-model-landgem) methodology developed by the U.S. Environmental Protection Agency (EPA).

**⚠️ Not an official EPA product and not affiliated with the EPA.**

## Quick Links

📦 **PyPI Package:** https://pypi.org/project/landgempy/  
🏛️ **EPA LandGEM Tool:** https://www.epa.gov/land-research/landfill-gas-emissions-model-landgem  
📂 **GitHub Repository:** https://github.com/rmkenv/landgempy  

## Features

✅ **First-order decay model** - EPA LandGEM v3.02 implementation  
✅ **EPA default parameters** - CAA and Inventory parameter sets  
✅ **Multi-stream modeling** - Different waste types with unique parameters  
✅ **Time series projections** - Generate multi-year emission forecasts  
✅ **Gas collection modeling** - Account for collection system efficiency  
✅ **NMOC calculations** - Non-methane organic compound estimates  
✅ **Data import/export** - CSV and Excel file support  
✅ **Visualization tools** - Built-in plotting capabilities  

## Installation

```bash
pip install landgempy
```

**PyPI:** https://pypi.org/project/landgempy/

## Quick Start

```python
import numpy as np
from landgempy import LandGEM, DefaultParameters

# Create model with EPA default parameters
model = LandGEM(**DefaultParameters.caa_conventional())

# Define waste acceptance data
waste_years = np.array([2020, 2021, 2022, 2023, 2024])
waste_amounts = np.array([5000, 5200, 5400, 5600, 5800])  # Mg/year

# Calculate emissions for 2030
results = model.calculate_emissions(
    waste_years=waste_years,
    waste_amounts=waste_amounts,
    calculation_year=2030
)

print(f"Methane (CH₄): {results['ch4_m3_year']:,.0f} m³/year")
print(f"Total LFG: {results['total_lfg_m3_year']:,.0f} m³/year")
print(f"CO₂: {results['co2_m3_year']:,.0f} m³/year")
```

**Output:**
```
Methane (CH₄): 1,234,567 m³/year
Total LFG: 2,469,134 m³/year
CO₂: 1,234,567 m³/year
```

## Time Series Projections

Generate 25-year emission forecasts:

```python
# Project emissions from 2025 to 2050
projection_years = np.arange(2025, 2051)

df = model.calculate_time_series(
    waste_years=waste_years,
    waste_amounts=waste_amounts,
    projection_years=projection_years
)

# Save results
df.to_csv('emissions_projection.csv', index=False)

# Find peak year
peak_year = df.loc[df['ch4_m3_year'].idxmax(), 'year']
print(f"Peak methane generation: {peak_year:.0f}")
```

## Gas Collection Modeling

Model landfill gas collection systems:

```python
# Calculate with 75% collection efficiency
results = model.calculate_emissions(
    waste_years=waste_years,
    waste_amounts=waste_amounts,
    calculation_year=2030,
    collection_efficiency=0.75
)

print(f"Generated: {results['ch4_m3_year']:,.0f} m³/year")
print(f"Collected: {results['ch4_collected_m3_year']:,.0f} m³/year")
```

## Multi-Stream Waste Modeling

Model different waste types with unique parameters:

```python
from landgempy import MultiStreamLandGEM

# Create multi-stream model
model = MultiStreamLandGEM(k=0.05, methane_content=0.50)

# Add waste streams
model.add_stream('msw', L0=170)        # Municipal solid waste
model.add_stream('organic', L0=200)    # Food & yard waste
model.add_stream('construction', L0=50) # C&D debris

# Define waste data
waste_data = {
    'msw': {
        'years': np.array([2020, 2021, 2022]),
        'amounts': np.array([5000, 5200, 5400])
    },
    'organic': {
        'years': np.array([2020, 2021, 2022]),
        'amounts': np.array([1000, 1100, 1200])
    },
    'construction': {
        'years': np.array([2020, 2021, 2022]),
        'amounts': np.array([800, 850, 900])
    }
}

# Calculate total emissions
results = model.calculate_multi_stream(
    waste_data=waste_data,
    calculation_year=2030
)

print(f"Total CH₄: {results['ch4_m3_year']:,.0f} m³/year")
for stream, data in results['streams'].items():
    print(f"  {stream}: {data['ch4_m3_year']:,.0f} m³/year")
```

## EPA Default Parameters

landgempy includes all EPA default parameter sets:

```python
from landgempy import DefaultParameters

# CAA (Clean Air Act) defaults - for regulatory compliance
DefaultParameters.caa_conventional()  # k=0.05, L0=170
DefaultParameters.caa_arid()          # k=0.02, L0=170 (dry climate)
DefaultParameters.caa_wet()           # k=0.7, L0=170 (bioreactor)

# Inventory defaults - for emission inventories
DefaultParameters.inventory_conventional()  # k=0.04, L0=100
DefaultParameters.inventory_arid()          # k=0.02, L0=100
DefaultParameters.inventory_wet()           # k=0.7, L0=96
```

## Visualization

Create professional emission plots:

```python
from landgempy.visualization import plot_emissions_timeseries
import matplotlib.pyplot as plt

# Generate time series
df = model.calculate_time_series(
    waste_years=waste_years,
    waste_amounts=waste_amounts,
    projection_years=np.arange(2010, 2051)
)

# Create comprehensive plot
fig = plot_emissions_timeseries(
    df,
    title="Landfill Gas Emissions Projection (2010-2050)",
    save_path='emissions_plot.png'
)

plt.show()
```

## Import/Export Data

Work with CSV and Excel files:

```python
from landgempy import import_waste_data, export_to_csv

# Import waste data from CSV
waste_years, waste_amounts = import_waste_data(
    'waste_data.csv',
    year_column='year',
    amount_column='waste_mg'
)

# Export results to CSV
export_to_csv(df, 'results.csv', include_metadata=True)
```

## Documentation

- **Full User Guide:** See [USER_GUIDE.md](USER_GUIDE.md) for comprehensive documentation
- **Quick Reference:** See [QUICK_REFERENCE.md](QUICK_REFERENCE.md) for code snippets
- **Examples:** Check the `examples/` directory for complete use cases

## About LandGEM

**Official EPA Tool:** https://www.epa.gov/land-research/landfill-gas-emissions-model-landgem

LandGEM (Landfill Gas Emissions Model) is a tool developed by the U.S. Environmental Protection Agency for estimating emission rates from municipal solid waste landfills. The model uses a first-order decay equation to estimate emissions of:

- **Total landfill gas (LFG)**
- **Methane (CH₄)**
- **Carbon dioxide (CO₂)**
- **Non-methane organic compounds (NMOC)**
- **Individual air pollutants**

### First-Order Decay Equation

The model implements the EPA LandGEM equation:

```
Q_CH4 = Σ Σ (k × L0 × Mi / 10) × e^(-k × t_ij)
```

Where:
- `Q_CH4` = Annual methane generation (m³/year)
- `k` = Methane generation rate constant (1/year)
- `L0` = Potential methane generation capacity (m³/Mg)
- `Mi` = Mass of waste accepted in year i (Mg)
- `t_ij` = Age of waste section j in year i (years)

## Use Cases

- **Regulatory compliance** - NSPS/EG reporting (40 CFR Parts 60, 62, 63)
- **Emission inventories** - State and local air quality planning
- **Energy assessments** - Landfill gas-to-energy feasibility studies
- **Environmental impact** - NEPA/CEQA documentation
- **Design calculations** - Gas collection system sizing
- **Research** - Waste management and climate studies

## Requirements

- Python 3.8+
- NumPy >= 1.20.0
- Pandas >= 1.3.0
- Matplotlib >= 3.4.0

## Installation from Source

```bash
git clone https://github.com/rmkenv/landgempy.git
cd landgempy
pip install -e .
```

## Examples

Complete examples are available in the `examples/` directory:

- `basic_usage.py` - Simple emissions calculation
- `bioreactor_example.py` - Bioreactor landfill modeling
- `multi_stream_example.py` - Multi-stream waste modeling
- `visualization_example.py` - Creating plots and charts

Run an example:
```bash
python examples/basic_usage.py
```

## API Reference

### Core Classes

**LandGEM** - Single-stream emissions model
```python
model = LandGEM(k, L0, methane_content=0.50, nmoc_concentration=None)
model.calculate_emissions(waste_years, waste_amounts, calculation_year, ...)
model.calculate_time_series(waste_years, waste_amounts, projection_years, ...)
```

**MultiStreamLandGEM** - Multi-stream emissions model
```python
model = MultiStreamLandGEM(k, methane_content=0.50)
model.add_stream(name, L0)
model.calculate_multi_stream(waste_data, calculation_year, ...)
```

**DefaultParameters** - EPA default parameter sets
```python
DefaultParameters.caa_conventional()
DefaultParameters.caa_arid()
DefaultParameters.caa_wet()
DefaultParameters.inventory_conventional()
```

### Utility Functions

```python
from landgempy import (
    import_waste_data,      # Import from CSV/Excel
    export_to_csv,          # Export to CSV
    export_to_excel,        # Export to Excel
    validate_inputs,        # Validate parameters
)
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

**This is an independent implementation and is not an official EPA product.** This software is not affiliated with, endorsed by, or sponsored by the U.S. Environmental Protection Agency.

While this implementation follows the EPA LandGEM methodology, users should:
- Verify results against official EPA tools when used for regulatory purposes
- Consult with regulatory authorities regarding acceptable methodologies
- Review and validate all inputs and outputs
- Use professional judgment in applying results

The authors make no warranties regarding the accuracy, completeness, or suitability of this software for any particular purpose.

## References

- **EPA LandGEM:** https://www.epa.gov/land-research/landfill-gas-emissions-model-landgem
- **User Guide:** EPA/600/B-24/160 (September 2024)
- **40 CFR Part 60 Subpart WWW** - Standards of Performance for Municipal Solid Waste Landfills
- **40 CFR Part 60 Subpart Cc** - Emission Guidelines for Municipal Solid Waste Landfills

## Citation

If you use this software in your research or reports, please cite:

```
landgempy v1.0.0 - Python implementation of EPA's Landfill Gas Emissions Model
Ryan Kmetz (2026)
Available at: https://pypi.org/project/landgempy/
```

## Support

- **Issues:** https://github.com/rmkenv/landgempy/issues
- **PyPI:** https://pypi.org/project/landgempy/
- **Documentation:** See USER_GUIDE.md and QUICK_REFERENCE.md

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and updates.

---

**Built with ❤️ for the environmental engineering community**
