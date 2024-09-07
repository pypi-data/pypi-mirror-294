'''
# GemPy 3: gravity inversion for normal fault model

Based on `GemPy3_Tutorial_XX_fault_gravity.ipynb`

For installation, see the first notebook - here only repeated if running on Google Colab.
'''

# Importing GemPy and viewer
import gempy as gp
import gempy_viewer as gpv
from gempy.core.data.enumerators import ExampleModel
from gempy_engine.core.backend_tensor import BackendTensor
# %% md
# And for some additional steps in this notebook:
# %%
# Auxiliary libraries
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pandas as pd
# %% md
# Packages for inversion
# %%
import torch
import pyro
import pyro.distributions as dist
from pyro.infer import MCMC, NUTS, Predictive
import arviz as az
from _aux_funcs import plot_model_and_grav

plt.rcParams['text.usetex'] = True

# %% md
## Set up Pyro model
geo_model = gp.generate_example_model(ExampleModel.ONE_FAULT_GRAVITY, compute_model=True)


device_loc = pd.DataFrame()
# x_vals = np.arange(20, 191, 10)
x_vals = np.linspace(20, 191, 6)

device_loc['X'] = x_vals
device_loc['Y'] = np.zeros_like(x_vals)
device_loc['Z'] = 0  # Add a Z-coordinate

resolution = geo_model.grid.regular_grid.resolution

fig = plot_model_and_grav(
    blocks=geo_model.solutions.raw_arrays.lith_block.reshape(resolution),
    grav=geo_model.solutions.gravity.detach().numpy(),
    x_vals=x_vals,
    input_data=geo_model.surface_points_copy.df
)
fig.show()


# %%
# Define hyperparameters for the Bayesian geological model
# Use first: lateral position of fault only
fault_1_x = torch.tensor(80.)
fault_2_x = torch.tensor(110.)


# %% md
### Probabilistic model

# @Miguel: how to adjust for input points as stochastic variables?


BackendTensor.change_backend_gempy(
    engine_backend=gp.data.AvailableBackends.PYTORCH,
    use_gpu=True,
    dtype="float32"
)

def gaussian_kernel(locations, length_scale, variance):
    import torch
    # Compute the squared Euclidean distance between each pair of points
    locations = torch.tensor(locations.values, dtype=torch.float32)
    distance_squared = torch.cdist(locations, locations, p=2.).pow(2.)
    # Compute the covariance matrix using the Gaussian kernel
    covariance_matrix = variance * torch.exp(-0.5 * distance_squared / length_scale ** 2)
    return covariance_matrix


# Configure the Pyro model for geological data
# * These are density values for the geological model
densities_tensor = BackendTensor.t.array([2., 2., 3., 2.])
prior_tensor = densities_tensor  # * This is the prior tensor

covariance_matrix = gaussian_kernel(  # * This is the likelihood function
    locations=device_loc,
    length_scale=torch.tensor(10, dtype=torch.float32),  # ! These are m!
    variance=torch.tensor(.5 ** 2, dtype=torch.float32)  # ! These are in property units
)

# * This is the observed gravity data
adapted_observed_grav = geo_model.solutions.gravity.detach().numpy()

# Placing the tensor pointer in the rest of the model
geo_model.geophysics_input = gp.data.GeophysicsInput(
    tz=geo_model.geophysics_input.tz,
    densities=prior_tensor,
)


# %%
# Define the Pyro probabilistic model for inversion
def pyro_model(y_obs_list, interpolation_input):
    """
    Pyro model representing the probabilistic aspects of the geological model.
    """
    import gempy_engine

    # * Prior definition
    prior_mean = 2.62
    mu_density = pyro.sample(
        name=r'$\mu_{\text{density}}$',
        fn=dist.Normal(
            loc=prior_mean,
            scale=torch.tensor(0.5, dtype=torch.float32))
    )

    # Changing the density of the first formation
    geo_model.geophysics_input.densities = torch.index_put(
        input=prior_tensor,
        indices=(torch.tensor([0]),),
        values=mu_density
    )

    # * Deterministic computation of the geological model
    # GemPy does not have API for this yet so we need to compute
    # the model directly by calling the engine
    geo_model.solutions = gempy_engine.compute_model(
        interpolation_input=interpolation_input,
        options=geo_model.interpolation_options,
        data_descriptor=geo_model.input_data_descriptor,
        geophysics_input=geo_model.geophysics_input
    )

    simulated_geophysics = geo_model.solutions.gravity
    pyro.deterministic(r'$\mu_{gravity}$', simulated_geophysics)

    # * Likelihood definition
    pyro.sample(
        name="obs",
        fn=dist.MultivariateNormal(simulated_geophysics, covariance_matrix),
        obs=y_obs_list
    )


# %%
# Prepare observed data for Pyro model and optimize mesh settings

# TODO: This is going to be a problem, that 17 should be number of observations
n_devices = device_loc.values.shape[0]
y_obs_list = torch.tensor(adapted_observed_grav).view(1, n_devices)

# Optimize for speed
geo_model.interpolation_options.mesh_extraction = False
geo_model.interpolation_options.number_octree_levels = 1

geo_model.grid.set_inactive("topography")
geo_model.grid.set_inactive("octree")

# %%
# Perform prior sampling and visualize the results
PRIOR_PREDICTIVE_SAMPLES = 20
INFERENCE_SAMPLES = 20
POSTERIOR_SAMPLES = 20


if PRIOR_PREDICTIVE := True:
    predictive_model = Predictive(
        model=pyro_model,
        num_samples=PRIOR_PREDICTIVE_SAMPLES
    )
    prior = predictive_model(
        y_obs_list=y_obs_list,
        interpolation_input=geo_model.interpolation_input_copy
    )

    data = az.from_pyro(prior=prior)
    az.plot_trace(data.prior)
    plt.show()

# %%
# Run Markov Chain Monte Carlo (MCMC) using the NUTS algorithm for probabilistic inversion
pyro.primitives.enable_validation(is_validate=True)
nuts_kernel = NUTS(pyro_model)
mcmc = MCMC(nuts_kernel, num_samples=INFERENCE_SAMPLES, warmup_steps=20)
mcmc.run(y_obs_list, interpolation_input=geo_model.interpolation_input_copy)

# %%
# Analyze posterior samples and predictives, and visualize the results
posterior_samples = mcmc.get_samples(50)
posterior_predictive = Predictive(pyro_model, posterior_samples)
posterior_predictive = posterior_predictive(
    y_obs_list=y_obs_list, 
    interpolation_input=geo_model.interpolation_input_copy
)

data = az.from_pyro(
    posterior=mcmc,
    prior=prior,
    posterior_predictive=posterior_predictive
)

az.plot_trace(data)
plt.show()

# %%
# Create density plots for posterior and prior distributions
# These plots provide insights into the parameter distributions and their changes.
from gempy_probability.plot_posterior import default_red, default_blue
az.plot_density(
    data=[data, data.prior],
    shade=.9,
    hdi_prob=.99,
    data_labels=["Posterior", "Prior"],
    colors=[default_red, default_blue],
)
plt.show()

plt.rcParams['text.usetex'] = True
# %%
az.plot_density(
    data=[data.posterior_predictive, data.prior_predictive],
    shade=.9,
    var_names=[r'$\mu_{\text{gravity}}$'],
    data_labels=["Posterior Predictive", "Prior Predictive"],
    colors=[default_red, default_blue],
)
plt.show()

pass
