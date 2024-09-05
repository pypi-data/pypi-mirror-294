import pandas as pd
import numpy as np
from riskinputs import RiskInputs

class Historical:
    """
    Class to calculate Value at Risk (VaR) and Conditional Value at Risk (CVaR) based on historical returns and confidence level

    Parameters
    ----------
    inputs : RiskInputs
        An instance of Risk inputs containing returns and confidence level

    Attributes
    ----------
    historicalVaR : float
        The calculated historical Value at Risk (VaR)
    historicalCVaR : float
        The calculated historical Conditional Value at Risk (CVaR)
    """

    def __init__(self, inputs: RiskInputs) -> None:       
        self.inputs = inputs
        self.returns = pd.Series(inputs.returns)

        self.VaR = self._hvar()
        self.CVaR = self._hcvar()

    def _hvar(self) -> float:
        """
        Calculate the Value at Risk (VaR) at the specified confidence level
        """
        var = np.percentile(self.returns, (1 - self.inputs.confidence_level) * 100)
        return var

    def _hcvar(self) -> float:
        """
        Calculate the Conditional Value at Risk (CVaR) at the specified confidence level
        """
        var = self.VaR
        below_var = self.returns[self.returns <= var]
        return below_var.mean() if len(below_var) > 0 else float('nan')