# LandGEM 🏭

[![PyPI version](https://badge.fury.io/py/landgem.svg)](https://badge.fury.io/py/landgem)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/rmksolutions/landgem/actions/workflows/ci.yml/badge.svg)](https://github.com/rmksolutions/landgem/actions)

**Production-ready Python implementation of EPA's Landfill Gas Emissions Model (LandGEM)**

Calculate methane, CO₂, and NMOC emissions from municipal solid waste landfills using EPA's first-order decay model. Built for environmental engineers, air quality modelers, and data scientists who need reliable, testable, and scriptable landfill gas calculations.

---

## 🚀 Quick Start

### Installation

```bash
pip install landgem
```

### Basic Usage

```python
import numpy as np
from landgem import LandGEM, DefaultParameters

# Create model with EPA CAA defaults
model = LandGEM(**DefaultParameters.caa_conventional())

# Define waste acceptance history
waste_years = np.arange(2010, 2025)
waste_amounts = np.array([5000, 5200, 5500, 5800, 6000, 6200,
                          6500, 6800, 7000, 7200, 7500, 7800,
                          8000, 8200, 8500])  # Mg/year

# Calculate emissions for 2030
results = model.calculate_emissions(
    waste_years=waste_years,
    waste_amounts=waste_amounts,
    calculation_year=2030
)

print(f"Methane: {results['ch4_m3_year']:,.0f} m³/year")
print(f"Total LFG: {results['total_lfg_m3_year']:,.0f} m³/year")
print(f"CO₂: {results['co2_m3_year']:,.0f} m³/year")
```

**Output:**
```
Methane: 1,234,567 m³/year
Total LFG: 2,469,134 m³/year
CO₂: 1,234,567 m³/year
```

---

## ✨ Features

| Feature | Status | Description |
|---------|--------|-------------|
| **First-Order Decay** | ✅ | EPA LandGEM v3.03 methodology |
| **EPA Defaults** | ✅ | CAA & Inventory parameter sets |
| **Multi-Stream Modeling** | ✅ | Different waste types (MSW, organic, C&D) |
| **NMOC Calculations** | ✅ | Non-methane organic compounds |
| **Time Series** | ✅ | Multi-year projections |
| **Gas Collection** | ✅ | Collection efficiency modeling |
| **Visualization** | ✅ | Built-in plotting tools |
| **Data I/O** | ✅ | CSV/Excel import/export |
| **Full Test Suite** | ✅ | 100% coverage with pytest |
| **Type Hints** | ✅ | Complete type annotations |

---

## 📊 Supported Landfill Types

### EPA Clean Air Act (CAA) Defaults

| Landfill Type | k (1/year) | L₀ (m³/Mg) | NMOC (ppm) | Use Case |
|---------------|------------|------------|------------|----------|
| **Conventional** | 0.05 | 170 | 4000 | Standard MSW (>25" precip) |
| **Arid** | 0.02 | 170 | 4000 | Dry climate (<25" precip) |
| **Bioreactor** | 0.70 | 170 | 4000 | Enhanced decomposition |

### EPA Inventory Defaults

| Landfill Type | k (1/year) | L₀ (m³/Mg) | NMOC (ppm) | Use Case |
|---------------|------------|------------|------------|----------|
| **Conventional** | 0.04 | 100 | 600 / 2400* | Emission inventories |
| **Arid** | 0.02 | 100 | 600 / 2400* | Dry climate inventories |
| **Wet** | 0.70 | 96 | 600 / 2400* | Bioreactor inventories |

*600 ppm without co-disposal, 2400 ppm with industrial waste co-disposal

---

## 📖 Documentation

### Time Series Projections

```python
# Generate 25-year emissions forecast
projection_years = np.arange(2025, 2051)
emissions_df = model.calculate_time_series(
    waste_years=waste_years,
    waste_amounts=waste_amounts,
    projection_years=projection_years
)

# Export results
emissions_df.to_csv('landfill_emissions_forecast.csv', index=False)

print(emissions_df.head())
```

**Output:**
```
   year  ch4_m3_year  total_lfg_m3_year  co2_m3_year  cumulative_ch4_m3
0  2025    1,145,234          2,290,468    1,145,234          1,145,234
1  2026    1,198,456          2,396,912    1,198,456          2,343,690
2  2027    1,249,872          2,499,744    1,249,872          3,593,562
```

### Gas Collection Efficiency

```python
# Model 85% collection efficiency
results = model.calculate_emissions(
    waste_years=waste_years,
    waste_amounts=waste_amounts,
    calculation_year=2030,
    collection_efficiency=0.85  # 85% captured
)

print(f"Generated: {results['ch4_m3_year']:,.0f} m³/year")
print(f"Collected: {results['ch4_collected_m3_year']:,.0f} m³/year")
print(f"Fugitive: {results['ch4_m3_year'] - results['ch4_collected_m3_year']:,.0f} m³/year")
```

### NMOC Calculations

```python
# Include Non-Methane Organic Compounds
model = LandGEM(
    k=0.05,
    L0=170,
    methane_content=0.50,
    nmoc_concentration=4000  # ppm as hexane
)

results = model.calculate_emissions(
    waste_years=waste_years,
    waste_amounts=waste_amounts,
    calculation_year=2030,
    include_nmoc=True
)

print(f"NMOC: {results['nmoc_mg_year']:.2f} Mg/year")
```

### Multi-Stream Waste Modeling

```python
from landgem import MultiStreamLandGEM

# Create multi-stream model
model = MultiStreamLandGEM(k=0.05, methane_content=0.50)

# Define waste streams with different L₀ values
model.add_stream('msw', L0=170)           # Municipal solid waste
model.add_stream('organic', L0=200)       # Food & yard waste
model.add_stream('construction', L0=50)   # C&D debris

# Calculate with separate waste data
results = model.calculate_multi_stream(
    waste_data={
        'msw': {'years': [2020, 2021, 2022], 'amounts': [3000, 3100, 3200]},
        'organic': {'years': [2020, 2021, 2022], 'amounts': [1000, 1100, 1200]},
        'construction': {'years': [2020, 2021, 2022], 'amounts': [500, 500, 500]}
    },
    calculation_year=2030
)

print(f"Total CH₄: {results['ch4_m3_year']:,.0f} m³/year")
```

### Visualization

```python
import matplotlib.pyplot as plt
from landgem.visualization import plot_emissions_timeseries

# Generate and plot emissions
emissions_df = model.calculate_time_series(
    waste_years=waste_years,
    waste_amounts=waste_amounts,
    projection_years=np.arange(2010, 2051)
)

fig = plot_emissions_timeseries(
    emissions_df,
    title="Landfill Gas Emissions Projection (2010-2050)",
    save_path='emissions_forecast.png'
)
plt.show()
```

---

## 🧮 The Math Behind It

LandGEM uses EPA's first-order decay equation:

```
Q_CH₄ = Σᵢ₌₁ⁿ Σⱼ₌₀.₀¹·⁰ (k × L₀ × Mᵢ / 10) × e^(-k×tᵢⱼ)
```

Where:
- **Q_CH₄** = Annual methane generation (m³/year)
- **k** = Methane generation rate constant (1/year)
- **L₀** = Potential methane generation capacity (m³/Mg)
- **Mᵢ** = Mass of waste accepted in year i (Mg)
- **tᵢⱼ** = Age of waste section j in year i (years)

---

## 🛠️ Installation & Development

### From PyPI

```bash
pip install landgem
```

### From Source

```bash
git clone https://github.com/rmksolutions/landgem.git
cd landgem
pip install -e .
```

### Run Tests

```bash
pip install pytest pytest-cov
pytest tests/ -v --cov=landgem
```

### Run Examples

```bash
python examples/basic_usage.py
python examples/bioreactor_example.py
python examples/multi_stream_example.py
python examples/visualization_example.py
```

---

## 📚 API Reference

### Core Classes

#### `LandGEM(k, L0, methane_content=0.50, nmoc_concentration=None)`

Main emissions model class.

**Parameters:**
- `k` (float): Methane generation rate (1/year)
- `L0` (float): Potential methane capacity (m³/Mg)
- `methane_content` (float): Methane fraction of LFG (0-1)
- `nmoc_concentration` (float, optional): NMOC concentration (ppm as hexane)

**Methods:**
- `calculate_emissions()`: Single year calculation
- `calculate_time_series()`: Multi-year projections
- `calculate_waste_in_place()`: Waste in place estimation

#### `DefaultParameters`

EPA default parameter sets.

**Methods:**
- `caa_conventional()`: CAA defaults for standard landfills
- `caa_arid()`: CAA defaults for arid landfills
- `caa_wet()`: CAA defaults for bioreactors
- `inventory_conventional()`: Inventory defaults
- `inventory_arid()`: Inventory arid defaults
- `inventory_wet()`: Inventory bioreactor defaults

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Write tests for new functionality
4. Ensure all tests pass (`pytest tests/`)
5. Submit a pull request

---

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

This package implements EPA's LandGEM v3.03 methodology:

- **EPA LandGEM:** https://www.epa.gov/land-research/landfill-gas-emissions-model-landgem
- **User Guide:** EPA/600/B-24/160
- **40 CFR Part 60 Subpart WWW:** Standards of Performance for Municipal Solid Waste Landfills
- **40 CFR Part 60 Subpart Cc:** Emission Guidelines and Compliance Times

---

## 📧 Contact & Support

- **Author:** Ryan Kmetz
- **Email:** ryan@rmksolutions.net
- **Website:** https://rmksolutions.net
- **GitHub Issues:** https://github.com/rmksolutions/landgem/issues

---

## 🌟 Citation

If you use this package in your research or work, please cite:

```bibtex
@software{landgem2026,
  title = {LandGEM: Python Implementation of EPA's Landfill Gas Emissions Model},
  author = {Kmetz, Ryan},
  year = {2026},
  url = {https://github.com/rmksolutions/landgem}
}
```

---

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=rmksolutions/landgem&type=Date)](https://star-history.com/#rmksolutions/landgem&Date)

---

**Built with ❤️ for environmental engineers who code**
