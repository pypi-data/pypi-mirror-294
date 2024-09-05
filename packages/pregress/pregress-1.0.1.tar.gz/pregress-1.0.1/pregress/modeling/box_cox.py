import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import boxcox
import statsmodels.api as sm
import statsmodels.formula.api as smf

def box_cox(model):
    """
    Perform a Box-Cox transformation on the response variable of a given statsmodels regression results object,
    output a plot of the log-likelihood as a function of lambda, the rounded lambda, and the actual lambda value.

    Args:
        model (statsmodels.regression.linear_model.RegressionResultsWrapper): A fitted statsmodels regression model.

    Returns:
        tuple: The rounded lambda (closest to -1, -0.5, 0, 0.5, 1, or 2) and the actual lambda value.
    """
    # Extract the response variable
    y = model.model.endog
    
    # Perform the Box-Cox transformation
    y_transformed, fitted_lambda = boxcox(y)
    
    # Define the possible rounded lambda values
    possible_lambdas = np.array([-1, -0.5, 0, 0.5, 1, 2])
    
    # Find the closest rounded lambda value
    rounded_lambda = possible_lambdas[np.argmin(np.abs(possible_lambdas - fitted_lambda))]
    
    # Plot the log-likelihood as a function of lambda
    lambdas = np.linspace(-2, 3, 100)
    log_likelihood = [boxcox(y, lmbda=lmbda)[1] for lmbda in lambdas]
    
    plt.figure(figsize=(10, 6))
    plt.plot(lambdas, log_likelihood, label='Log-Likelihood')
    plt.axvline(fitted_lambda, color='r', linestyle='--', label=f'Fitted Lambda: {fitted_lambda:.4f}')
    plt.axvline(rounded_lambda, color='g', linestyle='--', label=f'Rounded Lambda: {rounded_lambda}')
    plt.xlabel('Lambda')
    plt.ylabel('Log-Likelihood')
    plt.title('Box-Cox Transformation Log-Likelihood')
    plt.legend()
    plt.grid(True)
    plt.show()

    return rounded_lambda, fitted_lambda

# Example usage:
# Assuming 'model' is a fitted statsmodels regression model
# model = smf.ols('Y ~ X', data=data).fit()
# rounded_lambda, fitted_lambda = boxcox_transform(model)
# print(f"Rounded Lambda: {rounded_lambda}")
# print(f"Fitted Lambda: {fitted_lambda}")
