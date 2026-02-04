# LandGEM Python Package - Installation Instructions

## Quick Start

1. Create a new directory for the package:
```bash
mkdir landgem
cd landgem
```

2. Create the package structure:
```bash
mkdir -p landgem/tests/examples
```

3. Copy the downloaded files to their correct locations:
- `landgem_core.py` → `landgem/core.py`
- `landgem_equations.py` → `landgem/equations.py`
- `landgem_parameters.py` → `landgem/parameters.py`
- `landgem_multi_stream.py` → `landgem/multi_stream.py`
- `landgem_validation.py` → `landgem/validation.py`
- `landgem_io.py` → `landgem/io.py`
- `landgem_visualization.py` → `landgem/visualization.py`
- `setup.py` → `setup.py`
- Create `landgem/__init__.py` from the package
- Copy example files to `examples/` directory

4. Install the package:
```bash
pip install -e .
```

## Alternative: Use Complete Package File

If you have `landgem_complete_package.txt`, you can extract all files:

1. Open the file and copy each section to its corresponding filepath
2. Or use the provided script to auto-extract (see below)

## Dependencies

The package requires:
- Python 3.8+
- numpy >= 1.20.0
- pandas >= 1.3.0
- matplotlib >= 3.4.0

Install dependencies:
```bash
pip install numpy pandas matplotlib
```

## Verify Installation

```python
import landgem
from landgem import LandGEM, DefaultParameters

# Create a model
model = LandGEM(k=0.05, L0=170, methane_content=0.50)
print(model)
print("LandGEM installed successfully!")
```

## Run Examples

```bash
cd examples
python basic_usage.py
python bioreactor_example.py
python multi_stream_example.py
```

## Testing

Install pytest and run tests:
```bash
pip install pytest
pytest tests/
```

## Documentation

All modules include comprehensive docstrings. Access help:
```python
from landgem import LandGEM
help(LandGEM)
help(LandGEM.calculate_emissions)
```

## Support

For issues, questions, or contributions:
- GitHub: https://github.com/yourusername/landgem
- Email: your.email@example.com

## References

- EPA LandGEM: https://www.epa.gov/land-research/landfill-gas-emissions-model-landgem
- User Guide: EPA/600/B-24/160
- 40 CFR Part 60 Subpart WWW (NSPS)
- 40 CFR Part 60 Subpart Cc (Emission Guidelines)
