# landgempy User Guide

Complete guide with examples for using the landgempy package.

## Installation

```bash
pip install landgempy
```

## Quick Start

```python
import numpy as np
from landgempy import LandGEM, DefaultParameters

# Create model with EPA default parameters
params = DefaultParameters.caa_conventional()
model = LandGEM(**params)

# Define your waste data
waste_years = np.array([2020, 2021, 2022, 2023, 2024])
waste_amounts = np.array([5000, 5200, 5400, 5600, 5800])  # Mg/year

# Calculate emissions for a specific year
results = model.calculate_emissions(
    waste_years=waste_years,
    waste_amounts=waste_amounts,
    calculation_year=2030
)

print(f"Methane in 2030: {results['ch4_m3_year']:,.0f} m³/year")
print(f"Total LFG: {results['total_lfg_m3_year']:,.0f} m³/year")
print(f"CO₂: {results['co2_m3_year']:,.0f} m³/year")
```

## Table of Contents

1. [Basic Usage](#basic-usage)
2. [EPA Default Parameters](#epa-default-parameters)
3. [Custom Parameters](#custom-parameters)
4. [Time Series Projections](#time-series-projections)
5. [Gas Collection Modeling](#gas-collection-modeling)
6. [Multi-Stream Waste](#multi-stream-waste)
7. [Import/Export Data](#importexport-data)
8. [Visualization](#visualization)
9. [Complete Examples](#complete-examples)

---

## Basic Usage

### Creating a Model

```python
from landgempy import LandGEM

# Method 1: Specify parameters directly
model = LandGEM(
    k=0.05,              # Methane generation rate (1/year)
    L0=170,              # Potential methane capacity (m³/Mg)
    methane_content=0.50  # Methane fraction of LFG
)

# Method 2: Use EPA defaults
from landgempy import DefaultParameters

params = DefaultParameters.caa_conventional()
model = LandGEM(**params)
```

### Single Year Calculation

```python
import numpy as np

# Your waste acceptance data
waste_years = np.array([2015, 2016, 2017, 2018, 2019, 2020])
waste_amounts = np.array([4500, 4800, 5000, 5200, 5500, 5800])

# Calculate emissions for 2025
results = model.calculate_emissions(
    waste_years=waste_years,
    waste_amounts=waste_amounts,
    calculation_year=2025
)

# Access results
print(f"CH₄: {results['ch4_m3_year']:,.0f} m³/year")
print(f"Total LFG: {results['total_lfg_m3_year']:,.0f} m³/year")
print(f"CO₂: {results['co2_m3_year']:,.0f} m³/year")
```

---

## EPA Default Parameters

### Available Parameter Sets

```python
from landgempy import DefaultParameters

# CAA (Clean Air Act) Defaults - Regulatory Use
caa_conv = DefaultParameters.caa_conventional()  # k=0.05, L0=170
caa_arid = DefaultParameters.caa_arid()          # k=0.02, L0=170 (dry climate)
caa_wet = DefaultParameters.caa_wet()            # k=0.7, L0=170 (bioreactor)

# Inventory Defaults - Average Conditions
inv_conv = DefaultParameters.inventory_conventional()  # k=0.04, L0=100
inv_arid = DefaultParameters.inventory_arid()          # k=0.02, L0=100
inv_wet = DefaultParameters.inventory_wet()            # k=0.7, L0=96

# With industrial co-disposal
inv_codisposal = DefaultParameters.inventory_conventional_codisposal()

# See all available defaults
all_defaults = DefaultParameters.get_all_defaults()
for name, params in all_defaults.items():
    print(f"{name}: k={params['k']}, L0={params['L0']}")
```

### Choosing the Right Parameters

```python
# Conventional MSW landfill (most common)
model = LandGEM(**DefaultParameters.caa_conventional())

# Arid climate (<25 inches rain/year)
model = LandGEM(**DefaultParameters.caa_arid())

# Bioreactor/wet landfill
model = LandGEM(**DefaultParameters.caa_wet())

# Landfill accepting industrial waste
model = LandGEM(**DefaultParameters.inventory_conventional_codisposal())
```

---

## Custom Parameters

### Site-Specific Parameters

```python
from landgempy import LandGEM

# Use your own measured parameters
model = LandGEM(
    k=0.045,              # From gas pumping tests
    L0=150,               # From waste composition analysis
    methane_content=0.52, # From gas sampling
    nmoc_concentration=3500  # ppm as hexane
)
```

### Understanding Parameters

**k (Methane Generation Rate)**
- Typical range: 0.02 - 0.7 per year
- 0.02: Arid climate, slow decomposition
- 0.04-0.05: Average conventional landfill
- 0.7: Bioreactor, rapid decomposition

**L0 (Potential Methane Capacity)**
- Typical range: 50 - 200 m³/Mg
- Depends on waste composition
- Higher organic content = higher L0

**Methane Content**
- Typical range: 0.45 - 0.55
- Usually assumed 0.50 (50% CH₄, 50% CO₂)

---

## Time Series Projections

### Generate Multi-Year Projections

```python
import numpy as np
import pandas as pd
from landgempy import LandGEM, DefaultParameters

model = LandGEM(**DefaultParameters.caa_conventional())

# Historical waste acceptance
waste_years = np.arange(2010, 2025)
waste_amounts = np.linspace(4000, 8000, len(waste_years))

# Project emissions from 2025 to 2050
projection_years = np.arange(2025, 2051)

df = model.calculate_time_series(
    waste_years=waste_years,
    waste_amounts=waste_amounts,
    projection_years=projection_years
)

# View results
print(df.head())
print(f"\nColumns: {list(df.columns)}")

# Find peak year
peak_idx = df['ch4_m3_year'].idxmax()
peak_year = df.loc[peak_idx, 'year']
peak_value = df.loc[peak_idx, 'ch4_m3_year']

print(f"\nPeak methane: {peak_value:,.0f} m³/year in {peak_year:.0f}")

# Total cumulative emissions
total_ch4 = df['cumulative_ch4_m3'].iloc[-1]
print(f"Total CH₄ (2025-2050): {total_ch4:,.0f} m³")
```

### Save Results

```python
# Save to CSV
df.to_csv('emissions_projection.csv', index=False)

# Save to Excel
from landgempy import export_to_excel
export_to_excel(df, 'emissions_projection.xlsx')
```

---

## Gas Collection Modeling

### Model Gas Collection System

```python
from landgempy import LandGEM, DefaultParameters

model = LandGEM(**DefaultParameters.caa_conventional())

waste_years = np.array([2015, 2016, 2017, 2018, 2019, 2020])
waste_amounts = np.array([5000, 5200, 5400, 5600, 5800, 6000])

# Model with 75% collection efficiency
results = model.calculate_emissions(
    waste_years=waste_years,
    waste_amounts=waste_amounts,
    calculation_year=2030,
    collection_efficiency=0.75  # 75% of gas is collected
)

print(f"Total CH₄ generated: {results['ch4_m3_year']:,.0f} m³/year")
print(f"CH₄ collected: {results['ch4_collected_m3_year']:,.0f} m³/year")
print(f"CH₄ to atmosphere: {results['ch4_m3_year'] - results['ch4_collected_m3_year']:,.0f} m³/year")
```

### Time Series with Collection

```python
# Project with gas collection
projection_years = np.arange(2025, 2046)

df = model.calculate_time_series(
    waste_years=waste_years,
    waste_amounts=waste_amounts,
    projection_years=projection_years,
    collection_efficiency=0.85  # 85% efficient system
)

# Calculate energy potential
# Assume 1000 BTU/cf and 35.3147 cf/m³
total_collected = df['ch4_collected_m3_year'].sum()
energy_btu = total_collected * 35.3147 * 1000
energy_mwh = energy_btu / 3412141  # BTU to MWh

print(f"Total CH₄ collected: {total_collected:,.0f} m³")
print(f"Energy potential: {energy_mwh:,.0f} MWh")
```

---

## Multi-Stream Waste

### Model Different Waste Types

```python
from landgempy import MultiStreamLandGEM
import numpy as np

# Create multi-stream model
model = MultiStreamLandGEM(
    k=0.05,
    methane_content=0.50
)

# Define waste streams with different L0 values
model.add_stream('msw', L0=170)              # Municipal solid waste
model.add_stream('organic', L0=200)          # Food & yard waste
model.add_stream('construction', L0=50)       # C&D debris
model.add_stream('industrial', L0=100)        # Industrial waste

# Waste acceptance data by stream
years = np.arange(2015, 2025)

waste_data = {
    'msw': {
        'years': years,
        'amounts': np.array([5000, 5200, 5400, 5600, 5800, 
                            6000, 6200, 6400, 6600, 6800])
    },
    'organic': {
        'years': years,
        'amounts': np.array([1000, 1100, 1200, 1300, 1400,
                            1500, 1600, 1700, 1800, 1900])
    },
    'construction': {
        'years': years,
        'amounts': np.array([800, 850, 900, 950, 1000,
                            1050, 1100, 1150, 1200, 1250])
    },
    'industrial': {
        'years': years,
        'amounts': np.array([600, 620, 640, 660, 680,
                            700, 720, 740, 760, 780])
    }
}

# Calculate total emissions
results = model.calculate_multi_stream(
    waste_data=waste_data,
    calculation_year=2030
)

print(f"Total CH₄: {results['ch4_m3_year']:,.0f} m³/year")

# See breakdown by stream
for stream_name, stream_results in results['streams'].items():
    ch4 = stream_results['ch4_m3_year']
    pct = (ch4 / results['ch4_m3_year']) * 100
    print(f"  {stream_name}: {ch4:,.0f} m³/year ({pct:.1f}%)")
```

### Multi-Stream Time Series

```python
# Generate time series for all streams
projection_years = np.arange(2025, 2041)

df = model.calculate_time_series_multi_stream(
    waste_data=waste_data,
    projection_years=projection_years
)

print(df.head())

# Each stream has its own column
print(f"\nAvailable columns: {list(df.columns)}")
```

---

## Import/Export Data

### Import Waste Data from CSV

```python
from landgempy import import_waste_data

# CSV file format:
# year,waste_mg
# 2020,5000
# 2021,5200
# 2022,5400

waste_years, waste_amounts = import_waste_data(
    'waste_data.csv',
    year_column='year',
    amount_column='waste_mg'
)

# Use with model
model = LandGEM(**DefaultParameters.caa_conventional())
results = model.calculate_emissions(
    waste_years=waste_years,
    waste_amounts=waste_amounts,
    calculation_year=2030
)
```

### Import from Excel

```python
waste_years, waste_amounts = import_waste_data(
    'waste_data.xlsx',
    year_column='Year',
    amount_column='Waste_Tons'
)
```

### Export Results

```python
from landgempy import export_to_csv, export_to_excel

# Calculate time series
df = model.calculate_time_series(
    waste_years=waste_years,
    waste_amounts=waste_amounts,
    projection_years=np.arange(2025, 2051)
)

# Export to CSV
export_to_csv(df, 'results.csv')

# Export to Excel with metadata
export_to_excel(df, 'results.xlsx', sheet_name='Emissions')
```

---

## Visualization

### Basic Emissions Plot

```python
from landgempy.visualization import plot_emissions_timeseries
import matplotlib.pyplot as plt

# Calculate time series
df = model.calculate_time_series(
    waste_years=waste_years,
    waste_amounts=waste_amounts,
    projection_years=np.arange(2010, 2051)
)

# Create comprehensive plot
fig = plot_emissions_timeseries(
    df,
    title="Landfill Emissions Projection",
    save_path='emissions_plot.png'
)

plt.show()
```

### Gas Composition Pie Chart

```python
from landgempy.visualization import plot_gas_composition

# Plot composition for specific year
fig = plot_gas_composition(df, year=2030)
plt.savefig('composition_2030.png', dpi=300, bbox_inches='tight')
plt.show()
```

### Multi-Stream Comparison

```python
from landgempy.visualization import plot_multi_stream_comparison

# Calculate multi-stream data first
df_multi = model.calculate_time_series_multi_stream(
    waste_data=waste_data,
    projection_years=np.arange(2025, 2041)
)

# Plot comparison
fig = plot_multi_stream_comparison(
    df_multi,
    stream_names=['msw', 'organic', 'construction', 'industrial']
)

plt.savefig('stream_comparison.png', dpi=300, bbox_inches='tight')
plt.show()
```

### Custom Plotting

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 6))

# Plot methane over time
ax.plot(df['year'], df['ch4_m3_year'], 
        linewidth=2, color='blue', label='CH₄')

ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Methane (m³/year)', fontsize=12)
ax.set_title('Methane Generation Projection', fontsize=14, fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('my_plot.png', dpi=300)
plt.show()
```

---

## Complete Examples

### Example 1: Basic Landfill Assessment

```python
import numpy as np
from landgempy import LandGEM, DefaultParameters

# Setup
model = LandGEM(**DefaultParameters.caa_conventional())

# 10 years of waste data
waste_years = np.arange(2015, 2025)
waste_amounts = np.array([4500, 4800, 5000, 5200, 5500, 
                         5800, 6000, 6200, 6500, 6800])

# Calculate for current year
results = model.calculate_emissions(
    waste_years=waste_years,
    waste_amounts=waste_amounts,
    calculation_year=2025
)

print("=== 2025 Emissions Assessment ===")
print(f"Methane: {results['ch4_m3_year']:,.0f} m³/year")
print(f"Total LFG: {results['total_lfg_m3_year']:,.0f} m³/year")
print(f"CO₂: {results['co2_m3_year']:,.0f} m³/year")

# 25-year projection
projection_years = np.arange(2025, 2051)
df = model.calculate_time_series(
    waste_years=waste_years,
    waste_amounts=waste_amounts,
    projection_years=projection_years
)

# Save results
df.to_csv('landfill_projection.csv', index=False)
print("\n✓ Results saved to landfill_projection.csv")
```

### Example 2: Gas Collection System Design

```python
import numpy as np
from landgempy import LandGEM, DefaultParameters

model = LandGEM(**DefaultParameters.caa_conventional())

# Historical data
waste_years = np.arange(2010, 2025)
waste_amounts = np.linspace(4000, 7000, len(waste_years))

# Project with different collection efficiencies
projection_years = np.arange(2025, 2046)

print("=== Gas Collection System Analysis ===\n")

for efficiency in [0.60, 0.75, 0.85, 0.95]:
    df = model.calculate_time_series(
        waste_years=waste_years,
        waste_amounts=waste_amounts,
        projection_years=projection_years,
        collection_efficiency=efficiency
    )
    
    total_generated = df['ch4_m3_year'].sum()
    total_collected = df['ch4_collected_m3_year'].sum()
    
    print(f"{efficiency*100:.0f}% Efficiency:")
    print(f"  Total Generated: {total_generated:,.0f} m³")
    print(f"  Total Collected: {total_collected:,.0f} m³")
    print(f"  Energy (MWh): {total_collected * 35.3147 * 1000 / 3412141:,.0f}")
    print()
```

### Example 3: Parameter Sensitivity Analysis

```python
import numpy as np
import matplotlib.pyplot as plt
from landgempy import LandGEM

# Base data
waste_years = np.array([2020, 2021, 2022])
waste_amounts = np.array([5000, 5000, 5000])
projection_years = np.arange(2023, 2051)

# Test different k values
k_values = [0.02, 0.04, 0.05, 0.07, 0.10]

plt.figure(figsize=(12, 6))

for k in k_values:
    model = LandGEM(k=k, L0=170, methane_content=0.50)
    df = model.calculate_time_series(
        waste_years=waste_years,
        waste_amounts=waste_amounts,
        projection_years=projection_years
    )
    plt.plot(df['year'], df['ch4_m3_year'], label=f'k={k}', linewidth=2)

plt.xlabel('Year', fontsize=12)
plt.ylabel('CH₄ (m³/year)', fontsize=12)
plt.title('Effect of k Value on Methane Generation', fontsize=14, fontweight='bold')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('sensitivity_analysis.png', dpi=300)
plt.show()
```

### Example 4: Regulatory Compliance Report

```python
import numpy as np
from landgempy import LandGEM, DefaultParameters
from datetime import datetime

# Use CAA defaults for regulatory compliance
model = LandGEM(**DefaultParameters.caa_conventional())

# Site data
waste_years = np.arange(2015, 2025)
waste_amounts = np.array([4800, 5000, 5200, 5400, 5600, 
                         5800, 6000, 6200, 6400, 6600])

# Calculate for compliance year
results = model.calculate_emissions(
    waste_years=waste_years,
    waste_amounts=waste_amounts,
    calculation_year=2025,
    include_nmoc=True
)

# Generate report
report = f"""
LANDFILL GAS EMISSIONS ESTIMATE
Generated: {datetime.now().strftime('%Y-%m-%d')}

MODEL PARAMETERS:
- Method: EPA LandGEM v3.02
- k value: 0.05 /year (CAA default)
- L0 value: 170 m³/Mg (CAA default)
- Methane content: 50%
- NMOC: 4000 ppmv as hexane

WASTE IN PLACE (2015-2024):
- Total waste accepted: {waste_amounts.sum():,.0f} Mg
- Years of operation: {len(waste_years)}

ESTIMATED EMISSIONS (2025):
- Methane (CH₄): {results['ch4_m3_year']:,.0f} m³/year
- Total LFG: {results['total_lfg_m3_year']:,.0f} m³/year
- Carbon Dioxide (CO₂): {results['co2_m3_year']:,.0f} m³/year
- NMOC: {results['nmoc_mg_year']:.2f} Mg/year
"""

print(report)

# Save to file
with open('compliance_report.txt', 'w') as f:
    f.write(report)
```

---

## API Reference Quick Guide

### LandGEM Class

```python
model = LandGEM(k, L0, methane_content=0.50, nmoc_concentration=None)
```

**Methods:**
- `calculate_emissions()` - Single year calculation
- `calculate_time_series()` - Multi-year projection
- `calculate_waste_in_place()` - Waste in place calculation

### MultiStreamLandGEM Class

```python
model = MultiStreamLandGEM(k, methane_content=0.50)
model.add_stream(name, L0)
```

**Methods:**
- `calculate_multi_stream()` - Single year, all streams
- `calculate_time_series_multi_stream()` - Time series, all streams

### DefaultParameters

```python
DefaultParameters.caa_conventional()
DefaultParameters.caa_arid()
DefaultParameters.caa_wet()
DefaultParameters.inventory_conventional()
# ... and more
```

### Utility Functions

```python
from landgempy import (
    import_waste_data,
    export_to_csv,
    export_to_excel,
    validate_inputs
)
```

---

## Tips and Best Practices

1. **Always use EPA defaults** unless you have site-specific data
2. **CAA defaults** are more conservative (regulatory compliance)
3. **Inventory defaults** for emission inventories
4. **Test on TestPyPI first** when developing
5. **Save your projections** to CSV for documentation
6. **Include metadata** in your exports

## Getting Help

- PyPI: https://pypi.org/project/landgempy/
- GitHub: https://github.com/rmkenv/landgempy
- EPA LandGEM: https://www.epa.gov/land-research/landfill-gas-emissions-model-landgem

## Citation

If using this package in research or reports:

```
landgempy v1.0.0 - Python implementation of EPA's Landfill Gas Emissions Model
Based on EPA LandGEM v3.02 methodology
NOT AN OFFICAL EPA PRODUCT 
```
