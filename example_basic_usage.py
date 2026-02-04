"""
Basic LandGEM usage example.
"""
import numpy as np
from landgem import LandGEM, DefaultParameters

def main():
    print("="*60)
    print("LandGEM Basic Usage Example")
    print("="*60)

    # Method 1: Use default parameters
    print("\n1. Using EPA CAA Default Parameters:")
    params = DefaultParameters.caa_conventional()
    model = LandGEM(**params)
    print(f"   Model: {model}")

    # Define waste acceptance data
    waste_years = np.arange(2010, 2025)
    waste_amounts = np.array([
        5000, 5200, 5500, 5800, 6000, 6200,
        6500, 6800, 7000, 7200, 7500, 7800,
        8000, 8200, 8500
    ])

    print(f"\n   Waste data: {len(waste_years)} years")
    print(f"   Total waste: {waste_amounts.sum():,.0f} Mg")

    # Calculate emissions for 2030
    results = model.calculate_emissions(
        waste_years=waste_years,
        waste_amounts=waste_amounts,
        calculation_year=2030
    )

    print(f"\n2. Emissions for year 2030:")
    print(f"   Methane (CH₄):    {results['ch4_m3_year']:>15,.0f} m³/year")
    print(f"   Total LFG:        {results['total_lfg_m3_year']:>15,.0f} m³/year")
    print(f"   CO₂:              {results['co2_m3_year']:>15,.0f} m³/year")

    # Calculate time series
    print(f"\n3. Generating 25-year projection...")
    projection_years = np.arange(2025, 2051)
    emissions_df = model.calculate_time_series(
        waste_years=waste_years,
        waste_amounts=waste_amounts,
        projection_years=projection_years
    )

    print(f"   Generated {len(emissions_df)} years of data")
    print(f"\n   Peak methane year: {emissions_df.loc[emissions_df['ch4_m3_year'].idxmax(), 'year']:.0f}")
    print(f"   Peak methane: {emissions_df['ch4_m3_year'].max():,.0f} m³/year")

    # Export results
    emissions_df.to_csv('landgem_basic_output.csv', index=False)
    print(f"\n   Results saved to: landgem_basic_output.csv")

    # Method 2: Custom parameters
    print(f"\n4. Using Custom Parameters:")
    custom_model = LandGEM(
        k=0.045,  # Slightly lower than CAA default
        L0=150,   # Lower potential capacity
        methane_content=0.52  # Slightly higher methane content
    )

    custom_results = custom_model.calculate_emissions(
        waste_years=waste_years,
        waste_amounts=waste_amounts,
        calculation_year=2030
    )

    print(f"   Methane (CH₄):    {custom_results['ch4_m3_year']:>15,.0f} m³/year")

    # Compare results
    diff = ((custom_results['ch4_m3_year'] - results['ch4_m3_year']) / 
            results['ch4_m3_year'] * 100)
    print(f"   Difference from CAA: {diff:+.1f}%")

    print(f"\n{'='*60}")
    print("Example completed successfully!")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
