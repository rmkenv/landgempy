"""
Visualization tools for LandGEM results.
"""
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from typing import Optional, List, Tuple


def plot_emissions_timeseries(
    df: pd.DataFrame,
    title: str = "Landfill Gas Emissions Projection",
    figsize: Tuple[int, int] = (15, 10),
    save_path: Optional[str] = None
) -> plt.Figure:
    """
    Create comprehensive emissions visualization.

    Parameters
    ----------
    df : pd.DataFrame
        Emissions time series from LandGEM.calculate_time_series()
    title : str
        Plot title
    figsize : tuple
        Figure size (width, height)
    save_path : str, optional
        Path to save figure

    Returns
    -------
    matplotlib.figure.Figure
        The created figure
    """
    fig, axes = plt.subplots(2, 2, figsize=figsize)
    fig.suptitle(title, fontsize=16, fontweight='bold')

    # Methane generation
    axes[0, 0].plot(df['year'], df['ch4_m3_year'], 'b-', linewidth=2)
    axes[0, 0].set_title('Methane Generation', fontweight='bold')
    axes[0, 0].set_xlabel('Year')
    axes[0, 0].set_ylabel('CH₄ (m³/year)')
    axes[0, 0].grid(True, alpha=0.3)
    axes[0, 0].ticklabel_format(style='plain', axis='y')

    # Total LFG
    axes[0, 1].plot(df['year'], df['total_lfg_m3_year'], 'g-', linewidth=2)
    axes[0, 1].set_title('Total Landfill Gas Generation', fontweight='bold')
    axes[0, 1].set_xlabel('Year')
    axes[0, 1].set_ylabel('LFG (m³/year)')
    axes[0, 1].grid(True, alpha=0.3)
    axes[0, 1].ticklabel_format(style='plain', axis='y')

    # CO2
    axes[1, 0].plot(df['year'], df['co2_m3_year'], 'r-', linewidth=2)
    axes[1, 0].set_title('Carbon Dioxide Generation', fontweight='bold')
    axes[1, 0].set_xlabel('Year')
    axes[1, 0].set_ylabel('CO₂ (m³/year)')
    axes[1, 0].grid(True, alpha=0.3)
    axes[1, 0].ticklabel_format(style='plain', axis='y')

    # Cumulative CH4
    axes[1, 1].plot(df['year'], df['cumulative_ch4_m3'], 'purple', linewidth=2)
    axes[1, 1].set_title('Cumulative Methane Generation', fontweight='bold')
    axes[1, 1].set_xlabel('Year')
    axes[1, 1].set_ylabel('Cumulative CH₄ (m³)')
    axes[1, 1].grid(True, alpha=0.3)
    axes[1, 1].ticklabel_format(style='plain', axis='y')

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

    return fig


def plot_gas_composition(
    df: pd.DataFrame,
    year: int,
    figsize: Tuple[int, int] = (8, 8)
) -> plt.Figure:
    """
    Create pie chart of gas composition for a specific year.

    Parameters
    ----------
    df : pd.DataFrame
        Emissions time series
    year : int
        Year to visualize
    figsize : tuple
        Figure size

    Returns
    -------
    matplotlib.figure.Figure
    """
    row = df[df['year'] == year]
    if len(row) == 0:
        raise ValueError(f"Year {year} not found in data")

    ch4 = row['ch4_m3_year'].values[0]
    co2 = row['co2_m3_year'].values[0]

    fig, ax = plt.subplots(figsize=figsize)

    sizes = [ch4, co2]
    labels = [f'Methane (CH₄)
{ch4:,.0f} m³/year', 
              f'Carbon Dioxide (CO₂)
{co2:,.0f} m³/year']
    colors = ['#3b82f6', '#ef4444']
    explode = (0.1, 0)

    ax.pie(sizes, explode=explode, labels=labels, colors=colors,
           autopct='%1.1f%%', shadow=True, startangle=90)
    ax.set_title(f'Landfill Gas Composition - {year}', 
                 fontsize=14, fontweight='bold')

    return fig


def plot_multi_stream_comparison(
    df: pd.DataFrame,
    stream_names: List[str],
    figsize: Tuple[int, int] = (12, 6)
) -> plt.Figure:
    """
    Compare emissions from multiple waste streams.

    Parameters
    ----------
    df : pd.DataFrame
        Multi-stream time series data
    stream_names : list
        Names of streams to plot
    figsize : tuple
        Figure size

    Returns
    -------
    matplotlib.figure.Figure
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)

    # Time series comparison
    for stream in stream_names:
        col = f'{stream}_ch4_m3_year'
        if col in df.columns:
            ax1.plot(df['year'], df[col], marker='o', label=stream, linewidth=2)

    ax1.set_title('Methane Generation by Stream', fontweight='bold')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('CH₄ (m³/year)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Stacked area plot
    stream_data = []
    for stream in stream_names:
        col = f'{stream}_ch4_m3_year'
        if col in df.columns:
            stream_data.append(df[col].values)

    if stream_data:
        ax2.stackplot(df['year'], *stream_data, labels=stream_names, alpha=0.8)
        ax2.set_title('Cumulative Stream Contributions', fontweight='bold')
        ax2.set_xlabel('Year')
        ax2.set_ylabel('CH₄ (m³/year)')
        ax2.legend(loc='upper left')
        ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig
