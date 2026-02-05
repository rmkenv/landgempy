# landgempy Quick Reference

## Installation
```bash
pip install landgempy
```

## Basic Usage

### 1. Simple Single Calculation
```python
import numpy as np
from landgempy import LandGEM, DefaultParameters

# Create model
model = LandGEM(**DefaultParameters.caa_conventional())

# Your data
waste_years = np.array([2020, 2021, 2022, 2023, 2024])
waste_amounts = np.array([5000, 5200, 5400, 5600, 5800])

# Calculate
results = model.calculate_emissions(
    waste_years=waste_years,
    waste_amounts=waste_amounts,
    calculation_year=2030
)

print(f"Methane: {results['ch4_m3_year']:,.0f} m³/year")
```

### 2. Time Series (25-year projection)
```python
# Project 2025-2050
projection_years = np.arange(2025, 2051)

df = model.calculate_time_series(
    waste_years=waste_years,
    waste_amounts=waste_amounts,
    projection_years=projection_years
)

# Save results
df.to_csv('emissions.csv', index=False)

# Find peak year
peak_year = df.loc[df['ch4_m3_year'].idxmax(), 'year']
print(f"Peak year: {peak_year}")
```

### 3. With Gas Collection (75% efficiency)
```python
results = model.calculate_emissions(
    waste_years=waste_years,
    waste_amounts=waste_amounts,
    calculation_year=2030,
    collection_efficiency=0.75
)

print(f"Generated: {results['ch4_m3_year']:,.0f} m³/year")
print(f"Collected: {results['ch4_collected_m3_year']:,.0f} m³/year")
```

### 4. Multi-Stream Waste
```python
from landgempy import MultiStreamLandGEM

model = MultiStreamLandGEM(k=0.05, methane_content=0.50)

# Add streams
model.add_stream('msw', L0=170)
model.add_stream('organic', L0=200)

# Data
waste_data = {
    'msw': {
        'years': np.array([2020, 2021, 2022]),
        'amounts': np.array([5000, 5200, 5400])
    },
    'organic': {
        'years': np.array([2020, 2021, 2022]),
        'amounts': np.array([1000, 1100, 1200])
    }
}

# Calculate
results = model.calculate_multi_stream(
    waste_data=waste_data,
    calculation_year=2030
)

print(f"Total: {results['ch4_m3_year']:,.0f} m³/year")
for stream, data in results['streams'].items():
    print(f"  {stream}: {data['ch4_m3_year']:,.0f}")
```

### 5. Import Data from CSV
```python
from landgempy import import_waste_data

waste_years, waste_amounts = import_waste_data(
    'waste_data.csv',
    year_column='year',
    amount_column='waste_mg'
)
```

### 6. Visualize Results
```python
from landgempy.visualization import plot_emissions_timeseries
import matplotlib.pyplot as plt

fig = plot_emissions_timeseries(df, title="My Landfill")
plt.savefig('plot.png')
plt.show()
```

## EPA Default Parameters

```python
from landgempy import DefaultParameters

# Most common - use this for regulatory compliance
DefaultParameters.caa_conventional()  # k=0.05, L0=170

# Other options
DefaultParameters.caa_arid()          # k=0.02 (dry climate)
DefaultParameters.caa_wet()           # k=0.7 (bioreactor)
DefaultParameters.inventory_conventional()  # k=0.04, L0=100
```

## Common Workflows

### Compliance Report
```python
# EPA defaults for compliance
model = LandGEM(**DefaultParameters.caa_conventional())

results = model.calculate_emissions(
    waste_years=waste_years,
    waste_amounts=waste_amounts,
    calculation_year=2025,
    include_nmoc=True
)

print(f"NMOC: {results['nmoc_mg_year']:.2f} Mg/year")
```

### Energy Assessment
```python
# Project with collection
df = model.calculate_time_series(
    waste_years=waste_years,
    waste_amounts=waste_amounts,
    projection_years=np.arange(2025, 2046),
    collection_efficiency=0.85
)

# Energy potential (assumes 1000 BTU/cf, 35.3147 cf/m³)
total_ch4 = df['ch4_collected_m3_year'].sum()
energy_mwh = total_ch4 * 35.3147 * 1000 / 3412141

print(f"20-year energy: {energy_mwh:,.0f} MWh")
```

### Parameter Comparison
```python
import matplotlib.pyplot as plt

for k in [0.02, 0.04, 0.05, 0.07]:
    model = LandGEM(k=k, L0=170, methane_content=0.50)
    df = model.calculate_time_series(
        waste_years=waste_years,
        waste_amounts=waste_amounts,
        projection_years=np.arange(2025, 2051)
    )
    plt.plot(df['year'], df['ch4_m3_year'], label=f'k={k}')

plt.legend()
plt.xlabel('Year')
plt.ylabel('CH₄ (m³/year)')
plt.show()
```

## Key Parameters

| Parameter | Units | Typical Range | Notes |
|-----------|-------|---------------|-------|
| k | 1/year | 0.02 - 0.7 | Decomposition rate |
| L0 | m³/Mg | 50 - 200 | Gas generation potential |
| methane_content | fraction | 0.45 - 0.55 | Usually 0.50 |
| collection_efficiency | fraction | 0.60 - 0.95 | System dependent |

## Results Dictionary Keys

```python
results = {
    'ch4_m3_year': ...,              # Methane (m³/year)
    'total_lfg_m3_year': ...,        # Total LFG (m³/year)
    'co2_m3_year': ...,              # CO₂ (m³/year)
    'ch4_collected_m3_year': ...,    # Collected CH₄
    'lfg_collected_m3_year': ...,    # Collected LFG
    'nmoc_mg_year': ...              # NMOC (if enabled)
}
```

## DataFrame Columns

```python
df.columns:
# 'year', 'ch4_m3_year', 'total_lfg_m3_year', 'co2_m3_year',
# 'cumulative_ch4_m3', 'cumulative_lfg_m3'
# + collection columns if efficiency > 0
```

## Tips

✓ Use `DefaultParameters.caa_conventional()` for most cases  
✓ Always project at least 20 years  
✓ Save results to CSV for documentation  
✓ Test with small datasets first  
✓ Check peak year - usually 5-15 years after last waste  

## Common Errors

**"waste_years and waste_amounts must have same length"**
→ Arrays must match in size

**"k must be positive"**
→ Check your k value (should be 0.02-0.7)

**"methane_content must be between 0 and 1"**
→ Use fraction (0.50), not percent (50)

## Need More Help?

📖 Full Guide: [USER_GUIDE.md](USER_GUIDE.md)  
🐙 GitHub: https://github.com/rmkenv/landgempy  
📦 PyPI: https://pypi.org/project/landgempy/
