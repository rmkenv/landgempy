"""
EPA default parameters for LandGEM.
"""
from typing import Dict


class DefaultParameters:
    """
    EPA default parameter sets for LandGEM.

    Provides both CAA (Clean Air Act) and Inventory default
    parameter sets for different landfill types.

    CAA defaults are more conservative and typically used for
    regulatory compliance calculations.

    Inventory defaults represent average conditions and are
    suitable for emission inventories when site-specific data
    is unavailable.
    """

    @staticmethod
    def caa_conventional() -> Dict[str, float]:
        """
        CAA defaults for conventional landfills.

        Returns
        -------
        dict
            Parameters: k, L0, methane_content, nmoc_concentration
        """
        return {
            'k': 0.05,
            'L0': 170,
            'methane_content': 0.50,
            'nmoc_concentration': 4000
        }

    @staticmethod
    def caa_arid() -> Dict[str, float]:
        """
        CAA defaults for arid landfills (<25 inches precipitation).

        Returns
        -------
        dict
            Parameters with lower k value for dry conditions
        """
        return {
            'k': 0.02,
            'L0': 170,
            'methane_content': 0.50,
            'nmoc_concentration': 4000
        }

    @staticmethod
    def caa_wet() -> Dict[str, float]:
        """
        CAA defaults for wet/bioreactor landfills.

        Returns
        -------
        dict
            Parameters with high k value for enhanced decomposition
        """
        return {
            'k': 0.7,
            'L0': 170,
            'methane_content': 0.50,
            'nmoc_concentration': 4000
        }

    @staticmethod
    def inventory_conventional() -> Dict[str, float]:
        """
        Inventory defaults for conventional landfills.

        Returns
        -------
        dict
            Average parameters for typical MSW landfills
        """
        return {
            'k': 0.04,
            'L0': 100,
            'methane_content': 0.50,
            'nmoc_concentration': 600
        }

    @staticmethod
    def inventory_conventional_codisposal() -> Dict[str, float]:
        """
        Inventory defaults for conventional landfills with co-disposal.

        Returns
        -------
        dict
            Parameters for landfills accepting industrial waste
        """
        return {
            'k': 0.04,
            'L0': 100,
            'methane_content': 0.50,
            'nmoc_concentration': 2400
        }

    @staticmethod
    def inventory_arid() -> Dict[str, float]:
        """
        Inventory defaults for arid landfills.

        Returns
        -------
        dict
            Parameters for dry climate landfills
        """
        return {
            'k': 0.02,
            'L0': 100,
            'methane_content': 0.50,
            'nmoc_concentration': 600
        }

    @staticmethod
    def inventory_arid_codisposal() -> Dict[str, float]:
        """
        Inventory defaults for arid landfills with co-disposal.

        Returns
        -------
        dict
            Parameters for arid landfills accepting industrial waste
        """
        return {
            'k': 0.02,
            'L0': 100,
            'methane_content': 0.50,
            'nmoc_concentration': 2400
        }

    @staticmethod
    def inventory_wet() -> Dict[str, float]:
        """
        Inventory defaults for wet landfills.

        Returns
        -------
        dict
            Parameters for bioreactor/wet landfills
        """
        return {
            'k': 0.7,
            'L0': 96,
            'methane_content': 0.50,
            'nmoc_concentration': 600
        }

    @staticmethod
    def inventory_wet_codisposal() -> Dict[str, float]:
        """
        Inventory defaults for wet landfills with co-disposal.

        Returns
        -------
        dict
            Parameters for bioreactor landfills with industrial waste
        """
        return {
            'k': 0.7,
            'L0': 96,
            'methane_content': 0.50,
            'nmoc_concentration': 2400
        }

    @staticmethod
    def get_all_defaults() -> Dict[str, Dict[str, float]]:
        """
        Get all available default parameter sets.

        Returns
        -------
        dict
            Dictionary mapping parameter set names to parameters
        """
        return {
            'caa_conventional': DefaultParameters.caa_conventional(),
            'caa_arid': DefaultParameters.caa_arid(),
            'caa_wet': DefaultParameters.caa_wet(),
            'inventory_conventional': DefaultParameters.inventory_conventional(),
            'inventory_conventional_codisposal': DefaultParameters.inventory_conventional_codisposal(),
            'inventory_arid': DefaultParameters.inventory_arid(),
            'inventory_arid_codisposal': DefaultParameters.inventory_arid_codisposal(),
            'inventory_wet': DefaultParameters.inventory_wet(),
            'inventory_wet_codisposal': DefaultParameters.inventory_wet_codisposal(),
        }
